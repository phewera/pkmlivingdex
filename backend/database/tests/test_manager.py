from copy import deepcopy

from database.models import Pokedex, Generation, DexEntry, Pokemon
from database.tests.base import DatabaseTestCase, POKEDEX_DATA, GENERATION_DATA, DEXENTRY_DATA, POKEMON_DATA


class TestDatabaseManager(DatabaseTestCase):

    def test_create_pokedex(self):
        # setup
        data = {
            'title': 'pokedex-1'
        }

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 0)

        # do it
        result = self.db.create_pokedex(data)

        # post condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        self.assertIsInstance(result, Pokedex)
        self.assertEqual(result.title, data['title'])

    def test_create_pokedex__title_already_taken(self):
        # setup
        data = {
            'title': 'pokedex-1'
        }
        self.create_obj(Pokedex, data)

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        # do it
        result = self.db.create_pokedex(data)

        # post condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        self.assertIsNone(result)

    def test_create_generation(self):
        # setup
        pokedex = self.create_obj(Pokedex, POKEDEX_DATA)
        data = {
            'number': 1,
            'sprite': 'gen_1.png',
            'pokedex_id': pokedex.id
        }

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 0)

        # do it
        result = self.db.create_generation(data)

        # post condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        self.assertIsInstance(result, Generation)
        self.assertEqual(result.number, data['number'])
        self.assertEqual(result.sprite, data['sprite'])
        self.assertEqual(result.pokedex_id, data['pokedex_id'])
        self.assertEqual(result.pokedex, pokedex)

    def test_create_generation__two_generations(self):
        # setup
        pokedex: Pokedex = self.create_obj(Pokedex, POKEDEX_DATA)
        generation: Generation = self.create_obj(Generation, GENERATION_DATA)
        generation.pokedex_id = pokedex.id
        data = {
            'number': 2,
            'sprite': 'gen_2.png',
            'pokedex_id': pokedex.id
        }

        # pre condition
        self.assertEqual(generation.pokedex_id, pokedex.id)
        self.assertNotEqual(generation.number, data['number'])

        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        # do it
        result = self.db.create_generation(data)

        # post condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 2)

        self.assertIsInstance(result, Generation)
        self.assertEqual(result.number, data['number'])
        self.assertEqual(result.sprite, data['sprite'])
        self.assertEqual(result.pokedex_id, data['pokedex_id'])
        self.assertEqual(result.pokedex, pokedex)

    def test_create_generation__missing_pokedex_reference(self):
        # setup
        self.create_obj(Pokedex, POKEDEX_DATA)
        data = {
            'number': 1,
            'sprite': 'gen_1.png'
        }

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 0)

        # do it
        # noinspection PyTypeChecker
        result = self.db.create_generation(data)

        # post condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 0)

        self.assertIsNone(result)

    def test_create_generation__invalid_pokedex_reference(self):
        # setup
        self.create_obj(Pokedex, POKEDEX_DATA)
        data = {
            'number': 1,
            'sprite': 'gen_1.png',
            'pokedex_id': 0000
        }

        # pre condition
        self.assertIsNone(self.db._get(model=Pokedex, _id=data['pokedex_id']))

        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 0)

        # do it
        result = self.db.create_generation(data)

        # post condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 0)

        self.assertIsNone(result)

    def test_create_generation__number_already_exists(self):
        pokedex: Pokedex = self.create_obj(Pokedex, POKEDEX_DATA)
        data = {
            'number': 1,
            'sprite': 'gen_1.png',
            'pokedex_id': pokedex.id
        }
        generation: Generation = self.create_obj(Generation, data)
        generation.pokedex_id = pokedex.id

        # pre condition
        self.assertEqual(generation.pokedex_id, pokedex.id)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        # do it
        result = self.db.create_generation(data)

        # post condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        self.assertIsNone(result)

    def test_create_dexentry(self):
        # setup
        pokedex: Pokedex = self.create_obj(Pokedex, POKEDEX_DATA)
        generation: Generation = self.create_obj(Generation, GENERATION_DATA)
        generation.pokedex_id = pokedex.id
        data = {
            'number': 1,
            'name': 'Bulbasaur',
            'generation_id': generation.id
        }

        # pre condition
        self.assertEqual(generation.pokedex_id, pokedex.id)

        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 0)

        # do it
        result = self.db.create_dexentry(data)

        # post condition
        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        self.assertIsInstance(result, DexEntry)
        self.assertEqual(result.number, data['number'])
        self.assertEqual(result.name, data['name'])
        self.assertEqual(result.generation_id, data['generation_id'])
        self.assertEqual(result.generation, generation)

    def test_create_dexentry__two_dexentries(self):
        # setup
        pokedex: Pokedex = self.create_obj(Pokedex, POKEDEX_DATA)
        generation: Generation = self.create_obj(Generation, GENERATION_DATA)
        generation.pokedex_id = pokedex.id
        dexentry: DexEntry = self.create_obj(DexEntry, DEXENTRY_DATA)
        dexentry.generation_id = generation.id
        data = {
            'number': 2,
            'name': 'Ivysaur',
            'generation_id': generation.id
        }

        # pre condition
        self.assertEqual(generation.pokedex_id, pokedex.id)
        self.assertEqual(dexentry.generation_id, generation.id)

        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        # do it
        result = self.db.create_dexentry(data)

        # post condition
        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 2)

        self.assertIsInstance(result, DexEntry)
        self.assertEqual(result.number, data['number'])
        self.assertEqual(result.name, data['name'])
        self.assertEqual(result.generation_id, data['generation_id'])
        self.assertEqual(result.generation, generation)

    def test_create_dexentry__missing_generation_reference(self):
        # setup
        pokedex: Pokedex = self.create_obj(Pokedex, POKEDEX_DATA)
        generation: Generation = self.create_obj(Generation, GENERATION_DATA)
        generation.pokedex_id = pokedex.id
        data = {
            'number': 1,
            'name': 'Bulbasaur',
        }

        # pre condition
        self.assertEqual(generation.pokedex_id, pokedex.id)

        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 0)

        # do it
        # noinspection PyTypeChecker
        result = self.db.create_dexentry(data)

        # post condition
        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 0)

        self.assertIsNone(result)

    def test_create_dexentry__invalid_generation_reference(self):
        # setup
        pokedex: Pokedex = self.create_obj(Pokedex, POKEDEX_DATA)
        generation: Generation = self.create_obj(Generation, GENERATION_DATA)
        generation.pokedex_id = pokedex.id
        data = {
            'number': 1,
            'name': 'Bulbasaur',
            'generation_id': 0000
        }

        # pre condition
        self.assertEqual(generation.pokedex_id, pokedex.id)
        self.assertIsNone(self.db._get(model=Generation, _id=data['generation_id']))

        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 0)

        # do it
        result = self.db.create_dexentry(data)

        # post condition
        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 0)

        self.assertIsNone(result)

    def test_create_dexentry__number_already_exists(self):
        # setup
        pokedex: Pokedex = self.create_obj(Pokedex, POKEDEX_DATA)
        generation: Generation = self.create_obj(Generation, GENERATION_DATA)
        generation.pokedex_id = pokedex.id
        data = {
            'number': 1,
            'name': 'Bulbasaur',
            'generation_id': generation.id
        }
        dexentry: DexEntry = self.create_obj(DexEntry, data)

        # pre condition
        self.assertEqual(generation.pokedex_id, pokedex.id)
        self.assertEqual(dexentry.generation_id, generation.id)

        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        # do it
        result = self.db.create_dexentry(data)

        # post condition
        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        self.assertIsNone(result)

    def test_create_pokemon(self):
        # setup
        pokedex: Pokedex = self.create_obj(Pokedex, POKEDEX_DATA)
        generation: Generation = self.create_obj(Generation, GENERATION_DATA)
        generation.pokedex_id = pokedex.id
        dexentry: DexEntry = self.create_obj(DexEntry, DEXENTRY_DATA)
        dexentry.generation_id = generation.id
        data = {
            'form': 1,
            'sprite': 'bulbasaur_1.png',
            'caught': False,
            'shiny_caught': False,
            'lgplge': True,
            'swsh': True,
            'bdsp': True,
            'sv': False,
            'dexentry_id': dexentry.id,
        }

        # pre condition
        self.assertEqual(generation.pokedex_id, pokedex.id)
        self.assertEqual(dexentry.generation_id, generation.id)

        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 0)

        # do it
        result = self.db.create_pokemon(data)

        # post condition
        dexentries = self.db.session.query(Pokemon).all()
        self.assertEqual(len(dexentries), 1)

        self.assertIsInstance(result, Pokemon)
        self.assertEqual(result.form, data['form'])
        self.assertEqual(result.sprite, data['sprite'])
        self.assertEqual(result.caught, data['caught'])
        self.assertEqual(result.shiny_caught, data['shiny_caught'])
        self.assertEqual(result.lgplge, data['lgplge'])
        self.assertEqual(result.swsh, data['swsh'])
        self.assertEqual(result.bdsp, data['bdsp'])
        self.assertEqual(result.sv, data['sv'])
        self.assertEqual(result.dexentry_id, data['dexentry_id'])
        self.assertEqual(result.dexentry, dexentry)

    def test_create_pokemon__two_pokemon(self):
        # setup
        pokedex: Pokedex = self.create_obj(Pokedex, POKEDEX_DATA)
        generation: Generation = self.create_obj(Generation, GENERATION_DATA)
        generation.pokedex_id = pokedex.id
        dexentry: DexEntry = self.create_obj(DexEntry, DEXENTRY_DATA)
        dexentry.generation_id = generation.id
        pokemon: Pokemon = self.create_obj(Pokemon, POKEMON_DATA)
        pokemon.dexentry_id = dexentry.id
        data = {
            'form': 2,
            'sprite': 'bulbasaur_2.png',
            'caught': False,
            'shiny_caught': False,
            'lgplge': True,
            'swsh': False,
            'bdsp': False,
            'sv': False,
            'dexentry_id': dexentry.id,
        }

        # pre condition
        self.assertEqual(generation.pokedex_id, pokedex.id)
        self.assertEqual(dexentry.generation_id, generation.id)
        self.assertEqual(pokemon.dexentry_id, dexentry.id)

        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 1)

        # do it
        result = self.db.create_pokemon(data)

        # post condition
        dexentries = self.db.session.query(Pokemon).all()
        self.assertEqual(len(dexentries), 2)

        self.assertIsInstance(result, Pokemon)
        self.assertEqual(result.form, data['form'])
        self.assertEqual(result.sprite, data['sprite'])
        self.assertEqual(result.caught, data['caught'])
        self.assertEqual(result.shiny_caught, data['shiny_caught'])
        self.assertEqual(result.lgplge, data['lgplge'])
        self.assertEqual(result.swsh, data['swsh'])
        self.assertEqual(result.bdsp, data['bdsp'])
        self.assertEqual(result.sv, data['sv'])
        self.assertEqual(result.dexentry_id, data['dexentry_id'])
        self.assertEqual(result.dexentry, dexentry)

    def test_create_pokemon__missing_dexentry_reference(self):
        # setup
        pokedex: Pokedex = self.create_obj(Pokedex, POKEDEX_DATA)
        generation: Generation = self.create_obj(Generation, GENERATION_DATA)
        generation.pokedex_id = pokedex.id
        dexentry: DexEntry = self.create_obj(DexEntry, DEXENTRY_DATA)
        dexentry.generation_id = generation.id
        data = {
            'form': 1,
            'sprite': 'bulbasaur_1.png',
            'caught': False,
            'shiny_caught': False,
            'lgplge': True,
            'swsh': True,
            'bdsp': True,
            'sv': False
        }

        # pre condition
        self.assertEqual(generation.pokedex_id, pokedex.id)
        self.assertEqual(dexentry.generation_id, generation.id)

        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 0)

        # do it
        # noinspection PyTypeChecker
        result = self.db.create_pokemon(data)

        # post condition
        dexentries = self.db.session.query(Pokemon).all()
        self.assertEqual(len(dexentries), 0)

        self.assertIsNone(result)

    def test_create_pokemon__invalid_dexentry_reference(self):
        # setup
        pokedex: Pokedex = self.create_obj(Pokedex, POKEDEX_DATA)
        generation: Generation = self.create_obj(Generation, GENERATION_DATA)
        generation.pokedex_id = pokedex.id
        dexentry: DexEntry = self.create_obj(DexEntry, DEXENTRY_DATA)
        dexentry.generation_id = generation.id
        data = {
            'form': 1,
            'sprite': 'bulbasaur_1.png',
            'caught': False,
            'shiny_caught': False,
            'lgplge': True,
            'swsh': True,
            'bdsp': True,
            'sv': False,
            'dexentry_id': 0000
        }

        # pre condition
        self.assertEqual(generation.pokedex_id, pokedex.id)
        self.assertEqual(dexentry.generation_id, generation.id)
        self.assertIsNone(self.db._get(model=DexEntry, _id=data['dexentry_id']))

        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 0)

        # do it
        result = self.db.create_pokemon(data)

        # post condition
        dexentries = self.db.session.query(Pokemon).all()
        self.assertEqual(len(dexentries), 0)

        self.assertIsNone(result)

    def test_create_pokemon__form_already_exists(self):
        # setup
        pokedex: Pokedex = self.create_obj(Pokedex, POKEDEX_DATA)
        generation: Generation = self.create_obj(Generation, GENERATION_DATA)
        generation.pokedex_id = pokedex.id
        dexentry: DexEntry = self.create_obj(DexEntry, DEXENTRY_DATA)
        dexentry.generation_id = generation.id
        data = {
            'form': 1,
            'sprite': 'bulbasaur_1.png',
            'caught': False,
            'shiny_caught': False,
            'lgplge': True,
            'swsh': True,
            'bdsp': True,
            'sv': False,
            'dexentry_id': dexentry.id,
        }
        pokemon: Pokemon = self.create_obj(Pokemon, POKEMON_DATA)

        # pre condition
        self.assertEqual(generation.pokedex_id, pokedex.id)
        self.assertEqual(dexentry.generation_id, generation.id)
        self.assertEqual(pokemon.dexentry_id, dexentry.id)

        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 1)

        # do it
        result = self.db.create_pokemon(data)

        # post condition
        dexentries = self.db.session.query(Pokemon).all()
        self.assertEqual(len(dexentries), 1)

        self.assertIsNone(result)

    def test__create(self):
        # setup
        data = {
            'title': 'pokedex-1'
        }

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 0)

        # do it
        result = self.db._create(model=Pokedex, data=data)

        # post condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        self.assertIsInstance(result, Pokedex)
        self.assertEqual(result.title, data['title'])

    def test__create__IntegrityError(self):
        # setup
        data = {
            'title': 'pokedex-1'
        }
        self.create_obj(Pokedex, data)

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        # do it
        result = self.db._create(model=Pokedex, data=data)

        # post condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        self.assertIsNone(result)

    def test__validate_reference(self):
        # setup
        pokedex = self.create_obj(model=Pokedex, data=POKEDEX_DATA)

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)
        self.assertEqual(pokedex, pokedexes[0])

        # do it
        result = self.db._validate_reference(model=Pokedex, _id=pokedex.id)

        # post condition
        self.assertTrue(result)

    def test__validate_reference__reference_not_found(self):
        # setup
        pokedex = self.create_obj(model=Pokedex, data=POKEDEX_DATA)
        test_id = 0000

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)
        self.assertEqual(pokedex, pokedexes[0])
        self.assertNotEqual(pokedex.id, test_id)

        # do it
        result = self.db._validate_reference(model=Pokedex, _id=test_id)

        # post condition
        self.assertFalse(result)

    def test__validate_reference__no_data_available(self):
        # setup
        test_id = 0000

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 0)

        # do it
        result = self.db._validate_reference(model=Pokedex, _id=test_id)

        # post condition
        self.assertFalse(result)

    def test_update_pokedex(self):
        # setup
        pokedex = self.create_obj(
            model=Pokedex,
            data=POKEDEX_DATA
        )
        update_data = {
            'title': 'test-pokedex-changed'
        }

        # pre condition
        self.assertNotEqual(pokedex.title, update_data['title'])

        # do it
        result = self.db.update_pokedex(_id=pokedex.id, data=update_data)

        # post condition
        self.assertTrue(result)
        self.assertEqual(pokedex.title, update_data['title'])

    def test_update_pokedex__invalid_id(self):
        # setup
        pokedex = self.create_obj(
            model=Pokedex,
            data=POKEDEX_DATA
        )
        invalid_id = 0000
        update_data = {
            'title': 'test-pokedex-changed'
        }

        # pre condition
        self.assertNotEqual(pokedex.title, update_data['title'])

        # do it
        result = self.db.update_pokedex(_id=invalid_id, data=update_data)

        # post condition
        self.assertFalse(result)
        self.assertNotEqual(pokedex.title, update_data['title'])

    def test_update_generation(self):
        # setup
        generation = self.create_obj(
            model=Generation,
            data=GENERATION_DATA
        )
        update_data = {
            'sprite': 'gen_1-changed.png'
        }

        # pre condition
        self.assertNotEqual(generation.sprite, update_data['sprite'])

        # do it
        result = self.db.update_generation(_id=generation.id, data=update_data)

        # post condition
        self.assertTrue(result)
        self.assertEqual(generation.sprite, update_data['sprite'])

    def test_update_generation__invalid_id(self):
        # setup
        generation = self.create_obj(
            model=Generation,
            data=GENERATION_DATA
        )
        invalid_id = 0000
        update_data = {
            'sprite': 'gen_1-changed.png'
        }

        # pre condition
        self.assertNotEqual(generation.sprite, update_data['sprite'])

        # do it
        result = self.db.update_generation(_id=invalid_id, data=update_data)

        # post condition
        self.assertFalse(result)
        self.assertNotEqual(generation.sprite, update_data['sprite'])

    def test_update_dexentry(self):
        # setup
        dexentry = self.create_obj(
            model=DexEntry,
            data=DEXENTRY_DATA
        )
        update_data = {
            'name': 'Bulbasaur-changed'
        }

        # pre condition
        self.assertNotEqual(dexentry.name, update_data['name'])

        # do it
        result = self.db.update_dexentry(_id=dexentry.id, data=update_data)

        # post condition
        self.assertTrue(result)
        self.assertEqual(dexentry.name, update_data['name'])

    def test_update_dexentry__invalid_id(self):
        # setup
        dexentry = self.create_obj(
            model=DexEntry,
            data=DEXENTRY_DATA
        )
        invalid_id = 0000
        update_data = {
            'name': 'Bulbasaur-changed'
        }

        # pre condition
        self.assertNotEqual(dexentry.name, update_data['name'])

        # do it
        result = self.db.update_dexentry(_id=invalid_id, data=update_data)

        # post condition
        self.assertFalse(result)
        self.assertNotEqual(dexentry.name, update_data['name'])

    def test_update_pokemon(self):
        # setup
        pokemon = self.create_obj(
            model=Pokemon,
            data=POKEMON_DATA
        )
        update_data = {
            'sprite': 'bulbasaur_1-changed.png'
        }

        # pre condition
        self.assertNotEqual(pokemon.sprite, update_data['sprite'])

        # do it
        result = self.db.update_pokemon(_id=pokemon.id, data=update_data)

        # post condition
        self.assertTrue(result)
        self.assertEqual(pokemon.sprite, update_data['sprite'])

    def test_update_pokemon__invalid_id(self):
        # setup
        pokemon = self.create_obj(
            model=Pokemon,
            data=POKEMON_DATA
        )
        invalid_id = 0000
        update_data = {
            'sprite': 'bulbasaur_1-changed.png'
        }

        # pre condition
        self.assertNotEqual(pokemon.sprite, update_data['sprite'])

        # do it
        result = self.db.update_pokemon(_id=invalid_id, data=update_data)

        # post condition
        self.assertFalse(result)
        self.assertNotEqual(pokemon.sprite, update_data['sprite'])

    def test__update(self):
        # setup
        pokedex = self.create_obj(
            model=Pokedex,
            data=POKEDEX_DATA
        )
        update_data = {
            'title': 'test-pokedex-changed'
        }

        # pre condition
        self.assertNotEqual(pokedex.title, update_data['title'])

        # do it
        result = self.db._update(model=Pokedex, _id=pokedex.id, data=update_data)

        # post condition
        self.assertTrue(result)
        self.assertEqual(pokedex.title, update_data['title'])

    def test__update__invalid_id(self):
        # setup
        pokedex = self.create_obj(
            model=Pokedex,
            data=POKEDEX_DATA
        )
        invalid_id = 0000
        update_data = {
            'title': 'test-pokedex-changed'
        }

        # pre condition
        self.assertNotEqual(pokedex.title, update_data['title'])

        # do it
        result = self.db._update(model=Pokedex, _id=invalid_id, data=update_data)

        # post condition
        self.assertFalse(result)
        self.assertNotEqual(pokedex.title, update_data['title'])

    def test__get(self):
        # setup
        pokedex: Pokedex = self.create_obj(
            model=Pokedex,
            data=POKEDEX_DATA
        )

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        # do it
        result = self.db._get(model=Pokedex, _id=pokedex.id)

        # post condition
        self.assertEqual(result, pokedex)

    def test__get__no_result(self):
        # setup
        self.create_obj(
            model=Pokedex,
            data=POKEDEX_DATA
        )

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        # do it
        result = self.db._get(model=Pokedex, _id=0000)

        # post condition
        self.assertIsNone(result)

    def test__get_all(self):
        # setup
        pokedex1: Pokedex = self.create_obj(
            model=Pokedex,
            data=POKEDEX_DATA
        )

        data = deepcopy(POKEDEX_DATA)
        data['title'] = 'test-pokedex-2'
        pokedex2: Pokedex = self.create_obj(Pokedex, data)

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 2)

        # do it
        result = self.db._get_all(model=Pokedex)

        # post condition
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], pokedex1)
        self.assertEqual(result[1], pokedex2)

    def test__get_all__no_results(self):
        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 0)

        # do it
        result = self.db._get_all(model=Pokedex)

        # post condition
        self.assertEqual(len(result), 0)

    def test__format_data(self):
        self.skipTest('ToDo')

    def test_delete_pokedex(self):
        # setup
        pokedex = self.create_obj(
            model=Pokedex,
            data=POKEDEX_DATA
        )

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        # do it
        result = self.db.delete_pokedex(pokedex.id)

        # post condition
        self.assertTrue(result)

        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 0)

    def test_delete_pokdex__invalid_id(self):
        # setup
        invalid_id = 0000
        self.create_obj(
            model=Pokedex,
            data=POKEDEX_DATA
        )

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        # do it
        result = self.db.delete_pokedex(invalid_id)

        # post condition
        self.assertFalse(result)

        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

    def test_delete_generation(self):
        # setup
        generation = self.create_obj(
            model=Generation,
            data=GENERATION_DATA
        )

        # pre condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        # do it
        result = self.db.delete_generation(generation.id)

        # post condition
        self.assertTrue(result)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 0)

    def test_delete_generation__invalid_id(self):
        # setup
        invalid_id = 0000
        self.create_obj(
            model=Generation,
            data=GENERATION_DATA
        )

        # pre condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        # do it
        result = self.db.delete_pokedex(invalid_id)

        # post condition
        self.assertFalse(result)

        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

    def test_delete_dexentry(self):
        # setup
        dexentry = self.create_obj(
            model=DexEntry,
            data=DEXENTRY_DATA
        )

        # pre condition
        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        # do it
        result = self.db.delete_dexentry(dexentry.id)

        # post condition
        self.assertTrue(result)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 0)

    def test_delete_dexentry__invalid_id(self):
        # setup
        invalid_id = 0000
        self.create_obj(
            model=DexEntry,
            data=DEXENTRY_DATA
        )

        # pre condition
        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        # do it
        result = self.db.delete_dexentry(invalid_id)

        # post condition
        self.assertFalse(result)

        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

    def test_delete_pokemon(self):
        # setup
        pokemon = self.create_obj(
            model=Pokemon,
            data=POKEMON_DATA
        )

        # pre condition
        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 1)

        # do it
        result = self.db.delete_pokemon(pokemon.id)

        # post condition
        self.assertTrue(result)

        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 0)

    def test_delete_pokemon__invalid_id(self):
        # setup
        invalid_id = 0000
        self.create_obj(
            model=Pokemon,
            data=POKEMON_DATA
        )

        # pre condition
        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 1)

        # do it
        result = self.db.delete_pokemon(invalid_id)

        # post condition
        self.assertFalse(result)

        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 1)

    def test__delete(self):
        # setup
        pokedex = self.create_obj(
            model=Pokedex,
            data=POKEDEX_DATA
        )

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        # do it
        result = self.db._delete(model=Pokedex, _id=pokedex.id)

        # post condition
        self.assertTrue(result)

        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 0)

    def test__delete__invalid_id(self):
        # setup
        invalid_id = 0000
        self.create_obj(
            model=Pokedex,
            data=POKEDEX_DATA
        )

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        # do it
        result = self.db._delete(model=Pokedex, _id=invalid_id)

        # post condition
        self.assertFalse(result)

        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

    def test_get_pokedex(self):
        # setup
        pokedex = self.create_obj(
            model=Pokedex,
            data=POKEDEX_DATA
        )

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        # do it
        result = self.db.get_pokdex(pokedex.id)

        # post condition
        self.assertEqual(result, pokedex)

    def test_get_pokedex__no_result(self):
        # setup
        unknown_id = 0000
        self.create_obj(
            model=Pokedex,
            data=POKEDEX_DATA
        )

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        # do it
        result = self.db.get_pokdex(unknown_id)

        # post condition
        self.assertIsNone(result)

    def test_get_pokedexes(self):
        # setup
        pokedex = self.create_obj(
            model=Pokedex,
            data=POKEDEX_DATA
        )

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        # do it
        result = self.db.get_pokdexes()

        # post condition
        self.assertEqual(len(pokedexes), len(result))
        self.assertEqual(result[0], pokedex)

    def test_get_pokedexes__no_results(self):
        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 0)

        # do it
        result = self.db.get_pokdexes()

        # post condition
        self.assertEqual(len(result), 0)

    def test_get_generation(self):
        # setup
        generation = self.create_obj(
            model=Generation,
            data=GENERATION_DATA
        )

        # pre condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        # do it
        result = self.db.get_generation(generation.id)

        # post condition
        self.assertEqual(result, generation)

    def test_get_generation__no_result(self):
        # setup
        unknown_id = 0000
        self.create_obj(
            model=Generation,
            data=GENERATION_DATA
        )

        # pre condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        # do it
        result = self.db.get_generation(unknown_id)

        # post condition
        self.assertIsNone(result)

    def test_get_generations(self):
        # setup
        generation = self.create_obj(
            model=Generation,
            data=GENERATION_DATA
        )

        # pre condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        # do it
        result = self.db.get_generations()

        # post condition
        self.assertEqual(len(generations), len(result))
        self.assertEqual(result[0], generation)

    def test_get_generations__no_results(self):
        # pre condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 0)

        # do it
        result = self.db.get_generations()

        # post condition
        self.assertEqual(len(result), 0)

    def test_get_dexentry(self):
        # setup
        dexentry = self.create_obj(
            model=DexEntry,
            data=DEXENTRY_DATA
        )

        # pre condition
        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        # do it
        result = self.db.get_dexentry(dexentry.id)

        # post condition
        self.assertEqual(result, dexentry)

    def test_get_dexentry__no_result(self):
        # setup
        unknown_id = 0000
        self.create_obj(
            model=DexEntry,
            data=DEXENTRY_DATA
        )

        # pre condition
        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        # do it
        result = self.db.get_dexentry(unknown_id)

        # post condition
        self.assertIsNone(result)

    def test_get_dexentries(self):
        # setup
        dexentry = self.create_obj(
            model=DexEntry,
            data=DEXENTRY_DATA
        )

        # pre condition
        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

        # do it
        result = self.db.get_dexentries()

        # post condition
        self.assertEqual(len(dexentries), len(result))
        self.assertEqual(result[0], dexentry)

    def test_get_dexentries__no_results(self):
        # pre condition
        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 0)

        # do it
        result = self.db.get_dexentries()

        # post condition
        self.assertEqual(len(result), 0)

    def test_get_pokemon(self):
        # setup
        pokemon = self.create_obj(
            model=Pokemon,
            data=POKEMON_DATA
        )

        # pre condition
        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 1)

        # do it
        result = self.db.get_pokemon(pokemon.id)

        # post condition
        self.assertEqual(result, pokemon)

    def test_get_pokemon__no_result(self):
        # setup
        unknown_id = 0000
        self.create_obj(
            model=Pokemon,
            data=POKEMON_DATA
        )

        # pre condition
        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 1)

        # do it
        result = self.db.get_pokemon(unknown_id)

        # post condition
        self.assertIsNone(result)

    def test_get_pokemons(self):
        # setup
        pokemon = self.create_obj(
            model=Pokemon,
            data=POKEMON_DATA
        )

        # pre condition
        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 1)

        # do it
        result = self.db.get_pokemons()

        # post condition
        self.assertEqual(len(pokemons), len(result))
        self.assertEqual(result[0], pokemon)

    def test_get_pokemons__no_results(self):
        # pre condition
        pokemons = self.db.session.query(Pokemon).all()
        self.assertEqual(len(pokemons), 0)

        # do it
        result = self.db.get_pokemons()

        # post condition
        self.assertEqual(len(result), 0)
