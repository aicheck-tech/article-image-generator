import re
import logging
from typing import List, Dict

import torch
import openai
import tiktoken
from sklearn.feature_extraction.text import TfidfVectorizer

from article_image_generator.backend.errors import NotFoundAnyTerm
from article_image_generator.service import service
from article_image_generator.settings import (
    OPENAI_API_VERSION, OPENAI_ENCODING_NAME, OPENAI_SUMMARIZE_SYSTEM_TEXT, OPENAI_KEYWORDS_TO_PROMPT_SYSTEM_TEXT, OPENAI_KEYWORDS_TO_PROMPT_MAX_TOKENS,
    OPENAI_SUMMARIZATION_MAX_TOKENS, OPENAI_TEXT_TO_PROMPT_SYSTEM_TEXT, OPENAI_TEXT_TO_PROMPT_MAX_TOKENS,
    OPENAI_SUMMARIZE_TEXTS_LONGER_THAN_N_TOKENS, OPENAI_API_KEY, OPENAI_API_ENGINE_COMPLETION, OPENAI_API_ENGINE_EMBEDDING, OPENAI_CUSTOM_DOMAIN
)

logger = logging.getLogger(__name__)


class TextProcessing:
    def __init__(self,
                 openai_api_key,
                 openai_api_engine_completion,
                 openai_api_engine_embedding,
                 openai_custom_domain
                 ):
        self.OPENAI_API_KEY = openai_api_key
        self.OPENAI_API_ENGINE_COMPLETION = openai_api_engine_completion
        self.OPENAI_API_ENGINE_EMBEDDING = openai_api_engine_embedding
        self.OPENAI_CUSTOM_DOMAIN = openai_custom_domain
        self.COSSIM = torch.nn.CosineSimilarity(dim=0, eps=1e-8)
        self.TFIDF = TfidfVectorizer(norm="l2", stop_words='english')
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
    
    def tokenize_text_ada(self, text: str) -> torch.Tensor:
        """Tokenize text using ada engine"""
        # Not used yet
        embedings = openai.Embedding.create(
            input=text,
            engine=self.OPENAI_API_ENGINE_EMBEDDING,
        )["data"]["embedding"]
        return torch.tensor(embedings)
    
    def get_text_similarity_ada(self, a, b) -> float:
        ''' get cosine similarity between two text using ada engine'''
        # Not used yet
        a_vector = self.tokenize_text_ada(a)
        b_vector = self.tokenize_text_ada(b)
        vector_1 = torch.flatten(a_vector)
        vector_2 = torch.flatten(b_vector)
        return float(self.COSSIM(vector_1, vector_2).item())

    def tf_idf(self, text: str) -> Dict[str, float]:
        """Calculate tf-idf score for each term in text"""
        tfidf_matrix = self.TFIDF.fit_transform([text])
        feature_names = self.TFIDF.get_feature_names_out()
        tfidf_scores = tfidf_matrix[0].toarray().flatten()
        tfidf_dict = {}
        for term, score in zip(feature_names, tfidf_scores):
            tfidf_dict[term] = score
        if len(tfidf_dict) == 0:
            raise NotFoundAnyTerm("Not found any term in text, please try again with longer text")
        return tfidf_dict
    
    def extract_keywords(self, text: str):
        """Extract keywords from text"""
        terms = self.tf_idf(text.lower())
        return sorted(terms.items(), key=lambda term: term[1], reverse=True)
    
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
            engine=self.OPENAI_API_ENGINE_COMPLETION,
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
                        OPENAI_TEXT_TO_PROMPT_SYSTEM_TEXT +
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
            engine=self.OPENAI_API_ENGINE_COMPLETION,
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
    
    def keywords_to_prompt(self, keywords: List[str], tags: List[str]) -> str:
        """Text to prompt ready for image generation.

        Args:
            text: Text from article
            tags: List of tags to create more fitting prompt

        Returns: generated prompt
        """
        logger.debug(keywords)
        keywords_str = ", ".join(keywords)
        logger.info(f"Generating prompt from keywords {keywords_str}.")

        clean_batch = keywords_str.replace("\n", " ").strip()
        prompt = self._encode_prompt([
            {
                "role": "system",
                "content": (
                        OPENAI_KEYWORDS_TO_PROMPT_SYSTEM_TEXT +
                        (
                            f"The design should be {', '.join(tags)}\n\n"
                            "Annotate it as:\n"
                            "'prompt': <the prompt>"
                        )
                )
            },
            {
                "role": "user",
                "content": f"'keywords': {clean_batch}"
            }
        ])
        logger.debug(prompt)

        max_tokens = self.count_tokens(prompt) + OPENAI_KEYWORDS_TO_PROMPT_MAX_TOKENS
        logger.info("Text to prompt max tokens: %s", max_tokens)
        response = openai.Completion.create(
            engine=self.OPENAI_API_ENGINE_COMPLETION,
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
        OPENAI_API_ENGINE_COMPLETION,
        OPENAI_API_ENGINE_EMBEDDING,
        OPENAI_CUSTOM_DOMAIN)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    ok = text_processing = TextProcessing(
        OPENAI_API_KEY,
        OPENAI_API_ENGINE_COMPLETION,
        OPENAI_API_ENGINE_EMBEDDING,
        OPENAI_CUSTOM_DOMAIN)
    text = "This IDC Survey Spotlight highlights the approximate share of business process services (BPS) providers' customers that utilize Microsoft Azure, SAP, AWS, Oracle, Google Cloud, IBM Cloud, and other platforms as part of the outsourced finance business process services delivered to them. The data depicted in this document is from a 2022 Finance and Accounting Cloud BPS Survey, which included quantitative and qualitative feedback from nine finance and accounting BPS providers."
    keywords = ok.extract_keywords(text)
    print(keywords)
    keywords = [keyword[0] for keyword in keywords]
    keywords = keywords[:5]
    print(ok.keywords_to_prompt(keywords, ["realistic", "concept art"]))