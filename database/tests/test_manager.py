from database.models import Pokedex, Generation, DexEntry
from database.tests.base import DatabaseTestCase, POKEDEX_DATA, GENERATION_DATA, DEXENTRY_DATA


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
        self.assertIsNone(result)
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 0)

    def test_create_generation__invalid_pokedex_reference(self):
        # setup
        self.create_obj(Pokedex, POKEDEX_DATA)
        data = {
            'number': 1,
            'sprite': 'gen_1.png',
            'pokedex_id': 0000
        }

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 0)

        # do it
        result = self.db.create_generation(data)

        # post condition
        self.assertIsNone(result)
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 0)

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
        self.assertIsNone(result)
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

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
        self.assertIsNone(result)
        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 0)

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
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)
        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 0)

        # do it
        result = self.db.create_dexentry(data)

        # post condition
        self.assertIsNone(result)
        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 0)

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
        self.assertIsNone(result)
        dexentries = self.db.session.query(DexEntry).all()
        self.assertEqual(len(dexentries), 1)

    def test_create_pokemon(self):
        self.skipTest('ToDo')

    def test__create(self):
        self.skipTest('ToDo')

    def test__get__by_id(self):
        self.skipTest('ToDo')

    def test__get__all(self):
        self.skipTest('ToDo')

    def test__format_data(self):
        self.skipTest('ToDo')
