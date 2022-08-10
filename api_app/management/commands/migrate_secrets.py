# This file is a part of IntelOwl https://github.com/intelowlproject/IntelOwl
# See the file 'LICENSE' for copying permission.

import os

from django.core.management.base import BaseCommand

from api_app.analyzers_manager.serializers import AnalyzerConfigSerializer
from api_app.connectors_manager.serializers import ConnectorConfigSerializer
from api_app.models import PluginCredential


class Command(BaseCommand):
    help = "Migrates secrets from env_file_app (pre-v4.0) to database"

    # Explicit function to facilitate testing
    @staticmethod
    def _get_env_var(name):
        return os.getenv(name)

    @classmethod
    def _migrate_secrets(cls, plugin_list, plugin_type):
        plugin_credentials = []
        for plugin in plugin_list:
            for secret_name in plugin["secrets"].keys():
                secret = plugin["secrets"][secret_name]
                if cls._get_env_var(secret["env_var_key"]):
                    if not PluginCredential.objects.filter(
                        attribute=secret_name,
                        plugin_name=plugin["name"],
                        type=plugin_type,
                    ).exists():
                        plugin_credentials.append(
                            PluginCredential(
                                attribute=secret_name,
                                value=cls._get_env_var(secret["env_var_key"]),
                                plugin_name=plugin["name"],
                                type=plugin_type,
                            )
                        )
                        print(
                            f"Migrated secret {secret['env_var_key']} "
                            f"for plugin {plugin['name']}"
                        )
        PluginCredential.objects.bulk_create(plugin_credentials, ignore_conflicts=True)

    def handle(self, *args, **options):
        self._migrate_secrets(
            AnalyzerConfigSerializer.read_and_verify_config().values(),
            PluginCredential.PluginType.ANALYZER,
        )
        self._migrate_secrets(
            ConnectorConfigSerializer.read_and_verify_config().values(),
            PluginCredential.PluginType.CONNECTOR,
        )
        print(
            "Migration complete. Please delete all plugin secrets "
            "from docker/env_file_app."
        )
