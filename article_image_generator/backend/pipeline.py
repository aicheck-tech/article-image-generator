import base64
import json
import io
import os
from typing import List, Dict, Tuple, Union

import PIL
import requests
import torch

from article_image_generator.backend import clip_classification
from article_image_generator.settings import BACKEND_LOG_PATH, STABILITY_GENERATION_URL
from article_image_generator.backend.errors import BadPromptError
from article_image_generator.backend.text_processing import text_processing
from article_image_generator.service import service


STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")


class ArticleImageGenerator:
    def __init__(self, stability_api_key: str):
        self.classifier = clip_classification.load_classifiear()
        self.text_processor = text_processing()
        self.stability_api_key = stability_api_key

    def main(self, text: str, tags: List[str]) -> Dict[str, Union[float, PIL.Image.Image]]:
        """

        Args:
            text: article content or summary or heading
            tags: manually and automatically annotated tags describing content of article

        Returns: dict containing image bytes and confidence score <0, 1>

        """
        summmarized_text = self.text_processor.summarize_text(text)
        prompt: str = self.text_processor.text_to_tagged_prompt(summmarized_text, tags)
        image: PIL.Image.Image = self._prompt_to_image_with_stability_api(prompt)
        tensor_similarity = self._classify(image, summmarized_text)
        similarity_vector = tensor_similarity.cpu().numpy()  # [[similarity, 1-similarity]]
        confidence = similarity_vector[0][0]
        self._save_output(text, image, confidence, prompt)
        return {"image_bytes": image.tobytes(), "confidence": confidence, "prompt": prompt}

    def _save_output(self,
                     summarized_text: str,
                     image: PIL.Image.Image,
                     similarity: Tuple[float, float],
                     prompt: str) -> None:
        json_data = {
            "text": summarized_text,
            "prompt": prompt,
            "similarity": f"{similarity[0]}% similarity, {similarity[1]}% dissimilarity",
            "image": base64.b64encode(image.tobytes()).decode('utf-8')
        }
        json_output_path = self._generate_free_file_name()
        with json_output_path.open("w") as handler:
            json.dump(json_data, handler, indent=4, ensure_ascii=False)

    def _generate_free_file_name(self):
        # FIXME convert to db storage instead of file system
        counter = 0
        save_path = None
        while save_path is None or save_path.exists():
            save_path = BACKEND_LOG_PATH / f'{counter}.json'
            counter += 1
        return save_path

    def _classify(self, img: PIL.Image.Image, text: str) -> torch.Tensor:
        """
        Classifies the text and image and returns the similarity
        """
        with torch.no_grad():
            text_tensor = self.classifier.tokenize(text)
            img_tensor = self.classifier.convert_img(img)
            output = self.classifier(text_tensor, img_tensor)
        return torch.softmax(output, dim=1)

    def _prompt_to_image_with_stability_api(self,
                                            prompt: str,
                                            height: int = 512,
                                            width: int = 512,
                                            steps: int = 20) -> PIL.Image.Image:
        response = requests.post(
            STABILITY_GENERATION_URL,
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
            raise BadPromptError(f"Stability unable to create image using prompt {prompt}: {response.text}.")

        data = response.json()["artifacts"][0]
        return self._base64_to_image(data['base64'])

    @staticmethod
    def _base64_to_image(base64_string: str) -> PIL.Image.Image:
        # Remove the "data:image/jpeg;base64," prefix if present
        if base64_string.startswith("data:image"):
            _, base64_string = base64_string.split(",", 1)
        image_bytes = base64.b64decode(base64_string)
        image_buffer = io.BufferedReader(io.BytesIO(image_bytes))
        return PIL.Image.open(image_buffer)

@service
def load_pipeline() -> ArticleImageGenerator:
    return ArticleImageGenerator(stability_api_key=STABILITY_API_KEY)
