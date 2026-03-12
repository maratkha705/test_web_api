import sys
from logging import INFO, FileHandler, StreamHandler, basicConfig, getLogger
from pathlib import Path

from alembic.config import CommandLine, Config

from amtl_api.adapters.db.settings import Settings

settings = Settings()

basicConfig(
    level=INFO,
    format='%(asctime)s ms=%(msecs)03d | %(levelname)s | %(message)s [%(filename)s::%(lineno)d]',
    handlers=[
        FileHandler(
            f"{Path(__file__).parent.parent.parent}/{settings.ALEMBIC_LOG_LOCATION}/log_alembic.log"
        ), StreamHandler()
    ]
)
logger = getLogger("alembic")


def make_config():
    config = Config()
    config.set_main_option(
        'script_location', settings.ALEMBIC_SCRIPT_LOCATION
    )
    config.set_main_option(
        'version_locations', settings.ALEMBIC_VERSION_LOCATIONS
    )
    config.set_main_option('sqlalchemy.url', settings.db_uri)
    config.set_main_option(
        'file_template', settings.ALEMBIC_MIGRATION_FILENAME_TEMPLATE
    )
    config.set_main_option('timezone', 'UTC')

    return config


def run_cmd(*args):
    cli = CommandLine()
    args = cli.parser.parse_args(args)
    config = make_config()
    logger.info(f"Config: {config}")

    cli.run_cmd(config, args)


if __name__ == '__main__':
    run_cmd(*sys.argv[1:])
