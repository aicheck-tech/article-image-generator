import os

from dotenv import load_dotenv

from textProcessing import TextProcessing

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_ENGINE = os.getenv("OPENAI_API_ENGINE")
OPENAI_CUSTOM_DOMAIN = os.getenv("OPENAI_CUSTOM_DOMAIN")

testText = """Worldwide Home Video Game Console Market Shares, 2022: Xbox Shined Digitally While Nintendo Switch Slid
4 500 $
Lewis Ward
This IDC study assesses and contrasts the major home video game console platforms from several market share angles in the 2013–2022 period, with an emphasis on the 2021-2022 dynamic. Global market shares for Switch, Wii U, Wii, PlayStation 5, PlayStation 4, PlayStation 3, Xbox Series X/S, Xbox One, and Xbox 360 systems are tracked annually in several dimensions in this study. The impact of digital-only microconsoles, gaming-capable streaming media players, and smart TVs that support gaming services are briefly examined as well. "Given the smaller size of Microsoft's Xbox platform install base, it …
kvě 2023 | Doc #US49472823 | Market Share
"""

textProcessing = TextProcessing(
    testText, OPENAI_API_KEY, OPENAI_API_ENGINE, OPENAI_CUSTOM_DOMAIN
)

print(textProcessing.stable_diffusion_prompt_generator([
    "realistic",
    # "50mm photography",
    "8k",
    "octane render",
    "cinematic",
    "trending on artstation",
    # "movie concept art",
    "cinematic composition"
]))
