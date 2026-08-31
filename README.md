# AI Reply Drafter — LLM as a Personal Autocompleter

Research project exploring whether a fine tuned LLM can act as a smart autocomplete assistant, 
trained on personal chat using a Telegram bot.

## How it works

- Userbot (Pyrogram) listens to incoming messages from a chosen contact
- Messages + chat history are fed to a fine tuned LLM (Unsloth, LoRA)
- The model drafts 1+ candidate replies
- A bot sends the drafts to the owner via Telegram, who picks one
- The chosen draft is saved to Telegram as a message draft

## Setup

1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in your credentials
3. Get dataset using my parsing.py script
4. Train model using my fine_tuning1.ipynb script
5. Place your fine tuned model in `my_model1/`
6. `python main.py`

## Privacy note

This project is trained on my own private chat data.
The dataset itself is not published in this repository.

## Fine tuning methodology

- Base model: Qwen/Qwen3-4B-Instruct-2507(quantized)
- Method: LoRA using Unsloth
- Dataset: personal Telegram chat history obtained using parsing.py

## Version 1

- Dataset format: `message1 | message2`
- No usage/evaluation data yet — the current version is not yet reliable enough for real use