from collections import defaultdict
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Dict, List

from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas

from config import Settings


def get_years_of_life(year_of_origin, avg_days_in_year):
    now = datetime.datetime.utcnow()
    born = datetime.datetime(year_of_origin, 1, 1)
    delta = now - born

    years_of_life = int(delta.days / avg_days_in_year)
    return years_of_life


def get_wines(filename, columns_names_wines_mapper) -> List[Dict]:

    df_table_about_wines = pandas.read_excel(filename, keep_default_na=False)
    df_table_about_wines.rename(columns_names_wines_mapper, axis='columns',
                                inplace=True, errors='raise')
    df_table_about_wines.price = (
        df_table_about_wines.price
        .astype(int, errors='ignore')
    )

    wines = df_table_about_wines.to_dict(orient='records')

    return wines


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
                            .apply(sort_)
                            .to_dict(into=initialized_dd)
    )

    return goods_by_categories


def sort_(goods_row_by_category: List[Dict]) -> List[Dict]:
    for good in goods_row_by_category:
        for key_of_good in sorted(good):
            good[key_of_good] = good.pop(key_of_good)

    return goods_row_by_category


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    columns_names_wines_mapper = {
        'Название': 'name',
        'Сорт': 'sort',
        'Цена': 'price',
        'Картинка': 'image'
    }

    columns_names_goods_mapper = {
        'Категория': 'category',
        **columns_names_wines_mapper,
        'Акция': 'best_offer'
    }

    config = Settings()

    template = env.get_template(config.HTML_TEMPLATE_NAME)
    exclusive_category = 'Напитки'

    rendered_page = template.render(
        years_of_life=str(get_years_of_life(1920, 365.25)),
        goods_by_category=get_goods_by_categories(config.GOODS_FILEPATH,
                                                  columns_names_goods_mapper),
        exclusive_category=exclusive_category
    )

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
