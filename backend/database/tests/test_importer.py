from os import path

from database.importer import Importer, TCSVData, WORKING_DIR as IMPORTER_WORKING_DIR
from database.tests.base import DatabaseTestCase, POKEDEX_DATA, GENERATION_DATA, DEXENTRY_DATA, POKEMON_DATA
from database.models import Pokedex, Generation, DexEntry, Pokemon

WORKING_DIR = path.dirname(path.abspath(__file__))


class TestDatabaseManager(DatabaseTestCase):
    file_name: str = 'test-dex-data.csv'
    file_path: str = path.join(WORKING_DIR, 'data')
    pokedex: Pokedex
    importer: Importer

    def setUp(self) -> None:
        super().setUp()

        self.pokedex = self.create_obj(
            model=Pokedex,
            data=POKEDEX_DATA
        )

        # setup importer with test data
        self.importer = Importer(
            file_name=self.file_name,
            file_path=self.file_path,
            env='testing'
        )

    def tearDown(self) -> None:
        super().tearDown()
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

    def test__check_missing_values(self):
        # setup
        dataset = {
            'number': 1,
            'name': 'Bulbasaur',
            'form': 1,
            'sprite': 'bulbasaur_1.png',
            'generation': 1,
            'lgplge': True,
            'swsh': False,
            'arceus': True,
            'bdsp': False,
            'sv': True
        }

        # do it
        result = self.importer._check_missing_values(dataset)

        # post condition
        self.assertFalse(result)

    def test__check_missing_values__na_value(self):
        # setup
        dataset = {
            'number': 1,
            'name': 'Bulbasaur',
            'form': 1,
            'sprite': 'bulbasaur_1.png',
            'generation': 'NA',
            'lgplge': True,
            'swsh': False,
            'arceus': True,
            'bdsp': False,
            'sv': True
        }

        # do it
        # noinspection PyTypeChecker
        result = self.importer._check_missing_values(dataset)

        # post condition
        self.assertTrue(result)

    def test__handle_generation(self):
        self.skipTest('TODO')

    def test__handle_dexentry(self):
        self.skipTest('TODO')

    def test__handle_pokemon(self):
        self.skipTest('TODO')

    def test_run_import(self):
        # do it
        self.importer.run_import(pokedex_id=self.pokedex.id)

        # post condition
        self.assertEqual(self.importer.imported, 39)
        self.assertEqual(self.importer.updated, 0)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 2)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 18)

        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 19)

    def test_run_import__imported_data(self):
        # do it
        self.importer.run_import(pokedex_id=self.pokedex.id)

        # post condition
        generations = self.db.session.query(Generation).all()
        generation = generations[0]
        self.assertEqual(generation.pokedex_id, self.pokedex.id)
        self.assertEqual(generation.number, 1)
        self.assertEqual(generation.sprite, 'gen_1.png')

        dexentries = self.db.session.query(DexEntry).all()
        dexentry = dexentries[0]
        self.assertEqual(dexentry.generation_id, generation.id)
        self.assertEqual(dexentry.number, 1)
        self.assertEqual(dexentry.name, 'Bisasam')

        pokemons = self.db.session.query(Pokemon).all()
        pokemon = pokemons[0]
        self.assertEqual(pokemon.dexentry_id, dexentry.id)
        self.assertEqual(pokemon.sprite, '0001_1.png')
        self.assertEqual(pokemon.form, 1)
        self.assertTrue(pokemon.lgplge)
        self.assertTrue(pokemon.swsh)
        self.assertFalse(pokemon.arceus)
        self.assertFalse(pokemon.sv)
        self.assertFalse(pokemon.caught)
        self.assertFalse(pokemon.shiny_caught)

    def test_run_import__update_data(self):
        self.skipTest('TODO')

    def test_run_import__no_changes(self):
        self.skipTest('TODO')

    def test_run_import___missing_values(self):
        self.skipTest('TODO')
