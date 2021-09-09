import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Dict, List

from config import Settings

from jinja2 import Environment, FileSystemLoader, select_autoescape

import pandas


def get_goods_by_categories(filename,
                            columns_names_goods_mapper) -> Dict[str, List[Dict]]:

    df_table_about_goods = pandas.read_excel(filename, keep_default_na=False)
    df_table_about_goods.rename(columns_names_goods_mapper, axis='columns',
                                inplace=True, errors='raise')
    df_table_about_goods.price = (
        df_table_about_goods.price
        .astype(int, errors='ignore')
    )

    initialized_dd = defaultdict(list)
    goods_by_categories = (
        df_table_about_goods.groupby('category')
                            .apply(lambda goods: goods.to_dict(orient='records'))
                            .to_dict(into=initialized_dd)
    )

    return goods_by_categories


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    columns_names_goods_mapper = {
        'Категория': 'category',
        'Название': 'name',
        'Сорт': 'sort',
        'Цена': 'price',
        'Картинка': 'image',
        'Акция': 'best_offer'
    }

    config = Settings()

    template = env.get_template(config.HTML_TEMPLATE_NAME)
    age = datetime.date.today().year - 1920

    rendered_page = template.render(
        years_of_life=str(age),
        goods_by_category=get_goods_by_categories(config.GOODS_FILEPATH,
                                                  columns_names_goods_mapper),
    )

    with open(config.HTML_SITE_PAGE, 'w', encoding='utf8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
