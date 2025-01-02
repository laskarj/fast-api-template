import logging

from fastapi import FastAPI
from fastapi_cli.utils.cli import get_rich_toolkit, get_uvicorn_log_config
import uvicorn

from app.infrastructure import logger
from app.infrastructure.config import load_config
from app.infrastructure.config.dto import AppConfig, Config
from app.infrastructure.core.enums import Environment
from app.presentation.api.v1 import controllers, middlewares, providers


def init_app(config: Config) -> FastAPI:
    logger.setup(config.app_config.logging_level)

    app = FastAPI(title=config.app_config.project_name)
    middlewares.setup(app)
    controllers.setup(app)
    providers.setup(app, config)
    return app


def run_app() -> None:
    with get_rich_toolkit() as toolkit:
        config: Config = load_config()
        app = init_app(config)
        app_config: AppConfig = config.app_config
        log_level: int = logging.getLevelName(app_config.logging_level)
        toolkit.print_title(
            f'Starting {app_config.server_type} server 🚀', tag='FastAPI'
        )
        toolkit.print_line()

        toolkit.print(
            f'Server started at [link={app_config.url}]{app_config.url}[/]',
            f'Documentation at [link={app_config.url}/docs]{app_config.url}/docs[/]',
            tag='server',
        )

        toolkit.print('Logs:')
        toolkit.print_line()

        uvicorn_config = uvicorn.Config(
            app=app,
            host=app_config.host,
            port=app_config.port,
            log_level=log_level,
            log_config=get_uvicorn_log_config(),
            reload=app_config.server_type == Environment.DEV,
        )
        server = uvicorn.Server(config=uvicorn_config)
        server.run()


if __name__ == '__main__':
    run_app()
