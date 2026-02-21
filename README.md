<div align="center">

# 🧠 O-Series CLI Agent

### Unified OpenAI Reasoning Models — Professional CLI Interface

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?style=for-the-badge&logo=openai&logoColor=white)](https://platform.openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-F7DF1E?style=for-the-badge&logo=open-source-initiative&logoColor=black)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-00C7B7?style=for-the-badge&logo=semver&logoColor=white)](https://github.com/simonpierreboucher02/o-series-cli-agent/releases)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge&logo=statuspage&logoColor=white)](https://github.com/simonpierreboucher02/o-series-cli-agent)

---

[![Models](https://img.shields.io/badge/Models-O1%20%7C%20O3%20%7C%20O3--mini%20%7C%20O4--mini-blueviolet?style=flat-square&logo=openai)](https://platform.openai.com/docs/models)
[![Streaming](https://img.shields.io/badge/Streaming-Real--time-orange?style=flat-square&logo=rss&logoColor=white)](https://platform.openai.com/docs/api-reference/streaming)
[![Export Formats](https://img.shields.io/badge/Export-JSON%20%7C%20TXT%20%7C%20MD%20%7C%20HTML%20%7C%20CSV%20%7C%20XML-9cf?style=flat-square&logo=files&logoColor=white)](#export--formats)
[![CLI](https://img.shields.io/badge/CLI-argparse%20%2B%20rich-lightgrey?style=flat-square&logo=gnubash&logoColor=white)](#installation)
[![Context Window](https://img.shields.io/badge/Context%20Window-128K%20tokens-critical?style=flat-square&logo=databricks&logoColor=white)](#model-specs)
[![Presets](https://img.shields.io/badge/Presets-4%20Built--in-blue?style=flat-square&logo=settings&logoColor=white)](#configuration-presets)
[![Batch Mode](https://img.shields.io/badge/Batch%20Mode-Supported-success?style=flat-square&logo=buffer&logoColor=white)](#advanced-usage)
[![File Inclusion](https://img.shields.io/badge/File%20Inclusion-%7Bfilename%7D%20Syntax-yellow?style=flat-square&logo=file-code&logoColor=white)](#file-inclusion)

---

**A production-grade, feature-rich CLI agent for OpenAI's O-Series reasoning models.**
*Built for developers, researchers, and AI power users who need full control over model behavior, conversation management, and export pipelines.*

[✨ Features](#-features) •
[⚙️ Installation](#-installation) •
[🚀 Quick Start](#-quick-start) •
[📚 Commands](#-commands-reference) •
[📁 File Inclusion](#-file-inclusion) •
[🎨 Presets](#-configuration-presets) •
[📊 Model Specs](#-model-specs) •
[🏗️ Architecture](#-project-structure) •
[🔒 Security](#-security-features) •
[🐛 Troubleshooting](#-troubleshooting) •
[👥 Authors](#-authors) •
[📄 License](#-license)

</div>

---

## 📊 Project Metrics

<div align="center">

| Metric | Value |
|--------|-------|
| 🧩 **Modules** | 5 core Python files |
| 🤖 **Supported Models** | 4 (O1, O3, O3-mini, O4-mini) |
| 📤 **Export Formats** | 6 (JSON, TXT, MD, HTML, CSV, XML) |
| 🎯 **CLI Presets** | 4 (Creative, Balanced, Focused, Fast) |
| 📋 **Chat Commands** | 12 built-in |
| 🪟 **Max Context** | 128 000 tokens per model |
| ⏱️ **Max Timeout (O3 high)** | 20 minutes |
| 🔑 **Auth** | Environment variable / secure keyring |
| 🗂️ **Storage** | Per-agent JSON + YAML |
| 🔄 **Streaming** | Real-time token streaming |
| 🛡️ **Security** | Path traversal protection + input validation |
| 📦 **Dependencies** | 8 (3 core, 5 optional) |

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🤖 Model & Inference
- **Multi-Model Support**: O1, O3, O3-mini, O4-mini
- **Real-time Streaming**: Token-by-token output with progress indicators
- **Reasoning Effort Control**: Low / Medium / High per call
- **Temperature Override**: Fine-tune creativity on the fly
- **Max Token Limit**: Cap output per query
- **System Prompt Injection**: Custom context for any agent

</td>
<td width="50%">

### 🗂️ Conversation Management
- **Persistent History**: JSON storage per agent
- **Multi-Agent Support**: Isolated sessions per `agent-id`
- **Search History**: Keyword search across all messages
- **Backup & Restore**: Manual and automatic backups
- **Clear History**: With confirmation prompt
- **Timestamps**: Full ISO8601 on every message

</td>
</tr>
<tr>
<td width="50%">

### 📁 File & Context
- **`{filename}` Syntax**: Inline file injection into prompts
- **20+ File Types**: Python, JS, TS, Go, Rust, YAML, JSON, MD, C/C++, Java, HTML, CSS, etc.
- **Batch Mode**: Process a file of commands sequentially
- **Agent Directory Tree**: Organized uploads, exports, logs, backups

</td>
<td width="50%">

### 📤 Export & Reporting
- **6 Export Formats**: JSON, TXT, Markdown, HTML, CSV, XML
- **Export All at Once**: `--export-all` flag
- **Rich HTML Reports**: Styled conversation transcripts
- **CSV/XML Pipelines**: For downstream data processing
- **Per-Agent Export Directories**: Clean file organization

</td>
</tr>
<tr>
<td width="50%">

### 🎨 CLI Experience
- **Full ANSI Colors**: Roles, errors, warnings, highlights
- **Emoji-Rich Interface**: Visual feedback everywhere
- **Responsive Banner**: Dynamic header per session
- **Table Rendering**: Agent list, model specs, stats
- **`--no-color` Mode**: CI/CD-friendly plain output
- **`--debug` Mode**: Full traceback on errors

</td>
<td width="50%">

### 🔒 Security & Reliability
- **Encrypted Key Storage**: Keyring-backed API key management
- **Path Traversal Protection**: Safe file inclusion
- **Input Validation**: Agent IDs, temperatures, formats
- **Retry Logic**: Graceful API error handling
- **Rate Limit Awareness**: Configurable timeout per effort level
- **Audit Logging**: Per-agent log files

</td>
</tr>
</table>

---

## ⚙️ Installation

### Prerequisites

[![Python 3.10+](https://img.shields.io/badge/Requires-Python%203.10%2B-blue?style=flat-square&logo=python)](https://www.python.org/downloads/)
[![pip](https://img.shields.io/badge/Package%20Manager-pip-orange?style=flat-square&logo=pypi)](https://pip.pypa.io/)
[![OpenAI Key](https://img.shields.io/badge/Requires-OpenAI%20API%20Key-412991?style=flat-square&logo=openai)](https://platform.openai.com/api-keys)

### Step 1 — Clone

```bash
git clone https://github.com/simonpierreboucher02/o-series-cli-agent.git
cd o-series-cli-agent
```

### Step 2 — Virtual Environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

#### Dependency Overview

| Package | Version | Role |
|---------|---------|------|
| `requests` | ≥ 2.31.0 | HTTP API calls |
| `pyyaml` | ≥ 6.0.1 | Config file parsing |
| `colorama` | ≥ 0.4.6 | Cross-platform ANSI colors |
| `rich` | ≥ 13.7.0 | Enhanced terminal formatting *(optional)* |
| `click` | ≥ 8.1.7 | Advanced CLI features *(optional)* |
| `python-dotenv` | ≥ 1.0.0 | `.env` file support *(optional)* |
| `pytest` | ≥ 7.4.0 | Testing *(dev)* |
| `black` | ≥ 23.0.0 | Code formatting *(dev)* |

### Step 4 — Set API Key

```bash
# Option A — Export (session-scoped)
export OPENAI_API_KEY=sk-...your-key-here...

# Option B — .env file (persistent)
echo "OPENAI_API_KEY=sk-...your-key-here..." > .env

# Option C — Interactive prompt (first run auto-asks)
python main.py --agent-id my-agent --model o1
```

---

## 🚀 Quick Start

### Interactive Chat

```bash
# Start chat with O1 (default)
python main.py --agent-id my-agent --model o1

# Research session with O3
python main.py --agent-id research --model o3 --effort high

# Creative writing with O3-mini
python main.py --agent-id writer --model o3-mini --preset creative

# Fast Q&A with O4-mini
python main.py --agent-id quick --model o4-mini --preset fast
```

### Inspect & Manage Agents

```bash
# List all agent sessions
python main.py --list

# Show available models with specs
python main.py --models

# Inspect a specific agent
python main.py --info my-agent

# Show conversation statistics
python main.py --stats my-agent
```

### Configuration

```bash
# Interactive config wizard
python main.py --agent-id my-agent --config

# Apply a preset
python main.py --agent-id my-agent --preset focused

# Show current config
python main.py --agent-id my-agent --show-config
```

### Export

```bash
# Export as HTML
python main.py --agent-id my-agent --export html

# Export as Markdown
python main.py --agent-id my-agent --export md

# Export in all formats at once
python main.py --agent-id my-agent --export-all
```

### Advanced

```bash
# Override multiple parameters
python main.py --agent-id my-agent --model o3 --effort high --temperature 0.2 --max-tokens 4000

# Batch mode from file
python main.py --agent-id my-agent --batch commands.txt

# Search conversation history
python main.py --agent-id my-agent --search "neural network"

# Debug mode
python main.py --agent-id my-agent --model o1 --debug
```

---

## 📚 Commands Reference

### CLI Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--agent-id` | `str` | — | Session identifier (required for chat) |
| `--model` | `choice` | `o1` | Model to use |
| `--effort` | `choice` | `medium` | Reasoning effort: `low` \| `medium` \| `high` |
| `--temperature` | `float` | `1.0` | Creativity (0.0–2.0) |
| `--max-tokens` | `int` | model default | Max output tokens |
| `--no-stream` | `flag` | — | Disable token streaming |
| `--system-prompt` | `str` | — | Inject a system message |
| `--preset` | `choice` | — | Apply a config preset |
| `--config` | `flag` | — | Interactive configuration wizard |
| `--show-config` | `flag` | — | Print current config |
| `--list` | `flag` | — | List all agents |
| `--models` | `flag` | — | Show all model specs |
| `--info` | `str` | — | Show agent details |
| `--stats` | `str` | — | Show conversation statistics |
| `--export` | `choice` | — | Export format |
| `--export-all` | `flag` | — | Export in all formats |
| `--clear` | `flag` | — | Clear history (with confirmation) |
| `--backup` | `flag` | — | Create history backup |
| `--search` | `str` | — | Search history by keyword |
| `--batch` | `str` | — | Path to batch command file |
| `--debug` | `flag` | — | Enable full error tracebacks |
| `--no-color` | `flag` | — | Disable ANSI colors |
| `--version` | `flag` | — | Print version |

### In-Chat Commands

| Command | Description |
|---------|-------------|
| `/help` | Show all available chat commands |
| `/history [n]` | Show last `n` messages (default: 5) |
| `/search <term>` | Full-text search in conversation history |
| `/stats` | Conversation statistics (messages, chars, duration) |
| `/config` | Show current agent configuration |
| `/preset [name]` | Show available presets or apply one |
| `/export <format>` | Export conversation (`json`, `txt`, `md`, `html`, `csv`, `xml`) |
| `/switch <model>` | Switch to a different model mid-session |
| `/files` | List files available for `{filename}` inclusion |
| `/info` | Show full agent directory details |
| `/model` | Show current model specs and pricing |
| `/clear` | Clear conversation history (with confirmation) |
| `/quit` / `/exit` / `/q` | Exit chat session gracefully |

---

## 📁 File Inclusion

Embed file contents directly into your prompts using the `{filename}` syntax:

```
Review my Python script: {main.py}
Analyze this config: {config.yaml}
What does this do? {utils.py}
```

### Supported File Types

| Category | Extensions |
|----------|-----------|
| **Python** | `.py`, `.pyw` |
| **JavaScript / TypeScript** | `.js`, `.ts`, `.jsx`, `.tsx` |
| **Systems Languages** | `.c`, `.cpp`, `.h`, `.hpp`, `.rs`, `.go` |
| **JVM** | `.java`, `.kt`, `.scala` |
| **Web** | `.html`, `.css`, `.scss` |
| **Data & Config** | `.json`, `.yaml`, `.yml`, `.toml`, `.xml`, `.csv` |
| **Documentation** | `.md`, `.txt`, `.rst` |
| **Shell** | `.sh`, `.bash`, `.zsh` |
| **Other** | `.sql`, `.dockerfile` |

> **Note:** File paths are validated and path traversal (`../`) is blocked for security.

---

## 🎨 Configuration Presets

| Preset | Icon | Reasoning Effort | Temperature | Best For |
|--------|------|-----------------|-------------|----------|
| `creative` | 🎨 | High | 1.2 | Creative writing, brainstorming, ideation |
| `balanced` | ⚖️ | Medium | 1.0 | General-purpose tasks (default behavior) |
| `focused` | 🎯 | High | 0.3 | Analysis, code review, technical tasks |
| `fast` | ⚡ | Low | 0.7 | Quick Q&A, simple queries, summaries |

### Usage

```bash
# At startup
python main.py --agent-id my-agent --preset creative

# Inside chat
/preset focused
/preset fast
```

---

## 📊 Model Specs

<div align="center">

| Model | ID | Context | Max Output | Reasoning Timeout (Low/Med/High) | Best Use Case |
|-------|----|---------|------------|----------------------------------|---------------|
| **O1** | `o1` | 128K | 32K | 3 min / 8 min / 15 min | Complex multi-step reasoning |
| **O3** | `o3` | 128K | 32K | 4 min / 10 min / 20 min | Advanced research & long-form tasks |
| **O3-mini** | `o3-mini` | 128K | 16K | 2 min / 5 min / 10 min | Balanced performance & speed |
| **O4-mini** | `o4-mini` | 128K | 16K | 1.5 min / 4 min / 8 min | Fast responses, simple queries |

</div>

### Pricing Reference *(per 1K tokens)*

| Model | Input | Output |
|-------|-------|--------|
| O1 | $0.015 | $0.060 |
| O3 | $0.010 | $0.040 |
| O3-mini | $0.001 | $0.004 |
| O4-mini | $0.001 | $0.004 |

> Pricing subject to change. Always verify at [platform.openai.com/pricing](https://platform.openai.com/pricing).

---

## 🏗️ Project Structure

```
o-series-cli-agent/
│
├── main.py              # CLI entry point — argparse, UnifiedCLI
├── agent.py             # UnifiedOpenAIAgent — API calls, history, streaming
├── config.py            # AgentConfig, ModelConfig, ConfigManager, Presets
├── export.py            # ConversationExporter — 6 format exporters
├── utils.py             # ColorManager, UIEnhancer, ValidationUtils
├── requirements.txt     # Dependencies (core + optional + dev)
│
└── agents/
    └── {agent-id}/
        ├── history.json         # Full conversation history
        ├── config.yaml          # Agent-specific config
        ├── secrets.json         # Encrypted API credentials
        ├── backups/             # Timestamped history backups
        ├── exports/             # All exported files
        ├── logs/                # Audit logs
        └── uploads/             # Files for {filename} inclusion
```

### Module Responsibilities

| File | Responsibility |
|------|---------------|
| `main.py` | CLI parsing, command dispatch, interactive chat loop |
| `agent.py` | OpenAI API integration, streaming, history CRUD, search |
| `config.py` | Model definitions, presets, config validation, YAML I/O |
| `export.py` | Conversion of history to JSON/TXT/MD/HTML/CSV/XML |
| `utils.py` | Terminal colors, UI components, input validation |

---

## 🔒 Security Features

| Feature | Details |
|---------|---------|
| 🔑 **API Key Storage** | Keyring-backed encrypted storage, never hardcoded |
| 🚫 **Path Traversal Protection** | File inclusion blocks `../` and absolute paths |
| ✅ **Input Validation** | Agent IDs: alphanumeric + `-` `_` only; temperatures: 0.0–2.0 |
| 📜 **Error Handling** | All API errors caught and reported without leaking internals |
| 🔄 **Retry Logic** | Automatic retry on transient API failures |
| 📝 **Audit Logging** | Per-agent log files for all sessions |
| 🛡️ **No Shell Injection** | No `subprocess` calls with user input |
| 🔒 **Secrets File** | Isolated per-agent `secrets.json`, excluded from exports |

---

## 🐛 Troubleshooting

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError` | Missing dependencies | `pip install -r requirements.txt` |
| `AuthenticationError` | Invalid API key | `export OPENAI_API_KEY=sk-...` |
| `TimeoutError` | High reasoning effort + complex query | Use `--effort medium` or `--effort low` |
| `Permission denied` | No write access to `agents/` | `chmod 755 agents/` or run from different dir |
| `Invalid agent ID` | Special chars in `--agent-id` | Use only `a-z`, `A-Z`, `0-9`, `-`, `_` |
| `No streaming output` | Network or proxy issue | Try `--no-stream` flag |
| Colors not rendering | Windows CMD / old terminal | Add `--no-color` flag |

### Debug Mode

```bash
python main.py --agent-id my-agent --model o1 --debug
```

Enable full Python traceback on any unhandled exception.

### Reset an Agent

```bash
# Clear history only
python main.py --agent-id my-agent --clear

# Delete agent entirely
rm -rf agents/my-agent/
```

---

## 🔄 Advanced Usage

### Batch Processing

Create a `commands.txt` file:

```
Summarize the history of machine learning in 3 bullets
What are the main differences between O1 and O3?
Explain chain-of-thought prompting
```

Run it:

```bash
python main.py --agent-id batch-run --model o3-mini --batch commands.txt
```

### Custom System Prompts

```bash
python main.py --agent-id code-reviewer \
  --model o1 \
  --system-prompt "You are a senior software engineer. Review code for correctness, performance, and security." \
  --effort high
```

### Switching Models Mid-Session

Inside chat:

```
/switch o3
/switch o4-mini
```

### Export Pipeline Example

```bash
# Run session
python main.py --agent-id research-2024 --model o3 --effort high

# Export all formats for archiving
python main.py --agent-id research-2024 --export-all
```

---

## 🧪 Development & Testing

```bash
# Run tests
pytest tests/

# Format code
black *.py

# Lint
flake8 *.py

# Type checking
mypy *.py
```

---

## 🗺️ Roadmap

| Milestone | Status |
|-----------|--------|
| Multi-model support (O1, O3, O3-mini, O4-mini) | ✅ Done |
| Real-time streaming | ✅ Done |
| File inclusion `{filename}` | ✅ Done |
| 6 export formats | ✅ Done |
| Configuration presets | ✅ Done |
| Per-agent persistent history | ✅ Done |
| Batch mode | ✅ Done |
| Plugin / tool-call support | 🔜 Planned |
| Vision input (image prompts) | 🔜 Planned |
| Web UI (optional frontend) | 🔜 Planned |
| RAG / vector store integration | 🔜 Planned |
| LangChain / LlamaIndex bridge | 🔜 Planned |

---

## 👥 Authors

<div align="center">

### Simon-Pierre Boucher
**Lead Developer & Project Owner**

[![Email](https://img.shields.io/badge/Email-spbou4%40protonmail.com-8B89CC?style=for-the-badge&logo=protonmail&logoColor=white)](mailto:spbou4@protonmail.com)
[![Website](https://img.shields.io/badge/Website-www.spboucher.ai-00C7B7?style=for-the-badge&logo=safari&logoColor=white)](https://www.spboucher.ai)
[![GitHub](https://img.shields.io/badge/GitHub-simonpierreboucher02-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/simonpierreboucher02)

---

### Claude (Anthropic)
**AI Co-Author & Documentation Architect**

[![Anthropic](https://img.shields.io/badge/Powered%20by-Anthropic%20Claude-E07B54?style=for-the-badge&logo=anthropic&logoColor=white)](https://www.anthropic.com)
[![Model](https://img.shields.io/badge/Model-Claude%20Sonnet%204.6-E07B54?style=for-the-badge&logo=anthropic&logoColor=white)](https://www.anthropic.com/claude)

</div>

---

## 📄 License

```
MIT License

Copyright (c) 2025 Simon-Pierre Boucher

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "feat: add my feature"`
4. Push to your branch: `git push origin feature/my-feature`
5. Open a Pull Request

Please follow the existing code style (Black + Flake8) and include tests where applicable.

---

<div align="center">

**Built with precision by [Simon-Pierre Boucher](https://www.spboucher.ai) & Claude (Anthropic)**

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Powered by OpenAI](https://img.shields.io/badge/Powered%20by-OpenAI-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com/)
[![Docs by Claude](https://img.shields.io/badge/Docs%20by-Claude%20AI-E07B54?style=flat-square&logo=anthropic&logoColor=white)](https://www.anthropic.com/)

</div>
