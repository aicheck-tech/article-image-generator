import os
import re
from typing import List
import logging

import openai
import tiktoken
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_ENGINE = os.getenv("OPENAI_API_ENGINE")
OPENAI_CUSTOM_DOMAIN = os.getenv("OPENAI_CUSTOM_DOMAIN")

logger = logging.getLogger(__name__)

class TextProcessing:
    def __init__(self, openai_api_key, openai_api_engine, openai_custom_domain, summarized = None):
        self.OPENAI_API_KEY = openai_api_key
        self.OPENAI_API_ENGINE = openai_api_engine
        self.OPENAI_CUSTOM_DOMAIN = openai_custom_domain
        
        self.setup_openai()
    
    def setup_openai(self):
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
            prompt += message_template.format(message['role'], message.get('content', ''))
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
    
    def topic_from_text(self, text: str) -> str:
        """
        Args:
            text (str): The input text.

        Returns:
            dictionary:
                str: Extracted topic from the text.
                str: Description of how the topic looks in real life.
        """
        
        logger.info("Extracting topic from text")
        
        clean_batch = text.replace("\n", " ").strip()
        prompt = self._encode_prompt([
            {
                "role": "system",
                "content": (
                    "Act as a human, that tells you, what is the name of the main object in text.\n"
                    # "Create a very short description of how it propably looks, not where it came from and don't compare anything.\n"
                    "As this human, create short description of the looks of the main object, not subject in the text.\n"
                    "Example outputs: \n"
                    "topic_name: african warrior chief\n"
                    "topic_description: portrait photo of a african old warrior chief, tribal panther make up, gold on white, side profile, looking away, serious eyes \n"
                    "topic_name: modern living room\n"
                    "topic_description: interior design, open plan, kitchen and living room, modular furniture with cotton textiles, wooden floor, high ceiling, large steel windows viewing a city\n"
                    "Annotate it as: \n"
                    "topic_name: (name)\n"
                    "topic_description: (description)\n"
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
            temperature=0,
            max_tokens=4096,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["<|im_end|>"])

        logger.debug(response)
        answer = response["choices"][0]["text"]
        
        responses = {}  
        result = re.search(r"^topic_name: (.*)\ntopic_description: (.*)$", answer)
        
        final = {"topic_name": result.group(1), "topic_description": result.group(2)}
        
        logger.debug(final)
        return final
    
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
        
        summarized_text = self.summarize_text(text)
        tagged_prompt = self.topic_from_text(summarized_text)
        
        return  f"{tagged_prompt['topic_description']}, {', '.join(tags)}"

def text_processing() -> TextProcessing:
    return TextProcessing(OPENAI_API_KEY, OPENAI_API_ENGINE, OPENAI_CUSTOM_DOMAIN)
