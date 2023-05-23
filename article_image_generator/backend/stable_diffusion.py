import torch
from PIL import Image
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

from article_image_generator.settings import STABLE_DIFFUSION_HUGGING_FACE


class StableDiffusion:
    def __init__(self):
        self.pipeline = StableDiffusionPipeline.from_pretrained(STABLE_DIFFUSION_HUGGING_FACE, torch_dtype=torch.float16)
        self.generator = torch.Generator(device="cuda")
        self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(self.pipeline.scheduler.config)
        self.pipeline = self.pipeline.to("cuda")

    def generate_image(self, prompt: str, steps:int=50) -> Image:
        return self.pipeline(prompt, generator=self.generator, num_inference_steps=steps).images[0]
