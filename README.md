
# You Really Want an AI Agent in the Cloud… But You Only Have Five Dollars

Demo repository for the DebConf26 talk:

**You Really Want an AI Agent in the Cloud… But You Only Have Five Dollars**

**Speaker:** Esteban Monge  
**Track:** Artificial Intelligence & Debian  
**Type:** Long Talk (45 min)

---

## Overview

Artificial Intelligence agents are often presented as something that requires expensive GPUs, cloud subscriptions, and enterprise-scale infrastructure.

This project demonstrates a different approach.

The goal is to build a functional AI-powered operations assistant using:

- Debian GNU/Linux
- Python
- OpenRouter
- Telegram
- Self-hosted infrastructure
- Low-cost VPS resources

The repository contains a simple but practical AI workflow that receives monitoring alerts, investigates potential issues, generates a diagnosis using Large Language Models (LLMs), notifies operators through Telegram, and stores generated documentation in DokuWiki.

The focus is not absolute accuracy or enterprise-grade scale. The objective is to demonstrate what can be achieved with open technologies, limited resources, and a small budget.

---

## Architecture

```text
Nagios
  |
  v
AgenticAI
  |
  +--> Telegram Notification
  |
  +--> Investigation
  |
  +--> LLM Analysis
  |
  +--> Documentation
  |
  +--> DokuWiki Knowledge Base
```

### Components

| Component | Purpose |
|------------|----------|
| Debian | Operating system |
| Nagios | Monitoring platform |
| Python | Workflow automation |
| LangGraph | Agent orchestration |
| OpenRouter | Access to AI models |
| Telegram | User interface and notifications |
| DokuWiki | Knowledge base |
| Linode | Hosting platform |

---

## Repository Structure

```text
.
├── analyze_node.py
├── dokuwiki_node.py
├── graph.py
├── llm.py
├── logger.py
├── main.py
├── report_node.py
├── telegram_node.py
└── requirements.txt
```

### Main Flow

1. Nagios generates an alert.
2. Agent receives event details.
3. Basic diagnostics are executed.
4. An LLM analyzes the evidence.
5. A report is generated.
6. Telegram receives the notification.
7. Documentation is stored automatically in DokuWiki.

---

## Installation

The project was developed and tested on Debian running under the Nagios working directory.

Recommended layout:

```text
/usr/local/nagios/
├── agenticai/
│   ├── main.py
│   ├── graph.py
│   ├── analyze_node.py
│   ├── telegram_node.py
│   ├── report_node.py
│   ├── dokuwiki_node.py
│   ├── logger.py
│   ├── llm.py
│   ├── requirements.txt
│   └── .env
│
└── agenticai-venv/
```

### Clone Repository

```bash
cd /usr/local/nagios

git clone <repository-url> agenticai
```

### Create Virtual Environment

```bash
python3 -m venv /usr/local/nagios/agenticai-venv
```

Activate it:

```bash
source /usr/local/nagios/agenticai-venv/bin/activate
```

### Install Dependencies

```bash
cd /usr/local/nagios/agenticai

pip install -r requirements.txt
```

---

## Configuration

Create the environment file:

```bash
cd /usr/local/nagios/agenticai

cp dotenv.example .env
```

Example configuration:

```env
TELEGRAM_BOT_TOKEN="putyourbottoken"
TELEGRAM_CHAT_ID="putyourchatid"

OPENROUTER_MODEL="openrouter/free"
OPENROUTER_API_KEY="putyouropenrouterapikey"

DOKUWIKI_URL="http://dokuwiki.sempaispace.example.com/lib/exe/jsonrpc.php"
DOKUWIKI_USER="songohan"
DOKUWIKI_API_TOKEN="putyourdokuwikiapikey"
```

---

## Running

Example execution:

```bash
cd /usr/local/nagios/agenticai

source /usr/local/nagios/agenticai-venv/bin/activate

python3 main.py \
PROBLEM \
webserver01 \
192.168.1.100 \
HTTP \
CRITICAL \
"HTTP CRITICAL - 500 Internal Server Error"
```

---

## Integration with Nagios

The application expects the following parameters passed by Nagios:

```text
$NOTIFICATIONTYPE$
$HOSTNAME$
$HOSTADDRESS$
$SERVICEDESC$
$SERVICESTATE$
$SERVICEOUTPUT$
```

The workflow is:

```text
Nagios Alert
      │
      ▼
Telegram Notification
      │
      ▼
Investigation
      │
      ▼
AI Analysis (OpenRouter)
      │
      ▼
Report Generation
      │
      ▼
DokuWiki Knowledge Base
```

---

## What This Repository Demonstrates

This is not a production-ready enterprise AI platform.

It is a practical example showing how to build a useful AI-assisted operations workflow using:

- Debian
- Python
- LangGraph
- OpenRouter
- Telegram
- DokuWiki
- Nagios

while spending very little money.

The goal is to demonstrate that useful AI experimentation does not require GPUs, Kubernetes clusters, or large cloud budgets.


## Why This Project Exists

Modern AI discussions often focus on:

- Massive GPU clusters
- Proprietary platforms
- Expensive subscriptions
- Vendor lock-in

This project explores a different question:

> How much useful AI can you build with a Debian server, open tools, and a budget small enough to fit inside a hobby project?

The answer is often "more than you might expect."

---

## DebConf26

### You Really Want an AI Agent in the Cloud… But You Only Have Five Dollars

**Speaker:** Esteban Monge

**Track:** Artificial Intelligence & Debian

**Room:** Aula Magna - FADU

**Date:** July 23

**Time:** 11:00

The talk covers:

- Deploying AI agents on Debian
- Running useful automation with limited resources
- OpenRouter and low-cost LLM access
- Telegram as an AI interface
- Self-hosting considerations
- Operational costs and lessons learned
- Practical limitations of budget AI systems

---

## License

This repository is released under the MIT License unless otherwise specified.

---

## Acknowledgements

Thanks to the Debian community, DebConf organizers, DokuWiki developers, Nagios maintainers, OpenRouter, and the broader open-source ecosystem that makes experimentation like this possible.


And, of course, thanks to chatgpt and copilot AI models that patiently helped debug parts of this project at unreasonable hours of the night.

Any remaining bugs are the responsibility of the human.
