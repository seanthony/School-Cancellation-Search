import requests


def get_page_text():
    # r = requests.get('https://www.wtva.com/weather/closings/')
    r = requests.get('https://ftp2.wtva.com/All_Active.html')
    return r.text


def strip_row(row):
    return row.split('</tr>')[0].split('</td>')[0].split('>')[-1].strip()


def scrape_page(text):
    rows = list(map(strip_row, text.split('<tr>')))
    print('school closings:\n\t', end="")
    print('\n\t'.join(rows))


def main():
    text = get_page_text()
    scrape_page(text)


if __name__ == "__main__":
    main()
