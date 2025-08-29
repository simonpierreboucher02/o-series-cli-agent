# 🧠 Unified OpenAI O-Series CLI Agent  

**👨‍💻 Author: Simon-Pierre Boucher**  

<div align="center">  

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)  
![OpenAI](https://img.shields.io/badge/OpenAI-API-green?logo=openai&logoColor=white)  
![License](https://img.shields.io/badge/License-MIT-yellow)  
![Version](https://img.shields.io/badge/Version-1.0.0-purple)  

**A professional, feature-rich CLI agent for OpenAI’s O-Series reasoning models**  
*Supports O1, O3, O3-mini, and O4-mini with presets, advanced config, and modern CLI*  

[✨ Features](#-features) • [⚙️ Installation](#-installation) • [🚀 Quick Start](#-quick-start) • [📚 Commands](#-commands-reference) • [📁 File Inclusion](#-file-inclusion) • [🎨 Presets](#-configuration-presets) • [📊 Model Specs](#-model-specs) • [🏗️ Architecture](#-project-structure) • [🔒 Security](#-security-features) • [🐛 Troubleshooting](#-troubleshooting) • [📄 License](#-license) • [🤝 Contributing](#-contributing)  

</div>  

---

## ✨ Features  

- 🔹 **Multi-Model Support**: O1, O3, O3-mini, O4-mini  
- 🎨 **Beautiful CLI**: Colors, emojis, responsive design  
- ⚡ **Real-time streaming** with progress indicators  
- 📁 **File Inclusion**: `{filename}` syntax  
- 📊 **Rich statistics & analytics**  
- 🎯 **Presets**: Creative, Balanced, Focused, Fast  
- ⚙️ **Advanced config** with fine-grained parameters  
- 📤 **Multi-format Export**: JSON, TXT, Markdown, HTML, CSV, XML  
- 🛡️ **Secure key management & error handling**  

---

## ⚙️ Installation  

Clone the repository:  
```bash
git clone https://github.com/simonpierreboucher02/o-series-cli-agent.git
cd o-series-cli-agent
```

Create and activate a virtual environment (recommended):  
```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:  
```bash
pip install -r requirements.txt
```

Set your OpenAI API key:  
```bash
export OPENAI_API_KEY=your_api_key_here
```  

---

## 🚀 Quick Start  

### Start chat with O1 model  
```bash
python main.py --agent-id my-agent --model o1
```  

### Creative writing with O3-mini  
```bash
python main.py --agent-id writer --model o3-mini --preset creative
```  

### Fast responses with O4-mini  
```bash
python main.py --agent-id quick --model o4-mini --preset fast
```  

### List all models and agents  
```bash
python main.py --models
python main.py --list
```  

---

## 📚 Commands Reference  

| Command | Description |
|---------|-------------|
| `/help` | Show all commands |
| `/history [n]` | Show last n messages |
| `/search <term>` | Search history |
| `/stats` | Show stats |
| `/config` | Show current config |
| `/config edit` | Interactive config |
| `/preset [name]` | Show/apply preset |
| `/files` | List files |
| `/export <format>` | Export (json, txt, md, html, csv, xml) |
| `/switch <model>` | Switch model |
| `/quit` | Exit chat |  

---

## 📁 File Inclusion  

```
Analyze code: {script.py}  
Review config: {config.yaml}  
```  

Supported types: Python, JS, TS, Java, C/C++, Go, Rust, HTML, CSS, JSON, YAML, Markdown, etc.  

---

## 🎨 Configuration Presets  

- **Creative** 🎨 → High creativity, long reasoning  
- **Balanced** ⚖️ → Default for most tasks  
- **Focused** 🎯 → Analytical, technical  
- **Fast** ⚡ → Quick responses, minimal reasoning  

---

## 📊 Model Specs  

| Model | Timeout (Low/Med/High) | Context | Best Use Case |
|-------|------------------------|---------|---------------|
| O1 | 3m / 8m / 15m | 128K | Complex reasoning |
| O3 | 4m / 10m / 20m | 128K | Advanced tasks |
| O3-mini | 2m / 5m / 10m | 128K | Balanced performance |
| O4-mini | 1.5m / 4m / 8m | 128K | Fast/simple tasks |  

---

## 🏗️ Project Structure  

```
o-series-cli-agent/
├── main.py
├── agent.py
├── config.py
├── export.py
├── utils.py
├── requirements.txt
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

## 🔒 Security Features  

- 🔑 Encrypted API key storage  
- 🚫 Path traversal protection  
- ✅ Input validation  
- 📜 Error handling & retries  
- 📝 Audit logging  

---

## 🐛 Troubleshooting  

- ❌ Import errors → `pip install -r requirements.txt`  
- 🔑 API key issues → `export OPENAI_API_KEY=...`  
- ⏱️ Timeout issues → Adjust reasoning effort  
- 📂 Permission errors → Ensure directory access  

---

## 📄 License  

MIT License — professional & educational use.  

---

## 🤝 Contributing  

Contributions welcome!  

---

**2025-08-29**  
*Université Laval*  
