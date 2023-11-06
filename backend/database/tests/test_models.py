from database.models import Pokedex, Generation, DexEntry, Pokemon
from database.models import TPokedexData, TGenerationData, TDexEntryData, TPokemonData
from database.tests.base import DatabaseTestCase, POKEDEX_DATA, GENERATION_DATA, DEXENTRY_DATA, POKEMON_DATA


class TestDatabaseModels(DatabaseTestCase):
    pokedex: Pokedex
    generation: Generation
    dexentry: DexEntry
    pokemon: Pokemon

    def setUp(self):
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

    def test__data__(self):
        self.skipTest('TODO')

    def test__data__json_friendly(self):
        self.skipTest('TODO')

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
        self.skipTest('TODO')

    def test_update__nothing_to_update(self):
        self.skipTest('TODO')

    def test_update__invalid_data(self):
        self.skipTest('TODO')
