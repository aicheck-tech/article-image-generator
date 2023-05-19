import sys
from pathlib import Path

from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import torch
import PIL

parent_folder = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_folder))

import settings

class StableDiffusion:
    def __init__(self) -> None:
      self.pipeline = StableDiffusionPipeline.from_pretrained(settings.STABLE_DIFFUSION_MODEL_PATH, torch_dtype=torch.float16)
      self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(self.pipeline.scheduler.config)
      self.pipeline = self.pipeline.to("cuda")

    def generate_image(self, prompt: str) -> PIL.Image.Image:
      return self.pipeline(prompt).images[0]
    