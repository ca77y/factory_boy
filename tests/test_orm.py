import asyncio
import unittest

import factory
from factory.orm import OrmModelFactory
from tests.ormapp import models


class NoteFactory(OrmModelFactory):
    class Meta:
        model = models.Note

    text = factory.Sequence(lambda n: f"Text {n}")
    completed = factory.Faker('boolean')


class ORMTestCase(unittest.TestCase):

    def setUp(self):
        super().setUp()
        NoteFactory.reset_sequence(0)

    def test_build(self):
        note = NoteFactory.build()
        self.assertEqual('Text 0', note.text)
        self.assertIn(note.completed, [True, False])
        self.assertIsNone(note.id)

    def test_creation(self):
        loop = asyncio.get_event_loop()

        async def test():
            async with models.database:
                note = await NoteFactory.create_async()
                count = await models.Note.objects.filter(text__contains="Text").count()

            self.assertEqual('Text 0', note.text)
            self.assertIn(note.completed, [True, False])
            self.assertIsNotNone(note.id)
            self.assertEqual(count, 1)

        loop.run_until_complete(test())
