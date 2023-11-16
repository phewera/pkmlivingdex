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
            file_name=self.file_name,
            env='testing'
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
            file_name=file_name,
            env='testing'
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
            file_name=file_name,
            env='testing'
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
            file_name=file_name,
            env='testing'
        )

        # pre condition
        self.assertTrue(path.isfile(self.importer.file))

        # do it
        result = self.importer._parse_csv()

        # post condition
        self.assertIsNone(result)

    def test__parse_csv__missing_values(self):
        # setup
        file_name = 'test-dex-data_missing_values.csv'
        self.importer.__init__(
            file_path=self.file_path,
            file_name=file_name,
            env='testing'
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
            'number': DEXENTRY_DATA['number'],
            'name': DEXENTRY_DATA['name'],
            'form': POKEMON_DATA['form'],
            'sprite': POKEMON_DATA['sprite'],
            'generation': GENERATION_DATA['number'],
            'lgplge': POKEMON_DATA['lgplge'],
            'swsh': POKEMON_DATA['swsh'],
            'arceus': POKEMON_DATA['arceus'],
            'bdsp': POKEMON_DATA['bdsp'],
            'sv': POKEMON_DATA['sv']
        }

        # do it
        result = self.importer._check_missing_values(dataset)

        # post condition
        self.assertFalse(result)

    def test__check_missing_values__na_value(self):
        # setup
        dataset = {
            'number': DEXENTRY_DATA['number'],
            'name': DEXENTRY_DATA['name'],
            'form': POKEMON_DATA['form'],
            'sprite': POKEMON_DATA['sprite'],
            'generation': 'na',
            'lgplge': POKEMON_DATA['lgplge'],
            'swsh': POKEMON_DATA['swsh'],
            'arceus': POKEMON_DATA['arceus'],
            'bdsp': POKEMON_DATA['bdsp'],
            'sv': POKEMON_DATA['sv']
        }

        # do it
        # noinspection PyTypeChecker
        result = self.importer._check_missing_values(dataset)

        # post condition
        self.assertTrue(result)

    def test__check_missing_values__nan_value(self):
        # setup
        dataset = {
            'number': DEXENTRY_DATA['number'],
            'name': DEXENTRY_DATA['name'],
            'form': POKEMON_DATA['form'],
            'sprite': POKEMON_DATA['sprite'],
            'generation': 'nan',
            'lgplge': POKEMON_DATA['lgplge'],
            'swsh': POKEMON_DATA['swsh'],
            'arceus': POKEMON_DATA['arceus'],
            'bdsp': POKEMON_DATA['bdsp'],
            'sv': POKEMON_DATA['sv']
        }

        # do it
        # noinspection PyTypeChecker
        result = self.importer._check_missing_values(dataset)

        # post condition
        self.assertTrue(result)

    def test__check_missing_values__nan_and_na_value(self):
        # setup
        dataset = {
            'number': DEXENTRY_DATA['number'],
            'name': 'na',
            'form': POKEMON_DATA['form'],
            'sprite': POKEMON_DATA['sprite'],
            'generation': 'nan',
            'lgplge': POKEMON_DATA['lgplge'],
            'swsh': POKEMON_DATA['swsh'],
            'arceus': POKEMON_DATA['arceus'],
            'bdsp': POKEMON_DATA['bdsp'],
            'sv': POKEMON_DATA['sv']
        }

        # do it
        # noinspection PyTypeChecker
        result = self.importer._check_missing_values(dataset)

        # post condition
        self.assertTrue(result)

    def test__handle_generation__create(self):
        # setup
        csv_data = {
            'number': DEXENTRY_DATA['number'],
            'name': DEXENTRY_DATA['name'],
            'form': POKEMON_DATA['form'],
            'sprite': POKEMON_DATA['sprite'],
            'generation': GENERATION_DATA['number'],
            'lgplge': POKEMON_DATA['lgplge'],
            'swsh': POKEMON_DATA['swsh'],
            'arceus': POKEMON_DATA['arceus'],
            'bdsp': POKEMON_DATA['bdsp'],
            'sv': POKEMON_DATA['sv']
        }

        # pre condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 0)

        self.assertEqual(self.importer.imported, 0)
        self.assertEqual(self.importer.updated, 0)

        # do it
        result = self.importer._handle_generation(
            pokedex_id=self.pokedex.id,
            dataset=csv_data
        )

        # post condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        self.assertIsInstance(result, Generation)
        self.assertEqual(result.number, csv_data['generation'])
        self.assertEqual(result.sprite, f'gen_{csv_data["generation"]}.png')
        self.assertEqual(result.pokedex_id, self.pokedex.id)

        self.assertEqual(self.importer.imported, 1)
        self.assertEqual(self.importer.updated, 0)

    def test__handle_generation__already_exist__no_changes(self):
        # setup
        generation = self.create_obj(
            model=Generation,
            data=GENERATION_DATA
        )

        csv_data = {
            'number': DEXENTRY_DATA['number'],
            'name': DEXENTRY_DATA['name'],
            'form': POKEMON_DATA['form'],
            'sprite': POKEMON_DATA['sprite'],
            'generation': generation.number,
            'lgplge': POKEMON_DATA['lgplge'],
            'swsh': POKEMON_DATA['swsh'],
            'arceus': POKEMON_DATA['arceus'],
            'bdsp': POKEMON_DATA['bdsp'],
            'sv': POKEMON_DATA['sv']
        }

        # pre condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        self.assertEqual(self.importer.imported, 0)
        self.assertEqual(self.importer.updated, 0)

        # do it
        result = self.importer._handle_generation(
            pokedex_id=self.pokedex.id,
            dataset=csv_data
        )

        # post condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        self.assertIsInstance(result, Generation)
        self.assertEqual(result.id, generation.id)
        self.assertEqual(result.number, generation.number)
        self.assertEqual(result.sprite, generation.sprite)
        self.assertEqual(result.pokedex_id, generation.pokedex_id)

        self.assertEqual(self.importer.imported, 0)
        self.assertEqual(self.importer.updated, 0)

    def test__handle_dexentry__create(self):
        # setup
        generation = self.create_obj(
            model=Generation,
            data=GENERATION_DATA
        )

        csv_data = {
            'number': DEXENTRY_DATA['number'],
            'name': DEXENTRY_DATA['name'],
            'form': POKEMON_DATA['form'],
            'sprite': POKEMON_DATA['sprite'],
            'generation': generation.number,
            'lgplge': POKEMON_DATA['lgplge'],
            'swsh': POKEMON_DATA['swsh'],
            'arceus': POKEMON_DATA['arceus'],
            'bdsp': POKEMON_DATA['bdsp'],
            'sv': POKEMON_DATA['sv']
        }

        # pre condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 0)

        self.assertEqual(self.importer.imported, 0)
        self.assertEqual(self.importer.updated, 0)

        # do it
        result = self.importer._handle_dexentry(
            generation_id=generation.id,
            dataset=csv_data
        )

        # post condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        self.assertIsInstance(result, DexEntry)
        self.assertEqual(result.number, csv_data['number'])
        self.assertEqual(result.name, csv_data['name'])
        self.assertEqual(result.generation_id, generation.id)

        self.assertEqual(self.importer.imported, 1)
        self.assertEqual(self.importer.updated, 0)

    def test__handle_dexentry__already_exist__no_changes(self):
        # setup
        generation = self.create_obj(
            model=Generation,
            data=GENERATION_DATA
        )
        dexentry = self.create_obj(
            model=DexEntry,
            data=DEXENTRY_DATA
        )

        csv_data = {
            'number': dexentry.number,
            'name': dexentry.name,
            'form': POKEMON_DATA['form'],
            'sprite': POKEMON_DATA['sprite'],
            'generation': generation.number,
            'lgplge': POKEMON_DATA['lgplge'],
            'swsh': POKEMON_DATA['swsh'],
            'arceus': POKEMON_DATA['arceus'],
            'bdsp': POKEMON_DATA['bdsp'],
            'sv': POKEMON_DATA['sv']
        }

        # pre condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        self.assertEqual(self.importer.imported, 0)
        self.assertEqual(self.importer.updated, 0)

        # do it
        result = self.importer._handle_dexentry(
            generation_id=generation.id,
            dataset=csv_data
        )

        # post condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        self.assertIsInstance(result, DexEntry)
        self.assertEqual(result.number, dexentry.number)
        self.assertEqual(result.name, dexentry.name)
        self.assertEqual(result.generation_id, dexentry.generation_id)

        self.assertEqual(self.importer.imported, 0)
        self.assertEqual(self.importer.updated, 0)

    def test__handle_dexentry__already_exist__update_data(self):
        # setup
        generation = self.create_obj(
            model=Generation,
            data=GENERATION_DATA
        )
        dexentry = self.create_obj(
            model=DexEntry,
            data=DEXENTRY_DATA
        )

        csv_data = {
            'number': dexentry.number,
            'name': f'{dexentry.name}-changed',
            'form': POKEMON_DATA['form'],
            'sprite': POKEMON_DATA['sprite'],
            'generation': generation.number,
            'lgplge': POKEMON_DATA['lgplge'],
            'swsh': POKEMON_DATA['swsh'],
            'arceus': POKEMON_DATA['arceus'],
            'bdsp': POKEMON_DATA['bdsp'],
            'sv': POKEMON_DATA['sv']
        }

        # pre condition
        self.assertNotEqual(dexentry.name, csv_data['name'])

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        self.assertEqual(self.importer.imported, 0)
        self.assertEqual(self.importer.updated, 0)

        # do it
        result = self.importer._handle_dexentry(
            generation_id=generation.id,
            dataset=csv_data
        )

        # post condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        self.assertIsInstance(result, DexEntry)
        self.assertEqual(result.number, dexentry.number)
        self.assertEqual(result.name, csv_data['name'])
        self.assertEqual(result.generation_id, dexentry.generation_id)

        self.assertEqual(self.importer.imported, 0)
        self.assertEqual(self.importer.updated, 1)

    def test__handle_pokemon__create(self):
        # setup
        generation = self.create_obj(
            model=Generation,
            data=GENERATION_DATA
        )
        dexentry = self.create_obj(
            model=DexEntry,
            data=DEXENTRY_DATA
        )

        csv_data = {
            'number': dexentry.number,
            'name': DEXENTRY_DATA['name'],
            'form': POKEMON_DATA['form'],
            'sprite': POKEMON_DATA['sprite'],
            'generation': generation.number,
            'lgplge': POKEMON_DATA['lgplge'],
            'swsh': POKEMON_DATA['swsh'],
            'arceus': POKEMON_DATA['arceus'],
            'bdsp': POKEMON_DATA['bdsp'],
            'sv': POKEMON_DATA['sv']
        }

        # pre condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 0)

        self.assertEqual(self.importer.imported, 0)
        self.assertEqual(self.importer.updated, 0)

        # do it
        result = self.importer._handle_pokemon(
            dexentry_id=dexentry.id,
            dataset=csv_data
        )

        # post condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 1)

        self.assertIsInstance(result, Pokemon)
        self.assertEqual(result.form, csv_data['form'])
        self.assertEqual(result.sprite, csv_data['sprite'])
        self.assertFalse(result.caught)
        self.assertFalse(result.shiny_caught)
        self.assertEqual(result.lgplge, csv_data['lgplge'])
        self.assertEqual(result.swsh, csv_data['swsh'])
        self.assertEqual(result.arceus, csv_data['arceus'])
        self.assertEqual(result.bdsp, csv_data['bdsp'])
        self.assertEqual(result.sv, csv_data['sv'])
        self.assertEqual(result.dexentry_id, dexentry.id)

        self.assertEqual(self.importer.imported, 1)
        self.assertEqual(self.importer.updated, 0)

    def test__handle_pokemon__already_exist__no_changes(self):
        # setup
        generation = self.create_obj(
            model=Generation,
            data=GENERATION_DATA
        )
        dexentry = self.create_obj(
            model=DexEntry,
            data=DEXENTRY_DATA
        )
        pokemon = self.create_obj(
            model=Pokemon,
            data=POKEMON_DATA
        )

        csv_data = {
            'number': dexentry.number,
            'name': dexentry.name,
            'form': pokemon.form,
            'sprite': pokemon.sprite,
            'generation': generation.number,
            'lgplge': pokemon.lgplge,
            'swsh': pokemon.swsh,
            'arceus': pokemon.arceus,
            'bdsp': pokemon.bdsp,
            'sv': pokemon.sv
        }

        # pre condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 1)

        self.assertEqual(self.importer.imported, 0)
        self.assertEqual(self.importer.updated, 0)

        # do it
        result = self.importer._handle_pokemon(
            dexentry_id=dexentry.id,
            dataset=csv_data
        )

        # post condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 1)

        self.assertIsInstance(result, Pokemon)
        self.assertEqual(result.form, pokemon.form)
        self.assertEqual(result.sprite, pokemon.sprite)
        self.assertEqual(result.caught, pokemon.caught)
        self.assertEqual(result.shiny_caught, pokemon.shiny_caught)
        self.assertEqual(result.lgplge, pokemon.lgplge)
        self.assertEqual(result.swsh, pokemon.swsh)
        self.assertEqual(result.arceus, pokemon.arceus)
        self.assertEqual(result.bdsp, pokemon.bdsp)
        self.assertEqual(result.sv, pokemon.sv)
        self.assertEqual(result.dexentry_id, pokemon.dexentry_id)

        self.assertEqual(self.importer.imported, 0)
        self.assertEqual(self.importer.updated, 0)

    def test__handle_pokemon__already_exist__update_data(self):
        # setup
        generation = self.create_obj(
            model=Generation,
            data=GENERATION_DATA
        )
        dexentry = self.create_obj(
            model=DexEntry,
            data=DEXENTRY_DATA
        )
        pokemon = self.create_obj(
            model=Pokemon,
            data=POKEMON_DATA
        )

        csv_data = {
            'number': dexentry.number,
            'name': dexentry.name,
            'form': pokemon.form,
            'sprite': pokemon.sprite,
            'generation': generation.number,
            'lgplge': False,
            'swsh': pokemon.swsh,
            'arceus': pokemon.arceus,
            'bdsp': pokemon.bdsp,
            'sv': pokemon.sv
        }

        # pre condition
        self.assertNotEqual(pokemon.lgplge, csv_data['lgplge'])

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 1)

        self.assertEqual(self.importer.imported, 0)
        self.assertEqual(self.importer.updated, 0)

        # do it
        result = self.importer._handle_pokemon(
            dexentry_id=dexentry.id,
            dataset=csv_data
        )

        # post condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 1)

        self.assertIsInstance(result, Pokemon)
        self.assertEqual(result.form, pokemon.form)
        self.assertEqual(result.sprite, pokemon.sprite)
        self.assertEqual(result.caught, pokemon.caught)
        self.assertEqual(result.shiny_caught, pokemon.shiny_caught)
        self.assertEqual(result.lgplge, csv_data['lgplge'])
        self.assertEqual(result.swsh, pokemon.swsh)
        self.assertEqual(result.arceus, pokemon.arceus)
        self.assertEqual(result.bdsp, pokemon.bdsp)
        self.assertEqual(result.sv, pokemon.sv)
        self.assertEqual(result.dexentry_id, pokemon.dexentry_id)

        self.assertEqual(self.importer.imported, 0)
        self.assertEqual(self.importer.updated, 1)

    def test_run_import(self):
        # pre condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 0)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 0)

        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 0)

        # do it
        result = self.importer.run_import(pokedex_id=self.pokedex.id)

        # post condition
        self.assertEqual(result[0], 0)  # skipped
        self.assertEqual(result[1], 0)  # updated
        self.assertEqual(result[2], 39)  # imported

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

    def test_run_import___no_data(self):
        # setup
        file_name = 'test-dex-data_wrong_data_type.csv'
        self.importer.__init__(
            file_path=self.file_path,
            file_name=file_name,
            env='testing'
        )

        # pre condition
        self.assertTrue(path.isfile(self.importer.file))

        # do it
        result = self.importer.run_import(pokedex_id=self.pokedex.id)

        # post condition
        self.assertIsNone(result)

    def test_run_import___no_pokedex(self):
        # setup
        invalid_pokedex_id = 0000

        # pre condition
        self.assertIsNone(self.db.get_pokdex(_id=invalid_pokedex_id))

        # do it
        result = self.importer.run_import(pokedex_id=invalid_pokedex_id)

        # post condition
        self.assertIsNone(result)

    def test_run_import___missing_values(self):
        # setup
        file_name = 'test-dex-data_na_values.csv'
        self.importer.__init__(
            file_path=self.file_path,
            file_name=file_name,
            env='testing'
        )

        # pre condition
        self.assertTrue(path.isfile(self.importer.file))

        # do it
        result = self.importer.run_import(pokedex_id=self.pokedex.id)

        # post condition
        self.assertEqual(result[0], 1)  # skipped
        self.assertEqual(result[1], 0)  # updated
        self.assertEqual(result[2], 0)  # imported
