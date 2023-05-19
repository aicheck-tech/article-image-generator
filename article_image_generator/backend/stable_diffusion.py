import torch
import PIL
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

from article_image_generator.settings import STABLE_DIFFUSION_MODEL_PATH


class StableDiffusion:
    def __init__(self):
        self.pipeline = StableDiffusionPipeline.from_pretrained(STABLE_DIFFUSION_MODEL_PATH, torch_dtype=torch.float16)
        self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(self.pipeline.scheduler.config)
        self.pipeline = self.pipeline.to("cuda")

    def generate_image(self, prompt: str) -> PIL.Image.Image:
        return self.pipeline(prompt).images[0]
