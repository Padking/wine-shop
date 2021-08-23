import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


def get_years_of_life(year_of_origin, avg_days_in_year):
    now = datetime.datetime.utcnow()
    born = datetime.datetime(year_of_origin, 1, 1)
    delta = now - born

    years_of_life = int(delta.days / avg_days_in_year)
    return years_of_life


rendered_page = template.render(
    years_of_life=str(get_years_of_life(1920, 365.25)),
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
