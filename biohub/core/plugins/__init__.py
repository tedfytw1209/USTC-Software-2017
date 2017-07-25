from .config import PluginConfig  # noqa: F401
from .registry import manager

install = manager.install
remove = manager.remove
prepare_database = manager.prepare_database

default_app_config = 'biohub.core.plugins.apps.PluginsConfig'