import logging

from textProcessing import text_processing

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s', 
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        # filename="prompt-gen-test.log",
        # filemode="w"
        )

test_text = """Ukraine says it shot down hypersonic missiles amid an "exceptionally dense" barrage fired at Kyiv on Tuesday.

Kyiv said air defences intercepted six Kinzhal hypersonic missiles, which Russia has claimed can overcome all existing air defence systems.

They were among 18 missiles of different types fired at the city in a short space of time, officials said.

Russia denies its Kinzhals were stopped and said one destroyed a US-supplied Patriot air defence system.

Ukraine declined to comment. The BBC cannot independently verify the claims made by either country.

Russia has stepped up its air campaign in recent weeks - bombarding the Ukrainian capital eight times so far this month - ahead of an expected Ukrainian offensive.

On Tuesday evening Russian Defence Minister Sergei Shoigu said Moscow had not fired as many of the Kinzhal missiles as Kyiv had claimed to have shot down.

However if Ukraine's claims are true, Moscow will be feeling frustrated that the finest weapons from its missile fleet are now able to be intercepted. This is in large part due to the arrival of modern Western defence systems, including Patriots.

Russia continues to insist that the missiles, which it says can travel at more than 11,000kmh (7,000mph), cannot be destroyed by any of the world's air defence systems.

The Kinzhal, or "dagger", is an air-launched ballistic missile. Most ballistic missiles reach hypersonic speed - five times the speed of sound, or just over 6,000 kmh - at some point during their flight.

Kyiv said it shot down a Kinzhal for the first time last week.

In the past few days, President Volodymyr Zelensky has been on a European tour in which he has been promised several billion dollars' worth of military equipment by Western allies, including UK Prime Minister Rishi Sunak and President Emmanuel Macron of France.
"""
text_processor = text_processing()
print(text_processor.text_to_tagged_prompt(
    test_text,
    [
    "realistic",
    # "50mm photography",
    "8k",
    "octane render",
    "cinematic",
    "trending on artstation",
    # "movie concept art",
    "cinematic composition"
    ]
))
