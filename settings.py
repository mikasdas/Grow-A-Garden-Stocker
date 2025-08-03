# 🌐 API endpoint
api_url = ""


# 🔔 Ntfy topic for notification

ntfy_topic = ""


# ✅ Important items that should trigger a notification

important_seeds = [
    # 🌱 Seeds
    "Ember Lily",
    "Sugar Apple",
    "Burning Bud",
    "Giant Pinecone",
    "Elder Strawberry"
]

important_gear = [
    # 🔧 Gear
    "Godly Sprinkler", 
    "Master Sprinkler",
    "Grandmaster Sprinkler",
    "Levelup Lollipop"
]

important_egg = [
    # 🥚 Eggs
    "Mythical Egg", 
    "Bug Egg"
]

# ⏰ Time intervals for requests
# These sets define the minutes at which requests will be made.
# For example, if you want to make requests every 5 minutes, you can use {0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55}.
gear_seeds_minutes = {0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55}
eggs_minutes = {0, 30}