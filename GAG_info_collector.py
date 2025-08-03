from email.mime import message
import schedule
import os
import sys
import time
import logging
import requests
import datetime
import json
from tabulate import tabulate
from typing import Optional, List, Dict, Any

# Add parent directory to path and import local logger
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from logger import stock_logger, logs_logger, important_logger

# Import settings from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import settings

api_url = settings.api_url
important_seeds = settings.important_seeds
important_gear = settings.important_gear
important_egg = settings.important_egg

# Use schedule settings from settings module
gear_seeds_minutes = settings.gear_seeds_minutes
eggs_minutes = settings.eggs_minutes


def is_important(item_list, important_items, item_type="Item"):
    for item in item_list:
        name = item.get("name", "") if isinstance(item, dict) else str(item)
        if name in important_items:
            important_logger.info(f"🔔 Important {item_type} in Stock: {name}\n")
            send_notification(
                message=f"🔔 Important {item_type} in Stock: {name}",
                title=f"Important {item_type} Alert",
                priority=3,
                tags="important,stock",
            )

def send_notification(
    message: str,
    title: Optional[str] = None,
    priority: Optional[int] = None,
    tags: Optional[str] = None,
    click_url: Optional[str] = None,
    attach: Optional[List[str]] = None,
    actions: Optional[List[Dict[str, Any]]] = None,
    custom_headers: Optional[Dict[str, str]] = None
) -> None:
    """
    Sends an ntfy notification to the specified topic with advanced options.

    Parameters:
      - message: The message text to send in the body.
      - title: (Optional) Title of the notification.
      - priority: (Optional) Priority of the notification (1 to 5).
      - tags: (Optional) List of tags or comma-separated string; known tags will be converted to emojis.
      - click_url: (Optional) URL to open when the notification is clicked.
      - attach: (Optional) URL(s) of attachments; can be a string or a list of strings.
      - actions: (Optional) List of actions as dictionaries.
      - custom_headers: (Optional) Dictionary of additional HTTP headers.
    """
    url = f"https://ntfy.sh/{settings.ntfy_topic}"
    headers = {}

    if title:
        headers["Title"] = title
    if priority:
        headers["Priority"] = str(priority)
    if click_url:
        headers["Click"] = click_url
    if attach:
        if isinstance(attach, str):
            attach = [attach]
        headers["Attach"] = ", ".join(attach)
    if actions:
        headers["Actions"] = json.dumps(actions)

    """
    Emojis

    "warning": "⚠️",
    "skull": "💀",
    "fire": "🔥",
    "info": "ℹ️",
    "heart": "❤️",
    "star": "⭐",

    """

    if tags:
        headers["Tags"] = tags

    if custom_headers:
        headers.update(custom_headers)

    try:
        response = requests.post(url, headers=headers, data=message.encode('utf-8'))
        if response.status_code == 200:
            logging.info("Notification sent successfully!")
        else:
            logging.warning(f"Error sending notification: {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"Error sending notification: {e}")


def validate_response(data, data_type):
    """Validate API response format and check for errors"""
    # Check for rate limit error
    if isinstance(data, dict) and "error" in data:
        if "Rate limit exceeded" in data["error"]:
            logs_logger.error(f"❌ API Rate limit exceeded: {data['error']}")
            return False
        else:
            logs_logger.error(f"❌ API Error for {data_type}: {data['error']}")
            return False
    
    if not isinstance(data, list):
        logs_logger.error(f"❌ Invalid {data_type} response: Expected list, got {type(data)}")
        return False
    
    for item in data:
        if not isinstance(item, dict):
            logs_logger.error(f"❌ Invalid {data_type} item: Expected dict, got {type(item)}")
            return False
        if 'name' not in item or 'quantity' not in item:
            logs_logger.error(f"❌ Invalid {data_type} item: Missing 'name' or 'quantity' field")
            return False
    
    return True

def get_daily_stock_folder():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    stocks_dir = os.path.join(os.path.dirname(__file__), "stock_tracking", "stocks")
    daily_dir = os.path.join(stocks_dir, today)
    
    # Create directories if they don't exist
    os.makedirs(daily_dir, exist_ok=True)
    
    return daily_dir


def fetch_seeds():
    try:
        logs_logger.debug("⏱️ Requesting Seed Stock...")
        seeds = requests.get(f"{api_url}/seeds").json()
        
        if not validate_response(seeds, "seeds"):
            return
            
        seed_list = "\n".join([f"{item['name']:<20} x{item['quantity']}" for item in seeds])
        stock_logger.info(f"Seeds that are in stock:\n{seed_list}")

        # Write the data to daily folder
        daily_dir = get_daily_stock_folder()
        timestamp = datetime.datetime.now().isoformat()
        data_to_write = {
            timestamp: [
                {
                    "name": item["name"],
                    "quantity": item["quantity"]
                }
                for item in seeds
            ]
        }
        filepath = os.path.join(daily_dir, 'seeds_stock.txt')
        with open(filepath, 'a', encoding="utf-8") as f:
            f.write(json.dumps(data_to_write, indent=2, sort_keys=True, ensure_ascii=False) + "\n")

        # Check for important seeds
        is_important(seeds, important_seeds, item_type="Seed")
    except requests.exceptions.RequestException as e:
        logs_logger.error(f"Error fetching seeds: {e}")
    except Exception as e:
        logs_logger.error(f"Unexpected error fetching seeds: {e}")


def fetch_gear():
    try:
        logs_logger.debug("⏱️ Requesting Gear Stock ...")
        gear = requests.get(f"{api_url}/gear").json()
        
        if not validate_response(gear, "gear"):
            return
            
        gear_list = "\n".join([f"{item['name']:<20} x{item['quantity']}" for item in gear])
        stock_logger.info(f"Gear that is in stock:\n{gear_list}")
        
        # Write the data to daily folder
        daily_dir = get_daily_stock_folder()
        timestamp = datetime.datetime.now().isoformat()
        data_to_write = {
            timestamp: [
                {
                    "name": item["name"],
                    "quantity": item["quantity"]
                }
                for item in gear
            ]
        }
        filepath = os.path.join(daily_dir, 'gear_stock.txt')
        with open(filepath, 'a', encoding="utf-8") as f:
            f.write(json.dumps(data_to_write, indent=2, sort_keys=True, ensure_ascii=False) + "\n")

        # Check for important gear
        is_important(gear, important_gear, item_type="Gear")
    except requests.exceptions.RequestException as e:
        logs_logger.error(f"Error fetching gear: {e}")
    except Exception as e:
        logs_logger.error(f"Unexpected error fetching gear: {e}")


def fetch_eggs():
    try:
        logs_logger.debug("⏱️ Requesting Egg Stock...")
        eggs = requests.get(f"{api_url}/eggs").json()
        
        if not validate_response(eggs, "eggs"):
            return
            
        egg_list = "\n".join([f"{item['name']:<20} x{item['quantity']}" for item in eggs])
        stock_logger.info(f"Eggs that are in stock:\n{egg_list}")

        # Write the data to daily folder
        daily_dir = get_daily_stock_folder()
        timestamp = datetime.datetime.now().isoformat()
        data_to_write = {
            timestamp: [
                {
                    "name": item["name"],
                    "quantity": item["quantity"]
                }
                for item in eggs
            ]
        }
        filepath = os.path.join(daily_dir, 'eggs_stock.txt')
        with open(filepath, 'a', encoding="utf-8") as f:
            f.write(json.dumps(data_to_write, indent=2, sort_keys=True, ensure_ascii=False) + "\n")

        # Check for important eggs
        is_important(eggs, important_egg, item_type="Egg")
    except requests.exceptions.RequestException as e:
        logs_logger.error(f"Error fetching eggs: {e}")
    except Exception as e:
        logs_logger.error(f"Unexpected error fetching eggs: {e}")


last_gear_seeds_run = -1
last_eggs_run = -1


def daily_statistics_job():
    """Run daily statistics at midnight"""
    try:
        import stock_tracking.calculations as calc
        calc.load_stock_files()
        calc.create_daily_statistics()
    except Exception as e:
        logs_logger.error(f"Error running daily statistics: {e}")

def main():
    global last_gear_seeds_run, last_eggs_run
    
    daily_time = getattr(settings, 'daily_stats_time', '00:01')
    schedule.every().day.at(daily_time).do(daily_statistics_job)

    logs_logger.info(f"API URL: {api_url}")
    logs_logger.info(f"Gear/Seeds schedule: {sorted(gear_seeds_minutes)}")
    logs_logger.info(f"Eggs schedule: {sorted(eggs_minutes)}")
    logs_logger.info(f"Daily statistics scheduled at: {daily_time}")
    
    while True:
        # Run scheduled jobs
        schedule.run_pending()
        
        now = datetime.datetime.now()
        minute = now.minute

        if minute in gear_seeds_minutes and minute != last_gear_seeds_run:
            time.sleep(30)
            fetch_seeds()
            fetch_gear()
            last_gear_seeds_run = minute

        if minute in eggs_minutes and minute != last_eggs_run:
            time.sleep(10)
            fetch_eggs()
            last_eggs_run = minute

        time.sleep(10)

if __name__ == "__main__":
    logs_logger.info("Starting GAG info collector...")
    from stock_tracking.calculations import schedule_daily_stats
    main()