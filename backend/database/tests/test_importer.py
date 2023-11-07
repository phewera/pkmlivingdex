from os import path

from database.importer import Importer, WORKING_DIR as IMPORTER_WORKING_DIR
from database.tests.base import DatabaseTestCase

WORKING_DIR = path.dirname(path.abspath(__file__))


class TestDatabaseManager(DatabaseTestCase):
    file_name: str = 'test-dex-data.csv'
    file_path: str = path.join(WORKING_DIR, 'data')
    importer: Importer

    def setUp(self) -> None:
        super().setUp()

        # setup importer with test data
        self.importer = Importer(
            file_name=self.file_name,
            file_path=self.file_path
        )

    def test__init__(self):
        # do it
        importer = Importer()

        # post condition
        file_name = 'dex-data.csv'
        file_path = path.join(IMPORTER_WORKING_DIR, '../var/import')

        self.assertIsInstance(importer, Importer)
        self.assertEqual(importer.file_name, file_name)
        self.assertEqual(importer.file_path, file_path)
        self.assertEqual(importer.file, path.join(file_path, file_name))

    def test__init___extra_data(self):
        # setup
        file_name = 'test-dex-data.csv'
        file_path = path.join(WORKING_DIR, '../data')

        # do it
        importer = Importer(
            file_name=file_name,
            file_path=file_path
        )

        # post condition
        self.assertIsInstance(importer, Importer)
        self.assertEqual(importer.file_name, file_name)
        self.assertEqual(importer.file_path, file_path)
        self.assertEqual(importer.file, path.join(file_path, file_name))

    def test__get_default_file_path(self):
        # do it
        result = self.importer._get_default_file_path()

        # post condition
        self.assertEqual(result, path.join(IMPORTER_WORKING_DIR, '../var/import'))

    def test__get_file(self):
        # do it
        result = self.importer._get_file()

        # post condition
        self.assertEqual(result, path.join(self.file_path, self.file_name))

    def test__validate_file(self):
        # do it
        result = self.importer._validate_file()

        # post condition
        self.assertTrue(result)

    def test__validate_file__invalid_path(self):
        # setup
        self.importer.file = path.join(WORKING_DIR, 'invalid-path', self.file_name)

        # pre condition
        self.assertFalse(path.isfile(self.importer.file))

        # do it
        result = self.importer._validate_file()

        # post condition
        self.assertFalse(result)

    def test__validate_file__invalid_file_ending(self):
        # setup
        self.importer.file = path.join(WORKING_DIR, self.file_path, 'test-dex-data.invalid')

        # pre condition
        self.assertTrue(path.isfile(self.importer.file))

        # do it
        result = self.importer._validate_file()

        # post condition
        self.assertFalse(result)


