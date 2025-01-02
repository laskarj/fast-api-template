from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig
from alembic.script import Script, ScriptDirectory
import pytest


def get_revisions(alembic_config: AlembicConfig) -> list[Script]:
    script_location = alembic_config.get_main_option('script_location')
    revisions_directory = ScriptDirectory(script_location)
    revisions: list[Script] = list(revisions_directory.walk_revisions('base', 'heads'))
    return revisions


@pytest.mark.order('first')
def test_migrations_and_revisions(alembic_config: AlembicConfig) -> None:
    for revisions in get_revisions(alembic_config):
        upgrade(alembic_config, revisions.revision)
        downgrade(alembic_config, revisions.down_revision or '-1')
        upgrade(alembic_config, 'head')
