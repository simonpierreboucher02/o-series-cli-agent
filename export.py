#!/usr/bin/env python3
"""
Conversation Export Module

This module handles all export functionality for the unified OpenAI agent system,
supporting multiple formats including JSON, TXT, Markdown, HTML, and specialized formats.
"""

import json
import html
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path
from dataclasses import asdict


class ConversationExporter:
    """Advanced conversation exporter with multiple format support"""
    
    def __init__(self):
        self.supported_formats = ["json", "txt", "md", "html", "csv", "xml"]
    
    def export_conversation(
        self, 
        format_type: str,
        agent_id: str,
        model: str,
        model_display: str,
        config: Any,
        messages: List[Dict[str, Any]],
        statistics: Dict[str, Any],
        export_dir: Path
    ) -> str:
        """Export conversation to specified format"""
        
        if format_type not in self.supported_formats:
            raise ValueError(f"Unsupported export format: {format_type}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_dir.mkdir(parents=True, exist_ok=True)
        
        # Route to appropriate export method
        if format_type == "json":
            return self._export_json(timestamp, agent_id, model, config, messages, statistics, export_dir)
        elif format_type == "txt":
            return self._export_txt(timestamp, agent_id, model, model_display, messages, export_dir)
        elif format_type == "md":
            return self._export_markdown(timestamp, agent_id, model, model_display, messages, export_dir)
        elif format_type == "html":
            return self._export_html(timestamp, agent_id, model, model_display, config, messages, statistics, export_dir)
        elif format_type == "csv":
            return self._export_csv(timestamp, agent_id, model, messages, export_dir)
        elif format_type == "xml":
            return self._export_xml(timestamp, agent_id, model, config, messages, statistics, export_dir)
    
    def _export_json(
        self, 
        timestamp: str,
        agent_id: str,
        model: str,
        config: Any,
        messages: List[Dict[str, Any]],
        statistics: Dict[str, Any],
        export_dir: Path
    ) -> str:
        """Export to JSON format with comprehensive metadata"""
        filename = f"conversation_{timestamp}.json"
        filepath = export_dir / filename
        
        export_data = {
            "export_info": {
                "version": "2.0",
                "exported_at": datetime.now().isoformat(),
                "exporter": "Unified OpenAI Agent System",
                "format": "json"
            },
            "agent_info": {
                "agent_id": agent_id,
                "model": model,
                "config": asdict(config) if hasattr(config, '__dict__') else config
            },
            "conversation": {
                "messages": messages,
                "statistics": statistics
            },
            "metadata": {
                "total_tokens_estimate": self._estimate_tokens(messages),
                "conversation_topics": self._extract_topics(messages),
                "message_types": self._analyze_message_types(messages)
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
        
        return str(filepath)
    
    def _export_txt(
        self,
        timestamp: str,
        agent_id: str,
        model: str,
        model_display: str,
        messages: List[Dict[str, Any]],
        export_dir: Path
    ) -> str:
        """Export to plain text format"""
        filename = f"conversation_{timestamp}.txt"
        filepath = export_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Header
            f.write(f"OpenAI {model_display} Chat Agent Conversation Export\n")
            f.write("=" * 60 + "\n")
            f.write(f"Agent ID: {agent_id}\n")
            f.write(f"Model: {model}\n")
            f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            # Messages
            for msg in messages:
                timestamp_str = datetime.fromisoformat(msg["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                role = msg["role"].upper()
                content = msg["content"]
                
                f.write(f"[{timestamp_str}] {role}:\n")
                f.write("-" * 40 + "\n")
                f.write(f"{content}\n\n")
        
        return str(filepath)
    
    def _export_markdown(
        self,
        timestamp: str,
        agent_id: str,
        model: str,
        model_display: str,
        messages: List[Dict[str, Any]],
        export_dir: Path
    ) -> str:
        """Export to Markdown format with enhanced formatting"""
        filename = f"conversation_{timestamp}.md"
        filepath = export_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Header
            f.write(f"# 🧠 {model_display} Chat Agent Conversation\n\n")
            f.write(f"**Agent ID:** `{agent_id}`  \n")
            f.write(f"**Model:** `{model}`  \n")
            f.write(f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n\n")
            
            # Table of Contents
            f.write("## 📋 Table of Contents\n\n")
            for i, msg in enumerate(messages, 1):
                role_emoji = "👤" if msg["role"] == "user" else "🤖"
                timestamp_str = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M:%S")
                preview = msg["content"][:50].replace('\n', ' ')
                if len(msg["content"]) > 50:
                    preview += "..."
                f.write(f"{i}. [{role_emoji} {msg['role'].title()} - {timestamp_str}](#message-{i}) - {preview}\n")
            f.write("\n---\n\n")
            
            # Messages
            for i, msg in enumerate(messages, 1):
                timestamp_str = datetime.fromisoformat(msg["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                role_emoji = "👤" if msg["role"] == "user" else "🤖"
                role = msg["role"].title()
                content = msg["content"]
                
                f.write(f"## {role_emoji} {role} <a id=\"message-{i}\"></a>\n\n")
                f.write(f"**Time:** {timestamp_str}  \n")
                f.write(f"**Length:** {len(content)} characters  \n\n")
                
                # Format code blocks and content
                if "```" in content:
                    f.write(f"{content}\n\n")
                else:
                    # Add blockquote formatting for better readability
                    lines = content.split('\n')
                    for line in lines:
                        if line.strip():
                            f.write(f"> {line}\n")
                        else:
                            f.write(">\n")
                    f.write("\n")
                
                f.write("---\n\n")
            
            # Footer
            f.write(f"*Generated by OpenAI {model_display} Chat Agent • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        return str(filepath)
    
    def _export_html(
        self,
        timestamp: str,
        agent_id: str,
        model: str,
        model_display: str,
        config: Any,
        messages: List[Dict[str, Any]],
        statistics: Dict[str, Any],
        export_dir: Path
    ) -> str:
        """Export to HTML format with modern, responsive design"""
        filename = f"conversation_{timestamp}.html"
        filepath = export_dir / filename
        
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 OpenAI {model_display} Conversation - {agent_id}</title>
    <style>
        :root {{
            --primary-color: #6366f1;
            --secondary-color: #f8fafc;
            --accent-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
            --text-primary: #1f2937;
            --text-secondary: #6b7280;
            --border-color: #e5e7eb;
            --user-bg: #3b82f6;
            --assistant-bg: #8b5cf6;
            --code-bg: #f3f4f6;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
            line-height: 1.6;
            color: var(--text-primary);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 1rem;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 1rem;
            box-shadow: var(--shadow-xl);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--assistant-bg) 100%);
            color: white;
            padding: 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            opacity: 0.1;
        }}

        .header-content {{
            position: relative;
            z-index: 1;
        }}

        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: 800;
        }}

        .header-subtitle {{
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 1.5rem;
        }}

        .header-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
            font-size: 0.95rem;
        }}

        .info-card {{
            background: rgba(255, 255, 255, 0.1);
            padding: 1rem;
            border-radius: 0.5rem;
            backdrop-filter: blur(10px);
        }}

        .info-label {{
            font-weight: 600;
            margin-bottom: 0.25rem;
        }}

        .stats {{
            background: var(--secondary-color);
            padding: 2rem;
            border-bottom: 1px solid var(--border-color);
        }}

        .stats h2 {{
            text-align: center;
            margin-bottom: 1.5rem;
            color: var(--text-primary);
            font-size: 1.5rem;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
        }}

        .stat-card {{
            text-align: center;
            padding: 1.5rem;
            background: white;
            border-radius: 0.75rem;
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--border-color);
            transition: all 0.2s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }}

        .stat-value {{
            font-size: 2rem;
            font-weight: 800;
            color: var(--primary-color);
            margin-bottom: 0.25rem;
        }}

        .stat-label {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            font-weight: 500;
        }}

        .messages {{
            padding: 2rem;
            max-height: 70vh;
            overflow-y: auto;
        }}

        .message {{
            margin-bottom: 2rem;
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            animation: fadeIn 0.3s ease;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .message.user {{
            flex-direction: row-reverse;
        }}

        .message-avatar {{
            width: 3.5rem;
            height: 3.5rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: bold;
            color: white;
            flex-shrink: 0;
            box-shadow: var(--shadow-md);
        }}

        .message.user .message-avatar {{
            background: linear-gradient(135deg, var(--user-bg) 0%, #2563eb 100%);
        }}

        .message.assistant .message-avatar {{
            background: linear-gradient(135deg, var(--assistant-bg) 0%, #7c3aed 100%);
        }}

        .message-content {{
            flex: 1;
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: var(--shadow-sm);
            position: relative;
            transition: all 0.2s ease;
        }}

        .message-content:hover {{
            box-shadow: var(--shadow-md);
        }}

        .message.user .message-content {{
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border-color: var(--user-bg);
        }}

        .message.assistant .message-content {{
            background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
            border-color: var(--assistant-bg);
        }}

        .message-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--border-color);
        }}

        .message-role {{
            font-weight: 700;
            text-transform: capitalize;
            font-size: 1.1rem;
        }}

        .message-meta {{
            display: flex;
            gap: 1rem;
            font-size: 0.8rem;
            color: var(--text-secondary);
        }}

        .message-time {{
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }}

        .message-length {{
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }}

        .message-text {{
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1.7;
        }}

        .code-block {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
            overflow-x: auto;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 0.9rem;
            line-height: 1.4;
        }}

        .footer {{
            background: var(--secondary-color);
            padding: 2rem;
            text-align: center;
            font-size: 0.9rem;
            color: var(--text-secondary);
            border-top: 1px solid var(--border-color);
        }}

        .footer-links {{
            margin-top: 1rem;
            display: flex;
            justify-content: center;
            gap: 2rem;
        }}

        .footer-link {{
            color: var(--primary-color);
            text-decoration: none;
            font-weight: 500;
        }}

        .footer-link:hover {{
            text-decoration: underline;
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 0.5rem;
            }}

            .header {{
                padding: 1.5rem;
            }}

            .header h1 {{
                font-size: 2rem;
            }}

            .header-info {{
                grid-template-columns: 1fr;
            }}

            .stats {{
                padding: 1.5rem;
            }}

            .messages {{
                padding: 1rem;
            }}

            .message-content {{
                padding: 1rem;
            }}

            .message-avatar {{
                width: 3rem;
                height: 3rem;
                font-size: 1.2rem;
            }}
        }}

        .scroll-indicator {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: rgba(99, 102, 241, 0.3);
            z-index: 1000;
        }}

        .scroll-progress {{
            height: 100%;
            background: linear-gradient(90deg, var(--primary-color), var(--assistant-bg));
            width: 0%;
            transition: width 0.1s ease;
        }}
    </style>
</head>
<body>
    <div class="scroll-indicator">
        <div class="scroll-progress" id="scrollProgress"></div>
    </div>

    <div class="container">
        <div class="header">
            <div class="header-content">
                <h1>🧠 OpenAI {model_display} Chat Agent</h1>
                <p class="header-subtitle">Advanced AI Conversation Export</p>
                <div class="header-info">
                    <div class="info-card">
                        <div class="info-label">Agent ID</div>
                        <div>{agent_id}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">Model</div>
                        <div>{model}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">Reasoning Effort</div>
                        <div>{getattr(config, 'reasoning_effort', 'medium').title()}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">Exported</div>
                        <div>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">Temperature</div>
                        <div>{getattr(config, 'temperature', 1.0)}</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="stats">
            <h2>📊 Conversation Statistics</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{statistics['total_messages']}</div>
                    <div class="stat-label">Total Messages</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{statistics['user_messages']}</div>
                    <div class="stat-label">User Messages</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{statistics['assistant_messages']}</div>
                    <div class="stat-label">Assistant Messages</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{statistics['total_characters']:,}</div>
                    <div class="stat-label">Total Characters</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{statistics['average_message_length']:,}</div>
                    <div class="stat-label">Avg Message Length</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{statistics.get('conversation_duration', 'N/A')}</div>
                    <div class="stat-label">Duration</div>
                </div>
            </div>
        </div>

        <div class="messages">"""

        # Add messages
        for i, msg in enumerate(messages):
            timestamp_str = datetime.fromisoformat(msg["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            role = msg["role"]
            content = msg["content"]
            
            # Escape HTML and preserve formatting
            content_escaped = html.escape(content)
            
            # Enhanced code block detection
            if '```' in content_escaped:
                parts = content_escaped.split('```')
                formatted_content = ""
                for j, part in enumerate(parts):
                    if j % 2 == 1:  # Code block
                        formatted_content += f'<div class="code-block">{part}</div>'
                    else:  # Regular text
                        formatted_content += part
                content_escaped = formatted_content
            
            avatar_text = "👤" if role == "user" else "🤖"
            
            html_template += f"""
            <div class="message {role}">
                <div class="message-avatar">{avatar_text}</div>
                <div class="message-content">
                    <div class="message-header">
                        <span class="message-role">{role}</span>
                        <div class="message-meta">
                            <span class="message-time">🕒 {timestamp_str}</span>
                            <span class="message-length">📝 {len(content):,} chars</span>
                        </div>
                    </div>
                    <div class="message-text">{content_escaped}</div>
                </div>
            </div>"""

        # Close HTML
        html_template += f"""
        </div>

        <div class="footer">
            <p>Generated by OpenAI {model_display} Chat Agent</p>
            <p>Agent ID: <strong>{agent_id}</strong> • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <div class="footer-links">
                <a href="#" class="footer-link" onclick="window.print()">🖨️ Print</a>
                <a href="#" class="footer-link" onclick="scrollToTop()">⬆️ Top</a>
            </div>
        </div>
    </div>

    <script>
        // Scroll progress indicator
        window.addEventListener('scroll', function() {{
            const scrollProgress = document.getElementById('scrollProgress');
            const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
            const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrollPercentage = (scrollTop / scrollHeight) * 100;
            scrollProgress.style.width = scrollPercentage + '%';
        }});

        // Smooth scroll to top
        function scrollToTop() {{
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        // Add copy functionality to code blocks
        document.addEventListener('DOMContentLoaded', function() {{
            const codeBlocks = document.querySelectorAll('.code-block');
            codeBlocks.forEach(function(block) {{
                block.addEventListener('click', function() {{
                    navigator.clipboard.writeText(block.textContent);
                    // Visual feedback
                    const originalBg = block.style.backgroundColor;
                    block.style.backgroundColor = '#10b981';
                    setTimeout(() => {{
                        block.style.backgroundColor = originalBg;
                    }}, 200);
                }});
                block.style.cursor = 'pointer';
                block.title = 'Click to copy';
            }});
        }});
    </script>
</body>
</html>"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        return str(filepath)
    
    def _export_csv(
        self,
        timestamp: str,
        agent_id: str,
        model: str,
        messages: List[Dict[str, Any]],
        export_dir: Path
    ) -> str:
        """Export to CSV format for data analysis"""
        filename = f"conversation_{timestamp}.csv"
        filepath = export_dir / filename
        
        import csv
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Timestamp', 'Role', 'Content', 'Character_Count', 
                'Word_Count', 'Message_Index', 'Agent_ID', 'Model'
            ])
            
            # Data rows
            for i, msg in enumerate(messages):
                content = msg['content'].replace('\n', ' ').replace('\r', ' ')
                word_count = len(content.split())
                
                writer.writerow([
                    msg['timestamp'],
                    msg['role'],
                    content,
                    len(msg['content']),
                    word_count,
                    i + 1,
                    agent_id,
                    model
                ])
        
        return str(filepath)
    
    def _export_xml(
        self,
        timestamp: str,
        agent_id: str,
        model: str,
        config: Any,
        messages: List[Dict[str, Any]],
        statistics: Dict[str, Any],
        export_dir: Path
    ) -> str:
        """Export to XML format"""
        filename = f"conversation_{timestamp}.xml"
        filepath = export_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<conversation>\n')
            f.write(f'  <metadata>\n')
            f.write(f'    <agent_id>{html.escape(agent_id)}</agent_id>\n')
            f.write(f'    <model>{html.escape(model)}</model>\n')
            f.write(f'    <exported_at>{datetime.now().isoformat()}</exported_at>\n')
            f.write(f'  </metadata>\n')
            f.write(f'  <statistics>\n')
            for key, value in statistics.items():
                f.write(f'    <{key}>{html.escape(str(value))}</{key}>\n')
            f.write(f'  </statistics>\n')
            f.write(f'  <messages>\n')
            
            for i, msg in enumerate(messages):
                f.write(f'    <message index="{i + 1}">\n')
                f.write(f'      <timestamp>{msg["timestamp"]}</timestamp>\n')
                f.write(f'      <role>{html.escape(msg["role"])}</role>\n')
                f.write(f'      <content><![CDATA[{msg["content"]}]]></content>\n')
                f.write(f'      <character_count>{len(msg["content"])}</character_count>\n')
                f.write(f'    </message>\n')
            
            f.write(f'  </messages>\n')
            f.write('</conversation>\n')
        
        return str(filepath)
    
    def _estimate_tokens(self, messages: List[Dict[str, Any]]) -> int:
        """Rough token estimation (4 characters ≈ 1 token)"""
        total_chars = sum(len(msg['content']) for msg in messages)
        return total_chars // 4
    
    def _extract_topics(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Extract potential topics from conversation"""
        # Simple keyword extraction
        import re
        
        all_text = ' '.join(msg['content'] for msg in messages if msg['role'] == 'user')
        words = re.findall(r'\b[A-Z][a-z]+\b', all_text)
        
        # Count frequency and return top topics
        from collections import Counter
        word_counts = Counter(words)
        return [word for word, count in word_counts.most_common(10)]
    
    def _analyze_message_types(self, messages: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze types of messages in the conversation"""
        types = {
            'questions': 0,
            'code_blocks': 0,
            'long_messages': 0,
            'short_messages': 0
        }
        
        for msg in messages:
            content = msg['content']
            
            # Count questions
            if '?' in content:
                types['questions'] += 1
            
            # Count code blocks
            if '```' in content:
                types['code_blocks'] += 1
            
            # Count by length
            if len(content) > 500:
                types['long_messages'] += 1
            elif len(content) < 50:
                types['short_messages'] += 1
        
        return types