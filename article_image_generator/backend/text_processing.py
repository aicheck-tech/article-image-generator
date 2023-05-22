import re
import logging
import math
from typing import List, Dict, Tuple
from collections import Counter

import nltk
import openai
import tiktoken
from yake import KeywordExtractor

from article_image_generator.backend.errors import NotFoundKeyword
from article_image_generator.service import service
from article_image_generator.settings import (
    OPENAI_API_VERSION, OPENAI_ENCODING_NAME, OPENAI_SUMMARIZE_SYSTEM_TEXT,
    OPENAI_SUMMARIZATION_MAX_TOKENS, OPENAI_PROMPT_SYSTEM_TEXT, OPENAI_TEXT_TO_PROMPT_MAX_TOKENS,
    OPENAI_SUMMARIZE_TEXTS_LONGER_THAN_N_TOKENS, OPENAI_API_KEY, OPENAI_API_ENGINE, OPENAI_CUSTOM_DOMAIN
)

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
        self.kw_extractor = KeywordExtractor()
        self.WORD = re.compile(r'\w+')
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

    def count_tokens(self, text: str) -> int:
        encoding = tiktoken.get_encoding(OPENAI_ENCODING_NAME)
        num_tokens = len(encoding.encode(text))
        return num_tokens
    
    def get_cosine(self, vec1:Counter, vec2:Counter) -> float:
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum(vec1[x] * vec2[x] for x in intersection)
        sum1 = math.fsum(vec1[x]**2 for x in vec1)
        sum2 = math.fsum(vec2[x]**2 for x in vec2)
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        return float(numerator) / denominator if denominator else 0.0
    
    def text_to_vector(self, text:str) -> Counter:
        return Counter(self.WORD.findall(text.lower()))
    
    def get_text_similarity(self, a, b) -> float:
        a = self.text_to_vector(a.strip())
        b = self.text_to_vector(b.strip())
        return self.get_cosine(a, b)
    
    def add_value_from_substring(self, lst: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """Add value from substring in list of tuple to bigger string in list of tuple."""
        for i in range(len(lst)):
            for j in range(len(lst)):
                if i != j and lst[j][0] in lst[i][0] and (len(lst[i][0]) > len(lst[j][0])):
                    lst[i] = (lst[i][0], lst[i][1]+lst[j][1])
        return lst

    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        tokens_from_text = nltk.tokenize.word_tokenize(text)
        positional_tags = nltk.pos_tag(tokens_from_text)
        nouns = [word for word, tag in positional_tags if tag.startswith('N')]
        pronouns = [word for word, tag in positional_tags if tag == 'PRP']
        positional_word = nouns + pronouns
        # Extract Subjects
        keywords = self.kw_extractor.extract_keywords(text)

        if keywords == []:
            raise NotFoundKeyword("Not found keyword in text")
        ''' Calculate score for each title : tuple(title:str, score:float)
            Add score for cosine similarity with text if keyword is in positional_word
        ''' 
        keywords = [(keyword[0], keyword[1]+self.get_text_similarity(text, keyword[0])) if keyword[0] in positional_word else keyword for keyword in keywords]
        keywords = self.add_value_from_substring(keywords)
        # Sort by score
        keywords = sorted(keywords, key=lambda x: x[1], reverse=True)
        return keywords

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

        max_tokens = self.count_tokens(prompt) + OPENAI_SUMMARIZATION_MAX_TOKENS
        logger.info("Summarization max tokens: %s", max_tokens)
        response = openai.Completion.create(
            engine=self.OPENAI_API_ENGINE,
            prompt=prompt,
            temperature=0.7,
            max_tokens=max_tokens,
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

        Returns: generated prompt
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

        max_tokens = self.count_tokens(prompt) + OPENAI_TEXT_TO_PROMPT_MAX_TOKENS
        logger.info("Text to prompt max tokens: %s", max_tokens)
        response = openai.Completion.create(
            engine=self.OPENAI_API_ENGINE,
            prompt=prompt,
            temperature=0,
            max_tokens=max_tokens,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["<|im_end|>"]
        )

        logger.debug(response)
        answer = response["choices"][0]["text"]

        result = re.search(r"^'prompt': (.*)$", answer)

        return result.group(1)

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


@service
def text_processing() -> TextProcessing:
    return TextProcessing(
        OPENAI_API_KEY,
        OPENAI_API_ENGINE,
        OPENAI_CUSTOM_DOMAIN)
