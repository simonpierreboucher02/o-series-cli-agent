#!/usr/bin/env python3
"""
Configuration Management Module

This module handles all configuration aspects for the unified OpenAI agent system,
including model configurations, agent settings, and validation.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional, List
from datetime import datetime


@dataclass
class AgentConfig:
    """Configuration settings for the Unified OpenAI Agent"""
    model: str = "o1"
    temperature: float = 1.0
    reasoning_effort: str = "medium"  # low, medium, high
    reasoning_summary: str = "auto"   # auto, detailed, none
    max_output_tokens: Optional[int] = None
    max_history_size: int = 1000
    stream: bool = True
    system_prompt: Optional[str] = None
    store: bool = True
    text_format: str = "text"  # text
    text_verbosity: str = "medium"  # low, medium, high
    top_p: float = 1.0
    parallel_tool_calls: bool = True
    tool_choice: str = "auto"
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        
        # Validate model
        if self.model not in ModelConfig.SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model: {self.model}")
        
        # Validate reasoning effort
        if self.reasoning_effort not in ["low", "medium", "high"]:
            self.reasoning_effort = "medium"
        
        # Validate temperature
        if not (0.0 <= self.temperature <= 2.0):
            self.temperature = 1.0
            
        # Validate top_p
        if not (0.0 <= self.top_p <= 1.0):
            self.top_p = 1.0


class ModelConfig:
    """Model configuration and information management"""
    
    # Comprehensive model configurations
    SUPPORTED_MODELS = {
        "o1": {
            "name": "O1",
            "description": "Advanced reasoning model with sophisticated problem-solving capabilities",
            "reasoning_timeout": {"low": 180, "medium": 480, "high": 900},  # 3, 8, 15 minutes
            "has_reasoning": True,
            "context_window": 128000,
            "max_output_tokens": 65536,
            "pricing": {"input": 0.015, "output": 0.06}  # per 1K tokens
        },
        "o3": {
            "name": "O3",
            "description": "Latest generation reasoning model with enhanced capabilities",
            "reasoning_timeout": {"low": 240, "medium": 600, "high": 1200},  # 4, 10, 20 minutes
            "has_reasoning": True,
            "context_window": 128000,
            "max_output_tokens": 65536,
            "pricing": {"input": 0.02, "output": 0.08}
        },
        "o3-mini": {
            "name": "O3 Mini",
            "description": "Compact O3 model optimized for faster reasoning tasks",
            "reasoning_timeout": {"low": 120, "medium": 300, "high": 600},   # 2, 5, 10 minutes
            "has_reasoning": True,
            "context_window": 128000,
            "max_output_tokens": 65536,
            "pricing": {"input": 0.0025, "output": 0.01}
        },
        "o4-mini": {
            "name": "O4 Mini",
            "description": "Latest generation mini reasoning model with improved efficiency",
            "reasoning_timeout": {"low": 90, "medium": 240, "high": 480},    # 1.5, 4, 8 minutes
            "has_reasoning": True,
            "context_window": 128000,
            "max_output_tokens": 65536,
            "pricing": {"input": 0.002, "output": 0.008}
        }
    }
    
    @classmethod
    def get_model_config(cls, model: str) -> Dict[str, Any]:
        """Get configuration for a specific model"""
        if model not in cls.SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model: {model}")
        return cls.SUPPORTED_MODELS[model]
    
    @classmethod
    def get_available_models(cls) -> List[str]:
        """Get list of available models"""
        return list(cls.SUPPORTED_MODELS.keys())
    
    @classmethod
    def get_model_names(cls) -> Dict[str, str]:
        """Get mapping of model IDs to display names"""
        return {model: config["name"] for model, config in cls.SUPPORTED_MODELS.items()}
    
    @classmethod
    def get_reasoning_models(cls) -> List[str]:
        """Get list of models that support reasoning"""
        return [model for model, config in cls.SUPPORTED_MODELS.items() 
                if config.get("has_reasoning", False)]
    
    @classmethod
    def get_timeout_for_model(cls, model: str, reasoning_effort: str = "medium") -> int:
        """Get timeout for a specific model and reasoning effort"""
        config = cls.get_model_config(model)
        return config["reasoning_timeout"].get(reasoning_effort, 300)
    
    @classmethod
    def estimate_cost(cls, model: str, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost for a request"""
        config = cls.get_model_config(model)
        pricing = config.get("pricing", {"input": 0, "output": 0})
        
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        
        return input_cost + output_cost
    
    @classmethod
    def validate_model_params(cls, model: str, **params) -> Dict[str, Any]:
        """Validate and adjust parameters for a specific model"""
        config = cls.get_model_config(model)
        validated = {}
        
        # Validate max_output_tokens
        max_tokens = params.get("max_output_tokens")
        if max_tokens:
            max_allowed = config.get("max_output_tokens", 4096)
            validated["max_output_tokens"] = min(max_tokens, max_allowed)
        
        # Validate temperature
        temperature = params.get("temperature", 1.0)
        validated["temperature"] = max(0.0, min(2.0, temperature))
        
        # Validate reasoning effort
        reasoning_effort = params.get("reasoning_effort", "medium")
        if reasoning_effort not in ["low", "medium", "high"]:
            reasoning_effort = "medium"
        validated["reasoning_effort"] = reasoning_effort
        
        return validated


class ConfigManager:
    """Advanced configuration management with validation and presets"""
    
    # Predefined configuration presets
    PRESETS = {
        "creative": {
            "temperature": 1.5,
            "reasoning_effort": "high",
            "reasoning_summary": "detailed",
            "text_verbosity": "high"
        },
        "balanced": {
            "temperature": 1.0,
            "reasoning_effort": "medium",
            "reasoning_summary": "auto",
            "text_verbosity": "medium"
        },
        "focused": {
            "temperature": 0.3,
            "reasoning_effort": "high",
            "reasoning_summary": "detailed",
            "text_verbosity": "low"
        },
        "fast": {
            "temperature": 0.7,
            "reasoning_effort": "low",
            "reasoning_summary": "none",
            "text_verbosity": "low"
        }
    }
    
    @classmethod
    def create_config_from_preset(cls, model: str, preset: str) -> AgentConfig:
        """Create configuration from a preset"""
        if preset not in cls.PRESETS:
            raise ValueError(f"Unknown preset: {preset}")
        
        preset_config = cls.PRESETS[preset].copy()
        preset_config["model"] = model
        
        return AgentConfig(**preset_config)
    
    @classmethod
    def create_interactive_config(cls, model: str) -> AgentConfig:
        """Create configuration through interactive prompts"""
        from utils import ColorManager
        colors = ColorManager()
        
        print(f"\n{colors.format_text('CYAN')}Creating Agent Configuration{colors.format_text('RESET')}")
        print(f"{colors.format_text('YELLOW')}Press Enter to use default values{colors.format_text('RESET')}\n")
        
        config = AgentConfig(model=model)
        model_config = ModelConfig.get_model_config(model)
        
        # Show model info
        print(f"{colors.format_text('GREEN')}Selected Model: {model_config['name']} ({model})")
        print(f"{colors.format_text('WHITE')}  {model_config['description']}")
        timeouts = model_config["reasoning_timeout"]
        print(f"  Timeouts: Low={timeouts['low']}s, Medium={timeouts['medium']}s, High={timeouts['high']}s{colors.format_text('RESET')}\n")
        
        # Temperature
        temp_input = input(f"Temperature (0.0-2.0) [{config.temperature}]: ").strip()
        if temp_input:
            try:
                temperature = float(temp_input)
                if 0.0 <= temperature <= 2.0:
                    config.temperature = temperature
                else:
                    print(f"{colors.format_text('RED')}Temperature out of range, using default{colors.format_text('RESET')}")
            except ValueError:
                print(f"{colors.format_text('RED')}Invalid temperature, using default{colors.format_text('RESET')}")
        
        # Reasoning effort
        effort_input = input(f"Reasoning effort (low/medium/high) [{config.reasoning_effort}]: ").strip().lower()
        if effort_input and effort_input in ["low", "medium", "high"]:
            config.reasoning_effort = effort_input
            timeout = model_config["reasoning_timeout"].get(config.reasoning_effort, 300)
            print(f"{colors.format_text('YELLOW')}  → Timeout: {timeout}s ({timeout//60}min {timeout%60}s){colors.format_text('RESET')}")
        
        # Reasoning summary
        summary_input = input(f"Reasoning summary (auto/detailed/none) [{config.reasoning_summary}]: ").strip().lower()
        if summary_input and summary_input in ["auto", "detailed", "none"]:
            config.reasoning_summary = summary_input
        
        # System prompt
        system_prompt = input(f"System prompt (optional): ").strip()
        if system_prompt:
            config.system_prompt = system_prompt
        
        # Max output tokens
        tokens_input = input(f"Max output tokens (optional, max {model_config['max_output_tokens']}): ").strip()
        if tokens_input:
            try:
                max_tokens = int(tokens_input)
                if 0 < max_tokens <= model_config["max_output_tokens"]:
                    config.max_output_tokens = max_tokens
                else:
                    print(f"{colors.format_text('RED')}Token count out of range, leaving unset{colors.format_text('RESET')}")
            except ValueError:
                print(f"{colors.format_text('RED')}Invalid token count, leaving unset{colors.format_text('RESET')}")
        
        # Streaming
        stream_input = input(f"Enable streaming (y/n) [{'y' if config.stream else 'n'}]: ").strip().lower()
        if stream_input in ['n', 'no', 'false']:
            config.stream = False
        elif stream_input in ['y', 'yes', 'true']:
            config.stream = True
        
        return config
    
    @classmethod
    def validate_config(cls, config: AgentConfig) -> AgentConfig:
        """Validate and fix configuration values"""
        # Validate model-specific parameters
        model_params = ModelConfig.validate_model_params(
            config.model,
            max_output_tokens=config.max_output_tokens,
            temperature=config.temperature,
            reasoning_effort=config.reasoning_effort
        )
        
        # Apply validated parameters
        for key, value in model_params.items():
            setattr(config, key, value)
        
        # Update timestamp
        config.updated_at = datetime.now().isoformat()
        
        return config
    
    @classmethod
    def get_preset_names(cls) -> List[str]:
        """Get list of available presets"""
        return list(cls.PRESETS.keys())
    
    @classmethod
    def describe_preset(cls, preset: str) -> str:
        """Get description of a preset"""
        descriptions = {
            "creative": "High creativity with detailed reasoning for creative tasks",
            "balanced": "Balanced settings for general use",
            "focused": "Low temperature with high reasoning for analytical tasks",
            "fast": "Fast responses with minimal reasoning for quick interactions"
        }
        return descriptions.get(preset, "Custom preset")


# Configuration validation utilities
def validate_config_file(config_path: str) -> bool:
    """Validate a configuration file"""
    try:
        import yaml
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        # Try to create AgentConfig to validate
        AgentConfig(**config_data)
        return True
    except Exception:
        return False


def migrate_config(old_config_path: str, new_config_path: str) -> bool:
    """Migrate configuration from old format to new format"""
    try:
        import yaml
        with open(old_config_path, 'r') as f:
            old_config = yaml.safe_load(f)
        
        # Create new config with defaults, then update with old values
        new_config = AgentConfig()
        
        # Map old keys to new keys if needed
        key_mapping = {
            # Add any key mappings for backwards compatibility
        }
        
        for old_key, value in old_config.items():
            new_key = key_mapping.get(old_key, old_key)
            if hasattr(new_config, new_key):
                setattr(new_config, new_key, value)
        
        # Save migrated config
        with open(new_config_path, 'w') as f:
            yaml.dump(asdict(new_config), f, default_flow_style=False, allow_unicode=True)
        
        return True
    except Exception:
        return False