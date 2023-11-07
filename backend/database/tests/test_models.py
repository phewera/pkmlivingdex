from database.models import Pokedex, Generation, DexEntry, Pokemon
from database.models import TPokedexData, TGenerationData, TDexEntryData, TPokemonData
from database.tests.base import DatabaseTestCase, POKEDEX_DATA, GENERATION_DATA, DEXENTRY_DATA, POKEMON_DATA


class TestDatabaseModels(DatabaseTestCase):
    pokedex: Pokedex
    generation: Generation
    dexentry: DexEntry
    pokemon: Pokemon

    def setUp(self) -> None:
        super().setUp()
        self.pokedex = self.create_obj(
            model=Pokedex,
            data=POKEDEX_DATA
        )
        self.generation = self.create_obj(
            model=Generation,
            data=GENERATION_DATA
        )
        self.dexentry = self.create_obj(
            model=DexEntry,
            data=DEXENTRY_DATA
        )
        self.pokemon = self.create_obj(
            model=Pokemon,
            data=POKEMON_DATA
        )

    def test_get_data(self):
        # do it
        result = self.pokemon.get_data()

        # post condition
        expected_keys = set(TPokemonData.__annotations__.keys())
        self.assertEqual(set(result.keys()), expected_keys)

        self.assertEqual(result['id'], self.pokemon.id)
        self.assertEqual(result['form'], self.pokemon.form)
        self.assertEqual(result['sprite'], self.pokemon.sprite)
        self.assertEqual(result['caught'], self.pokemon.caught)
        self.assertEqual(result['shiny_caught'], self.pokemon.shiny_caught)
        self.assertEqual(result['lgplge'], self.pokemon.lgplge)
        self.assertEqual(result['swsh'], self.pokemon.swsh)
        self.assertEqual(result['bdsp'], self.pokemon.bdsp)
        self.assertEqual(result['dexentry_id'], self.pokemon.dexentry_id)
        self.assertEqual(result['dexentry'], self.pokemon.dexentry)

    def test_get_data__json_friendly(self):
        # do it
        result = self.pokemon.get_data(json_friendly=True)

        # post condition
        expected_keys = set(TPokemonData.__annotations__.keys())
        expected_keys.remove('dexentry')
        self.assertEqual(set(result.keys()), expected_keys)
        self.assertNotIn('dexentry', list(result.keys()))

        self.assertEqual(result['id'], self.pokemon.id)
        self.assertEqual(result['form'], self.pokemon.form)
        self.assertEqual(result['sprite'], self.pokemon.sprite)
        self.assertEqual(result['caught'], self.pokemon.caught)
        self.assertEqual(result['shiny_caught'], self.pokemon.shiny_caught)
        self.assertEqual(result['lgplge'], self.pokemon.lgplge)
        self.assertEqual(result['swsh'], self.pokemon.swsh)
        self.assertEqual(result['bdsp'], self.pokemon.bdsp)
        self.assertEqual(result['dexentry_id'], self.pokemon.dexentry_id)

    def test_get_field_ids__pokedex(self):
        # do it
        result = self.pokedex.get_field_ids()

        # post condition
        expected_field_ids = set(TPokedexData.__annotations__.keys())
        self.assertEqual(set(result), expected_field_ids)

    def test_get_field_ids__generation(self):
        # do it
        result = self.generation.get_field_ids()

        # post condition
        expected_field_ids = set(TGenerationData.__annotations__.keys())
        self.assertEqual(set(result), expected_field_ids)

    def test_get_field_ids__dexentry(self):
        # do it
        result = self.dexentry.get_field_ids()

        # post condition
        expected_field_ids = set(TDexEntryData.__annotations__.keys())
        self.assertEqual(set(result), expected_field_ids)

    def test_get_field_ids__pokemon(self):
        # do it
        result = self.pokemon.get_field_ids()

        # post condition
        expected_field_ids = set(TPokemonData.__annotations__.keys())
        self.assertEqual(set(result), expected_field_ids)

    def test_update(self):
        # setup
        data = {
            'sprite': 'bulbasaur_1-changed.png'
        }

        # pre condition
        self.assertNotEqual(self.pokemon.sprite, data['sprite'])

        # do it
        result = self.pokemon.update(data)

        # post condition
        self.assertTrue(result)
        self.assertEqual(self.pokemon.sprite, data['sprite'])

    def test_update__nothing_to_update(self):
        # setup
        data = {
            'sprite': 'bulbasaur_1.png'
        }

        # pre condition
        self.assertEqual(self.pokemon.sprite, data['sprite'])

        # do it
        result = self.pokemon.update(data)

        # post condition
        self.assertFalse(result)
        self.assertEqual(self.pokemon.sprite, data['sprite'])

    def test_update__invalid_data(self):
        # setup
        data = {
            'unknown_attr': 'test'
        }

        # pre condition
        self.assertFalse(hasattr(self.pokemon, 'unknown_attr'))

        # do it
        result = self.pokemon.update(data)

        # post condition
        self.assertFalse(result)
        self.assertFalse(hasattr(self.pokemon, 'unknown_attr'))
