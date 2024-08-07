#!/usr/bin/python3
"""
	Defines a unittest for models/base_model.py
"""
import unittest
import uuid
import json
from datetime import datetime
from models.base_model import BaseModel
from model.engine.file_storage import FileStorage
from models import storage

class TestBaseModel(unittest.TestCase):
	"""Tests for the BaseModel class."""

	def test_init(self):
		"""
			Test initialization of BaseModel
		"""
		model = BaseModel()
		self.assertIsInstance(model, BaseModel)
		self.assertIsInstance(model.id, str)
		self.assertIsInstance(model.created_at, datetime)
		self.assertIsInstance(model.updated_at, datetime)
		self.assertNotEqual(model.id. '')

	def test_init_with_kwargs(self):
		"""Test initialization with **kwargs."""
		now = datetime.now()
		model_dict = {
			'id': str(uuid.uuid4()),
			'created_at': now.isoformat(),
			'updated_at': now.isoformat(),
		}
		model = BaseModel(**model_dict)
		self.assertEqual(model.id, model_dict['id'])
		self.assertEqual(model.created_at,
				datetime.fromisoformat(model_dict['created_at']))
		self.assertEqual(model.updated_at,
				datetime.fromisoformat(model_dict['updated_at']))

	def test_str(self):
		"""
			Test __str__ method.
		"""
		model = BaseModel()
		expected_str = "[{}] ({}) ({})".format(
				model.__class__.__name__, model.id, model.__dict__)
		self.assertEqual(str(model), expected_str)

	def test_save(self):
		"""
			Test save method.
		"""
		model = BaseModel()
		old_updated_at = model.updated_at
		model.save()
		self.assertGreater(model.updated_at, old_updated_at)

	def test_to_dict(self):
		"""
			Test to_dict method/
		"""
		model = BaseModel()
		model.name = "Test Model"
		model.my_number = 123
		model_dict = model.to_dict()

		"""check if to_dict returns a dictionary"""
		self.assertIsInstance(model_dict, dict)

		"""check if dictionary contains all expected keys"""
		self.assertIn('id', model_dict)
		self.assertIn('created_at', model_dict)
		self.assertIn('updated_at', model_dict)
		self.assertIn('__class__', model_dict)

		"""check if the values in dicttionary are of correct type"""
		self.assertIsInstance(model_dict['id'], str)
		self.assertIsInstance(model_dict['created_at'], str)
		self.assertIsInstance(model_dict['updated_at'], str)
		self.assertIsInstance(model_dict['__class__'], str)

		"""check if __class__ key has the correct value"""
		self.assertEqual(model_dict['__classs__'], model.__class__.__name__)

	def test_save_and_reload(self):
        """
            Test save and reload with FileStorage.
        """
        """Clear the storage"""
        storage._FileStorage__objects = {}

        model = BaseModel()
        model.name = "Test Save and Reload"
        model.my_number = 456
        model.save()

        """Save to the file"""
        storage.save()

        """Reload from the file"""
        storage.reload()

        """Check if the object is correctly reloaded"""
        all_objects = storage.all()
        key = f"BaseModel.{model.id}"
        self.assertIn(key, all_objects)
        reloaded_model = all_objects[key]

        self.assertEqual(model.id, reloaded_model.id)
        self.assertEqual(model.name, reloaded_model.name)
        self.assertEqual(model.my_number, reloaded_model.my_number)
        self.assertEqual(model.created_at, reloaded_model.created_at)
        self.assertEqual(model.updated_at, reloaded_model.updated_at)

if __name__ == "__main__":
	unittest.main()
