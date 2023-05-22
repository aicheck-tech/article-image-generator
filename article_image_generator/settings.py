import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DEBUG = False

BACKEND_LOG_PATH = Path("article_image_generator/backend/logs")

# FastAPI
FASTAPI_PORT = 8001
FASTAPI_WORKERS = 1

# OpenAI
OPENAI_API_VERSION = "2022-12-01"
OPENAI_ENCODING_NAME = "cl100k_base"
OPENAI_SUMMARIZE_TEXTS_LONGER_THAN_N_TOKENS = 100
OPENAI_SUMMARIZATION_MAX_TOKENS = 350
OPENAI_TEXT_TO_PROMPT_MAX_TOKENS = 256
OPENAI_SUMMARIZE_SYSTEM_TEXT = (
    "Act as a human, that summarizes given text to be as short as possible.\n"
)

OPENAI_PROMPT_SYSTEM_TEXT = (
    "Generate a prompt for image generator based on text in variable called 'text':\n"
    "Two examples of good prompt:\n"
    "'prompt': 'Imagine a stunning woman standing in a garden surrounded by a riot of colorful blooms, with the sun setting in the distance. Use soft lighting to capture the warmth of the golden hour and the subtle nuances of her expression.'\n\n"
    "'prompt':  'a portrait of an old coal miner in 19th century, beautiful painting with highly detailed face by greg rutkowski and magali villanueve'\n\n"
    "Two examples of bad prompt:\n"
    "'prompt':  'Worldwide Wi-Fi Technology Forecast is a report that is likely to be a document consisting of text and graphs. The cover page may have the title in bold letters with a background color that is eye-catching. The report may be bound with a spiral or a perfect binding. The pages may be white with black text and colored graphs. The graphs may show the growth of Wi-Fi technology in different regions of the world. The report may be placed on a desk or a shelf in an office.'\n\n"
    "'prompt': 'SaaSPath 2023 is a list of various application categories including Banner Books, CPQ, Digital Commerce, Employee Experience, Facility Management, Field Service Management, PIM/PXM, and Procurement. It also includes information on adoption, deployment models, budget plans, replacement cycle timing, purchasing preferences, and attitudes towards SaaS buying channels. The report provides insights on packaging, pricing options, vendor reviews, ratings, spend, and advocacy scores for functional application markets.'\n\n"
    "If it's for paper or a study, generate prompt for some real physical object, that the study is about.\n\n"
    "the text must be short and to the point\n"
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_ENGINE = os.getenv("OPENAI_API_ENGINE")
OPENAI_CUSTOM_DOMAIN = os.getenv("OPENAI_CUSTOM_DOMAIN")

# Stable Diffusion
STABLE_DIFFUSION_MODEL_PATH = "stabilityai/stable-diffusion-2-1"

# DreamStudio API - Stable Diffusion
STABILITY_ENGINE = "stable-diffusion-512-v2-1"
STABILITY_GENERATION_URL = f"https://api.stability.ai/v1/generation/{STABILITY_ENGINE}/text-to-image"

# Train settings
TRAIN_TEST_SPLIT_RATIO = 0.9
BATCH_SIZE = 1

DATASETS = {
    "bbc": "Dzeniks/BBC-article"
}

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