# Wine shop

Урок № 1 модуля "Вёрстка для питониста" от [Devman](https://dvmn.org/).

## Описание

Сайт магазина авторского вина "Новое русское вино".


### Особенности

- отображает ассортимент, цены на продукцию, предлагаемую магазином "Новое русское вино",
- скрипт `main.py`:
    + позволяет автоматически рассчитывать дату с момента основания, в частности, винодельни,
    + подготавливает к отображению произвольное кол-во продуктов различных категорий согласно [Excel-таблице](https://github.com/Padking/wine-shop#%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80-%D0%B8%D1%81%D1%85%D0%BE%D0%B4%D0%BD%D1%8B%D1%85-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85),
    + позволяет отмечать желаемые товары знаком "Выгодное предложение".

#### Пример исходных данных

![f](https://github.com/Padking/wine-shop/blob/master/snapshots/goods_table.png)


### Требования к окружению

* Python 3.7 и выше,
* Linux/Windows,
* ПеО.

Проект настраивается через ПеО, достаточно указать их в файле `.env`.
Передача значений ПеО происходит с использованием [pydantic[dotenv]](https://pydantic-docs.helpmanual.io/usage/settings/#dotenv-env-support).

#### Параметры проекта

|       Ключ        |     Назначение     |   По умолчанию   |
|-------------------|------------------|------------------|
|`GOODS_FILEPATH`| Путь к Excel-файлу с ассортиментом |-|
|`HTML_TEMPLATE_NAME`| Имя html-шаблона для Jinja2 |-|

### Установка

- Клонирование проекта,
- создание каталога виртуального окружения (ВО)*,
- связывание каталогов ВО и проекта,
- установка зависимостей,
- запуск скрипта:
```bash
git clone https://github.com/Padking/wine-shop.git
cd wine-shop
mkvirtualenv -p <path to python> <name of virtualenv>
setvirtualenvproject <path to virtualenv> <path to project>
pip install -r requirements.txt
python main.py
```
- Перейти на сайт по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).


\* с использованием [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/index.html).
