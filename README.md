# Chris's Hackathon May 2023

- [Chris's Hackathon May 2023](#chriss-hackathon-may-2023)
  - [Goal](#goal)
  - [About](#about)
    - [FastChat](#fastchat)
    - [LangChain](#langchain)
    - [ChainLit](#chainlit)
    - [Stable Diffusion server](#stable-diffusion-server)
    - [PictureBook App](#picturebook-app)
  - [Run](#run)
    - [Setup Notes](#setup-notes)
    - [Docker](#docker)
    - [Local Run](#local-run)
  - [TODO / Improvements](#todo--improvements)
    - [Better Performance](#better-performance)
    - [Add live dictation](#add-live-dictation)

## Goal

- Play around with Generative AI
  - Picturebook creation app
- Run local
  - I have a Puget with 2 GPUs
- Run free (ideally commercial use ok)
  - see list of [open LLMS](https://github.com/eugeneyan/open-llms)
  - stable diffusion

## About

### [FastChat](https://github.com/lm-sys/FastChat)

Run a server with FastChat LLM.

- benefits
  - The local running API is OpenAI API compatible
  - Supports several open source [LLMs](https://github.com/lm-sys/FastChat#supported-models)
  - Supports usage of multiple GPUs, which helps when a model needs more than one GPU's worth of memory.

### [LangChain](https://python.langchain.com/en/latest/)

Python library that helps build LLM apps. Integrates with various LLMs including using OpenAI API.

FastChat notes on [LangChain integration](https://github.com/lm-sys/FastChat/blob/main/docs/langchain_integration.md)

### [ChainLit](https://docs.chainlit.io/overview)

Easily build a Chat UI on top of LangChain.

- [chainlit.py](chainlit.py) is an example using our local running FastChat OpenAI API server

### Stable Diffusion server

Generate images.

- [stable_diffusion_api.py](stable_diffusion_api.py) is a simple API on top of it

### PictureBook App

My demo [notebook](PictureBookMaking.ipynb) allows human to input a story line by line, and for each line have LLM generate a related image generation prompt which stable diffusion then uses to generate an image.

Story history is maintained by the LLM conversation history and style history is maintained by previous image.

## Run

### Setup Notes

- This was developed using a Puget with **two** 12GB Nvidia GPUs
  - 7b LLMs need more than 12GB so FastChat API supports multiple
    - See Makefile fastchat_worker command usage
    - When using multiple, 1st one's memory gets filled up more than 2nd.
  - Stable Diffusion can run in one GPU
    - See Makefile stable_diffusion command usage
    - Set to 2nd GPU because LLM is mostly on 1st.
- First time runs will take a few minutes to download models from HuggingFace.

### Docker

`docker compose up`

- See jupyter notebook at <http://localhost:8888/notebooks/PictureBookMaking.ipynb>
- See chainlit at <http://localhost:8002>

### Local Run

Uses python 3.10

```bash
# first time, create python virtual env
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -U pip
python3 -m pip install -r requirements.txt
```

```bash
source venv/bin/activate
make all -j
```

- See jupyter notebook at <http://localhost:8888/notebooks/PictureBookMaking.ipynb>
- See chainlit at <http://localhost:8002>

## TODO / Improvements

### Better Performance

- Prompt Engineering
  - Modify the templates in the [notebook](PictureBookMaking.ipynb))
- LLM update [llm_lib.py](llm_lib.py)
  - use different models
  - try different kinds of conversation memory.
- Stable Diffusion
  - update pipeline parameters in update [stable_diffusion_api.py](stable_diffusion_api.py) , such as steps, strength, guidance
  - if using update() with use_previous_image=True, change how much effect it has

### Add live dictation

Can look into [WhisperAI](https://github.com/openai/whisper)
