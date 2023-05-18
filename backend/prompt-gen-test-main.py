# import logging

# from textProcessing import text_processing

# if __name__ == '__main__':
#     logging.basicConfig(
#         format='%(asctime)s %(levelname)s %(message)s', 
#         level=logging.INFO,
#         datefmt='%Y-%m-%d %H:%M:%S',
#         # filename="prompt-gen-test.log",
#         # filemode="w"
#         )

# test_text = """Ukraine says it shot down hypersonic missiles amid an "exceptionally dense" barrage fired at Kyiv on Tuesday.

# Kyiv said air defences intercepted six Kinzhal hypersonic missiles, which Russia has claimed can overcome all existing air defence systems.

# They were among 18 missiles of different types fired at the city in a short space of time, officials said.

# Russia denies its Kinzhals were stopped and said one destroyed a US-supplied Patriot air defence system.

# Ukraine declined to comment. The BBC cannot independently verify the claims made by either country.

# Russia has stepped up its air campaign in recent weeks - bombarding the Ukrainian capital eight times so far this month - ahead of an expected Ukrainian offensive.

# On Tuesday evening Russian Defence Minister Sergei Shoigu said Moscow had not fired as many of the Kinzhal missiles as Kyiv had claimed to have shot down.

# However if Ukraine's claims are true, Moscow will be feeling frustrated that the finest weapons from its missile fleet are now able to be intercepted. This is in large part due to the arrival of modern Western defence systems, including Patriots.

# Russia continues to insist that the missiles, which it says can travel at more than 11,000kmh (7,000mph), cannot be destroyed by any of the world's air defence systems.

# The Kinzhal, or "dagger", is an air-launched ballistic missile. Most ballistic missiles reach hypersonic speed - five times the speed of sound, or just over 6,000 kmh - at some point during their flight.

# Kyiv said it shot down a Kinzhal for the first time last week.

# In the past few days, President Volodymyr Zelensky has been on a European tour in which he has been promised several billion dollars' worth of military equipment by Western allies, including UK Prime Minister Rishi Sunak and President Emmanuel Macron of France.
# """
# text_processor = text_processing()
# print(text_processor.text_to_tagged_prompt(
#     test_text,
#     [
#     "realistic",
#     # "50mm photography",
#     "8k",
#     "octane render",
#     "cinematic",
#     "trending on artstation",
#     # "movie concept art",
#     "cinematic composition"
#     ]
# ))

tags = [
    "realistic",
    "50mm photography",
    "8k",
    "octane render",
    "cinematic",
    "trending on artstation",
    # "movie concept art",
    "cinematic composition"
    ]

XTEXT = (
        "Generate a prompt for image generator based on text in variable called 'text':\n"
        "Two examples of good prompt:\n"
        "'prompt': 'Imagine a stunning woman standing in a garden surrounded by a riot of colorful blooms, with the sun setting in the distance. Use soft lighting to capture the warmth of the golden hour and the subtle nuances of her expression.'\n\n"
        "'prompt':  'a portrait of an old coal miner in 19th century, beautiful painting with highly detailed face by greg rutkowski and magali villanueve'\n\n"
        "Two examples of bad prompt:\n"
        "'prompt':  'Worldwide Wi-Fi Technology Forecast is a report that is likely to be a document consisting of text and graphs. The cover page may have the title in bold letters with a background color that is eye-catching. The report may be bound with a spiral or a perfect binding. The pages may be white with black text and colored graphs. The graphs may show the growth of Wi-Fi technology in different regions of the world. The report may be placed on a desk or a shelf in an office.'\n\n"
        "'prompt': 'SaaSPath 2023 is a list of various application categories including Banner Books, CPQ, Digital Commerce, Employee Experience, Facility Management, Field Service Management, PIM/PXM, and Procurement. It also includes information on adoption, deployment models, budget plans, replacement cycle timing, purchasing preferences, and attitudes towards SaaS buying channels. The report provides insights on packaging, pricing options, vendor reviews, ratings, spend, and advocacy scores for functional application markets.'\n\n"
        "If it's for paper or a study, generate prompt for some real physical object, that the study is about.\n\n"
    )

prompt = (
        XTEXT +
        (
            f"The design should be {', '.join(tags)}\n\n"
            "Annotate it as:\n"
            "'prompt': <the prompt>"
        )
    )
print(prompt)