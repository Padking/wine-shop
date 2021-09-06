import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import pprint
from typing import Dict, List

from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas


def get_years_of_life(year_of_origin, avg_days_in_year):
    now = datetime.datetime.utcnow()
    born = datetime.datetime(year_of_origin, 1, 1)
    delta = now - born

    years_of_life = int(delta.days / avg_days_in_year)
    return years_of_life


def get_wines(filename) -> List[Dict]:
    new_columns_names = ['name', 'sort', 'price', 'image']
    df_table_about_wines = pandas.read_excel(filename)

    df_table_about_wines.columns = new_columns_names
    df_table_about_wines.price = df_table_about_wines.price.astype(int)

    wines = df_table_about_wines.to_dict(orient='records')

    return wines


def get_goods_by_categories(filename) -> Dict[str, List[Dict]]:
    # new_columns_names = ['category', 'name', 'sort', 'price', 'image']
    df_table_about_goods = pandas.read_excel(filename, keep_default_na=False)

    # df_table_about_goods.columns = new_columns_names
    # df_table_about_goods.price = df_table_about_goods.price.astype(int)

    goods_by_categories = (
        df_table_about_goods.groupby('Категория')
                            .apply(lambda g: g.to_dict(orient='records'))
                            .apply(sort_)
                            .to_dict()
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

    template = env.get_template('template.html')

    pprint.pprint(get_goods_by_categories('for_project/wine2.xlsx'))

    rendered_page = template.render(
        years_of_life=str(get_years_of_life(1920, 365.25)),
        wines=get_wines('for_project/wine.xlsx')
    )

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
