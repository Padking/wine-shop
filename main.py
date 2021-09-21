import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Dict, List

from config import Settings

from jinja2 import Environment, FileSystemLoader, select_autoescape

import pandas


def get_goods_by_categories(filename) -> Dict[str, List[Dict]]:

    df_table_about_goods = pandas.read_excel(filename, keep_default_na=False)
    goods_by_categories = defaultdict(list)
    goods = df_table_about_goods.to_dict('records')
    for good in goods:
        goods_by_categories[good['Категория']].append(good)

    return goods_by_categories


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    config = Settings()

    template = env.get_template(config.HTML_TEMPLATE_NAME)
    age = datetime.date.today().year - 1920

    rendered_page = template.render(
        years_of_life=str(age),
        goods_by_category=get_goods_by_categories(config.GOODS_FILEPATH)
    )

    with open(config.HTML_SITE_PAGE, 'w', encoding='utf-8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
