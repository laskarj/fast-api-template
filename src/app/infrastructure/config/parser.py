from configparser import ConfigParser

from app.infrastructure.config.dto import AppConfig, Config, DatabaseConfig

DEFAULT_CONFIG_PATH = './config/local.ini'


def load_config(path_file: str = None) -> Config:
    if path_file is None:
        path_file = DEFAULT_CONFIG_PATH

    parser = ConfigParser()
    parser.read(path_file)

    app_data, database_data = (
        parser['application'],
        parser['database'],
    )

    app_config = AppConfig(
        secret_key=app_data.get('secret_key'),
        host=app_data.get('host'),
        port=app_data.getint('port', 8000),
        project_name=app_data.get('project_name'),
        logging_level=app_data.get('logging_level'),
        server_type=app_data.get('server_type'),
    )
    database_config = DatabaseConfig(
        host=database_data.get('host'),
        port=database_data.getint('port'),
        database=database_data.get('database'),
        user=database_data.get('user'),
        password=database_data.get('password'),
        echo=database_data.getboolean('echo'),
        echo_pool=database_data.getboolean('echo_pool'),
    )
    return Config(app_config=app_config, database_config=database_config)
