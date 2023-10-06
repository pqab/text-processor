from dotenv import dotenv_values
from bs4 import BeautifulSoup

# Load config
input_path = 'input/extract_html/'
config = dotenv_values(f'{input_path}extract_html.env')
element_name = config.get('element_name')
class_name = config.get('class_name')


def run(data: dict):

    soup = BeautifulSoup(open(f'{input_path}input.html'), features='html.parser')

    result = dict()

    for element in soup.find_all(element_name, class_=class_name):
        element_id = element.get('id')
        if '{{' + element_id + '}}' in soup.prettify():
            result[element_id] = element.renderContents().decode('utf-8')

    print(f'Processed: {result}')
    return result
