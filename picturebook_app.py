import base64
import io

import httpx
import ipywidgets as widgets
from PIL import Image, ImageDraw
import textwrap

from local_llm import create_red_pajama_llmchain

LLM_TEMPLATE = """I need help illustrating a story. I will read you the story line by line. 
Respond with a short description of a cartoon illustration that could be used to illustrate the story so far.

Begin!
----------------
"""

OLD_TEMPLATE = """You are a chatbot having a conversation with a human. 
The human is reading a children's theme story to you one section at a time.
Respond with a short image generation prompt describing a children's cartoon.
"""


def generate_image_desc(llm_chain, human_input):
    image_desc = llm_chain.predict(question=human_input)
    return image_desc

def generate_image(image_desc, image_input=None):
    post_req = {'prompt': f"children's cartoon: {image_desc}"}
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
    
    def __init__(self, llm_chain):
        self.llm_chain = llm_chain
        self.images = []
        self.captions = []
        self.cap_images = []
        
    def update(self, caption):
        print(f"{caption=}")
        image_desc = generate_image_desc(self.llm_chain, caption)
        print(f"{image_desc=}")
        image = generate_image(image_desc, None)
        cap_image = image.copy()
        add_text(cap_image, caption, margin=40, offset=40)
        add_text(cap_image, image_desc, margin=40, offset=100)
        self.images.append(image)
        self.captions.append(caption)
        self.cap_images.append(cap_image)


class DemoApp:
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        llm_chain = create_red_pajama_llmchain(
            human_template="The next line of the story is: {question}",
            system_template=LLM_TEMPLATE
        )

        self.sp = StoryProcessor(llm_chain=llm_chain)
        
        self.out = widgets.Output(layout={'border': '1px solid black', 'height': '480px', 'overflow': 'scroll'})
        self.out.clear_output()
        
    def save(self):
        self.sp.cap_images[0].save(
            "/tmp/book.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=self.sp.cap_images[1:]
        )
