import unittest

from omicron_server.config import Config, default_config

__author__ = 'Michal Kononenko'

environment = {'DATABASE_URL': 'postgres://user:password@postgres.com'}


class TestConfigConstructor(unittest.TestCase):

    def test_config(self):
        conf = Config(conf_dict=environment)

        self.assertEqual(conf.DATABASE_URL, environment['DATABASE_URL'])

    def test_engine_creator(self):
        """
        Fixes issue #119. Tests that changing the database url re-creates
        the database engine
        """
        self.assertNotEqual(
                environment["DATABASE_URL"], default_config.DATABASE_URL
        )

        conf = Config(environment)

        self.assertNotEqual(
                conf.DATABASE_ENGINE, default_config.DATABASE_ENGINE
        )
