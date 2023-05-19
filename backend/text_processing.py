import os
import re
from typing import List, Dict
import logging
from pathlib import Path
import sys

import openai
from dotenv import load_dotenv
import tiktoken

from settings import (
    OPENAI_API_VERSION, OPENAI_ENCODING_NAME, OPENAI_SUMMARIZE_SYSTEM_TEXT,
    OPENAI_SUMMARIZATION_MAX_TOKENS, OPENAI_PROMPT_SYSTEM_TEXT, OPENAI_TEXT_TO_PROMPT_MAX_TOKENS,
    OPENAI_SUMMARIZE_TEXTS_LONGER_THAN_N_TOKENS
)


parent_folder = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_folder))


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
        openai.api_version = OPENAI_API_VERSION
        openai.api_key = self.OPENAI_API_KEY

    def _encode_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Defining a function to create the prompt from the system message and the messages."""

        logger.info("Encoding prompt")

        prompt = ""
        message_template = "\n<|im_start|>{}\n{}\n<|im_end|>"
        for message in messages:
            if message.get("content", "") == "":
                raise ValueError("Content of message cannot be empty")
            prompt += message_template.format(
                message['role'], message.get('content', ''))
        prompt += "\n<|im_start|>assistant\n"

        logger.debug(prompt)
        return prompt

    def count_tokens(self, text:str) -> int:
        encoding = tiktoken.get_encoding(OPENAI_ENCODING_NAME)
        num_tokens = len(encoding.encode(text))
        return num_tokens

    def summarize_text(self, text: str) -> str:
        """Summarize text using OpenAI API.
        Args:
            text (str): The input text. (long article)

        Returns:
            str: The summarized text.
        """

        logger.info("Summarizing text %s.", text.replace("\n", "\n"))

        clean_batch = text.replace("\n", " ").strip()

        prompt = self._encode_prompt([
            {
                "role": "system",
                "content": OPENAI_SUMMARIZE_SYSTEM_TEXT
            },
            {
                "role": "user",
                "content": f"text: {clean_batch}"
            }
        ])

        MAX_TOKENS = self.count_tokens(prompt) + OPENAI_SUMMARIZATION_MAX_TOKENS
        logger.info("Summarization max tokens: %s", MAX_TOKENS)
        response = openai.Completion.create(
            engine=self.OPENAI_API_ENGINE,
            prompt=prompt,
            temperature=0.7,
            max_tokens=MAX_TOKENS,
            top_p=0.95,
            frequency_penalty=0.3,
            presence_penalty=0,
            stop=["<|im_end|>"])
        

        logger.debug(response)
        logger.info("Summarized text %s.", response["choices"][0]["text"])
        return response["choices"][0]["text"]

    def text_to_prompt(self, text: str, tags: List[str]) -> str:
        """Text to prompt ready for image generation.

        Args:
            text: Text from article
            tags: List of tags to create more fitting prompt

        Returns:
            str: generated prompt
        """
        logger.info("Generating prompt from text %s.", text.replace("\n", "\n"))

        clean_batch = text.replace("\n", " ").strip()
        prompt = self._encode_prompt([
            {
                "role": "system",
                "content": (
                    OPENAI_PROMPT_SYSTEM_TEXT +
                    (
                    f"The design should be {', '.join(tags)}\n\n"
                    "Annotate it as:\n"
                    "'prompt': <the prompt>"
                    )
                )
            },
            {
                "role": "user",
                "content": f"'text': {clean_batch}"
            }
        ])

        MAX_TOKENS = self.count_tokens(prompt) + OPENAI_TEXT_TO_PROMPT_MAX_TOKENS
        logger.info("Text to prompt max tokens: %s", MAX_TOKENS)
        response = openai.Completion.create(
            engine=self.OPENAI_API_ENGINE,
            prompt=prompt,
            temperature=0,
            max_tokens=MAX_TOKENS,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["<|im_end|>"]
            )

        logger.debug(response)
        answer = response["choices"][0]["text"]
        
        result = re.search(r"^'prompt': (.*)$", answer)
        
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

        if self.count_tokens(text) > OPENAI_SUMMARIZE_TEXTS_LONGER_THAN_N_TOKENS:
            text = self.summarize_text(text)
        text_to_prompt = self.text_to_prompt(text, tags)
        
        logging.info(text_to_prompt)
        return text_to_prompt


def text_processing() -> TextProcessing:
    return TextProcessing(
        OPENAI_API_KEY,
        OPENAI_API_ENGINE,
        OPENAI_CUSTOM_DOMAIN)
