#!/usr/bin/env python3
"""
Unified OpenAI Agent System - Main CLI Interface

A professional, feature-rich command-line interface for interacting with OpenAI's
reasoning models (O1, O3, O3-mini, O4-mini) with advanced conversation management,
export capabilities, and legendary user experience.

Usage:
    python main.py --agent-id my-agent --model o1    # Start interactive chat
    python main.py --list                            # List all agents  
    python main.py --agent-id my-agent --export html # Export conversation
    python main.py --models                          # Show available models
"""

import sys
import os
import argparse
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Import our modules
from agent import UnifiedOpenAIAgent
from config import AgentConfig, ModelConfig, ConfigManager
from utils import ColorManager, UIEnhancer, ValidationUtils
from export import ConversationExporter


class UnifiedCLI:
    """Main CLI interface with enhanced user experience"""
    
    def __init__(self):
        self.colors = ColorManager()
        self.ui = UIEnhancer()
        self.validator = ValidationUtils()
        self.version = "2.0.0"
        
    def create_argument_parser(self) -> argparse.ArgumentParser:
        """Create comprehensive argument parser"""
        parser = argparse.ArgumentParser(
            description="Unified OpenAI Agent System - Advanced AI Chat Interface",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=f"""
{self.colors.highlight('Examples:')}
  {self.colors.dim('Basic Usage:')}
  %(prog)s --agent-id my-agent --model o1         # Start chat with O1 model
  %(prog)s --agent-id research --model o3-mini    # Start chat with O3-mini
  
  {self.colors.dim('Configuration:')}
  %(prog)s --agent-id my-agent --config           # Interactive configuration
  %(prog)s --agent-id my-agent --preset creative  # Use creative preset
  
  {self.colors.dim('Management:')}
  %(prog)s --list                                 # List all agents
  %(prog)s --models                               # Show available models
  %(prog)s --info my-agent                        # Show agent details
  
  {self.colors.dim('Export & Import:')}
  %(prog)s --agent-id my-agent --export html      # Export as HTML
  %(prog)s --agent-id my-agent --export json      # Export as JSON
  
  {self.colors.dim('Advanced:')}
  %(prog)s --agent-id my-agent --effort high --temperature 0.3
  %(prog)s --agent-id my-agent --no-stream --max-tokens 1000

{self.colors.highlight('Supported Models:')}
  • O1: Advanced reasoning model (15min timeout)
  • O3: Latest generation model (20min timeout)  
  • O3-mini: Compact model (10min timeout)
  • O4-mini: Efficient model (8min timeout)
            """,
            add_help=True
        )
        
        # Core arguments
        parser.add_argument("--version", action="version", version=f"Unified OpenAI Agent System {self.version}")
        parser.add_argument("--agent-id", help="Agent ID for the chat session")
        parser.add_argument("--model", choices=ModelConfig.get_available_models(), 
                          default="o1", help="OpenAI model to use (default: o1)")
        
        # Information commands
        info_group = parser.add_argument_group("Information Commands")
        info_group.add_argument("--list", action="store_true", help="List all available agents")
        info_group.add_argument("--models", action="store_true", help="Show detailed model information")
        info_group.add_argument("--info", metavar="AGENT_ID", help="Show detailed agent information")
        info_group.add_argument("--stats", metavar="AGENT_ID", help="Show agent conversation statistics")
        
        # Configuration
        config_group = parser.add_argument_group("Configuration")
        config_group.add_argument("--config", action="store_true", help="Configure agent interactively")
        config_group.add_argument("--preset", choices=ConfigManager.get_preset_names(), 
                                help="Use configuration preset")
        config_group.add_argument("--show-config", action="store_true", help="Show current configuration")
        
        # Model parameters
        param_group = parser.add_argument_group("Model Parameters")
        param_group.add_argument("--effort", choices=["low", "medium", "high"], 
                               help="Override reasoning effort level")
        param_group.add_argument("--temperature", type=float, 
                               help="Override temperature (0.0-2.0)")
        param_group.add_argument("--max-tokens", type=int, 
                               help="Maximum output tokens")
        param_group.add_argument("--no-stream", action="store_true", 
                               help="Disable streaming responses")
        param_group.add_argument("--system-prompt", 
                               help="Set system prompt")
        
        # Export and import
        export_group = parser.add_argument_group("Export & Import")
        export_group.add_argument("--export", choices=["json", "txt", "md", "html", "csv", "xml"], 
                                help="Export conversation format")
        export_group.add_argument("--export-all", action="store_true", 
                                help="Export in all formats")
        
        # Conversation management
        conv_group = parser.add_argument_group("Conversation Management")
        conv_group.add_argument("--clear", action="store_true", 
                              help="Clear conversation history")
        conv_group.add_argument("--backup", action="store_true", 
                              help="Create backup of conversation")
        conv_group.add_argument("--search", metavar="TERM", 
                              help="Search conversation history")
        
        # Advanced options
        advanced_group = parser.add_argument_group("Advanced Options")
        advanced_group.add_argument("--debug", action="store_true", 
                                  help="Enable debug output")
        advanced_group.add_argument("--no-color", action="store_true", 
                                  help="Disable colored output")
        advanced_group.add_argument("--batch", metavar="FILE", 
                                  help="Process batch commands from file")
        
        return parser
    
    def list_agents(self):
        """List all available agents with enhanced formatting"""
        agents = self._get_all_agents()
        
        if not agents:
            print(f"{self.colors.warning('No agents found')}")
            print(f"{self.colors.dim('Create your first agent with: python main.py --agent-id my-agent')}")
            return
        
        self.ui.print_banner("Available Agents", f"Found {len(agents)} agents")
        
        # Prepare table data
        headers = ["Agent ID", "Model", "Messages", "Last Updated", "Size"]
        rows = []
        
        for agent in agents:
            updated = agent.get("updated_at", "Unknown")
            if updated != "Unknown":
                try:
                    updated = datetime.fromisoformat(updated).strftime("%m-%d %H:%M")
                except:
                    pass
            
            model = agent.get('model', 'unknown')
            model_config = ModelConfig.get_model_config(model) if model in ModelConfig.SUPPORTED_MODELS else None
            model_display = model_config["name"] if model_config else model
            
            # Format file size
            size = agent.get('history_size', 0)
            if size > 1024*1024:
                size_str = f"{size/(1024*1024):.1f}MB"
            elif size > 1024:
                size_str = f"{size/1024:.1f}KB"
            else:
                size_str = f"{size}B"
            
            rows.append([
                agent['id'],
                model_display,
                str(agent.get('message_count', 0)),
                updated,
                size_str
            ])
        
        self.ui.print_table(headers, rows)
        print(f"\n{self.colors.dim('💡 Use --info AGENT_ID for detailed information')}")
    
    def show_models(self):
        """Show detailed model information"""
        self.ui.print_banner("Available OpenAI Models", "Reasoning-capable models")
        
        for model_id, model_config in ModelConfig.SUPPORTED_MODELS.items():
            print(f"\n{self.colors.highlight(f'🧠 {model_config['name']} ({model_id})')}")
            print(f"   {self.colors.dim(model_config['description'])}")
            
            # Timeouts
            timeouts = model_config["reasoning_timeout"]
            timeout_info = f"Low: {timeouts['low']//60}m, Medium: {timeouts['medium']//60}m, High: {timeouts['high']//60}m"
            print(f"   ⏱️  {self.colors.bold('Timeouts:')} {timeout_info}")
            
            # Pricing
            pricing = model_config.get("pricing", {})
            if pricing:
                input_cost = pricing.get('input', 0)
                output_cost = pricing.get('output', 0)
                print(f"   💰 {self.colors.bold('Pricing:')} ${input_cost:.4f}/${output_cost:.4f} per 1K tokens")
            
            # Context window
            context = model_config.get("context_window", 0)
            if context:
                print(f"   📖 {self.colors.bold('Context:')} {context:,} tokens")
        
        print(f"\n{self.colors.dim('💡 Use --model MODEL_ID to select a specific model')}")
    
    def show_agent_info(self, agent_id: str):
        """Show detailed agent information"""
        agent_dir = Path(f"agents/{agent_id}")
        
        if not agent_dir.exists():
            print(f"{self.colors.error(f'Agent \"{agent_id}\" not found')}")
            return
        
        self.ui.print_banner(f"Agent Information: {agent_id}")
        
        # Load configuration
        config_file = agent_dir / "config.yaml"
        if config_file.exists():
            try:
                with open(config_file) as f:
                    config = yaml.safe_load(f)
                
                model = config.get('model', 'unknown')
                model_config = ModelConfig.get_model_config(model) if model in ModelConfig.SUPPORTED_MODELS else None
                
                self.ui.print_section("Configuration")
                if model_config:
                    self.ui.print_model_info(model, model_config)
                else:
                    print(f"  {self.colors.bold('Model:')} {model} (unknown)")
                
                print(f"  {self.colors.bold('Temperature:')} {config.get('temperature', 1.0)}")
                print(f"  {self.colors.bold('Reasoning Effort:')} {config.get('reasoning_effort', 'medium')}")
                print(f"  {self.colors.bold('Streaming:')} {'Enabled' if config.get('stream', True) else 'Disabled'}")
                print(f"  {self.colors.bold('Created:')} {config.get('created_at', 'Unknown')}")
                print(f"  {self.colors.bold('Updated:')} {config.get('updated_at', 'Unknown')}")
                
            except Exception as e:
                print(f"{self.colors.error(f'Error loading config: {e}')}")
        
        # Show conversation statistics
        history_file = agent_dir / "history.json"
        if history_file.exists():
            try:
                with open(history_file) as f:
                    history = json.load(f)
                
                user_msgs = len([m for m in history if m.get("role") == "user"])
                assistant_msgs = len([m for m in history if m.get("role") == "assistant"])
                total_chars = sum(len(m.get("content", "")) for m in history)
                
                self.ui.print_section("Conversation History")
                
                # Create stats table
                stats_data = [
                    ["Total Messages", str(len(history))],
                    ["User Messages", str(user_msgs)],
                    ["Assistant Messages", str(assistant_msgs)],
                    ["Total Characters", f"{total_chars:,}"],
                    ["File Size", f"{history_file.stat().st_size:,} bytes"]
                ]
                
                if history:
                    first_msg = datetime.fromisoformat(history[0]["timestamp"])
                    last_msg = datetime.fromisoformat(history[-1]["timestamp"])
                    stats_data.extend([
                        ["First Message", first_msg.strftime('%Y-%m-%d %H:%M:%S')],
                        ["Last Message", last_msg.strftime('%Y-%m-%d %H:%M:%S')]
                    ])
                
                for stat, value in stats_data:
                    print(f"  {self.colors.bold(stat + ':')} {value}")
                    
            except Exception as e:
                print(f"{self.colors.error(f'Error loading history: {e}')}")
        else:
            print(f"{self.colors.warning('No conversation history found')}")
        
        # Show directory structure
        self.ui.print_section("Files")
        for item in sorted(agent_dir.rglob("*")):
            if item.is_file():
                size = item.stat().st_size
                size_str = f"{size:,}" if size < 1024 else f"{size/1024:.1f}K"
                rel_path = item.relative_to(agent_dir)
                print(f"  {rel_path} ({size_str})")
    
    def interactive_chat(self, agent: UnifiedOpenAIAgent):
        """Enhanced interactive chat session"""
        model_display = agent.get_model_display_name()
        
        # Show welcome banner
        self.ui.print_banner(
            f"OpenAI {model_display} Chat", 
            f"Agent: {agent.agent_id} • Type /help for commands • /quit to exit"
        )
        
        # Show quick tips
        print(f"{self.colors.dim('💡 Tips:')}")
        print(f"{self.colors.dim('  • Use {{filename}} to include file contents')}")
        print(f"{self.colors.dim('  • Try /files to see available files')}")
        print(f"{self.colors.dim('  • Use /preset to change model behavior')}")
        print()
        
        while True:
            try:
                user_input = input(f"{self.colors.format_text('CYAN', '❯')} {self.colors.format_text('RESET')}").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    if self._handle_chat_command(user_input, agent):
                        break  # Exit chat
                    continue
                
                # Regular message - send to API
                print(f"\n{self.colors.format_text('MAGENTA', '🤖 Assistant:')} ", end="", flush=True)
                
                response_text = ""
                try:
                    for chunk in agent.call_api(user_input):
                        print(chunk, end="", flush=True)
                        response_text += chunk
                except Exception as e:
                    print(f"{self.colors.error(f'Error: {e}')}")
                
                print("\n")
                
            except KeyboardInterrupt:
                print(f"\n{self.colors.warning('💡 Use /quit to exit gracefully')}")
            except EOFError:
                print(f"\n{self.colors.success('Goodbye! 👋')}")
                break
            except Exception as e:
                print(f"\n{self.colors.error(f'Unexpected error: {e}')}")
    
    def _handle_chat_command(self, user_input: str, agent: UnifiedOpenAIAgent) -> bool:
        """Handle chat commands, return True if should exit"""
        command_parts = user_input[1:].split()
        command = command_parts[0].lower()
        
        if command == 'help':
            self._show_chat_help(agent)
            
        elif command == 'quit' or command == 'exit' or command == 'q':
            print(f"{self.colors.success('Goodbye! 👋')}")
            return True
            
        elif command == 'history':
            limit = 5
            if len(command_parts) > 1:
                try:
                    limit = int(command_parts[1])
                except ValueError:
                    print(f"{self.colors.error('Invalid number')}")
                    return False
            
            self._show_recent_history(agent, limit)
            
        elif command == 'search':
            if len(command_parts) < 2:
                print(f"{self.colors.error('Usage: /search <term>')}")
                return False
            
            search_term = ' '.join(command_parts[1:])
            self._search_conversation(agent, search_term)
            
        elif command == 'stats':
            self._show_conversation_stats(agent)
            
        elif command == 'config':
            self._show_current_config(agent)
            
        elif command == 'preset':
            if len(command_parts) < 2:
                self._show_available_presets()
            else:
                self._apply_preset(agent, command_parts[1])
                
        elif command == 'export':
            if len(command_parts) < 2:
                print(f"{self.colors.error('Usage: /export <json|txt|md|html|csv|xml>')}")
                return False
            
            format_type = command_parts[1].lower()
            self._export_conversation(agent, format_type)
            
        elif command == 'clear':
            self._clear_conversation_history(agent)
            
        elif command == 'files':
            self._show_available_files(agent)
            
        elif command == 'info':
            self.show_agent_info(agent.agent_id)
            
        elif command == 'model':
            self._show_current_model_info(agent)
            
        else:
            print(f"{self.colors.error(f'Unknown command: {command}')}")
            print(f"{self.colors.dim('Type /help for available commands')}")
        
        return False
    
    def _show_chat_help(self, agent: UnifiedOpenAIAgent):
        """Show chat help"""
        model_config = ModelConfig.get_model_config(agent.model)
        
        print(f"\n{self.colors.highlight('📋 Available Commands:')}")
        
        commands = [
            ("/help", "Show this help message"),
            ("/history [n]", "Show last n messages (default 5)"),
            ("/search <term>", "Search conversation history"),
            ("/stats", "Show conversation statistics"),
            ("/config", "Show current configuration"),
            ("/preset [name]", "Show/apply configuration presets"),
            ("/export <format>", "Export conversation (json|txt|md|html|csv|xml)"),
            ("/clear", "Clear conversation history"),
            ("/files", "List available files for inclusion"),
            ("/info", "Show agent information"),
            ("/model", "Show current model information"),
            ("/quit", "Exit chat")
        ]
        
        for cmd, desc in commands:
            print(f"  {self.colors.highlight(cmd.ljust(15))} {self.colors.dim(desc)}")
        
        print(f"\n{self.colors.highlight('🧠 Model Information:')}")
        print(f"  {self.colors.bold('Current:')} {model_config['name']} ({agent.model})")
        
        timeouts = model_config["reasoning_timeout"]
        print(f"  {self.colors.bold('Timeouts:')} Low={timeouts['low']}s, Medium={timeouts['medium']}s, High={timeouts['high']}s")
        
        print(f"\n{self.colors.highlight('📁 File Inclusion:')}")
        print(f"  {self.colors.dim('Use {{filename}} in messages to include file contents')}")
        print(f"  {self.colors.dim('Supported: Programming files, config files, documentation')}")
        print()
    
    def _show_recent_history(self, agent: UnifiedOpenAIAgent, limit: int):
        """Show recent conversation history"""
        recent_messages = agent.messages[-limit:]
        if not recent_messages:
            print(f"{self.colors.warning('No messages in history')}")
            return
        
        print(f"\n{self.colors.highlight(f'📜 Last {len(recent_messages)} messages:')}")
        for msg in recent_messages:
            timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M:%S")
            role_color = 'CYAN' if msg["role"] == "user" else 'MAGENTA'
            role_icon = "👤" if msg["role"] == "user" else "🤖"
            
            content_preview = msg["content"][:80].replace('\n', ' ')
            if len(msg["content"]) > 80:
                content_preview += "..."
            
            print(f"  {self.colors.dim(f'[{timestamp}]')} {self.colors.format_text(role_color, role_icon + ' ' + msg['role'])}: {content_preview}")
        print()
    
    def _search_conversation(self, agent: UnifiedOpenAIAgent, search_term: str):
        """Search conversation history"""
        results = agent.search_history(search_term)
        
        if not results:
            print(f"{self.colors.warning(f'No matches found for \"{search_term}\"')}")
            return
        
        print(f"\n{self.colors.highlight(f'🔍 Found {len(results)} matches for \"{search_term}\":')}")
        for result in results:
            msg = result["message"]
            timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M:%S")
            role_color = 'CYAN' if msg["role"] == "user" else 'MAGENTA'
            role_icon = "👤" if msg["role"] == "user" else "🤖"
            
            print(f"  {self.colors.dim(f'[{timestamp}]')} {self.colors.format_text(role_color, role_icon + ' ' + msg['role'])}: {result['preview']}")
        print()
    
    def _show_conversation_stats(self, agent: UnifiedOpenAIAgent):
        """Show conversation statistics"""
        stats = agent.get_statistics()
        model_display = agent.get_model_display_name()
        
        print(f"\n{self.colors.highlight('📊 Conversation Statistics:')}")
        print(f"  {self.colors.bold('Model:')} {agent.model} ({model_display})")
        print(f"  {self.colors.bold('Total Messages:')} {stats['total_messages']}")
        print(f"  {self.colors.bold('User Messages:')} {stats['user_messages']}")
        print(f"  {self.colors.bold('Assistant Messages:')} {stats['assistant_messages']}")
        print(f"  {self.colors.bold('Total Characters:')} {stats['total_characters']:,}")
        print(f"  {self.colors.bold('Average Message Length:')} {stats['average_message_length']:,}")
        
        if stats['first_message']:
            print(f"  {self.colors.bold('First Message:')} {stats['first_message']}")
            print(f"  {self.colors.bold('Last Message:')} {stats['last_message']}")
            print(f"  {self.colors.bold('Duration:')} {stats['conversation_duration']}")
        print()
    
    def _show_current_config(self, agent: UnifiedOpenAIAgent):
        """Show current configuration"""
        print(f"\n{self.colors.highlight('⚙️  Current Configuration:')}")
        
        config_dict = agent.config.__dict__
        for key, value in config_dict.items():
            if key not in ['created_at', 'updated_at']:
                if key == 'model':
                    model_config = ModelConfig.get_model_config(str(value))
                    model_name = model_config["name"]
                    print(f"  {self.colors.bold(key + ':')} {value} ({model_name})")
                elif key == 'reasoning_effort':
                    timeout = agent._get_timeout_for_reasoning(str(value))
                    print(f"  {self.colors.bold(key + ':')} {value} (timeout: {timeout}s)")
                else:
                    print(f"  {self.colors.bold(key + ':')} {value}")
        print()
    
    def _show_available_presets(self):
        """Show available configuration presets"""
        print(f"\n{self.colors.highlight('🎯 Available Presets:')}")
        for preset in ConfigManager.get_preset_names():
            description = ConfigManager.describe_preset(preset)
            print(f"  {self.colors.highlight(preset.ljust(10))} {self.colors.dim(description)}")
        print(f"\n{self.colors.dim('Usage: /preset <name>')}")
    
    def _apply_preset(self, agent: UnifiedOpenAIAgent, preset_name: str):
        """Apply configuration preset"""
        try:
            new_config = ConfigManager.create_config_from_preset(agent.model, preset_name)
            agent.config = new_config
            agent._save_config()
            print(f"{self.colors.success(f'Applied preset: {preset_name}')}")
        except ValueError as e:
            print(f"{self.colors.error(str(e))}")
    
    def _export_conversation(self, agent: UnifiedOpenAIAgent, format_type: str):
        """Export conversation"""
        try:
            filepath = agent.export_conversation(format_type)
            print(f"{self.colors.success(f'Exported to: {filepath}')}")
        except Exception as e:
            print(f"{self.colors.error(f'Export failed: {e}')}")
    
    def _clear_conversation_history(self, agent: UnifiedOpenAIAgent):
        """Clear conversation history with confirmation"""
        response = input(f"{self.colors.warning('Clear conversation history? (y/N): ')}").strip().lower()
        if response in ['y', 'yes']:
            agent.clear_history()
            print(f"{self.colors.success('Conversation history cleared')}")
        else:
            print(f"{self.colors.dim('Operation cancelled')}")
    
    def _show_available_files(self, agent: UnifiedOpenAIAgent):
        """Show available files for inclusion"""
        files = agent.list_files()
        if not files:
            print(f"{self.colors.warning('No supported files found for inclusion')}")
            return
        
        print(f"\n{self.colors.highlight('📁 Available files for inclusion:')}")
        for file_info in files[:20]:  # Limit display
            print(f"  {file_info}")
        
        if len(files) > 20:
            print(f"{self.colors.dim(f'... and {len(files) - 20} more files')}")
        
        print(f"\n{self.colors.dim('💡 Use {{filename}} in your message to include file contents')}")
    
    def _show_current_model_info(self, agent: UnifiedOpenAIAgent):
        """Show current model information"""
        model_config = ModelConfig.get_model_config(agent.model)
        
        print(f"\n{self.colors.highlight('🧠 Current Model:')}")
        self.ui.print_model_info(agent.model, model_config)
        print()
    
    def _get_all_agents(self) -> List[Dict[str, Any]]:
        """Get information about all available agents"""
        agents_dir = Path("agents")
        agents = []
        
        if not agents_dir.exists():
            return agents
        
        for agent_dir in agents_dir.iterdir():
            if agent_dir.is_dir():
                agent_info = {
                    "id": agent_dir.name,
                    "path": str(agent_dir),
                    "exists": True
                }
                
                # Get config info
                config_file = agent_dir / "config.yaml"
                if config_file.exists():
                    try:
                        with open(config_file) as f:
                            config = yaml.safe_load(f)
                            agent_info["model"] = config.get("model", "unknown")
                            agent_info["created_at"] = config.get("created_at")
                            agent_info["updated_at"] = config.get("updated_at")
                    except:
                        pass
                
                # Get history info
                history_file = agent_dir / "history.json"
                if history_file.exists():
                    try:
                        with open(history_file) as f:
                            history = json.load(f)
                            agent_info["message_count"] = len(history)
                            agent_info["history_size"] = history_file.stat().st_size
                    except:
                        agent_info["message_count"] = 0
                        agent_info["history_size"] = 0
                else:
                    agent_info["message_count"] = 0
                    agent_info["history_size"] = 0
                
                agents.append(agent_info)
        
        return sorted(agents, key=lambda x: x.get("updated_at", ""))
    
    def run(self):
        """Main entry point"""
        parser = self.create_argument_parser()
        args = parser.parse_args()
        
        # Handle no-color flag
        if args.no_color:
            self.colors.colors_available = False
            self.colors._setup_colors()
        
        # Handle information commands
        if args.list:
            self.list_agents()
            return
        
        if args.models:
            self.show_models()
            return
        
        if args.info:
            self.show_agent_info(args.info)
            return
        
        if args.stats:
            self.show_agent_info(args.stats)  # Stats are shown in info
            return
        
        # Require agent-id for other operations
        if not args.agent_id:
            if not any([args.list, args.models, args.info, args.stats]):
                self.ui.print_banner("Unified OpenAI Agent System", f"Version {self.version}")
                parser.print_help()
                print(f"\n{self.colors.error('Error: --agent-id is required for chat operations')}")
                print(f"{self.colors.dim('Use --list to see available agents or --models to see available models')}")
            return
        
        # Validate agent ID
        if not self.validator.validate_agent_id(args.agent_id):
            print(f"{self.colors.error('Invalid agent ID. Use only letters, numbers, hyphens, and underscores.')}")
            return
        
        try:
            # Initialize agent
            agent = UnifiedOpenAIAgent(args.agent_id, args.model)
            
            # Handle configuration commands
            if args.config:
                new_config = ConfigManager.create_interactive_config(args.model)
                agent.config = new_config
                agent._save_config()
                print(f"{self.colors.success('Configuration saved')}")
                return
            
            if args.preset:
                try:
                    new_config = ConfigManager.create_config_from_preset(args.model, args.preset)
                    agent.config = new_config
                    agent._save_config()
                    print(f"{self.colors.success(f'Applied preset: {args.preset}')}")
                    return
                except ValueError as e:
                    print(f"{self.colors.error(str(e))}")
                    return
            
            if args.show_config:
                self._show_current_config(agent)
                return
            
            # Handle export commands
            if args.export:
                filepath = agent.export_conversation(args.export)
                print(f"{self.colors.success(f'Exported to: {filepath}')}")
                return
            
            if args.export_all:
                formats = ["json", "txt", "md", "html", "csv", "xml"]
                exported_files = []
                for fmt in formats:
                    try:
                        filepath = agent.export_conversation(fmt)
                        exported_files.append(filepath)
                    except Exception as e:
                        print(f"{self.colors.error(f'Failed to export {fmt}: {e}')}")
                
                if exported_files:
                    print(f"{self.colors.success(f'Exported {len(exported_files)} files:')}")
                    for filepath in exported_files:
                        print(f"  {filepath}")
                return
            
            # Handle conversation management
            if args.clear:
                response = input(f"{self.colors.warning('Clear conversation history? (y/N): ')}").strip().lower()
                if response in ['y', 'yes']:
                    agent.clear_history()
                    print(f"{self.colors.success('Conversation history cleared')}")
                return
            
            if args.backup:
                agent._create_backup()
                print(f"{self.colors.success('Backup created')}")
                return
            
            if args.search:
                results = agent.search_history(args.search)
                if results:
                    print(f"\n{self.colors.highlight(f'Found {len(results)} matches:')}")
                    for result in results:
                        msg = result["message"]
                        timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M:%S")
                        print(f"  [{timestamp}] {msg['role']}: {result['preview']}")
                else:
                    print(f"{self.colors.warning(f'No matches found for \"{args.search}\"')}")
                return
            
            # Apply command line overrides
            overrides = {}
            if args.effort:
                overrides["reasoning_effort"] = args.effort
            if args.temperature is not None:
                if self.validator.validate_temperature(args.temperature):
                    overrides["temperature"] = args.temperature
                else:
                    print(f"{self.colors.error('Temperature must be between 0.0 and 2.0')}")
                    return
            if args.max_tokens:
                overrides["max_output_tokens"] = args.max_tokens
            if args.no_stream:
                overrides["stream"] = False
            if args.system_prompt:
                overrides["system_prompt"] = args.system_prompt
            
            # Apply overrides
            if overrides:
                for key, value in overrides.items():
                    setattr(agent.config, key, value)
                agent._save_config()
            
            # Handle batch mode
            if args.batch:
                batch_file = Path(args.batch)
                if not batch_file.exists():
                    print(f"{self.colors.error(f'Batch file not found: {args.batch}')}")
                    return
                
                try:
                    with open(batch_file, 'r') as f:
                        commands = f.readlines()
                    
                    for i, command in enumerate(commands, 1):
                        command = command.strip()
                        if command and not command.startswith('#'):
                            print(f"{self.colors.dim(f'[{i}] Processing:')} {command}")
                            # Process batch command (simplified for now)
                            for chunk in agent.call_api(command):
                                print(chunk, end="", flush=True)
                            print("\n")
                except Exception as e:
                    print(f"{self.colors.error(f'Error processing batch file: {e}')}")
                return
            
            # Start interactive chat
            self.interactive_chat(agent)
            
        except KeyboardInterrupt:
            print(f"\n{self.colors.warning('Interrupted by user')}")
        except Exception as e:
            if args.debug:
                import traceback
                traceback.print_exc()
            print(f"{self.colors.error(f'Error: {e}')}")
            sys.exit(1)


def main():
    """Main entry point"""
    cli = UnifiedCLI()
    cli.run()


if __name__ == "__main__":
    main()