from database.models import Pokedex, Generation
from database.tests.base import DatabaseTestCase, POKEDEX_DATA, GENERATION_DATA
from database.models import TGenerationData


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
        pokedex = self.create_obj(Pokedex, POKEDEX_DATA)
        generation = self.create_obj(Generation, GENERATION_DATA)
        data = {
            'number': 2,
            'sprite': 'gen_2.png',
            'pokedex_id': pokedex.id
        }

        # pre condition
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
            'pokedex_id': 'invalid-id'
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
        pokedex = self.create_obj(Pokedex, POKEDEX_DATA)
        data = {
            'number': 1,
            'sprite': 'gen_1.png',
            'pokedex_id': pokedex.id
        }
        self.create_obj(Generation, data)

        # pre condition
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

        # do it
        result = self.db.create_generation(data)

        # post condition
        self.assertIsNone(result)
        generations = self.db.session.query(Generation).all()
        self.assertEqual(len(generations), 1)

    def test_create_dexentry(self):
        self.skipTest('ToDo')

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