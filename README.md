# 🧠 Unified OpenAI o Series Agent System  

**👨‍💻 Author: Simon-Pierre Boucher**  

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

### 🤖 Multi-Model Support  
- 🔹 **O1 Model** → Advanced reasoning (up to 15 min timeout)  
- 🔹 **O3 Model** → Latest generation (up to 20 min timeout)  
- 🔹 **O3-mini** → Compact & efficient (up to 10 min timeout)  
- 🔹 **O4-mini** → Fast & optimized (up to 8 min timeout)  

### 💬 Advanced Chat Interface  
- 🎨 Beautiful CLI with colors, emojis, responsive design  
- ⚡ Real-time streaming with progress indicators  
- 📁 File inclusion using `{filename}` syntax  
- 🔍 Smart search in conversation history  
- 📊 Rich statistics & analytics  

### ⚙️ Professional Configuration  
- 🎯 Presets: Creative, Balanced, Focused, Fast  
- 🛠️ Interactive setup wizard with validation  
- 🔧 Fine-grained control over all parameters  
- 💾 Persistent settings with automatic backup  

### 📤 Multi-Format Export  
- 📄 **JSON**: Full metadata  
- 📝 **TXT**: Clean plain text  
- 📖 **Markdown**: Syntax highlighting  
- 🌐 **HTML**: Responsive webpage  
- 📊 **CSV**: Data analysis friendly  
- 🗂️ **XML**: Structured format  

### 🛡️ Security & Reliability  
- 🔐 Encrypted API key management  
- 🚫 Path traversal protection  
- 🔄 Automatic retries with backoff  
- 💾 Rolling backups of history  

---

## 🚀 Installation  

### Prerequisites  
- Python 3.8+ (3.10+ recommended)  
- OpenAI API key with reasoning access  

### Install Dependencies  
```bash
git clone <repo>
cd o-series
pip install -r requirements.txt

# Optional
pip install rich click python-dotenv
```  

### Setup API Key  

**Option 1: Env Variable**  
```bash
export OPENAI_API_KEY="your-api-key-here"
```  

**Option 2: Interactive**  
```bash
python main.py --agent-id test --model o1
```  

**Option 3: Manual Config**  
`agents/your-agent-id/secrets.json`:  
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

```bash
# O1 model
python main.py --agent-id my-first-agent --model o1  

# Creative writing
python main.py --agent-id writer --model o3-mini --preset creative  

# Fast responses
python main.py --agent-id quick-chat --model o4-mini --preset fast  
```  

---

## 📖 Usage  

### Basic Commands  

| Command | Description | Example |
|---------|-------------|---------|
| `--agent-id` | Specify agent identifier | `--agent-id research` |
| `--model` | Choose model | `--model o3-mini` |
| `--list` | Show all agents | `python main.py --list` |
| `--models` | Show model info | `python main.py --models` |
| `--export` | Export conversation | `--export html` |  

### Interactive Chat  

| Command | Description |
|---------|-------------|
| `/help` | Show commands |
| `/history [n]` | Show last n messages |
| `/search <term>` | Search history |
| `/stats` | Conversation stats |
| `/export <format>` | Export conversation |
| `/preset [name]` | Show/apply presets |
| `/files` | List files |
| `/quit` | Exit chat |  

---

## 🎯 Examples  

**File Inclusion**  
```
Analyze this code: {script.py}  
Review my configuration: {config.yaml}  
```  

**Batch Processing**  
```bash
python main.py --agent-id batch --batch prompts.txt
python main.py --agent-id my-agent --export-all
```  

**Advanced Config**  
```bash
python main.py --agent-id creative --model o3 --temperature 1.5 --effort high
python main.py --agent-id focused --model o4-mini --temperature 0.3 --effort low --no-stream
```  

---

## 📁 Project Structure  

```
o-series/
├── main.py
├── agent.py
├── config.py
├── export.py
├── utils.py
├── requirements.txt
├── README.md
└── agents/
    └── {agent-id}/
        ├── history.json
        ├── config.yaml
        ├── secrets.json
        ├── backups/
        ├── exports/
        ├── logs/
        └── uploads/
```  

---

## 🎨 Configuration Presets  

- **Creative** 🎨 → Temp 1.5, High effort, detailed  
- **Balanced** ⚖️ → Temp 1.0, Medium effort, general use  
- **Focused** 🎯 → Temp 0.3, High effort, analysis  
- **Fast** ⚡ → Temp 0.7, Low effort, quick tasks  

---

## 🔧 Model Specs  

| Model | Timeout | Context | Best For |
|-------|---------|---------|----------|
| O1 | 15 min | 128K | Complex reasoning |
| O3 | 20 min | 128K | Advanced tasks |
| O3-mini | 10 min | 128K | Balanced use |
| O4-mini | 8 min | 128K | Speed tasks |  

---

## 📊 Export Formats  

- **JSON** → full metadata & stats  
- **HTML** → responsive, styled, mobile-friendly  
- **Markdown** → GitHub-compatible  
- **CSV** → analysis-ready  
- **TXT** → clean logs  

---

## 🛡️ Security  

- 🔐 Encrypted API key storage  
- 🚫 Path traversal protection  
- ✅ Input validation  
- 📝 Audit logging  
- 📏 File size limits  

---

## 🎯 Pro Tips  

- Use high effort for analysis, low for quick Q&A  
- Keep included files <2MB  
- Backup before major config changes  
- Export in multiple formats for sharing  

---

## 🤝 Contributing  

1. 🐛 Report bugs  
2. 💡 Suggest features  
3. 📝 Improve documentation  
4. 🔧 Submit code via PR  

Development setup:  
```bash
pip install -r requirements.txt
pip install pytest black flake8 mypy
pytest
black *.py
mypy *.py
```  

---

## 📝 License  

MIT License — see [LICENSE](LICENSE).  

---

## 🙏 Acknowledgments  

- OpenAI for reasoning models  
- Python community for ecosystem  
- Contributors for improvements  

---

**2025-08-29**  
*Université Laval*  
