#!/usr/bin/python3
"""
	Defines a base class Model.
"""
import models
import uuid
from datetime import datetime

class BaseModel:
	"""
		Represent a BaseModel Class of the hbnb project.
	"""
	def __init__(self, *args, **kwargs):
		"""
			Initializes a new instance of BaseModel.

		Args:
			*args (any): unused.
			**kwargs (dict): key/value pairs of attributes.
		"""
		if len(kwargs) > 0:
			for key, value in kwargs.items():
				if key == '__class__':
					continue
				if key in ['created_at', 'updated_at']:
					value = datetime.fromisoformat(value)
				setattr(self, key, value)
		else:
			self.id = str(uuid.uuid4())
			self.created_at = datetime.now()
			self.updated_at = datetime.now()
			models.storage.new(self)

	def __str__(self):
		"""
			Return a string representation of the instance.
		"""
		return "[{}] ({}) ({})".format(self.__class__.__name__, self.id, self.__dict__)

	def save(self):
		"""
			Update the public insatnce attribute `updated_at` with the current datetime.
		"""
		self.updated_at = datetime.now()
		models.storage.save()

	def to_dict(self):
		"""
			Returns a dictionary containing all keys/values of the instance's __dict__.

			Includes the key/value pair __class__ representing the class name of the object.
		"""
		dict_r = self.__dict__.copy()
		dict_r['created_at'] = self.created_at.isoformat()
		dict_r['updated_at'] = self.updated_at.isoformat()
		dict_r['__class__'] = self.__class__.__name__
		return dict_r
