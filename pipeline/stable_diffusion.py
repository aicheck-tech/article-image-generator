# example
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import torch

model_id = "stabilityai/stable-diffusion-2-1"

# Use the DPMSolverMultistepScheduler (DPM-Solver++) scheduler here instead
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe = pipe.to("cuda") # type: ignore

prompt = "Generate an image depicting an astronaut riding a majestic horse on the vast red landscapes of Mars. The astronaut should be dressed in a futuristic spacesuit, complete with a helmet and oxygen tank, while the horse should appear strong and agile, adapted to the alien environment. Let the image capture the sense of adventure and exploration as the astronaut and horse traverse the otherworldly terrain, with the backdrop showcasing the distinctive Martian features such as craters, mountains, and a reddish sky. Bring to life the unique juxtaposition of the technological and the natural, evoking a sense of wonder and curiosity about the possibilities that lie beyond our planet."
image = pipe(prompt).images[0] # type: ignore
    
image.save("astronaut_rides_horse.png")
