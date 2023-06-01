import base64
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
from fastapi import FastAPI
import io
from PIL import Image
from pydantic import BaseModel
import torch
from xformers.ops import MemoryEfficientAttentionFlashAttentionOp


pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16)
pipe = pipe.to("cuda:1")
pipe.enable_xformers_memory_efficient_attention(attention_op=MemoryEfficientAttentionFlashAttentionOp)
# Workaround for not accepting attention shape using VAE for Flash Attention
pipe.vae.enable_xformers_memory_efficient_attention(attention_op=None)
pipe.set_use_memory_efficient_attention_xformers(True)

pipe_im = StableDiffusionImg2ImgPipeline.from_pretrained("stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16)
pipe_im = pipe_im.to("cuda:1")
pipe_im.enable_xformers_memory_efficient_attention(attention_op=MemoryEfficientAttentionFlashAttentionOp)
# Workaround for not accepting attention shape using VAE for Flash Attention
pipe_im.vae.enable_xformers_memory_efficient_attention(attention_op=None)
pipe_im.set_use_memory_efficient_attention_xformers(True)


class GenerateParams(BaseModel):
    prompt: str
    image: bytes | None


app = FastAPI()


@app.post("/generate")
def generate(params: GenerateParams):
    if params.image:
        image = pipe_im(
            prompt=f"{params.prompt}",
            image = Image.open(io.BytesIO(base64.b64decode(params.image))),
            num_inference_steps=50,
            guidance_scale=7.5,
            strength=0.8
        ).images[0]
    else:
        image = pipe(
            prompt=f"{params.prompt}",
            num_inference_steps=50,
            height=480,
            width=640
        ).images[0]
    
    b = io.BytesIO()
    image.save(b, "JPEG")
    return {
        "image_bytes_base64": base64.b64encode(b.getbuffer())
    }