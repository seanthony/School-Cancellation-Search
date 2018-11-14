import requests


def get_page_text():
    r = requests.get('https://www.wtva.com/weather/closings/')
    return r.text


def main():
    text = get_page_text()
    # scrape_page(text)


if __name__ == "__main__":
    main()
