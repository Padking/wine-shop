from pydantic import BaseSettings


class Settings(BaseSettings):
    GOODS_FILEPATH: str
    HTML_TEMPLATE_NAME: str
    HTML_SITE_PAGE: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
