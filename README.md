# 🧠 Unified OpenAI o Series Agent System
**Author:** Simon-Pierre Boucher
<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-API-green?logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Version](https://img.shields.io/badge/Version-2.0.0-purple)

**A professional, feature-rich command-line interface for OpenAI's reasoning models**

*Supporting O1, O3, O3-mini, and O4-mini with advanced conversation management*

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Usage](#-usage) • [Documentation](#-documentation)

</div>

---

## 🌟 Features

### 🤖 **Multi-Model Support**
- **O1 Model**: Advanced reasoning (up to 15min timeout)
- **O3 Model**: Latest generation (up to 20min timeout)  
- **O3-mini**: Compact and efficient (up to 10min timeout)
- **O4-mini**: Fast and optimized (up to 8min timeout)

### 💬 **Advanced Chat Interface**
- 🎨 **Beautiful CLI** with colors, emojis, and responsive design
- ⚡ **Real-time streaming** responses with progress indicators
- 📁 **File inclusion** support - use `{filename}` to include any file
- 🔍 **Smart search** through conversation history
- 📊 **Rich statistics** and conversation analytics

### ⚙️ **Professional Configuration**
- 🎯 **Configuration presets**: Creative, Balanced, Focused, Fast
- 🛠️ **Interactive setup** wizard with validation
- 🔧 **Fine-grained control** over all model parameters
- 💾 **Persistent settings** with automatic backup

### 📤 **Multi-Format Export**
- 📄 **JSON**: Complete data with metadata
- 📝 **TXT**: Clean plain text format
- 📖 **Markdown**: Formatted with syntax highlighting
- 🌐 **HTML**: Beautiful responsive web page
- 📊 **CSV**: Data analysis friendly
- 🗂️ **XML**: Structured data format

### 🛡️ **Security & Reliability**
- 🔐 **Secure API key management** with encryption
- 🚫 **Path traversal protection** for file inclusion
- 🔄 **Automatic retries** with exponential backoff
- 💾 **Rolling backups** of conversation history

---

## 🚀 Installation

### Prerequisites
- **Python 3.8+** (3.10+ recommended)
- **OpenAI API key** with access to reasoning models

### Install Dependencies
```bash
# Clone or download the repository
cd o-series

# Install required packages
pip install -r requirements.txt

# Optional: Install additional features
pip install rich click python-dotenv
```

### Setup API Key
Choose one of these methods:

**Method 1: Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Method 2: Interactive Setup**
```bash
python main.py --agent-id test --model o1
# You'll be prompted to enter your API key
```

**Method 3: Manual Configuration**
Create `agents/your-agent-id/secrets.json`:
```json
{
  "provider": "openai",
  "keys": {
    "default": "your-api-key-here"
  }
}
```

---

## ⚡ Quick Start

### 1. **Start Your First Chat**
```bash
# Basic chat with O1 model
python main.py --agent-id my-first-agent --model o1

# Creative writing with O3-mini
python main.py --agent-id writer --model o3-mini --preset creative

# Fast responses with O4-mini
python main.py --agent-id quick-chat --model o4-mini --preset fast
```

### 2. **Explore Available Models**
```bash
# See all available models with details
python main.py --models

# List your existing agents
python main.py --list
```

### 3. **Configure Your Agent**
```bash
# Interactive configuration wizard
python main.py --agent-id my-agent --config

# Apply a preset configuration
python main.py --agent-id my-agent --preset balanced
```

---

## 📖 Usage

### **Basic Commands**

| Command | Description | Example |
|---------|-------------|---------|
| `--agent-id` | Specify agent identifier | `--agent-id research` |
| `--model` | Choose model (o1, o3, o3-mini, o4-mini) | `--model o3-mini` |
| `--list` | Show all agents | `python main.py --list` |
| `--models` | Show model information | `python main.py --models` |
| `--export` | Export conversation | `--export html` |

### **Configuration Options**

| Parameter | Description | Values |
|-----------|-------------|--------|
| `--preset` | Use configuration preset | `creative`, `balanced`, `focused`, `fast` |
| `--effort` | Reasoning effort level | `low`, `medium`, `high` |
| `--temperature` | Response creativity | `0.0` - `2.0` |
| `--max-tokens` | Maximum response length | Any positive integer |
| `--system-prompt` | Set system instructions | Any text string |

### **Interactive Chat Commands**

Once in chat mode, use these commands:

| Command | Description |
|---------|-------------|
| `/help` | Show all available commands |
| `/history [n]` | Show last n messages |
| `/search <term>` | Search conversation history |
| `/stats` | Show conversation statistics |
| `/export <format>` | Export conversation |
| `/preset [name]` | Show/apply presets |
| `/files` | List available files for inclusion |
| `/quit` | Exit chat |

---

## 🎯 Advanced Usage Examples

### **File Inclusion**
Include any supported file in your messages:
```
Analyze this code: {script.py}

Review my configuration: {config.yaml}

Compare these files: {file1.js} and {file2.js}
```

**Supported file types**: Python, JavaScript, TypeScript, Java, C/C++, Go, Rust, HTML, CSS, JSON, YAML, Markdown, and 50+ more formats.

### **Batch Processing**
```bash
# Process multiple prompts from a file
python main.py --agent-id batch --batch prompts.txt

# Export in all formats
python main.py --agent-id my-agent --export-all
```

### **Advanced Configuration**
```bash
# High creativity, detailed reasoning
python main.py --agent-id creative --model o3 --temperature 1.5 --effort high

# Fast, focused responses
python main.py --agent-id focused --model o4-mini --temperature 0.3 --effort low --no-stream
```

### **Search & Analytics**
```bash
# Search conversation history
python main.py --agent-id my-agent --search "machine learning"

# Show detailed agent information
python main.py --info my-agent

# View conversation statistics
python main.py --stats my-agent
```

---

## 📁 Project Structure

```
o-series/
├── 📄 main.py          # CLI entry point with legendary UX
├── 🤖 agent.py         # Unified agent system for all models
├── ⚙️ config.py        # Configuration management & presets
├── 📤 export.py        # Multi-format conversation export
├── 🛠️ utils.py         # Utilities (colors, files, security, UI)
├── 📋 requirements.txt # Python dependencies
├── 📖 README.md        # This file
└── 📁 agents/          # Agent data (auto-created)
    └── 📁 {agent-id}/
        ├── 💬 history.json     # Conversation history
        ├── ⚙️ config.yaml      # Agent configuration
        ├── 🔐 secrets.json     # API keys (auto-created)
        ├── 📁 backups/         # Rolling backups
        ├── 📁 exports/         # Exported conversations
        ├── 📁 logs/            # Debug logs
        └── 📁 uploads/         # File uploads
```

---

## 🎨 Configuration Presets

### **Creative** 🎨
- **Temperature**: 1.5 (high creativity)
- **Reasoning**: High effort, detailed summary
- **Best for**: Creative writing, brainstorming, artistic projects

### **Balanced** ⚖️
- **Temperature**: 1.0 (moderate creativity)  
- **Reasoning**: Medium effort, auto summary
- **Best for**: General conversations, Q&A, learning

### **Focused** 🎯
- **Temperature**: 0.3 (low creativity)
- **Reasoning**: High effort, detailed analysis
- **Best for**: Analysis, research, technical discussions

### **Fast** ⚡
- **Temperature**: 0.7 (balanced)
- **Reasoning**: Low effort, minimal summary
- **Best for**: Quick questions, simple tasks, rapid iteration

---

## 🔧 Model Specifications

| Model | Name | Timeout (Low/Med/High) | Context | Best For |
|-------|------|----------------------|---------|----------|
| `o1` | O1 | 3m / 8m / 15m | 128K | Complex reasoning, research |
| `o3` | O3 | 4m / 10m / 20m | 128K | Latest capabilities, advanced tasks |  
| `o3-mini` | O3 Mini | 2m / 5m / 10m | 128K | Balanced performance and speed |
| `o4-mini` | O4 Mini | 1.5m / 4m / 8m | 128K | Fast responses, simple tasks |

---

## 📊 Export Formats

### **JSON** 📄
Complete conversation data with metadata, statistics, and configuration.
```json
{
  "export_info": { "version": "2.0", "format": "json" },
  "agent_info": { "agent_id": "...", "model": "..." },
  "conversation": { "messages": [...], "statistics": {...} }
}
```

### **HTML** 🌐
Beautiful, responsive web page with:
- Modern CSS design with dark/light theme support
- Syntax highlighting for code blocks
- Interactive elements (copy code, scroll progress)
- Detailed statistics dashboard
- Mobile-friendly responsive layout

### **Markdown** 📖
Clean, GitHub-compatible format with:
- Table of contents with jump links
- Syntax highlighting for code blocks  
- Proper message formatting with timestamps
- Emoji indicators for user/assistant roles

---

## 🛡️ Security Features

- **🔐 Secure API Key Storage**: Keys encrypted and stored with restricted file permissions
- **🚫 Path Traversal Protection**: File inclusion system prevents directory traversal attacks
- **✅ Input Validation**: All user inputs validated and sanitized
- **🔄 Safe File Handling**: Size limits, encoding detection, and error handling
- **📝 Audit Logging**: Comprehensive logs for debugging and security monitoring

---

## 🎯 Pro Tips

### **Maximize Model Performance**
- Use **high reasoning effort** for complex analytical tasks
- Use **low reasoning effort** for simple questions to save time
- Adjust **temperature** based on creativity needs (0.0 = deterministic, 2.0 = very creative)

### **Efficient File Management**
- Organize files in standard directories (`src/`, `docs/`, `config/`)
- Use descriptive filenames for better file inclusion
- Keep included files under 2MB for optimal performance

### **Conversation Management**  
- Use `/backup` before making major configuration changes
- Export important conversations in multiple formats
- Use `/search` to quickly find specific information
- Regular `/clear` for fresh contexts on new topics

### **Workflow Integration**
- Create different agents for different use cases (coding, writing, research)
- Use batch mode for processing multiple similar tasks
- Export HTML for sharing conversations with stakeholders

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **🐛 Report bugs** - Open an issue with detailed reproduction steps
2. **💡 Suggest features** - Describe your use case and proposed solution
3. **📝 Improve documentation** - Help make the docs clearer and more comprehensive
4. **🔧 Submit code** - Fork, create a feature branch, and submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Run tests
pytest

# Format code
black *.py

# Type checking
mypy *.py
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** for providing the incredible reasoning models
- **Python Community** for the excellent ecosystem of libraries
- **Contributors** who help make this project better

---

<div align="center">

**Made with ❤️ for the AI community**

*If this project helped you, please consider giving it a ⭐!*

[🔝 Back to top](#-unified-openai-agent-system)

</div>
