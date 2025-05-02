import os
from urllib import parse
from dynaconf import Dynaconf
from app.common.utils import gm


ENV = os.getenv('ENV') or 'dev'
PROJECT_DIR = os.path.dirname(__file__)
DEBUG = ENV == 'dev'


def encrypt(word):
    """
    加密
    :param public_key:
    :param word:
    :return:
    """
    return gm.encrypt(settings.encrypt.public_key, word)


def decrypt(token):
    """
    解密
    :param private_key:
    :param token:
    :return:
    """
    return gm.decrypt(settings.encrypt.private_key, token)


settings = Dynaconf(
    envvar_prefix="KISS",
    root_path= os.sep.join([PROJECT_DIR, '.env']),
    settings_files=['settings.toml', '.secrets.toml'],
    environments=True,
    env= ENV
)

def get_database_dsn():
    password = decrypt(settings.database.passwprd_encrypted)
    return f'{settings.database.dialect}://{parse.quote(settings.database.user)}:{parse.quote(password)}@{settings.database.hostname}/{settings.database.name}'

