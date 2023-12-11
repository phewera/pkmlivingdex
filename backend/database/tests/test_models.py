from copy import deepcopy
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

    def test__base__get_data(self):
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

    def test__base__get_data__json_friendly(self):
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

    def test__base__get_field_ids__pokedex(self):
        # do it
        result = self.pokedex.get_field_ids()

        # post condition
        expected_field_ids = set(TPokedexData.__annotations__.keys())
        self.assertEqual(set(result), expected_field_ids)

    def test__base__get_field_ids__generation(self):
        # do it
        result = self.generation.get_field_ids()

        # post condition
        expected_field_ids = set(TGenerationData.__annotations__.keys())
        self.assertEqual(set(result), expected_field_ids)

    def test__base__get_field_ids__dexentry(self):
        # do it
        result = self.dexentry.get_field_ids()

        # post condition
        expected_field_ids = set(TDexEntryData.__annotations__.keys())
        self.assertEqual(set(result), expected_field_ids)

    def test__base__get_field_ids__pokemon(self):
        # do it
        result = self.pokemon.get_field_ids()

        # post condition
        expected_field_ids = set(TPokemonData.__annotations__.keys())
        self.assertEqual(set(result), expected_field_ids)

    def test__base__update(self):
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

    def test__base__update__nothing_to_update(self):
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

    def test__base__update__invalid_data(self):
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

    def test__generation__get_pokemon_count(self):
        # post condition
        self.assertFalse(self.pokemon.caught)
        self.assertFalse(self.pokemon.shiny_caught)

        # do it
        result = self.generation.get_pokemon_count()

        # post condition
        self.assertEqual(result[0], len(self.dexentry.pokemons))
        self.assertEqual(result[1], 0)

    def test__generation__get_pokemon_count__pokemon_caught(self):
        # setup
        self.pokemon.caught = True

        # post condition
        self.assertTrue(self.pokemon.caught)
        self.assertFalse(self.pokemon.shiny_caught)

        # do it
        result = self.generation.get_pokemon_count()

        # post condition
        self.assertEqual(result[0], len(self.dexentry.pokemons))
        self.assertEqual(result[1], 1)

    def test__generation__get_pokemon_count__pokemon_shiny_caught(self):
        # setup
        self.pokemon.shiny_caught = True

        # post condition
        self.assertTrue(self.pokemon.shiny_caught)
        self.assertFalse(self.pokemon.caught)

        # do it
        result = self.generation.get_pokemon_count()

        # post condition
        self.assertEqual(result[0], len(self.dexentry.pokemons))
        self.assertEqual(result[1], 1)

    def test__generation__get_pokemon_count__2_pokemon(self):
        # setup
        data = deepcopy(POKEMON_DATA)
        data['form'] = 2
        pokemon2 = self.create_obj(Pokemon, data)

        # post condition
        self.assertEqual(len(self.dexentry.pokemons), 2)

        self.assertFalse(self.pokemon.caught)
        self.assertFalse(self.pokemon.shiny_caught)

        self.assertFalse(pokemon2.caught)
        self.assertFalse(pokemon2.shiny_caught)

        # do it
        result = self.generation.get_pokemon_count()

        # post condition
        self.assertEqual(result[0], len(self.dexentry.pokemons))
        self.assertEqual(result[1], 0)

    def test__generation__get_pokemon_count__2_pokemon__1_caught(self):
        # setup
        data = deepcopy(POKEMON_DATA)
        data['form'] = 2
        data['caught'] = True
        pokemon2 = self.create_obj(Pokemon, data)

        # post condition
        self.assertEqual(len(self.dexentry.pokemons), 2)

        self.assertFalse(self.pokemon.caught)
        self.assertFalse(self.pokemon.shiny_caught)

        self.assertTrue(pokemon2.caught)
        self.assertFalse(pokemon2.shiny_caught)

        # do it
        result = self.generation.get_pokemon_count()

        # post condition
        self.assertEqual(result[0], len(self.dexentry.pokemons))
        self.assertEqual(result[1], 1)

    def test__generation__get_pokemon_count__2_dexentries_with_forms(self):
        # setup
        dexentry_data = deepcopy(DEXENTRY_DATA)
        dexentry_data['number'] = 2
        dexentry2 = self.create_obj(DexEntry, dexentry_data)

        data = deepcopy(POKEMON_DATA)
        data['dexentry_id'] = dexentry2.id
        pokemon2 = self.create_obj(Pokemon, data)

        # post condition
        self.assertEqual(len(self.dexentry.pokemons), 1)
        self.assertEqual(len(dexentry2.pokemons), 1)

        self.assertFalse(self.pokemon.caught)
        self.assertFalse(self.pokemon.shiny_caught)

        self.assertFalse(pokemon2.caught)
        self.assertFalse(pokemon2.shiny_caught)

        # do it
        result = self.generation.get_pokemon_count()

        # post condition
        self.assertEqual(result[0], len(self.dexentry.pokemons) + len(dexentry2.pokemons))
        self.assertEqual(result[1], 0)
