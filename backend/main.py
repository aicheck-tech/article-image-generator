import sys
from pathlib import Path
import os
import io
from typing import List, Dict, Tuple
import logging
import base64
import json

import torch
from dotenv import load_dotenv
import requests
import PIL
import numpy as np

from stable_diffusion import StableDiffusion
from textProcessing import text_processing
import clip_classification
import settings

parent_folder = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_folder))


load_dotenv()
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")


class Main:
    def __init__(self, STABILITY_API_KEY) -> None:
        self.classifier = clip_classification.load_classifiear()
        self.text_processor = text_processing()
        self.stability_api_key = STABILITY_API_KEY

    def main(self, text: str, tags: List[str]) -> Dict[PIL.Image.Image, Tuple[float, float]]:
        summmarized_text = self.text_processor.summarize_text(text)
        prompt = self.text_processor.text_to_tagged_prompt(
            summmarized_text, tags)['prompt']
        image = self._request_on_stability_api(prompt)
        tensor_similarity = self._classify(image, summmarized_text)
        similarity = tensor_similarity.cpu().numpy()
        similarity *= 100
        similarity = (similarity[0][0], similarity[0][1])
        self._log_output(text, image, similarity, prompt)
        return {"image": image, "similarity": similarity}

    def _log_output(self,
                    summirized_text: str,
                    image: PIL.Image.Image,
                    similarity: Tuple[float, float],
                    prompt: str) -> None:
        json_data = {
            "text": summirized_text,
            "prompt": prompt,
            "similarity": f"{similarity[0]}% similarity, {similarity[1]}% dissimilarity",
            "image": base64.b64encode(image.tobytes()).decode('utf-8')
        }
        json_output_path = self._save_non_duplicate_file_as_number(
            settings.BACKEND_LOG_PATH, 'json')
        with open(json_output_path, 'w') as f:
            json.dump(json_data, f, indent=4)

    def _save_non_duplicate_file_as_number(self, path: str, file_type: str):
        counter = 0
        while path.exists():
            path = settings.BACKEND_LOG_PATH / f'{counter}.{file_type}'
            counter += 1
        return path

    def _classify(self, img, text):
        """
        Classifies the text and image and returns the similarity
        """
        with torch.no_grad():
            text_tensor = self.classifier.tokenize(text)
            img_tensor = self.classifier.convert_img(img)
            output = self.classifier(text_tensor, img_tensor)
        return torch.softmax(output, dim=1)

    def _request_on_stability_api(self,
                                  prompt: str,
                                  height: int = 512,
                                  width: int = 512,
                                  steps: int = 20) -> PIL.Image.Image:

        response = requests.post(
            settings.STABILITY_GENERATION_URL,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.stability_api_key}"
            },
            json={
                "text_prompts": [
                    {
                        "text": prompt
                    }
                ],
                "cfg_scale": 7,
                "height": height,
                "width": width,
                "samples": 1,
                "steps": steps,
            },
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()["artifacts"][0]
        return self._base64_to_image(data['base64'])

    def _base64_to_image(self, base64_string: str) -> PIL.Image.Image:
        # Remove the "data:image/jpeg;base64," prefix if present
        if base64_string.startswith("data:image"):
            _, base64_string = base64_string.split(",", 1)

        # Decode the base64 string into bytes
        image_bytes = base64.b64decode(base64_string)

        # Create a BytesIO object and wrap it with io.BufferedReader for efficiency
        image_buffer = io.BufferedReader(io.BytesIO(image_bytes))

        # Open the image using PIL
        image = PIL.Image.open(image_buffer)
        return image


def load_main() -> Main:
    return Main(STABILITY_API_KEY)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main = load_main()
    text = "The IDC Manufacturing Insights: Worldwide Manufacturing B2B Commerce and Customer Experience Technology Strategies advisory service explores how manufacturers engage customers through B2B channels and deliver value and innovative customer experiences by leveraging digital technologies. The CIS analyzes key trends and identifies market opportunities around B2B sales and improving customer experience(CX) in this segment. Manufacturing companies have traditionally been slow to adopt digital B2B commerce, but this is gradually changing. In the same way, delivering a value-driven CX in B2B settings is getting increased attention due to its inherent complexity(i.e., the need to build long-term relationships and more collaborative processes and involving multiple stakeholders) as well as customers demanding more seamless, personalized, and connected buying experiences. In many instances, this is a new endeavor, and they need to step out of their comfort zone and try to address the market in a much more dynamic way. It is therefore crucial that IT vendors articulate the value of their solutions for manufacturing companies to address this fast-evolving segment. Approach The IDC Manufacturing Insights: Worldwide Manufacturing B2B Commerce and Customer Experience Technology Strategies service provides comprehensive data and analysis leveraging IDC Manufacturing Insights' proprietary research and correspondence with industry experts, manufacturing executives and practitioners, and IT product and service providers. To ensure relevance, IDC analysts work with subscribers to determine and prioritize topics of interest and are available to provide customized advice to meet their specific needs. Topics Addressed Throughout the year, this service will address the following topics: Evolution of B2B digital commerce and omni-channel strategies Connected B2B buyer customer journey Customer relationship management(CRM) trends Data-driven insights and monetization Automated sales and fulfilment and digitalization of other CX related processes(i.e., customization and product visualization) New B2B business models Multi-step B2B channels B2B networks and business ecosystems Sales enablement practices and technologies Immersive selling/customer experience(e.g., AR/VR, Metaverse) Key Questions Answered Our research addresses the following issues that are critical to your success: How are manufacturing companies evolving their B2B commerce and omni-channel strategies? What are the key technologies they are investing in to improve customer experience? How do they manage data across the entire customer journey? Which areas are companies focusing on to create a simplified and seamless buying experience? What are the business model improvement opportunities and how to enable product-as -a-service offerings? Which are the key players, emerging vendors, and key value propositions for B2B commerce in manufacturing? Who Should Subscribe IDC Manufacturing Insights: Worldwide Manufacturing B2B Commerce and Customer Experience Technology Strategies is ideally suited for IT product and service providers with dedicated value propositions that support manufacturers in delivering value across the entire B2B customer journey. These include providers of digital commerce solutions, CRM and customer data platforms, sales enablement tools, customer feedback and data & analytics platforms, among others. This service is targeted towards C-level executives and divisional heads in marketing, sales, product development and management, market intelligence, and related areas."
    tags = [
        "realistic",
        "8k",
        "octane render",
        "cinematic",
        "trending on artstation",
        "cinematic composition"]

    out = main.main(text, tags)
    out["image"].show()
