import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DEBUG = False

BACKEND_LOG_PATH = Path("article_image_generator/backend/logs")

# FastAPI
FASTAPI_HOST = "127.0.0.1"
FASTAPI_PORT = 8001
FASTAPI_WORKERS = 1

# FastAPI - stability api settings
MAX_STEPS = 90
MIN_STEPS = 20
MAX_SAMPLES = 4
MIN_SAMPLES = 1

# OpenAI
OPENAI_API_VERSION = "2022-12-01"
OPENAI_ENCODING_NAME = "cl100k_base"
OPENAI_SUMMARIZE_TEXTS_LONGER_THAN_N_TOKENS = 100
OPENAI_SUMMARIZATION_MAX_TOKENS = 350
OPENAI_TEXT_TO_PROMPT_MAX_TOKENS = 256
OPENAI_KEYWORDS_TO_PROMPT_MAX_TOKENS = 256

OPENAI_SUMMARIZE_SYSTEM_TEXT = (
    "Act as a human, that summarizes given text to be as short as possible.\n"
)

OPENAI_TEXT_TO_PROMPT_SYSTEM_TEXT = (
    "Generate a prompt for image generator based on text in variable called 'text':\n"
    "Two examples of good prompt:\n"
    "'prompt': 'Imagine a stunning woman standing in a garden surrounded by a riot of colorful blooms, with the sun setting in the distance. Use soft lighting to capture the warmth of the golden hour and the subtle nuances of her expression.'\n\n"
    "'prompt': 'a portrait of an old coal miner in 19th century, beautiful painting with highly detailed face by greg rutkowski and magali villanueve'\n\n"
    "Two examples of bad prompt:\n"
    "'prompt': 'Worldwide Wi-Fi Technology Forecast is a report that is likely to be a document consisting of text and graphs. The cover page may have the title in bold letters with a background color that is eye-catching. The report may be bound with a spiral or a perfect binding. The pages may be white with black text and colored graphs. The graphs may show the growth of Wi-Fi technology in different regions of the world. The report may be placed on a desk or a shelf in an office.'\n\n"
    "'prompt': 'SaaSPath 2023 is a list of various application categories including Banner Books, CPQ, Digital Commerce, Employee Experience, Facility Management, Field Service Management, PIM/PXM, and Procurement. It also includes information on adoption, deployment models, budget plans, replacement cycle timing, purchasing preferences, and attitudes towards SaaS buying channels. The report provides insights on packaging, pricing options, vendor reviews, ratings, spend, and advocacy scores for functional application markets.'\n\n"
    "If it's for paper or a study, generate prompt for some real physical object, that the study is about.\n\n"
    "the text must be short and to the point\n"
)


OPENAI_KEYWORDS_TO_PROMPT_SYSTEM_TEXT = (
    "Generate a prompt for an image generator based on the keywords provided in a variable called 'keywords'.\n"
    "Examples of great prompt:\n"
    "'prompt': 'Create an image that represents the power of AI in customer data analysis. Imagine a futuristic dashboard that displays real-time customer data, with lines of code running in the background. The dashboard should highlight the advantage of using AI to analyze customer behavior, with inferred insights that can help businesses act quickly and bring value to their customers. The image should be cinematic and visually striking, with a composition that showcases the complexity and sophistication of the technology. Let your creativity flow and build a design that captures the essence of these keywords: customer, data, analyze, code, customers, inferred, 12, 30, act, advantage, ai, bring, and build.'\n\n"
    "Examples of good prompts:\n"
    "'prompt': 'Imagine a breathtaking landscape with a majestic mountain range covered in snow, reflecting the vibrant colors of the sunrise. Capture the serenity of the scene and the crispness of the air.'\n\n"
    "'prompt': 'Create an image of an antique wooden chest adorned with intricate carvings and metal embellishments. Highlight the textures and reveal the history and craftsmanship through careful lighting.'\n\n"
    "'prompt': 'Generate a compelling image that encapsulates the essence of 'Business,' 'Money,' and 'Analyst.' Capture the dynamic energy of the corporate world, the allure of financial success, and the meticulous analysis that drives it all. Your image should evoke a sense of professionalism, ambition, and strategic thinking. Let your creativity flow and create an impactful visual representation that brings these keywords to life.'\n\n"
    "'prompt': 'Immerse yourself in the awe-inspiring panorama of a magnificent mountain range adorned in a glistening blanket of pristine snow, harmoniously mirroring the resplendent hues of a vivid sunrise. Embark on a captivating journey that encapsulates the tranquility of the scene and the invigorating clarity of the atmosphere.\n\n"
    "Examples of bad prompts:\n"
    "'prompt': 'Create an image that showcases the power of data-driven customer relationships in driving revenue growth for businesses. Imagine a scene where a business is using data to activate customer relationships and drive revenue growth. The image should highlight the importance of a customer-centric approach and the value of leveraging data to understand and engage with customers. Use cinematic composition and trending art styles to create a visually stunning image that captures the essence of these keywords.'\n\n"
    "'prompt': 'Visualize a world where independent content creators have endless opportunities to create and grow their platforms. Your image should capture the essence of creativity and innovation, highlighting the power of independent voices in shaping political discourse and driving revenue. Use your artistic skills to create a stunning visual representation that showcases the potential of content creation in 2021 and beyond. Your design should be realistic, 8k, octane render, cinematic, trending on artstation, and feature a dynamic composition that draws the viewer in.'\n\n"
    "The prompt should be focused on visually descriptive scenes or objects. If the prompt is for a paper or study, generate an image prompt related to a specific physical object that the study is about.\n\n"
)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_ENGINE_COMPLETION = "gpt-35-turbo"
OPENAI_API_ENGINE_EMBEDDING = "text-similarity-ada-001"
OPENAI_CUSTOM_DOMAIN = "nextgen"

# Stable Diffusion
STABLE_DIFFUSION_HUGGING_FACE = "stabilityai/stable-diffusion-2-1"

# DreamStudio API - Stable Diffusion
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
STABILITY_ENGINE = "stable-diffusion-xl-beta-v2-2-2"
STABILITY_GENERATION_URL = f"https://api.stability.ai/v1/generation/{STABILITY_ENGINE}/text-to-image"

# Train settings
TRAIN_TEST_SPLIT_RATIO = 0.9
BATCH_SIZE = 1

DATASETS = {
    "bbc": "Dzeniks/BBC-article"
}

# Image generator settings

IMAGE_STYLES = {
    "realistic": [
        "realistic",
        "8k",
        "octane render",
        "cinematic",
        "trending on artstation",
        "cinematic composition"
    ],
    "cinematic": [
        "cinematic",
        "cinematic composition",
        "ray tracing",
        "log3",
        "8k"
    ],
    "cartoon": [
        "cartoon",
        "hand drawn",
        "full color",
        "anime key visual",
        "trending on artstation",
    ],
    "sketch": [
        "high quality of sketching",
        "ultra - detailed technical precision",
        "monumentally art composition",
        "octane render",
        "grey paper sketch ink style"
    ]
}

NEGATIVE_PROMPT_KEYWORDS = [
        {
            "text": "Create an image that showcases a vibrant urban landscape with elements like towns, cities, and imposing skyscrapers.",
            "weight": -0.3,
        },
        {
            "text": "Create an informative chart that visually represents key sustainability metrics and their impact on environmental, social, and economic dimensions.",
            "weight": -1.0,
        },
        {
            "text": "Create an image that depicts a scene with elements such as paper, books, and a study environment or posters.",
            "weight": -1.5,
        },
        {
            "text": "Create an image focusing on the intricate details of human legs, hands, and fingers, capturing their unique form and movement.",
            "weight": -1.5,
        },
        {
            "text": "Create an image that does contain any text, titles, numbers, or any form of alphanumeric characters.",
            "weight": -2.0,
        },
]