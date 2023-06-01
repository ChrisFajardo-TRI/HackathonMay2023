# Chris's Hackathon May 2023

- [Chris's Hackathon May 2023](#chriss-hackathon-may-2023)
  - [Goal](#goal)
  - [Setup Notes](#setup-notes)
  - [FastChat](#fastchat)
  - [LangChain](#langchain)
  - [(aside) Example with ChainLit](#aside-example-with-chainlit)
  - [Stable Diffusion server](#stable-diffusion-server)
  - [Run the notebook](#run-the-notebook)
  - [TODO](#todo)

## Goal

- Play around with Generative AI
  - Picturebook creation app
- Run local
  - I have a Puget with 2 GPUs
- Run free (ideally commercial use ok)
  - see list of [open LLMS](https://github.com/eugeneyan/open-llms)
  - stable diffusion

## Setup Notes

- Use a python virtual env
- For now hardcoded GPU 0 for LLM and GPU 1 for Stable Diffusion

## [FastChat](https://github.com/lm-sys/FastChat)

Run a server with FastChat LLM (fastchat-t5-3b-v1.0). The local running API is OpenAI API compatible!

- install `pip install fschat`
- serve from 3 terminals
  - `python3 -m fastchat.serve.controller`
  - `python3 -m fastchat.serve.model_worker --model-path lmsys/fastchat-t5-3b-v1.0 --num-gpus 2 `
  - `python3 -m fastchat.serve.openai_api_server --host localhost --port 8000`

## [LangChain](https://python.langchain.com/en/latest/)

Python library that helps build LLM apps. Integrates with various LLMs including OpenAI API.

FastChat notes on [LangChain integration](https://github.com/lm-sys/FastChat/blob/main/docs/langchain_integration.md)

- `pip install langchain`
- `pip install openai`

## (aside) Example with [ChainLit](https://docs.chainlit.io/overview)

Chat UI on top of LangChain using the local FastChat OpenAI

- `pip install chainlit`
- `chainlit run chainlit.py --port 8002`

## Stable Diffusion server

- follow installation <https://www.nbshare.io/notebook/481422769/Install-and-Run-Stable-Diffusion-2-on-Ubuntu/>
- also do `pip install accelerate`
- Made my own simple server
  - `uvicorn main:app --reload --port 8001`

## Run the notebook

- `pip install jupyter`
- if all the above was also installed in the same python environment, the rest of the modules should be there already.
- `jupyter notebook`

## TODO

- dockerize
- refine prompts (prompt engineering)
- WhisperAI for dictation
