import os
import re
from typing import List
import logging

import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_ENGINE = os.getenv("OPENAI_API_ENGINE")
OPENAI_CUSTOM_DOMAIN = os.getenv("OPENAI_CUSTOM_DOMAIN")

logger = logging.getLogger(__name__)


class TextProcessing:
    def __init__(self,
                 openai_api_key,
                 openai_api_engine,
                 openai_custom_domain
                 ):
        self.OPENAI_API_KEY = openai_api_key
        self.OPENAI_API_ENGINE = openai_api_engine
        self.OPENAI_CUSTOM_DOMAIN = openai_custom_domain

        self._setup_openai()

    def _setup_openai(self):
        """Setup connection to Azure Open AI service.

        Information source: https://learn.microsoft.com/en-us/azure/cognitive-services/openai/quickstart

        """
        logger.info("Setting up OpenAI")

        openai.api_type = "azure"
        openai.api_base = f"https://{self.OPENAI_CUSTOM_DOMAIN}.openai.azure.com/"
        openai.api_version = "2022-12-01"
        openai.api_key = self.OPENAI_API_KEY

    def _encode_prompt(self, messages) -> str:
        """Defining a function to create the prompt from the system message and the messages."""

        logger.info("Encoding prompt")

        prompt = ""
        message_template = "\n<|im_start|>{}\n{}\n<|im_end|>"
        for message in messages:
            prompt += message_template.format(
                message['role'], message.get('content', ''))
        prompt += "\n<|im_start|>assistant\n"

        logger.debug(prompt)
        return prompt

    def summarize_text(self, text: str) -> str:
        """Summarize text using OpenAI API.
        Args:
            text (str): The input text. (long article)

        Returns:
            str: The summarized text.
        """

        logger.info("Summarizing text")

        clean_batch = text.replace("\n", " ").strip()

        prompt = self._encode_prompt([
            {
                "role": "system",
                "content": (
                    "Act as a human, that summarizes given text to be as short as possible.\n"
                )
            },
            {
                "role": "user",
                "content": f"text: {clean_batch}"
            }
        ])

        response = openai.Completion.create(
            engine=self.OPENAI_API_ENGINE,
            prompt=prompt,
            temperature=0.7,
            max_tokens=350,
            top_p=0.95,
            frequency_penalty=0.3,
            presence_penalty=0,
            stop=["<|im_end|>"])
        

        logger.debug(response)
        return response["choices"][0]["text"]

    def text_to_prompt(self, text: str, tags: List[str]) -> str:
        logger.info("Generating prompt from text")

        clean_batch = text.replace("\n", " ").strip()
        prompt = self._encode_prompt([
            {
                "role": "system",
                "content": (
                    "Generate a prompt for image generator based on text in variable called 'text':\n"
                    "Two examples of good prompt:\n"
                    "'prompt': 'Imagine a stunning woman standing in a garden surrounded by a riot of colorful blooms, with the sun setting in the distance. Use soft lighting to capture the warmth of the golden hour and the subtle nuances of her expression.'\n\n"
                    "'prompt':  'a portrait of an old coal miner in 19th century, beautiful painting with highly detailed face by greg rutkowski and magali villanueve'\n\n"
                    "Two examples of bad prompt:\n"
                    "'prompt':  'Worldwide Wi-Fi Technology Forecast is a report that is likely to be a document consisting of text and graphs. The cover page may have the title in bold letters with a background color that is eye-catching. The report may be bound with a spiral or a perfect binding. The pages may be white with black text and colored graphs. The graphs may show the growth of Wi-Fi technology in different regions of the world. The report may be placed on a desk or a shelf in an office.'\n\n"
                    "'prompt': 'SaaSPath 2023 is a list of various application categories including Banner Books, CPQ, Digital Commerce, Employee Experience, Facility Management, Field Service Management, PIM/PXM, and Procurement. It also includes information on adoption, deployment models, budget plans, replacement cycle timing, purchasing preferences, and attitudes towards SaaS buying channels. The report provides insights on packaging, pricing options, vendor reviews, ratings, spend, and advocacy scores for functional application markets.'\n\n"
                    "If it's for paper or a study, generate prompt for some real physical object, that the study is about.\n\n"
                    f"The design should be {', '.join(tags)}\n\n"
                    "Annotate it as:\n"
                    "'prompt': <the prompt>"
                )
            },
            {
                "role": "user",
                "content": f"'text': {clean_batch}"
            }
        ])

        response = openai.Completion.create(
            engine=self.OPENAI_API_ENGINE,
            prompt=prompt,
            temperature=0,
            max_tokens=256,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["<|im_end|>"]
            )

        logger.debug(response)
        answer = response["choices"][0]["text"]
        
        result = re.search(
            r"^'prompt': (.*)$", answer)
        
        return {"prompt": result.group(1)}

    def text_to_tagged_prompt(self, text, tags: List[str]) -> str:
        """
        args:
            tags (list): List of tags to generate prompt from.

        returns:
            prompt (str): Prompt for stable diffusion with added tags.

        examples:
            tags = ["realistic", "concept art"]  
            prompt = "Create a realistic concept art of a ..."
        """

        logger.info("Generating prompt from text and tags")

        if (len(text.split(" ")) > 100):
            text = self.summarize_text(text)
        text_to_prompt = self.text_to_prompt(text, tags)
        logging.info(text_to_prompt)
        return text_to_prompt


def text_processing() -> TextProcessing:
    return TextProcessing(
        OPENAI_API_KEY,
        OPENAI_API_ENGINE,
        OPENAI_CUSTOM_DOMAIN)
