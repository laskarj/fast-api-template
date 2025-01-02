from dataclasses import dataclass

from app.infrastructure.core.enums import Environment
from app.infrastructure.logger.enums import LoggingLevel


@dataclass
class AppConfig:
    secret_key: str
    host: str
    port: int
    project_name: str
    logging_level: LoggingLevel = LoggingLevel.INFO
    server_type: Environment = Environment.DEV

    @property
    def url(self) -> str:
        return f'http://{self.host}:{self.port}'


@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    user: str
    password: str
    echo: bool = False
    echo_pool: bool = False

    rdbms: str = 'postgresql'
    connector: str = 'psycopg'

    @property
    def full_url(self) -> str:
        return '{}+{}://{}:{}@{}:{}/{}'.format(
            self.rdbms,
            self.connector,
            self.user,
            self.password,
            self.host,
            self.port,
            self.database,
        )


@dataclass
class Config:
    app_config: AppConfig
    database_config: DatabaseConfig
