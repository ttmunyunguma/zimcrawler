import math
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import pandas


# Get total number of pages
def get_total_pages():
    request = requests.get('https://www.property.co.zw/property-for-sale/harare')
    content = request.content
    soup = BeautifulSoup(content, 'html.parser')
    return int(soup.find('li', {'class': 'pager-description site-color'}).get_text().strip().split()[-1])


# Get Property Data from website
def get_property_data():
    property_list = []
    # tot_pages = get_total_pages()
    base_url = 'https://www.property.co.zw/property-for-sale/harare?page='

    for page in range(1, 2, 1):  # math.ceil(tot_pages / 20) + 1
        url = base_url + str(page)
        print(page)
        request = requests.get(url)
        content = request.content
        soup = BeautifulSoup(content, 'html.parser')

        get_colored_results(property_list, soup, 'result-card col-sm-12 cleafix gold-result')
        get_colored_results(property_list, soup, 'result-card col-sm-12 cleafix silver-result')

        # For postgreSql DB
        # database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
        #     user=user,
        #     password=password,
        #     database_name=database_name,
        # )
        # engine = create_engine(database_url, echo=False)

        engine = create_engine('sqlite:///C:/Users/Terrence/PycharmProjects/ZimCrawler/db.sqlite3', echo=False)

        df = pandas.DataFrame(property_list)
        df.to_sql('property', con=engine, if_exists='replace', index_label='id')

        return df


def get_colored_results(property_list, soup, color):
    all_properties = soup.find_all('div', {'class': color})
    for properti in all_properties:
        try:
            usd_price = properti.find('div', {'class': 'listing-price-first'}).contents[0].strip()
        except TypeError:
            usd_price = None
        try:
            zwl_price = properti.find('div', {'class': 'listing-price-second'}).contents[0].strip()
        except TypeError:
            zwl_price = None
        try:
            prop_title = properti.find('span', {'class': 'teaser'}).get_text()
        except TypeError:
            prop_title = None
        try:
            address = properti.find('div', {'class': 'col-md-12 full-address detail-row'}).contents[2].strip()
        except TypeError:
            address = None
        try:
            detail = properti.find('div', {
                'class': 'col-md-12 listing-description detail-row truncate'}).get_text().strip()
        except TypeError:
            detail = None
        try:
            link = properti.find('a', {'class': 'link-primary'}).get('href')
        except TypeError:
            link = '#'

        property_list.append({
            'usd_price': usd_price,
            'zwl_price': zwl_price,
            'prop_title': prop_title,
            'address': address,
            'detail': detail,
            'link': 'https://www.property.co.zw'+link
        })


if __name__ == '__main__':
    get_property_data()
