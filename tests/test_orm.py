import unittest

import factory
from factory.orm import OrmModelFactory
from tests.ormapp import models


class NoteFactory(OrmModelFactory):
    class Meta:
        model = models.Note

    text = factory.Sequence(lambda n: f"Text {n}")
    completed = factory.Faker('boolean')


class ORMTestCase(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        super().setUp()
        NoteFactory.reset_sequence(0)

    def test_build(self):
        note = NoteFactory.build()
        self.assertEqual('Text 0', note.text)
        self.assertIn(note.completed, [True, False])
        self.assertIsNone(note.id)

    async def test_creation(self):
        async with models.database:
            note = await NoteFactory.create_async()
            self.assertEqual('Text 0', note.text)
            self.assertIn(note.completed, [True, False])
            self.assertIsNotNone(note.id)

            count = await models.Note.objects.filter(text__contains="Text").count()
            assert count == 1
