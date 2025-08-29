#!/usr/bin/env python3
"""
Unified OpenAI Agent System - Advanced AI Chat Interface

This module provides a unified agent system that supports all OpenAI reasoning models
including O1, O3, O3-mini, and O4-mini. Features include:

- Support for all OpenAI reasoning models with model-specific configurations
- Persistent conversation history with rolling backups
- Streaming and non-streaming response support
- File inclusion in messages via {filename} syntax
- Advanced configuration management
- Comprehensive logging and statistics
- Export capabilities (JSON, TXT, MD, HTML)
- Secure API key management
- Professional CLI interface with enhanced user experience
"""

import os
import sys
import json
import requests
import re
import logging
import time
from dataclasses import dataclass, asdict
from typing import Optional, Generator, List, Dict, Any, Union
from pathlib import Path
from datetime import datetime
from requests.exceptions import RequestException, HTTPError, Timeout

from config import AgentConfig, ModelConfig
from utils import ColorManager, FileHandler, SecurityManager
from export import ConversationExporter


class UnifiedOpenAIAgent:
    """Unified OpenAI Agent supporting all reasoning models with advanced features"""

    def __init__(self, agent_id: str, model: str = "o1"):
        """
        Initialize the unified agent
        
        Args:
            agent_id: Unique identifier for the agent
            model: Model to use (o1, o3, o3-mini, o4-mini)
        """
        self.agent_id = agent_id
        self.model = model
        self.base_dir = Path(f"agents/{agent_id}")
        self.api_url = "https://api.openai.com/v1/chat/completions"
        
        # Initialize components
        self.colors = ColorManager()
        self.file_handler = FileHandler()
        self.security = SecurityManager()
        self.exporter = ConversationExporter()
        
        # Setup directories and logging
        self._setup_directories()
        self._setup_logging()
        
        # Load configuration and history
        self.config = self._load_config()
        self.messages = self._load_history()
        
        # Setup API key
        self.api_key = self._get_api_key()
        
        self.logger.info(f"Initialized Unified OpenAI Agent: {agent_id} with model: {self.model}")
        
    def _setup_directories(self):
        """Create necessary directory structure"""
        directories = [
            self.base_dir,
            self.base_dir / "backups",
            self.base_dir / "logs",
            self.base_dir / "exports",
            self.base_dir / "uploads"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
    def _setup_logging(self):
        """Configure logging to file and console"""
        log_file = self.base_dir / "logs" / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        
        # Create logger
        self.logger = logging.getLogger(f"UnifiedAgent_{self.agent_id}")
        self.logger.setLevel(logging.INFO)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler with color support
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.WARNING)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def _load_config(self) -> AgentConfig:
        """Load agent configuration from config file"""
        config_file = self.base_dir / "config.yaml"
        
        if config_file.exists():
            try:
                import yaml
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
                    # Ensure model is set correctly
                    config_data['model'] = self.model
                    return AgentConfig(**config_data)
            except Exception as e:
                self.logger.error(f"Error loading config: {e}")
                return AgentConfig(model=self.model)
        else:
            config = AgentConfig(model=self.model)
            self._save_config(config)
            return config
            
    def _save_config(self, config: Optional[AgentConfig] = None):
        """Save agent configuration to config file"""
        if config is None:
            config = self.config
            
        config.updated_at = datetime.now().isoformat()
        config_file = self.base_dir / "config.yaml"
        
        try:
            import yaml
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(asdict(config), f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
            
    def _get_api_key(self) -> str:
        """Get API key using security manager"""
        return self.security.get_api_key(self.model, self.base_dir)
        
    def _load_history(self) -> List[Dict[str, Any]]:
        """Load conversation history from history.json"""
        history_file = self.base_dir / "history.json"
        
        if history_file.exists():
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading history: {e}")
                return []
        return []
        
    def _save_history(self):
        """Save conversation history to history.json with backup"""
        history_file = self.base_dir / "history.json"
        
        # Create backup if history exists
        if history_file.exists():
            self._create_backup()
        
        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving history: {e}")
            
    def _create_backup(self):
        """Create rolling backup of history"""
        history_file = self.base_dir / "history.json"
        backup_dir = self.base_dir / "backups"
        
        if not history_file.exists():
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"history_{timestamp}.json"
        
        try:
            import shutil
            shutil.copy2(history_file, backup_file)
            
            # Keep only last 10 backups
            backups = sorted(backup_dir.glob("history_*.json"))
            while len(backups) > 10:
                oldest = backups.pop(0)
                oldest.unlink()
                
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            
    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Add a message to conversation history"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.messages.append(message)
        
        # Truncate history if needed
        if len(self.messages) > self.config.max_history_size:
            removed = self.messages[:-self.config.max_history_size]
            self.messages = self.messages[-self.config.max_history_size:]
            self.logger.info(f"Truncated history: removed {len(removed)} old messages")
        
        self._save_history()
        
    def _build_api_payload(self, new_message: str, override_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Build the API request payload for the current model"""
        # Process file inclusions
        processed_message = self.file_handler.process_file_inclusions(
            new_message, self.base_dir, self.logger
        )
        
        # Build messages in the API structure
        messages = []
        
        # Add system prompt as developer role if configured
        if self.config.system_prompt:
            messages.append({
                "role": "developer",
                "content": [
                    {"type": "text", "text": self.config.system_prompt}
                ]
            })
        
        # Add conversation history (convert from storage format to API format)
        for msg in self.messages:
            if msg["role"] in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": [
                        {"type": "text", "text": msg["content"]}
                    ]
                })
        
        # Add new user message
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": processed_message}
            ]
        })
        
        # Apply config overrides
        config = asdict(self.config)
        if override_config:
            config.update(override_config)
        
        # Build payload matching the API structure
        payload = {
            "model": config["model"],
            "messages": messages,
            "response_format": {"type": config["text_format"]},
            "reasoning_effort": config["reasoning_effort"]
        }
        
        # Add streaming if enabled
        if config["stream"]:
            payload["stream"] = True
        
        # Add optional parameters
        if config.get("max_output_tokens"):
            payload["max_completion_tokens"] = config["max_output_tokens"]
            
        if config.get("temperature") != 1.0:
            payload["temperature"] = config["temperature"]
            
        if config.get("top_p") != 1.0:
            payload["top_p"] = config["top_p"]
            
        return payload
        
    def _get_timeout_for_reasoning(self, reasoning_effort: str = "medium") -> int:
        """Get appropriate timeout based on model and reasoning effort"""
        model_config = ModelConfig.get_model_config(self.model)
        return model_config["reasoning_timeout"].get(reasoning_effort, 300)
        
    def _make_api_request(self, payload: Dict[str, Any]) -> requests.Response:
        """Make API request with retries and error handling"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Get appropriate timeout
        reasoning_effort = payload.get("reasoning_effort", "medium")
        timeout = self._get_timeout_for_reasoning(reasoning_effort)
        
        model_config = ModelConfig.get_model_config(self.model)
        model_display = model_config["name"]
        
        self.logger.info(f"Using timeout of {timeout}s for {model_display} with reasoning effort: {reasoning_effort}")
        
        max_retries = 3
        base_delay = 1
        
        for attempt in range(max_retries):
            try:
                self.logger.info(f"Making API request to {model_display} (attempt {attempt + 1}/{max_retries}) with {timeout}s timeout...")
                
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    stream=payload.get("stream", True),
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    self.logger.info("API request successful")
                    return response
                elif response.status_code == 401:
                    raise ValueError("Invalid API key")
                elif response.status_code == 403:
                    raise ValueError("API access forbidden")
                elif response.status_code == 429:
                    # Rate limited - wait and retry
                    delay = base_delay * (2 ** attempt)
                    self.logger.warning(f"Rate limited, retrying in {delay}s...")
                    time.sleep(delay)
                    continue
                elif response.status_code >= 500:
                    # Server error - retry
                    delay = base_delay * (2 ** attempt)
                    self.logger.warning(f"Server error {response.status_code}, retrying in {delay}s...")
                    time.sleep(delay)
                    continue
                else:
                    response.raise_for_status()
                    
            except Timeout as e:
                self.logger.warning(f"Request timed out after {timeout}s (attempt {attempt + 1}/{max_retries})")
                if attempt == max_retries - 1:
                    raise Exception(f"Request timed out after {timeout}s. Try reducing reasoning effort.")
                delay = base_delay * (2 ** attempt)
                self.logger.warning(f"Retrying in {delay}s...")
                time.sleep(delay)
            except RequestException as e:
                if attempt == max_retries - 1:
                    raise
                delay = base_delay * (2 ** attempt)
                self.logger.warning(f"Request failed ({e}), retrying in {delay}s...")
                time.sleep(delay)
        
        raise Exception(f"Failed to complete API request after {max_retries} attempts")
        
    def _parse_streaming_response(self, response: requests.Response) -> Generator[str, None, None]:
        """Parse streaming Server-Sent Events response"""
        assistant_message = ""
        
        try:
            for line in response.iter_lines(decode_unicode=True):
                if not line or line.strip() == "":
                    continue
                
                try:
                    # Handle Server-Sent Events format
                    if line.startswith("data: "):
                        data_str = line[5:].strip()
                        
                        if data_str == "[DONE]":
                            break
                            
                        data = json.loads(data_str)
                        
                        # Handle streaming format
                        choices = data.get("choices", [])
                        if choices:
                            choice = choices[0]
                            delta = choice.get("delta", {})
                            content = delta.get("content", "")
                            
                            if content:
                                assistant_message += content
                                yield content
                                
                            # Check for completion
                            finish_reason = choice.get("finish_reason")
                            if finish_reason == "stop":
                                break
                                
                except json.JSONDecodeError as e:
                    self.logger.warning(f"Invalid JSON in stream: {e}")
                    continue
                except Exception as e:
                    self.logger.warning(f"Error processing stream line: {e}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error parsing streaming response: {e}")
            
        # Add assistant message to history if we got content
        if assistant_message.strip():
            self.add_message("assistant", assistant_message)
            
    def _parse_non_streaming_response(self, response: requests.Response) -> str:
        """Parse non-streaming response from OpenAI chat completions API"""
        try:
            data = response.json()
            
            # Extract message content
            choices = data.get("choices", [])
            if choices:
                message = choices[0].get("message", {})
                # Handle structured content format
                content_array = message.get("content", [])
                if isinstance(content_array, list) and content_array:
                    content = content_array[0].get("text", "")
                else:
                    content = message.get("content", "")
                    
                if content:
                    self.add_message("assistant", content)
                    return content
                                
            return "No response content received"
            
        except Exception as e:
            self.logger.error(f"Error parsing non-streaming response: {e}")
            return f"Error parsing response: {e}"
            
    def call_api(self, new_message: str, override_config: Optional[Dict[str, Any]] = None) -> Generator[str, None, None]:
        """Call OpenAI API with the new message"""
        try:
            # Add user message to history
            self.add_message("user", new_message)
            
            # Build API payload
            payload = self._build_api_payload(new_message, override_config)
            
            self.logger.info(f"Making API call to {self.api_url}")
            self.logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
            
            # Show model and reasoning info to user
            reasoning_effort = payload.get("reasoning_effort", "medium")
            model_config = ModelConfig.get_model_config(self.model)
            model_display = model_config["name"]
            
            if reasoning_effort in ["medium", "high"]:
                timeout = self._get_timeout_for_reasoning(reasoning_effort)
                print(f"{self.colors.format_text('YELLOW')}🧠 Using {model_display} with {reasoning_effort.upper()} reasoning (timeout: {timeout//60}min {timeout%60}s)...{self.colors.format_text('RESET')}")
            
            # Make request
            response = self._make_api_request(payload)
            
            # Handle streaming vs non-streaming
            if payload.get("stream", True):
                yield from self._parse_streaming_response(response)
            else:
                result = self._parse_non_streaming_response(response)
                yield result
                
        except Exception as e:
            error_msg = f"API call failed: {e}"
            self.logger.error(error_msg)
            yield error_msg
            
    def clear_history(self):
        """Clear conversation history"""
        self._create_backup()
        self.messages.clear()
        self._save_history()
        self.logger.info("Conversation history cleared")
        
    def get_statistics(self) -> Dict[str, Any]:
        """Get conversation statistics"""
        if not self.messages:
            return {
                "total_messages": 0,
                "user_messages": 0,
                "assistant_messages": 0,
                "total_characters": 0,
                "average_message_length": 0,
                "first_message": None,
                "last_message": None,
                "conversation_duration": None
            }
            
        user_msgs = [m for m in self.messages if m["role"] == "user"]
        assistant_msgs = [m for m in self.messages if m["role"] == "assistant"]
        
        total_chars = sum(len(m["content"]) for m in self.messages)
        avg_length = total_chars // len(self.messages) if self.messages else 0
        
        first_time = datetime.fromisoformat(self.messages[0]["timestamp"])
        last_time = datetime.fromisoformat(self.messages[-1]["timestamp"])
        duration = last_time - first_time
        
        return {
            "total_messages": len(self.messages),
            "user_messages": len(user_msgs),
            "assistant_messages": len(assistant_msgs),
            "total_characters": total_chars,
            "average_message_length": avg_length,
            "first_message": first_time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_message": last_time.strftime("%Y-%m-%d %H:%M:%S"),
            "conversation_duration": str(duration).split('.')[0] if duration.total_seconds() > 0 else "0:00:00"
        }
        
    def export_conversation(self, format_type: str) -> str:
        """Export conversation to specified format"""
        model_config = ModelConfig.get_model_config(self.model)
        return self.exporter.export_conversation(
            format_type, 
            self.agent_id,
            self.model,
            model_config["name"],
            self.config,
            self.messages,
            self.get_statistics(),
            self.base_dir / "exports"
        )
        
    def search_history(self, term: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search conversation history for a term"""
        results = []
        term_lower = term.lower()
        
        for i, msg in enumerate(self.messages):
            if term_lower in msg["content"].lower():
                results.append({
                    "index": i,
                    "message": msg,
                    "preview": msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
                })
                
            if len(results) >= limit:
                break
                
        return results
        
    def list_files(self) -> List[str]:
        """List available files for inclusion"""
        return self.file_handler.list_files(self.base_dir)
        
    def get_model_display_name(self) -> str:
        """Get the display name for the current model"""
        model_config = ModelConfig.get_model_config(self.model)
        return model_config["name"]