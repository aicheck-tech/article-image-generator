import sys
from pathlib import Path
import os
import io
from typing import List, Dict, Tuple
import base64
import json

import torch
from dotenv import load_dotenv
import requests
import PIL

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
        image_bytes = base64.b64decode(base64_string)
        image_buffer = io.BufferedReader(io.BytesIO(image_bytes))
        image = PIL.Image.open(image_buffer)
        return image


def load_main() -> Main:
    return Main(STABILITY_API_KEY)
