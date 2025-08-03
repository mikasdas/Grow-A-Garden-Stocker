# 🌱 Grow a Garden - Stock Notifyer

This project monitors the stock of seeds, gear, and eggs in the Roblox game **Grow a Garden** via API.  
It logs stock data over time, identifies important items, and sends notifications via [`ntfy`](https://ntfy.sh).


## 🚀 Features

- 🔔 Notifies you when **important items** appear
- 🧾 Logs item stock every few minutes
- 📊 Generates **daily summaries** of shop inventory
- 🌐 Easy to configure with `settings.py`

---

## 🖥️ Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/GAG-Stock-Notifyer.git
```


### 2. Install Dependencies
```bash
cd GAG-Stock-Notifyer
pip install -r requirements.txt
```


### 3. Configure `settings.py`
Adjust items that should trigger a notification.

Just copy the item you want from the reference lists at the bottom of this README and paste it into the appropriate section in your `settings.py` file using the following structure:

```python
important_seeds = [
    "Carrot",
    "Dragon Fruit",
    "Cacao"
]

important_gear = [
    "Trowel",
    "Recall Wrench"
]

important_egg = [
    "Rare Summer Egg",
    "Mythical Egg"
]
```

Also set your `server_url` and `ntfy_topic` in `settings.py`.


### 4. Start the Program
```bash
python GAG_info_collector.py
```

---

## 🔌 API Endpoint

I use the [GAGAPI from @Liriosha](https://github.com/Liriosha/GAGAPI).

If you want to use a different API, just replace the path `/seeds`, `/gear`, and `/eggs` in the requests like this:

```python
seeds = requests.get(f"{server_url}/seeds").json()
```


## 🔔 Notifications

This project uses [ntfy.sh](https://ntfy.sh) to send push notifications to your devices (browser, phone, etc.).


## 📲 How to Subscribe to a Topic

1. Download or open ntfy on your device:
   - 🌐 Web: https://ntfy.sh/app
   - 📱 iOS: https://apps.apple.com/us/app/ntfy/id1625396347
   - 📱 Android: https://play.google.com/store/apps/details?id=io.heckel.ntfy
   - 🐧 F-Droid: https://f-droid.org/en/packages/io.heckel.ntfy/
2. Allow notifications.
3. Tap ➕ and enter a topic name you want to subscribe to.  
   ➤ Tip: Use a strong, unique topic name if you want to avoid spam.
4. You're now ready to receive notifications!


## 📡 Subscribe to My Alerts

If you want to receive Grow a Garden notifications **without running the program yourself**, just subscribe to my public topic (running 24/7 – if my server is up):

```bash
GAG_important_items75921
```

> ⚠️ **Caution:** Anyone can send messages to public ntfy topics. It’s possible that this topic may be abused.

<details>
<summary>📬 Items that trigger notifications in my topic</summary>

### 🌱 Seeds
- Pepper  
- Cacao  
- Beanstalk  
- Ember Lily  
- Sugar Apple  
- Burning Bud  
- Giant Pinecone  
- Elder Strawberry  

### 🔧 Gear
- Godly Sprinkler  
- Master Sprinkler  
- Grandmaster Sprinkler  
- Levelup Lollipop  

### 🥚 Eggs
- Rare Summer Egg  
- Mythical Egg  
- Bug Egg  

</details>


## 🗃️ File Structure

- `GAG_info_collector.py` – main runner and scheduler  
- `logger.py` – custom logger with color and file output  
- `stock_tracking/calculations.py` – daily stock statistics  
- `settings.py` – your configuration file  
- `data/logs/` – folder for logs  
- `stock_tracking/stocks/` – daily stock snapshots  

---

## 🛠️ Planned Features

- 🧩 Web overlay for live display  
- 💰 Pet/plant sell price calculator  
- 🌦️ Weather alert system  
- 🤖 Discord bot integration  

Have ideas or found bugs? [Open an issue](https://github.com/your-username/GAG-Stock-Notifyer/issues) or contact me!


## 📜 License

MIT – do whatever you want, just keep attribution.


## 📋 All Items

<details>
<summary>🌱 Seeds</summary>

- Carrot  
- Strawberry  
- Blueberry  
- Orange Tulip  
- Tomato  
- Daffodil  
- Watermelon  
- Pumpkin  
- Apple  
- Bamboo  
- Coconut  
- Cactus  
- Dragon Fruit  
- Mango  
- Grape  
- Mushroom  
- Pepper  
- Cacao  
- Beanstalk  
- Ember Lily  
- Sugar Apple  
- Burning Bud  
- Giant Pinecone  
- Elder Strawberry

</details>

<details>
<summary>🔧 Gear</summary>

- Watering Can  
- Trading Ticket  
- Trowel  
- Recall Wrench  
- Basic Sprinkler  
- Advanced Sprinkler  
- Medium Toy  
- Medium Treat  
- Godly Sprinkler  
- Magnifying Glass  
- Master Sprinkler  
- Cleaning Spray  
- Favorite Tool  
- Harvest Tool  
- Friendship Pot  
- Grandmaster Sprinkler  
- Levelup Lollipop

</details>

<details>
<summary>🥚 Eggs</summary>

- Common Egg  
- Common Summer Egg  
- Rare Summer Egg  
- Mythical Egg  
- Paradise Egg  
- Bug Egg

</details>
