# example
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import torch
import PIL

class StableDiffusion:
    def __init__(self) -> None:
      self.pipeline = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16)
      self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(self.pipeline.scheduler.config)
      self.pipeline = self.pipeline.to("cuda")

    def generate_image(self, prompt: str) -> PIL.Image.Image:
      return self.pipeline(prompt).images[0]
    