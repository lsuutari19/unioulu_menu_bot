"""
Gives a random emoji for nicer markdown
"""

import random


def random_emoji():
    """
    Function for getting a random emoji, used for the markdown message
    """
    emojis = [
        "😀",
        "😳",
        "😵",
        "😡",
        "😷",
        "🤒",
        "🤕",
        "🤠",
        "🤖",
        "💻",
        "🎉",
        "🎈",
        "✨",
        "❤️",
        "🌟",
        "🌈",
        "🐶",
        "🐱",
        "🦁",
        "🐯",
        "🐻",
        "🐼",
        "🦄",
        "🐔",
        "🐢",
        "🦊",
        "🌻",
        "🌺",
        "🌸",
        "🌼",
        "🍀",
        "🍉",
        "🍕",
        "🍔",
        "🌭",
        "🍟",
        "🍦",
        "🍰",
        "🎂",
        "🍩",
        "🥨",
        "🍿",
        "🌮",
        "🥗",
        "🌽",
        "🍇",
        "🍊",
        "🍏",
        "🍌",
        "🥥",
        "🎈",
        "🎉",
        "🎊",
        "🎵",
        "🎶",
        "🔔",
        "📚",
        "🎮",
        "💼",
        "📸",
        "✈️",
        "⛷️",
        "🏖️",
    ]
    return random.choice(emojis)
