import base64
import io
import pathlib

import httpx
import ipywidgets as widgets
from PIL import Image, ImageDraw
import textwrap

from llm_lib import create_red_pajama_llmchain

LLM_SYSTEM_TEMPLATE = """You are a professional childrens' book illustrator having a conversation with a human. 
In conversation, the human provides one line of a children's story.
Your response is a short description of a cartoon image that could be drawn that matches the story so far.
The response should be a 1-2 sentence paragraph.

Begin!
----------------"""
LLM_HUMAN_TEMPLATE = "{question}"
IMAGE_TEMPLATE = "children's cartoon: "
USE_PREVIOUS_IMAGE = True


def generate_image_desc(llm_chain, human_input):
    image_desc = llm_chain.predict(question=human_input)
    return image_desc

def generate_image(image_prompt, image_input=None):
    post_req = {'prompt': image_prompt}
    if image_input:
        b = io.BytesIO()
        image_input.save(b, "JPEG")
        post_req["image"] = base64.b64encode(b.getbuffer()).decode('utf-8')
        
    r = httpx.post('http://localhost:8001/generate', json=post_req, timeout=60)
    image = Image.open(io.BytesIO(base64.b64decode(r.json()["image_bytes_base64"])))
    return image
    
def add_text(image, text, margin=40, offset=40, fill=(255, 255, 255)):
    im_draw = ImageDraw.Draw(image)
    for line in textwrap.wrap(text):
        im_draw.text((margin, offset), line, fill=fill)
        offset += 10
        
    
class StoryProcessor:
    
    def __init__(self, llm_chain, image_template = ""):
        self.llm_chain = llm_chain
        self.images = []
        self.captions = []
        self.cap_images = []
        self.image_template = image_template
        
    def update(self, caption, use_previous_image=USE_PREVIOUS_IMAGE):
        print(f"{caption=}")
        image_desc = generate_image_desc(self.llm_chain, caption)
        image_prompt = f"{self.image_template}{image_desc}"
        print(f"{image_prompt=}")
        image = generate_image(caption, self.images[-1] if (self.images and use_previous_image) else None)
        cap_image = image.copy()
        add_text(cap_image, caption, margin=40, offset=40)
        add_text(cap_image, image_desc, margin=40, offset=100)
        self.images.append(image)
        self.captions.append(caption)
        self.cap_images.append(cap_image)


class DemoApp:
    
    def __init__(
        self, 
        system_template=LLM_SYSTEM_TEMPLATE, 
        human_template=LLM_HUMAN_TEMPLATE, 
        image_template=IMAGE_TEMPLATE
    ):
        self.sp = StoryProcessor(
            llm_chain=create_red_pajama_llmchain(
                human_template=human_template,
                system_template=system_template,
                verbose=True
            ), 
            image_template=image_template
        )
        
        self.out = widgets.Output(layout={'border': '1px solid black', 'height': '480px', 'overflow': 'scroll'})
        self.out.clear_output()
        
    def save(self):
        self.sp.cap_images[0].save(
            pathlib.Path(__file__).parent / "book.pdf", 
            "PDF" ,
            resolution=100.0, 
            save_all=True, 
            append_images=self.sp.cap_images[1:]
        )
