#!/usr/bin/python3
"""Defines the Place class."""
from models.base_model import BaseModel

class Place(BaseModel):
	"""Represent a Place for the HBNB project.

	Attributes:
		city_id (str): The city id
		user_id (str): The user id
		name (str): The name of the place.
		description (str): The description of the place.
		number_rooms (int): The number of rooms.
		number_bathrooms (str): The number of bathrooms
		max_guest (int): The max number of guest.
		prince_by_night (int): The price of room per night.
		latitude (float): The latitude of the place.
		longitude (float): The longitude of the place.
		amenity_ids (list): The list of amenity ids.
	"""

	city_id = ""
	user_id = ""
	name = ""
	description = ""
	number_rooms = 0
	number_bathrooms = 0
	max_guest = 0
	price_by_night = 0
	latitude = 0.0
	longitude = 0.0
	amenity_ids = []
