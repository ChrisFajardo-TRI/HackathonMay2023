fastchat_controller:
	python3 -m fastchat.serve.controller --host 0.0.0.0

fastchat_worker:
	python3 -m fastchat.serve.model_worker --host 0.0.0.0 --model-path togethercomputer/RedPajama-INCITE-Chat-7B-v0.1 --num-gpus 2

fastchat_api:
	python3 -m fastchat.serve.openai_api_server --host 0.0.0.0 --port 8000

stable_diffusion:
	CUDA_VISIBLE_DEVICES=1 uvicorn stable_diffusion_api:app --host 0.0.0.0 --port 8001

chainlit:
	chainlit run chainlit.py --host 0.0.0.0 --port 8002
   
juptyer:
	jupyter notebook --ip 0.0.0.0 --allow-root

all: fastchat_controller fastchat_worker fastchat_api stable_diffusion chainlit juptyer
