from os import path

from database.importer import Importer, TCSVData, WORKING_DIR as IMPORTER_WORKING_DIR
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

    def tearDown(self) -> None:
        del self.importer

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
        file_name = 'another-file.csv'
        file_path = 'another-path'

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
        file_path = 'invalid-path'
        self.importer.__init__(
            file_path=file_path,
            file_name=self.file_name
        )

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
        file_name = 'test-dex-data.invalid'
        self.importer.__init__(
            file_path=self.file_path,
            file_name=file_name
        )

        # pre condition
        self.assertTrue(path.isfile(self.importer.file))

        # do it
        result = self.importer._validate_file()

        # post condition
        self.assertFalse(result)

    def test___parse_csv__validate_columns(self):
        # do it
        result = self.importer._parse_csv()

        # post condition
        expected_keys = set(TCSVData.__annotations__.keys())
        self.assertEqual(expected_keys, set(result[0].keys()))

    def test___parse_csv__validate_data_types(self):
        # do it
        result = self.importer._parse_csv()

        # post condition
        for row in result:
            for key, value in TCSVData.__annotations__.items():
                self.assertIsInstance(row[key], value)

    def test___parse_csv__validate_data(self):
        # do it
        result = self.importer._parse_csv()

        # post condition
        row1 = result[0]
        self.assertEqual(row1['number'], 1)
        self.assertEqual(row1['name'], 'Bisasam')
        self.assertEqual(row1['form'], 1)
        self.assertEqual(row1['sprite'], '0001_1.png')
        self.assertEqual(row1['generation'], 1)
        self.assertEqual(row1['lgplge'], True)
        self.assertEqual(row1['swsh'], True)
        self.assertEqual(row1['arceus'], False)
        self.assertEqual(row1['bdsp'], True)
        self.assertEqual(row1['sv'], False)

    def test___parse_csv__wrong_datatypes(self):
        # setup
        file_name = 'test-dex-data_wrong_data_type.csv'
        self.importer.__init__(
            file_path=self.file_path,
            file_name=file_name
        )

        # pre condition
        self.assertTrue(path.isfile(self.importer.file))

        # do it
        result = self.importer._parse_csv()

        # post condition
        self.assertIsNone(result)

    def test__parse_csv__missing_columns(self):
        # setup
        file_name = 'test-dex-data_missing_columns.csv'
        self.importer.__init__(
            file_path=self.file_path,
            file_name=file_name
        )

        # pre condition
        self.assertTrue(path.isfile(self.importer.file))

        # do it
        result = self.importer._parse_csv()

        # post condition
        self.assertIsNone(result)