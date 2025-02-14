import requests
import csv
import logging
import time
import re
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Настройка логирования
handler = RotatingFileHandler("vk_scraper.log", maxBytes=5 * 1024 * 1024, backupCount=3)
logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


access_token = "access_token"
version = "version"

# List of group IDs
group_ids = []


def determine_content_type(post):
    """
    Определение типа контента в посте в улучшенном варианте:
    - attachments:<type1>[,<type2>,...]_text[_with_link]
    - text_only / text_with_link
    - attachments:<type1>[,<type2>,...]_no_text
    - empty
    """
    text = str(post.get("text", "")).strip()
    attachments = post.get("attachments", [])

    url_pattern = re.compile(r"https?://[^\s]+")
    has_link = bool(url_pattern.search(text))

    content_types = {att.get("type", "unknown") for att in attachments if isinstance(att, dict)}

    if content_types:
        base = "attachments:" + ",".join(sorted(content_types))
        if text:
            if has_link:
                return base + "_text_with_link"
            else:
                return base + "_text"
        else:
            return base + "_no_text"
    else:
        if text:
            if has_link:
                return "text_with_link"
            else:
                return "text_only"
        else:
            return "empty"

def fetch_posts(group_id, token, api_version, total_posts=500, pause=2):

    collected_posts = []
    offset = 0

    while len(collected_posts) < total_posts:
        url = "https://api.vk.com/method/wall.get"
        params = {
            "access_token": token,
            "v": api_version,
            "owner_id": f"-{group_id}",
            "count": min(100, total_posts - len(collected_posts)),
            "offset": offset
        }
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 429:
            logging.warning("Превышен лимит запросов. Пауза 60 сек.")
            time.sleep(60)
            continue

        if "response" in data:
            posts = data["response"].get("items", [])
            collected_posts.extend(posts)
            offset += len(posts)
            if len(posts) < 100:
                break
        elif "error" in data:
            logging.error(f"Ошибка для группы {group_id}: {data['error']['error_msg']}")
            break
        else:
            logging.error(f"Неизвестная ошибка для группы {group_id}: {data}")
            break

        time.sleep(pause)

    return collected_posts[:total_posts]

def extract_post_data(post, group_id):
    post_id = post.get("id", "")
    post_link = f"https://vk.com/wall-{group_id}_{post_id}"
    text = post.get("text", "Нет текста")
    date_ts = post.get("date", 0)
    likes = post.get("likes", {}).get("count", 0)
    comments = post.get("comments", {}).get("count", 0)
    reposts = post.get("reposts", {}).get("count", 0)

    hashtags = re.findall(r"#\w+", text)
    hashtags_str = ", ".join(hashtags) if hashtags else "Нет"

    post_datetime = datetime.utcfromtimestamp(date_ts)
    hour = post_datetime.hour
    if 5 <= hour < 12:
        time_of_day = "Утро"
    elif 12 <= hour < 18:
        time_of_day = "День"
    elif 18 <= hour < 23:
        time_of_day = "Вечер"
    else:
        time_of_day = "Ночь"

    content_type = determine_content_type(post)

    return {
        "post_id": post_id,
        "post_link": post_link,
        "text": text[:500],
        "date_time": post_datetime.isoformat(),
        "author_id": group_id,
        "likes": likes,
        "comments": comments,
        "reposts": reposts,
        "hashtags": hashtags_str,
        "content_type": content_type,
        "text_length": len(text),
        "time_of_day": time_of_day
    }

if __name__ == "__main__":
    output_file = "filtered_vk_posts9.csv"
    # Пишем заголовки один раз
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow([
            "Post ID", "Post Link", "Text", "Date & Time", "Author ID",
            "Likes", "Comments", "Reposts", "Hashtags", "Content Type",
            "Text Length", "Time of Day"
        ])


    for group_id in group_ids:
        logging.info(f"Сбор постов из группы {group_id}...")
        try:
            posts = fetch_posts(group_id, access_token, version, total_posts=500)
            if posts:
                with open(output_file, "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
                    for post in posts:
                        data = extract_post_data(post, group_id)
                        writer.writerow([
                            data["post_id"], data["post_link"], data["text"], data["date_time"], data["author_id"],
                            data["likes"], data["comments"], data["reposts"], data["hashtags"],
                            data["content_type"], data["text_length"], data["time_of_day"]
                        ])
                logging.info(f"Сбор данных из группы {group_id} завершён. Собрано {len(posts)} постов.")
            else:
                logging.info(f"В группе {group_id} не найдено постов.")
        except Exception as e:
            logging.error(f"Ошибка при обработке группы {group_id}: {e}")

    print(f"Сбор данных завершён. Результаты сохранены в '{output_file}'.")
    logging.info("Сбор данных завершён.")
