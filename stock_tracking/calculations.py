import json
import sys
import os
import requests
from tabulate import tabulate
from collections import defaultdict, Counter
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from logger import stock_logger, logs_logger, important_logger


seed_names = [
    "Carrot",
    "Strawberry",
    "Blueberry",
    "Orange Tulip",
    "Tomato",
    "Daffodil",
    "Watermelon",
    "Pumpkin",
    "Apple",
    "Bamboo",
    "Coconut",
    "Cactus",
    "Dragon Fruit",
    "Mango",
    "Grape",
    "Mushroom",
    "Pepper",
    "Cacao",
    "Beanstalk",
    "Ember Lily",
    "Sugar Apple",
    "Burning Bud",
    "Giant Pinecone",
    "Elder Strawberry"
]

gear_names = [
    "Watering Can",
    "Trading Ticket",
    "Trowel",
    "Recall Wrench",
    "Basic Sprinkler",
    "Advanced Sprinkler",
    "Medium Toy",
    "Medium Treat",
    "Godly Sprinkler",
    "Magnifying Glass",
    "Master Sprinkler",
    "Cleaning Spray",
    "Favorite Tool",
    "Harvest Tool",
    "Friendship Pot",
    "Grandmaster Sprinkler",
    "Levelup Lollipop"
]


egg_names = [
    "Common Egg",
    "Common Summer Egg",
    "Rare Summer Egg",
    "Mythical Egg",
    "Paradise Egg",
    "Bug Egg",
]

stock_history = {}

def get_daily_stock_folder():
    """Get daily stock folder (don't create it)"""
    yesterday = datetime.now() - timedelta(days=1)
    today = yesterday.strftime("%Y-%m-%d")
    stocks_dir = os.path.join(os.path.dirname(__file__), "stocks")
    daily_dir = os.path.join(stocks_dir, today)
    
    return daily_dir

def load_stock_files():
    """Load stock data from JSON files"""
    global stock_history
    daily_dir = get_daily_stock_folder()
    
    # Check if daily folder exists first
    if not os.path.exists(daily_dir):
        logs_logger.error(f"Daily stock folder not found: {daily_dir}")
        stock_history = {"seeds": {}, "gear": {}, "eggs": {}}
        return
    
    stock_files = {
        "seeds": "seeds_stock.txt",
        "gear": "gear_stock.txt",
        "eggs": "eggs_stock.txt"
    }
    
    missing_files = []
    
    for category, filename in stock_files.items():
        filepath = os.path.join(daily_dir, filename)
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()

                    merged_data = {}
                    if content:
                        json_objects = []
                        current_json = ""
                        brace_count = 0
                        
                        for line in content.split('\n'):
                            line = line.strip()
                            if line:
                                current_json += line + '\n'
                                brace_count += line.count('{') - line.count('}')
                                
                                if brace_count == 0 and current_json.strip():
                                    try:
                                        obj = json.loads(current_json.strip())
                                        json_objects.append(obj)
                                    except json.JSONDecodeError:
                                        pass
                                    current_json = ""
                        
                        # Merge all objects
                        for obj in json_objects:
                            merged_data.update(obj)
                    
                    stock_history[category] = merged_data
                stock_logger.info(f"Loaded {category} stock data: {len(merged_data)} timestamps")
            else:
                stock_history[category] = {}
                missing_files.append(filename)
        except Exception as e:
            stock_history[category] = {}
            logs_logger.error(f"Error loading {category} stock: {e}")

    if missing_files:
        logs_logger.error(f"Stock files not found: {', '.join(missing_files)}")

def get_todays_items():
    """Get items that appeared in shop yesterday with total quantities"""
    yesterday = datetime.now() - timedelta(days=1)
    today = yesterday.strftime("%Y-%m-%d")
    daily_stats = {"seeds": {}, "gear": {}, "eggs": {}}
    
    for category in ["seeds", "gear", "eggs"]:
        if category not in stock_history:
            continue
            
        item_quantities = defaultdict(int)

        for timestamp, items_array in stock_history[category].items():
            try:
                ts_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).strftime("%Y-%m-%d")
                if ts_date == today:
                    for item in items_array:
                        if isinstance(item, dict) and "name" in item and "quantity" in item:
                            item_name = item["name"]
                            quantity = item["quantity"]
                            item_quantities[item_name] += quantity
            except (ValueError, AttributeError, TypeError):
                continue
        
        daily_stats[category] = dict(item_quantities)
    
    return daily_stats

def write_daily_report_to_files():
    """Write daily report to the end of each stock file"""
    daily_dir = get_daily_stock_folder()
    
    if not os.path.exists(daily_dir):
        return
    
    yesterday = datetime.now() - timedelta(days=1)
    today_str = yesterday.strftime('%d.%m.%Y')
    daily_stats = get_todays_items()

    stock_files = ["seeds_stock.txt", "gear_stock.txt", "eggs_stock.txt"]
    existing_files = []
    
    for filename in stock_files:
        filepath = os.path.join(daily_dir, filename)
        if os.path.exists(filepath):
            existing_files.append(filename)
    
    if not existing_files:
        return

    for filename in existing_files:
        filepath = os.path.join(daily_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                if f"DAILY {filename.split('_')[0].upper()} REPORT - {today_str}" in content:
                    logs_logger.info(f"Daily report already exists in {filename}")
                    return
        except Exception:
            pass
    
    seeds_report = [
        f"\n\n# DAILY SEEDS REPORT - {today_str}",
        "# " + "=" * 40,
        "\n# 🌱 SEEDS SUMMARY:"
    ]
    
    if not daily_stats["seeds"]:
        seeds_report.append("#   No seeds appeared yesterday")
    else:
        for item_name, total_quantity in sorted(daily_stats["seeds"].items(), key=lambda x: x[1], reverse=True):
            seeds_report.append(f"#   {item_name:<25} x{total_quantity}")
        
        total_quantity = sum(daily_stats["seeds"].values())
        unique_items = len(daily_stats["seeds"])
        seeds_report.append(f"#   📊 Total: {unique_items} unique items, {total_quantity} total quantity")
    
    seeds_report.append("# " + "=" * 40)

    gear_report = [
        f"\n\n# DAILY GEAR REPORT - {today_str}",
        "# " + "=" * 40,
        "\n# 🔧 GEAR SUMMARY:"
    ]
    
    if not daily_stats["gear"]:
        gear_report.append("#   No gear appeared yesterday")
    else:
        for item_name, total_quantity in sorted(daily_stats["gear"].items(), key=lambda x: x[1], reverse=True):
            gear_report.append(f"#   {item_name:<25} x{total_quantity}")
        
        total_quantity = sum(daily_stats["gear"].values())
        unique_items = len(daily_stats["gear"])
        gear_report.append(f"#   📊 Total: {unique_items} unique items, {total_quantity} total quantity")
    
    gear_report.append("# " + "=" * 40)
    
    eggs_report = [
        f"\n\n# DAILY EGGS REPORT - {today_str}",
        "# " + "=" * 40,
        "\n# 🥚 EGGS SUMMARY:"
    ]
    
    if not daily_stats["eggs"]:
        eggs_report.append("#   No eggs appeared yesterday")
    else:
        for item_name, total_quantity in sorted(daily_stats["eggs"].items(), key=lambda x: x[1], reverse=True):
            eggs_report.append(f"#   {item_name:<25} x{total_quantity}")
        
        total_quantity = sum(daily_stats["eggs"].values())
        unique_items = len(daily_stats["eggs"])
        eggs_report.append(f"#   📊 Total: {unique_items} unique items, {total_quantity} total quantity")
    
    eggs_report.append("# " + "=" * 40)

    reports = {
        "seeds_stock.txt": seeds_report,
        "gear_stock.txt": gear_report,
        "eggs_stock.txt": eggs_report
    }
    
    reports_written = 0
    for filename, report_lines in reports.items():
        filepath = os.path.join(daily_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'a', encoding='utf-8') as f:
                    f.write('\n'.join(report_lines))
                reports_written += 1
            except Exception as e:
                logs_logger.error(f"Error writing daily report to {filename}: {e}")
    
    if reports_written > 0:
        logs_logger.info(f"Daily reports written to {reports_written} files")


def create_daily_statistics():
    """Create and display daily statistics with nice formatting"""
    daily_stats = get_todays_items()
    
    # Check if there's any data to show
    has_data = any(daily_stats[category] for category in daily_stats)
    
    if not has_data:
        logs_logger.info("No stock data available for yesterday - skipping statistics display")
        return
    
    yesterday = datetime.now() - timedelta(days=1)
    today_str = yesterday.strftime('%d.%m.%Y')
    print(f"\n📋 DAILY SHOP STATISTICS - {today_str}")
    print("=" * 60)
    
    # Seeds section
    print(f"\n🌱 SEEDS IN SHOP:")
    print("-" * 40)
    if not daily_stats["seeds"]:
        print("   No seeds appeared yesterday")
    else:
        for item_name, total_quantity in sorted(daily_stats["seeds"].items(), key=lambda x: x[1], reverse=True):
            print(f"   {item_name:<25} x{total_quantity}")
        
        total_quantity = sum(daily_stats["seeds"].values())
        unique_items = len(daily_stats["seeds"])
        print(f"\n   📊 Total: {unique_items} unique items, {total_quantity} total quantity")
    
    # Gear section
    print(f"\n🔧 GEAR IN SHOP:")
    print("-" * 40)
    if not daily_stats["gear"]:
        print("   No gear appeared yesterday")
    else:
        for item_name, total_quantity in sorted(daily_stats["gear"].items(), key=lambda x: x[1], reverse=True):
            print(f"   {item_name:<25} x{total_quantity}")
        
        total_quantity = sum(daily_stats["gear"].values())
        unique_items = len(daily_stats["gear"])
        print(f"\n   📊 Total: {unique_items} unique items, {total_quantity} total quantity")
    
    # Eggs section
    print(f"\n🥚 EGGS IN SHOP:")
    print("-" * 40)
    if not daily_stats["eggs"]:
        print("   No eggs appeared yesterday")
    else:
        for item_name, total_quantity in sorted(daily_stats["eggs"].items(), key=lambda x: x[1], reverse=True):
            print(f"   {item_name:<25} x{total_quantity}")
        
        total_quantity = sum(daily_stats["eggs"].values())
        unique_items = len(daily_stats["eggs"])
        print(f"\n   📊 Total: {unique_items} unique items, {total_quantity} total quantity")
    
    print("\n" + "=" * 60)

    write_daily_report_to_files()

def schedule_daily_stats():
    load_stock_files()
    create_daily_statistics()
