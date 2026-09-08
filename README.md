# 🤖 Market Price Assistant

An AI agent built for the Schull AI Academy LLM Engineering Capstone.

## What it does
This agent helps Nigerian shoppers check food prices, calculate totals for multiple bags, and compare prices between two items. It uses an LLM with custom tools to give warm, practical answers.

## Tools
1. **get_price** — Looks up the current market price of a food item in Naira
2. **calculate_total** — Multiplies unit price by quantity
3. **compare_items** — Compares two items and says which is cheaper

## How to run locally
1. Clone the repo
2. Create a .env file with your OPENAI_API_KEY
3. Run: uv run streamlit run app.py

## Live Demo
🔗 (https://my-ai-agent-mwokppjkpzzfbfyzgxb2wi.streamlit.app/)

## Tech Stack
- Python
- Streamlit
- OpenAI GPT-4o-mini
