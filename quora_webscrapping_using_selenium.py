import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def scrape_quora(url):
    # Set up the Chrome driver
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Load the Quora page
    driver.get(url)

    # Scroll to the bottom of the page to load all questions and answers
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    all_questions = driver.find_elements(By.CLASS_NAME, "q-click-wrapper.qu-display--block.qu-tapHighlight--none")

    # Extract questions and answers
    questions = [question.text.strip() for question in all_questions]

    # Quit the driver
    driver.quit()

    return questions

if __name__ == "__main__":
    quora_url = "https://www.quora.com/What-are-the-trending-sub-fields-of-electrical-and-computer-engineering-industry-in-Canada"
    questions = scrape_quora(quora_url)

    print("Questions and Answer:")
    for i, question in enumerate(questions, start=1):
        print(f"{i}. {question}")
        print("*"*200)


# <div class="q-click-wrapper qu-display--block qu-tapHighlight--none ClickWrapper___StyledClickWrapperBox-zoqi4f-0 daLTSH"