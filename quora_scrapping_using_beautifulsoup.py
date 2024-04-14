import csv
import json
import pprint

import requests
from bs4 import BeautifulSoup as Soup


def fetch_questions_and_answers(url, quora_scrapper):
    req = requests.get(url)
    page_soup = Soup(req.content, "html.parser")
    main_box = page_soup.findAll("script", {"type": "application/ld+json"})[0].text
    data = json.loads(main_box)

    try:
        for suggestion in data["mainEntity"]["suggestedAnswer"]:
            qa = {}
            qa["question"] = suggestion.get("parentItem", data["mainEntity"]).get("text")
            qa["answer"] = suggestion["text"]
            qa["url"] = suggestion.get("url")
            qa["date_created"] = suggestion.get("dateCreated")
            qa["date_modified"] = suggestion.get("dateModified")
            qa["upvote_count"] = suggestion.get("upvoteCount")
            qa["author_name"] = suggestion.get("author", {}).get("name")
            qa["author_url"] = suggestion.get("author", {}).get("url")
            quora_scrapper.append(qa)
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")


def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # fieldnames = ['question', 'answer', 'url', 'date_created', 'date_modified', 'upvote_count', 'author_name', 'author_url']
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in data:
            writer.writerow(item)


quora_url = [
    "https://www.quora.com/What-are-the-trending-sub-fields-of-electrical-and-computer-engineering-industry-in-Canada",
]
quora_scrapper = []
for each_url in quora_url:
    fetch_questions_and_answers(each_url, quora_scrapper)

pprint.pprint(quora_scrapper)
print(len(quora_scrapper))

csv_filename = "quora_questions_and_answers.csv"
write_to_csv(quora_scrapper, csv_filename)