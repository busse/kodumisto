import random

# List of haikus
haikus = [
    "Autumn moonlight,\na worm digs silently\ninto the chestnut\n",
    "Winter solitude -\nin a world of one color\nthe sound of wind\n",
    "Cherry blossoms bloom,\nSoftly falling on the ground;\nSpringtime has arrived.\n",
    "Green grass, tall tree, birds\nSing sweetly as flowers bloom\nSummer is now here\n"
]

# Generate random index to select a haiku
random_index = random.randint(0, 3)

# Print the selected haiku
print(haikus[random_index])