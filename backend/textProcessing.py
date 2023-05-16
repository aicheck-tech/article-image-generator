import re

import openai
import tiktoken

class TextProcessing:
    def __init__(self, 
                 text, openai_api_key, openai_api_engine, 
                 openai_custom_domain, summarized = None):
        self.text = text
        self.OPENAI_API_KEY = openai_api_key
        self.OPENAI_API_ENGINE = openai_api_engine
        self.OPENAI_CUSTOM_DOMAIN = openai_custom_domain
        
        self.setup_openai()
        self.summarized = summarized
    
    def setup_openai(self):
        """Setup connection to Azure Open AI service.

        Information source: https://learn.microsoft.com/en-us/azure/cognitive-services/openai/quickstart

        """
        openai.api_type = "azure"
        openai.api_base = f"https://{self.OPENAI_CUSTOM_DOMAIN}.openai.azure.com/"
        openai.api_version = "2022-12-01"
        openai.api_key = self.OPENAI_API_KEY
        
    def num_tokens_from_messages(self, messages, model="gpt-3.5-turbo-0301"):
        """Returns the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        
        return sum(len(encoding.encode(message)) for message in messages["items"])
    
    def _encode_prompt(self, messages) -> str:
        """Defining a function to create the prompt from the system message and the messages."""
        
        prompt = ""
        message_template = "\n<|im_start|>{}\n{}\n<|im_end|>"
        for message in messages:
            prompt += message_template.format(message['role'], message.get('content', ''))
        prompt += "\n<|im_start|>assistant\n"
        return prompt
    
    def summarize(self):
        prompt = f"Summarize the following text as short as possible:\n{self.text}\nSummary:"

        response = openai.Completion.create(
            engine=self.OPENAI_API_ENGINE,
            prompt=prompt,
            temperature=0.7,
            max_tokens=350,
            top_p=0.95,
            frequency_penalty=0.3,
            presence_penalty=0,
            stop=["<|im_end|>"])
        return response
    
    def text_object_description(self, text: str) -> str:
        """
        Args:
            text (str): The input text.

        Returns:
            object (dict):
                name (str): The name of the object.
                description (str): The description of the object.
        """
        clean_batch = text.replace("\n", " ").strip()
        prompt = self._encode_prompt([
            {
                "role": "system",
                "content": (
                    "Act as a human, that tells you, what is the name of the main object in text.\n"
                    "Create a very short description of how it propably looks, not where it came from.\n"
                    "Annotate it as: \n"
                    "name: (name)\n"
                    "description: (description)\n"
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

        answer = response["choices"][0]["text"]
        responses = {}  
        
        result = re.search(r"name: (.*)\ndescription: (.*)", answer)
        return {"name": result.group(1), "description": result.group(2)}
    
    def stable_diffusion_prompt_generator(self, tags: list):
        """
        args:
        tags (list): List of tags to generate prompt from.
        
        returns:
        prompt (str): Prompt for stable diffusion with added tags.
        
        examples:
        tags = ["realistic", "concept art"]  
        prompt = "Create a realistic concept art of a ..."
        """
        
        if (not self.summarized):
            self.summarized = self.summarize()["choices"][0]["text"]
        
        object_to_generate = self.text_object_description(self.summarized)
        result = f"{object_to_generate['description']}, {', '.join(tags)}"
        
        return result

