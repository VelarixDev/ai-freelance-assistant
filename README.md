# 🚀 AI Freelance Bidding Assistant

An advanced, asynchronous Telegram bot designed to help freelancers instantly generate highly professional, tailored cover letters for Upwork and other platforms using both Cloud APIs and Local LLMs.

## ✨ Features
- Universal LLM Integration: Works seamlessly with Cloud APIs (like OpenRouter, OpenAI, Groq) or completely local neural networks (like Gemma or Qwen via LM Studio/Ollama) using the AsyncOpenAI client.
- Smart Prompt Engineering: The bot enforces strict formatting rules (no placeholders, direct approach, confident tone) to generate ready-to-send proposals.
- Dynamic Creativity Engine: Features an interactive inline button to regenerate proposals. The bot uses FSMContext to remember the job description and dynamically increases the LLM's temperature (+0.2 per click) to offer different variations.
- Modern Architecture: Built on the latest aiogram 3.x framework for fast, non-blocking asynchronous performance.

## ⚙️ Configuration & Setup
To run this bot, you need to create a token.txt file in the root directory. It must contain exactly two lines:
1. Your Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
2. Your LLM API Key (e.g., from OpenRouter sk-or-v1-... or local for local setups)

**Example of token.txt:**
123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ
sk-or-v1-abcdef1234567890...
## 🛠 Tech StacPython 3.1313*aiogram 3.x.x*AsyncOpenAIAI*FSMSM**

## 🔒 Security
Tokens and sensitive keys are managed via local environments and are strictly excluded from the repository via .gitignore.

---

### Here is an example of how the bot works:
<img width="1173" height="986" alt="Screenshot 2026-04-21 231244" src="https://github.com/user-attachments/assets/2dd4be30-f156-4c23-b911-562628521dd0" />
*Developed by[VelarixDev](https://github.com/VelarixDev)*
