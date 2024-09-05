import requests
from bs4 import BeautifulSoup


def get_parser_type(content_type):
    if 'xml' in content_type:
        return 'xml'
    else:
        return 'html.parser'


respons = requests.get('https://scipost.org/atom/publications/comp-ai')
parser_type = get_parser_type(respons.headers.get('Content-Type', ''))
bs = BeautifulSoup(respons.text, parser_type)

parser = {}

for one_link in bs.find_all('link'):

    if one_link.get('href'):
        link = one_link['href']

        try:
            respons1 = requests.get(link)
            parser_type = get_parser_type(respons1.headers.get('Content-Type', ''))
            bs1 = BeautifulSoup(respons1.text, parser_type)
            title = bs1.find('h2', class_='text-blue')
            abstract = bs1.find('p', class_='abstract')

            if title or abstract:
                parser[link] = [{'Заголовок': title.text, 'Текст': abstract.text}]

            else:
                print("Title or abstract not found for:", link)

        except Exception as e:
            print(f"Error fetching or parsing {link}: {e}")

print(parser)
