import requests
from weather import Weather, Unit
from termcolor import colored, cprint


def get_weather():
    weather = Weather(unit=Unit.FAHRENHEIT)
    # 2515032 is WOEID for Water Valley, MS
    lookup = weather.lookup(2515032)
    condition = lookup.condition
    title = lookup.title
    output = '''Weather Forcast
    {}, {}
    {}°F {}
    Forecast: {} Hi: {}°F, Lo: {}°F 
    '''.format(lookup.location.city, lookup.location.region, lookup.condition.temp, lookup.condition.text, lookup.forecast[0].text, lookup.forecast[0].high, lookup.forecast[0].low)
    return output


def get_page_text():
    # r = requests.get('https://www.wtva.com/weather/closings/')
    r = requests.get('https://ftp2.wtva.com/All_Active.html')
    return r.text


def strip_row(row):
    if 'SCHOOLS' in row:
        tds = row.split('</td>')
        if len(tds) >= 3:
            school, dismiss = tds[1].split(
                '>')[-1].strip(), tds[2].split('>')[-1].strip()
            text = '{} is \'{}\''.format(school, dismiss)
            if is_bcca_school(text):
                return colored(text, 'yellow', attrs=['reverse'])
            return text
    return row.split('</tr>')[0].split('</td>')[0].split('>')[-1].strip()


def scrape_page(text):
    rows = list(filter(lambda b: b, map(strip_row, text.split('<tr>'))))
    return rows


def is_bcca_school(text):
    schools = ['pontotoc', 'grenada', 'charleston', 'water valley',
               'oxford', 'lafayette', 'south panola', 'coffeeville']
    for school in schools:
        if school in text.lower():
            return True
    return False


def get_bcca_schools(rows):
    return list(filter(is_bcca_school, rows))


def main():
    print('\n\n')
    # weather info
    weather = get_weather()
    print(weather)

    # cancellation info
    text = get_page_text()
    rows = scrape_page(text)
    bcca_rows = get_bcca_schools(rows)
    if len(bcca_rows):
        print()
        text = colored('BCCA Schools:', 'red', attrs=['reverse'])
        print(text, '\n\t', '\n\t'.join(bcca_rows), sep="")
    if len(rows):
        print('\nAll School Closings:\n\t', '\n\t'.join(rows), sep="")
    else:
        print('No closings')
    print('\n\n')


if __name__ == "__main__":
    main()
