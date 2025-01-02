from app.presentation import api


def run() -> None:
    api.v1.run_app()


if __name__ == '__main__':
    run()
