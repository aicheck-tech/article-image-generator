import base64
import json
import io
import os
from typing import List, Dict

from PIL import Image
import requests

from article_image_generator.settings import BACKEND_LOG_PATH, STABILITY_GENERATION_URL, NEGATIVE_PROMPT_KEYWORDS, STABILITY_API_KEY
from article_image_generator.backend.errors import BadPromptError
from article_image_generator.backend.text_processing import text_processing
from article_image_generator.service import service



class ArticleImageGenerator:
    def __init__(self, stability_api_key: str):
        self.text_processor = text_processing()
        self.stability_api_key = stability_api_key

    def main(self,
             text: str,
             tags: List[str],
             height: int = 512,
             width: int = 512,
             steps: int = 20,
             samples: int=1) -> Dict[str, Image.Image]: pass
    
    def _save_output(self,
                     type: str,
                     summarized_text: str,
                     images: List[Image.Image],
                     prompt: str) -> None:
        json_output_path = self._generate_free_file_name()
        img_output_path = json_output_path.with_suffix(".jpg") 
        json_data = {
            "type": type,
            "text": summarized_text,
            "prompt": prompt,
            "image": f"{img_output_path}"
        }
        for i, image in enumerate(images):
            image.save(f"{json_output_path}_{i}.jpg")
        with json_output_path.open("w", encoding="utf-8") as handler:
            json.dump(json_data, handler, indent=4, ensure_ascii=False)

    def _generate_free_file_name(self):
        # FIXME convert to db storage instead of file system
        counter = 0
        save_path = None
        while save_path is None or save_path.exists():
            save_path = BACKEND_LOG_PATH / f'{counter}.json'
            counter += 1
        return save_path

    def _prompt_to_image_with_stability_api(self,
                                            prompt: List[Dict[str, float]],
                                            height: int = 512,
                                            width: int = 512,
                                            steps: int = 20,
                                            samples: int=1) -> List[Image.Image]:
        """Generates an image using the stability API.
            example prompt:
            [
              {
                'text': 'A lighthouse on a cliff',
                'weight': 0.5
              }
            ]
        """
        
        response = requests.post(
            STABILITY_GENERATION_URL,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.stability_api_key}"
            },
            json={
                "text_prompts": prompt,
                "cfg_scale": 7,
                "height": height,
                "width": width,
                "samples": samples,
                "steps": steps,
            },
        )

        if response.status_code != 200:
            raise BadPromptError(f"Stability unable to create image using prompt {prompt}: {response.text}.")
        return [self._base64_to_image(base64_img['base64']) for base64_img in response.json()["artifacts"]]

    @staticmethod
    def _base64_to_image(base64_string: str) -> Image.Image:
        # Remove the "data:image/jpeg;base64," prefix if present
        if base64_string.startswith("data:image"):
            _, base64_string = base64_string.split(",", 1)
        image_bytes = base64.b64decode(base64_string)
        image_buffer = io.BufferedReader(io.BytesIO(image_bytes))
        return Image.open(image_buffer)


class ArticleImageGeneratorSummarization(ArticleImageGenerator):
    
    def __init__(self, stability_api_key: str):
        super().__init__(stability_api_key)

    def main(self,
             text: str,
             tags: List[str],
             height: int = 512,
             width: int = 512,
             steps: int = 30,
             samples: int=1) -> Dict[str, float]:
        """

        Args:
            text: article content or summary or heading
            tags: manually and automatically annotated tags describing content of article

        Returns: dict containing image bytes and prompt

        """
        summmarized_text = self.text_processor.summarize_text(text)
        prompt: str = self.text_processor.text_to_tagged_prompt(summmarized_text, tags)
        prompt: List[Dict[str, float]] = [{"text": prompt, "weight": 1.0}] + NEGATIVE_PROMPT_KEYWORDS
        images: List[Image.Image] = self._prompt_to_image_with_stability_api(prompt,height=height, width=width, steps=steps, samples=samples)
        self._save_output("Summarization",summmarized_text, images, prompt)
        return {"pil_images": images, "prompt": prompt}


class ArticleImageGeneratorKeywords(ArticleImageGenerator):
    
    def __init__(self, stability_api_key: str):
        super().__init__(stability_api_key)
        self.PERCENTAGE_OF_KEYWORDS = 0.2

    def main(self,
             text: str,
             tags: List[str],
             height: int = 512,
             width: int = 512,
             steps: int = 20,
             samples: int=1) -> Dict[str, float]:
        """

        Args:
            text: article content or summary or heading
            tags: manually and automatically annotated tags describing content of article

        Returns: dict containing image bytes, prompt and keywords

        """
        keywords = self.text_processor.extract_keywords(text)
        keywords = [keyword[0] for keyword in keywords]
        keywords = keywords[:round(len(keywords)*self.PERCENTAGE_OF_KEYWORDS)]
        prompt: str = self.text_processor.keywords_to_prompt(keywords, tags)
        prompt: List[Dict[str, float]] = [{"text": prompt, "weight": 1.0}] + NEGATIVE_PROMPT_KEYWORDS
        image: Image.Image = self._prompt_to_image_with_stability_api(prompt,height=height, width=width, steps=steps, samples=samples)
        self._save_output("Keywords", text, image, prompt)
        return {"pil_image": image, "prompt": prompt, "keywords": keywords}



@service
def load_pipeline_from_keywords() -> ArticleImageGeneratorKeywords:
    """Load pipeline for generating images from keywords"""
    return ArticleImageGeneratorKeywords(stability_api_key=STABILITY_API_KEY)

@service
def load_pipeline_by_summarization() -> ArticleImageGeneratorSummarization:
    """Load pipeline for generating images from summarization"""
    return ArticleImageGeneratorSummarization(stability_api_key=STABILITY_API_KEY)


