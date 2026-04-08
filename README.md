# 🚀 AI Freelance Bidding Assistant

An advanced, asynchronous Telegram bot designed to help freelancers instantly generate highly professional, tailored cover letters for Upwork and other platforms using Local LLMs.

## ✨ Features
- Local LLM Integration: Fully integrated with local neural networks (like Gemma or Qwen via LM Studio/Ollama) using the AsyncOpenAI client. Zero API costs and 100% privacy.
- Smart Prompt Engineering: The bot enforces strict formatting rules (no placeholders, direct approach, confident tone) to generate ready-to-send proposals.
- Dynamic Creativity Engine: Features an interactive inline button to regenerate proposals. The bot uses FSMContext to remember the job description and dynamically increases the LLM's temperature (+0.2 per click) to offer different variations of the text, preventing repetitive outputs.
- Modern Architecture: Built on the latest aiogram 3.x framework for fast, non-blocking asynchronous performance.

## 🛠 Tech Stack
- Python 3.13
- aiogram 3.x (Telegram Bot API)
- AsyncOpenAI (LLM Communication)
- FSM (Finite State Machine for context management)

## ⚙️ How It Works
1. The user sends a job description from a freelance platform to the bot.
2. The bot securely forwards the text to the locally hosted LLM with a specialized system prompt.
3. The generated cover letter is sent back to the user.
4. If the user wants a different angle, they can click the "🔄 Сгенерировать другой вариант" button. The bot will automatically adjust the generation temperature and provide a fresh perspective.

## 🔒 Security
Tokens and sensitive keys are managed via local environments and are strictly excluded from the repository via .gitignore.

---
*Developed by [VelarixDev](https://github.com/VelarixDev)*
