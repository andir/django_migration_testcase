from django.test import TestCase, SimpleTestCase
from django.core.management import call_command
from django.apps import apps
from django.db import connection
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.state import ProjectState


class MigrationTest(TestCase):

    __abstract__ = True

    def setUp(self):
        super(MigrationTest, self).setUp()
        call_command('migrate', self.app_name, self.before, no_initial_data=True, verbosity=0)

    def tearDown(self):
        super(MigrationTest, self).tearDown()
        call_command('migrate', self.app_name, no_initial_data=True, verbosity=0)

    def _get_apps_for_migration(self, app_label, migration_name):
        loader = MigrationLoader(connection)
        state = loader.project_state((app_label, migration_name))
        state.render()
        return state.apps

    def get_model_before(self, model_name):
        return (self._get_apps_for_migration(self.app_name, self.before)
                .get_model(self.app_name, model_name))
        
    def get_model_after(self, model_name):
        return (self._get_apps_for_migration(self.app_name, self.after)
                .get_model(self.app_name, model_name))

    def run_migration(self):
        call_command('migrate', self.app_name, self.after, no_initial_data=True, verbosity=0)
