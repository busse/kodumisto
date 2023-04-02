import random

# Jokes in English
english_jokes = [
    "Why did the fish blush? Because it saw the ocean's bottom!",
    "What is a fish's favorite game? Name that tuna!",
    "How do you communicate with a fish? Drop it a line!",
    "Why do fish swim in salt water? Because pepper water makes them sneeze!",
    "What is a fish's favorite instrument? A bass guitar!"
]

# Jokes in Icelandic
icelandic_jokes = [
    "Hvað segir fiskur í þurrfiskihúsinu? Ég missi þig í varinu!",
    "Hvað gerir fiskur á hádeginu? Hann fer í máltíð.",
    "Hvað gerir feitur fiskur á grillinu? Han setur sig og segir: Ég erfði gramman minn frá faðir mínum.",
    "Hvað segja litlir fiskar þegar þeir mæta stórum fiski á hafsbotninum? Gott að sjá ykkur!",
    "Hvað segir sammeti fiskur við dauðann fisk? Takk, takk, takk fyrir litina."
]

# Randomly choose a joke
english = random.choice(english_jokes)
icelandic = random.choice(icelandic_jokes)
if random.random() < 0.5:
    print(english)
else:
    print(icelandic)