#!/usr/bin/env python3
"""
Utility Functions Module

This module provides utility functions and classes for the unified OpenAI agent system,
including color management, file handling, security, and UI enhancements.
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime


class ColorManager:
    """Enhanced color management with fallback support"""
    
    def __init__(self):
        self.colors_available = self._check_color_support()
        self._setup_colors()
    
    def _check_color_support(self) -> bool:
        """Check if terminal supports colors"""
        try:
            # Try to import colorama
            from colorama import init as colorama_init
            colorama_init(autoreset=True)
            return True
        except ImportError:
            # Check environment variables
            return (
                os.getenv('FORCE_COLOR') == '1' or
                (hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()) or
                os.getenv('TERM', '').lower() in ['xterm', 'xterm-color', 'xterm-256color', 'screen', 'screen-256color']
            )
    
    def _setup_colors(self):
        """Setup color codes"""
        if self.colors_available:
            try:
                from colorama import Fore, Style, Back
                self.colors = {
                    'RED': Fore.RED,
                    'GREEN': Fore.GREEN,
                    'YELLOW': Fore.YELLOW,
                    'BLUE': Fore.BLUE,
                    'MAGENTA': Fore.MAGENTA,
                    'CYAN': Fore.CYAN,
                    'WHITE': Fore.WHITE,
                    'BRIGHT': Style.BRIGHT,
                    'DIM': Style.DIM,
                    'RESET': Style.RESET_ALL,
                    'BG_BLACK': Back.BLACK,
                    'BG_RED': Back.RED,
                    'BG_GREEN': Back.GREEN,
                    'BG_YELLOW': Back.YELLOW,
                    'BG_BLUE': Back.BLUE,
                    'BG_MAGENTA': Back.MAGENTA,
                    'BG_CYAN': Back.CYAN,
                    'BG_WHITE': Back.WHITE
                }
            except ImportError:
                # ANSI color codes fallback
                self.colors = {
                    'RED': '\033[91m',
                    'GREEN': '\033[92m',
                    'YELLOW': '\033[93m',
                    'BLUE': '\033[94m',
                    'MAGENTA': '\033[95m',
                    'CYAN': '\033[96m',
                    'WHITE': '\033[97m',
                    'BRIGHT': '\033[1m',
                    'DIM': '\033[2m',
                    'RESET': '\033[0m',
                    'BG_BLACK': '\033[40m',
                    'BG_RED': '\033[41m',
                    'BG_GREEN': '\033[42m',
                    'BG_YELLOW': '\033[43m',
                    'BG_BLUE': '\033[44m',
                    'BG_MAGENTA': '\033[45m',
                    'BG_CYAN': '\033[46m',
                    'BG_WHITE': '\033[47m'
                }
        else:
            # No color fallback
            self.colors = {key: '' for key in [
                'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE',
                'BRIGHT', 'DIM', 'RESET', 'BG_BLACK', 'BG_RED', 'BG_GREEN',
                'BG_YELLOW', 'BG_BLUE', 'BG_MAGENTA', 'BG_CYAN', 'BG_WHITE'
            ]}
    
    def format_text(self, color: str, text: str = '') -> str:
        """Format text with color"""
        if text:
            return f"{self.colors.get(color, '')}{text}{self.colors.get('RESET', '')}"
        return self.colors.get(color, '')
    
    def success(self, text: str) -> str:
        """Format success message"""
        return self.format_text('GREEN', f"✅ {text}")
    
    def error(self, text: str) -> str:
        """Format error message"""
        return self.format_text('RED', f"❌ {text}")
    
    def warning(self, text: str) -> str:
        """Format warning message"""
        return self.format_text('YELLOW', f"⚠️  {text}")
    
    def info(self, text: str) -> str:
        """Format info message"""
        return self.format_text('BLUE', f"ℹ️  {text}")
    
    def highlight(self, text: str) -> str:
        """Highlight text"""
        return self.format_text('CYAN', text)
    
    def bold(self, text: str) -> str:
        """Bold text"""
        return f"{self.colors.get('BRIGHT', '')}{text}{self.colors.get('RESET', '')}"
    
    def dim(self, text: str) -> str:
        """Dim text"""
        return f"{self.colors.get('DIM', '')}{text}{self.colors.get('RESET', '')}"


class FileHandler:
    """Advanced file handling with security and validation"""
    
    # Enhanced file extensions support
    SUPPORTED_EXTENSIONS = {
        # Programming languages
        '.py', '.r', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.cc', '.cxx',
        '.h', '.hpp', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala',
        '.clj', '.hs', '.ml', '.fs', '.vb', '.pl', '.pm', '.sh', '.bash', '.zsh', '.fish',
        '.ps1', '.bat', '.cmd', '.sql', '.html', '.htm', '.css', '.scss', '.sass', '.less',
        '.xml', '.xsl', '.xslt', '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf',
        '.properties', '.env', '.dockerfile', '.docker', '.makefile', '.cmake', '.gradle',
        '.sbt', '.pom', '.lock', '.mod', '.sum', '.proto', '.graphql', '.gql', '.prisma',
        
        # Data and markup
        '.md', '.markdown', '.rst', '.tex', '.latex', '.csv', '.tsv', '.jsonl', '.ndjson',
        '.svg', '.rss', '.atom', '.plist', '.hcl', '.tf', '.tfvars',
        
        # Configuration and infrastructure
        '.nomad', '.consul', '.vault', '.k8s', '.kubectl', '.helm', '.kustomize',
        '.ansible', '.inventory', '.playbook', '.requirements', '.pipfile',
        
        # Documentation and text
        '.txt', '.log', '.out', '.err', '.trace', '.debug', '.info', '.warn', '.error',
        '.readme', '.license', '.changelog', '.authors', '.contributors', '.todo',
        '.notes', '.docs',
        
        # Notebooks and scripts
        '.ipynb', '.rmd', '.qmd', '.jl', '.m', '.octave', '.R', '.Rmd', '.nb',
        
        # Web and API
        '.rest', '.http', '.api', '.postman', '.insomnia', '.har',
        
        # Other useful formats
        '.editorconfig', '.gitignore', '.gitattributes', '.dockerignore', '.eslintrc',
        '.prettierrc', '.babelrc', '.webpack', '.rollup', '.vite', '.parcel',
        '.browserslistrc', '.nvmrc', '.npmrc', '.yarnrc'
    }
    
    KNOWN_FILENAMES = {
        'makefile', 'dockerfile', 'rakefile', 'gemfile', 'podfile',
        'readme', 'license', 'changelog', 'authors', 'contributors',
        'todo', 'manifest', 'requirements', 'pipfile', 'poetry',
        'cmakelists.txt', 'configure', 'install', 'news', 'copying'
    }
    
    def __init__(self):
        self.max_file_size = 2 * 1024 * 1024  # 2MB default
        self.encoding_fallbacks = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
    
    def is_supported_file(self, file_path: Path) -> bool:
        """Check if file is supported for inclusion"""
        if file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
            return True
        
        return file_path.name.lower() in self.KNOWN_FILENAMES
    
    def read_file_safely(self, file_path: Path) -> Optional[str]:
        """Safely read file with encoding detection and size limits"""
        try:
            # Check file size
            if file_path.stat().st_size > self.max_file_size:
                return None
            
            # Try different encodings
            for encoding in self.encoding_fallbacks:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    return content
                except UnicodeDecodeError:
                    continue
            
            return None
        except Exception:
            return None
    
    def process_file_inclusions(self, content: str, base_dir: Path, logger) -> str:
        """Process {filename} patterns with enhanced file inclusion"""
        def replace_file(match):
            filename = match.group(1)
            
            # Search paths with priority
            search_paths = [
                Path('.'),
                Path('src'),
                Path('lib'),
                Path('scripts'),
                Path('data'),
                Path('documents'),
                Path('files'),
                Path('config'),
                Path('configs'),
                Path('examples'),
                Path('samples'),
                Path('templates'),
                base_dir / 'uploads'
            ]
            
            for search_path in search_paths:
                file_path = search_path / filename
                if file_path.exists() and file_path.is_file():
                    
                    # Security check - prevent path traversal
                    try:
                        file_path.resolve().relative_to(Path('.').resolve())
                    except ValueError:
                        logger.warning(f"Security: Path traversal attempt blocked for {filename}")
                        return f"[SECURITY: Access denied for {filename}]"
                    
                    # Check if file is supported
                    if not self.is_supported_file(file_path):
                        logger.warning(f"Unsupported file type: {filename}")
                        return f"[WARNING: Unsupported file type {filename}]"
                    
                    # Read file safely
                    file_content = self.read_file_safely(file_path)
                    if file_content is None:
                        if file_path.stat().st_size > self.max_file_size:
                            logger.error(f"File {filename} too large (max {self.max_file_size//1024//1024}MB)")
                            return f"[ERROR: File {filename} too large (max {self.max_file_size//1024//1024}MB)]"
                        else:
                            logger.error(f"Could not read file {filename}")
                            return f"[ERROR: Could not read {filename}]"
                    
                    # Add enhanced file info header
                    file_info = self._generate_file_header(filename, file_path)
                    full_content = file_info + file_content
                    
                    logger.info(f"Included file: {filename} ({len(file_content)} chars, {file_path.suffix})")
                    return full_content
            
            logger.warning(f"File not found: {filename}")
            return f"[ERROR: File {filename} not found]"
        
        return re.sub(r'\{([^}]+)\}', replace_file, content)
    
    def _generate_file_header(self, filename: str, file_path: Path) -> str:
        """Generate appropriate file header based on file type"""
        extension = file_path.suffix.lower()
        
        # Language-specific comment styles
        comment_styles = {
            ('.py', '.r', '.sh', '.bash', '.zsh', '.fish', '.yml', '.yaml', '.toml'): lambda f, e: f"# File: {f} ({e})\n",
            ('.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.cc', '.cxx', '.h', '.hpp', '.cs', '.go', '.rs', '.swift', '.kt', '.scala'): lambda f, e: f"// File: {f} ({e})\n",
            ('.html', '.htm', '.xml', '.xsl', '.xslt', '.svg'): lambda f, e: f"<!-- File: {f} ({e}) -->\n",
            ('.css', '.scss', '.sass', '.less'): lambda f, e: f"/* File: {f} ({e}) */\n",
            ('.sql',): lambda f, e: f"-- File: {f} ({e})\n",
            ('.php',): lambda f, e: f"<?php\n// File: {f} ({e})\n",
            ('.rb',): lambda f, e: f"# File: {f} ({e})\n",
            ('.hs',): lambda f, e: f"-- File: {f} ({e})\n",
            ('.ml', '.fs'): lambda f, e: f"(* File: {f} ({e}) *)\n",
            ('.clj',): lambda f, e: f";; File: {f} ({e})\n"
        }
        
        for extensions, comment_func in comment_styles.items():
            if extension in extensions:
                return comment_func(filename, extension)
        
        # Default comment style
        return f"# File: {filename} ({extension})\n"
    
    def list_files(self, base_dir: Path) -> List[str]:
        """List available files for inclusion with enhanced information"""
        files = []
        search_paths = [
            Path('.'),
            Path('src'),
            Path('lib'),
            Path('scripts'),
            Path('data'),
            Path('documents'),
            Path('files'),
            Path('config'),
            Path('configs'),
            Path('examples'),
            Path('samples'),
            Path('templates'),
            base_dir / 'uploads'
        ]
        
        for search_path in search_paths:
            if search_path.exists():
                for file_path in search_path.rglob("*"):
                    if (
                        file_path.is_file() and
                        not file_path.name.startswith('.') and
                        self.is_supported_file(file_path)
                    ):
                        try:
                            size = file_path.stat().st_size
                            if size > self.max_file_size:
                                size_str = f"{size/(1024*1024):.1f} MB (too large)"
                                status = "❌"
                            elif size < 1024:
                                size_str = f"{size} bytes"
                                status = "✅"
                            elif size < 1024*1024:
                                size_str = f"{size/1024:.1f} KB"
                                status = "✅"
                            else:
                                size_str = f"{size/(1024*1024):.1f} MB"
                                status = "✅"
                            
                            # Get modification time
                            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                            time_str = mtime.strftime("%Y-%m-%d %H:%M")
                            
                            files.append(f"{status} {file_path} ({size_str}) [{file_path.suffix}] {time_str}")
                        except Exception:
                            files.append(f"❓ {file_path} (unknown size) [{file_path.suffix}]")
        
        return sorted(files)


class SecurityManager:
    """Security utilities for API key management and validation"""
    
    def __init__(self):
        self.colors = ColorManager()
    
    def get_api_key(self, model: str, base_dir: Path) -> str:
        """Securely get API key from environment, file, or prompt"""
        # First try environment variable
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            return api_key
        
        # Try secrets file
        secrets_file = base_dir / "secrets.json"
        if secrets_file.exists():
            try:
                with open(secrets_file, 'r') as f:
                    secrets = json.load(f)
                    keys = secrets.get('keys', {})
                    api_key = keys.get(model) or keys.get('default')
                    if api_key:
                        return api_key
            except Exception:
                pass
        
        # Prompt user for API key with enhanced UX
        from config import ModelConfig
        model_config = ModelConfig.get_model_config(model)
        model_display = model_config["name"]
        
        print(f"\n{self.colors.warning('API key not found')}")
        print(f"{self.colors.info('For OpenAI ' + model_display + ' model')}")
        print(f"{self.colors.dim('You can set the OPENAI_API_KEY environment variable or enter it now.')}")
        print()
        
        # Show pricing info
        pricing = model_config.get("pricing", {})
        if pricing:
            print(f"{self.colors.highlight('Pricing Information:')}")
            print(f"  Input:  ${pricing.get('input', 0):.4f} per 1K tokens")
            print(f"  Output: ${pricing.get('output', 0):.4f} per 1K tokens")
            print()
        
        while True:
            try:
                api_key = input(f"{self.colors.format_text('CYAN')}Enter API key for OpenAI {model_display}: {self.colors.format_text('RESET')}").strip()
                
                if not api_key:
                    print(f"{self.colors.error('API key is required')}")
                    continue
                
                # Basic validation
                if not self._validate_api_key_format(api_key):
                    print(f"{self.colors.error('Invalid API key format')}")
                    continue
                
                break
                
            except KeyboardInterrupt:
                print(f"\n{self.colors.warning('Operation cancelled')}")
                sys.exit(1)
        
        # Save to secrets file
        self._save_api_key(api_key, model, secrets_file)
        
        return api_key
    
    def _validate_api_key_format(self, api_key: str) -> bool:
        """Basic API key format validation"""
        if not api_key:
            return False
        
        # OpenAI API keys typically start with 'sk-' and are ~51 characters
        if api_key.startswith('sk-') and len(api_key) >= 40:
            return True
        
        return False
    
    def _save_api_key(self, api_key: str, model: str, secrets_file: Path):
        """Save API key to secrets file with proper security"""
        secrets = {
            "provider": "openai",
            "created_at": datetime.now().isoformat(),
            "keys": {
                "default": api_key,
                model: api_key
            }
        }
        
        try:
            # Create secrets file with restricted permissions
            secrets_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(secrets_file, 'w') as f:
                json.dump(secrets, f, indent=2)
            
            # Set restrictive permissions (owner only)
            try:
                os.chmod(secrets_file, 0o600)
            except Exception:
                pass  # Ignore permission errors on Windows
            
            # Update .gitignore
            self._update_gitignore()
            
            masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
            print(f"{self.colors.success(f'API key saved ({masked_key})')}")
            
        except Exception as e:
            print(f"{self.colors.error(f'Warning: Could not save API key to file: {e}')}")
    
    def _update_gitignore(self):
        """Update .gitignore to exclude secrets"""
        gitignore_file = Path('.gitignore')
        gitignore_content = ""
        
        if gitignore_file.exists():
            gitignore_content = gitignore_file.read_text()
        
        # Add secrets patterns if not present
        patterns_to_add = [
            "# API Keys and Secrets",
            "**/secrets.json",
            "secrets.json",
            ".env",
            "**/.env"
        ]
        
        patterns_needed = []
        for pattern in patterns_to_add:
            if pattern not in gitignore_content:
                patterns_needed.append(pattern)
        
        if patterns_needed:
            with open(gitignore_file, 'a', encoding='utf-8') as f:
                if gitignore_content and not gitignore_content.endswith('\n'):
                    f.write('\n')
                f.write('\n' + '\n'.join(patterns_needed) + '\n')


class UIEnhancer:
    """UI enhancement utilities for better user experience"""
    
    def __init__(self):
        self.colors = ColorManager()
        self.terminal_width = self._get_terminal_width()
    
    def _get_terminal_width(self) -> int:
        """Get terminal width with fallback"""
        try:
            return os.get_terminal_size().columns
        except:
            return 80  # Fallback width
    
    def print_banner(self, title: str, subtitle: str = ""):
        """Print an attractive banner"""
        width = min(self.terminal_width, 80)
        
        print()
        print(self.colors.format_text('CYAN', '=' * width))
        
        # Center the title
        title_line = f"  🤖 {title}  "
        padding = (width - len(title_line)) // 2
        print(self.colors.format_text('CYAN', '=') + ' ' * padding + 
              self.colors.bold(title_line) + ' ' * padding + 
              self.colors.format_text('CYAN', '='))
        
        if subtitle:
            subtitle_line = f"  {subtitle}  "
            padding = (width - len(subtitle_line)) // 2
            print(self.colors.format_text('CYAN', '=') + ' ' * padding + 
                  self.colors.dim(subtitle_line) + ' ' * padding + 
                  self.colors.format_text('CYAN', '='))
        
        print(self.colors.format_text('CYAN', '=' * width))
        print()
    
    def print_section(self, title: str):
        """Print a section header"""
        print(f"\n{self.colors.highlight(f'━━━ {title} ━━━')}")
    
    def print_model_info(self, model: str, model_config: Dict[str, Any]):
        """Print formatted model information"""
        print(f"{self.colors.highlight('Model Information:')}")
        print(f"  {self.colors.bold('Name:')} {model_config['name']} ({model})")
        print(f"  {self.colors.bold('Description:')} {model_config['description']}")
        
        # Reasoning timeouts
        timeouts = model_config.get('reasoning_timeout', {})
        if timeouts:
            print(f"  {self.colors.bold('Timeouts:')}")
            for effort, timeout in timeouts.items():
                mins = timeout // 60
                secs = timeout % 60
                print(f"    {effort.title()}: {timeout}s ({mins}m {secs}s)")
        
        # Pricing info
        pricing = model_config.get('pricing', {})
        if pricing:
            print(f"  {self.colors.bold('Pricing:')}")
            print(f"    Input: ${pricing.get('input', 0):.4f} per 1K tokens")
            print(f"    Output: ${pricing.get('output', 0):.4f} per 1K tokens")
    
    def print_progress_bar(self, current: int, total: int, width: int = 30):
        """Print a progress bar"""
        if total == 0:
            return
        
        progress = current / total
        filled = int(width * progress)
        bar = '█' * filled + '░' * (width - filled)
        percentage = int(progress * 100)
        
        print(f"\r{self.colors.format_text('GREEN', bar)} {percentage}% ({current}/{total})", end='', flush=True)
    
    def print_table(self, headers: List[str], rows: List[List[str]], title: str = ""):
        """Print a formatted table"""
        if not rows:
            return
        
        # Calculate column widths
        widths = [len(header) for header in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(widths):
                    widths[i] = max(widths[i], len(str(cell)))
        
        # Print title
        if title:
            total_width = sum(widths) + len(widths) * 3 - 1
            print(f"\n{self.colors.highlight(title)}")
            print(self.colors.dim('─' * total_width))
        
        # Print header
        header_row = " │ ".join(headers[i].ljust(widths[i]) for i in range(len(headers)))
        print(f"{self.colors.bold(header_row)}")
        
        # Print separator
        separator = "─┼─".join('─' * width for width in widths)
        print(self.colors.dim(separator))
        
        # Print rows
        for row in rows:
            formatted_row = " │ ".join(str(row[i]).ljust(widths[i]) if i < len(row) else " " * widths[i] 
                                     for i in range(len(widths)))
            print(formatted_row)
    
    def print_loading_animation(self, message: str, duration: float = 2.0):
        """Print a loading animation"""
        import time
        
        frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for frame in frames:
                if time.time() >= end_time:
                    break
                print(f"\r{self.colors.format_text('CYAN', frame)} {message}", end='', flush=True)
                time.sleep(0.1)
        
        print(f"\r{self.colors.success('✓')} {message}")


class ValidationUtils:
    """Validation utilities for various inputs and configurations"""
    
    @staticmethod
    def validate_agent_id(agent_id: str) -> bool:
        """Validate agent ID format"""
        if not agent_id:
            return False
        
        # Allow alphanumeric, hyphens, and underscores
        return re.match(r'^[a-zA-Z0-9_-]+$', agent_id) is not None
    
    @staticmethod
    def validate_temperature(temperature: float) -> bool:
        """Validate temperature range"""
        return 0.0 <= temperature <= 2.0
    
    @staticmethod
    def validate_reasoning_effort(effort: str) -> bool:
        """Validate reasoning effort"""
        return effort in ["low", "medium", "high"]
    
    @staticmethod
    def validate_export_format(format_type: str) -> bool:
        """Validate export format"""
        return format_type in ["json", "txt", "md", "html", "csv", "xml"]
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe file operations"""
        # Remove or replace unsafe characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove any path separators
        sanitized = sanitized.replace('..', '_')
        # Limit length
        if len(sanitized) > 255:
            sanitized = sanitized[:255]
        return sanitized


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def get_system_info() -> Dict[str, str]:
    """Get system information for debugging"""
    import platform
    
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": platform.python_version(),
        "architecture": platform.architecture()[0],
        "terminal_width": str(os.get_terminal_size().columns if hasattr(os, 'get_terminal_size') else "unknown"),
        "encoding": sys.stdout.encoding or "unknown"
    }