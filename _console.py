#!/usr/bin/python3
"""Defines the entry point of the command interpreter."""
import cmd
import json
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review



class HBNBCommand(cmd.Cmd):
	"""Command interpreter for AirBnB.

	Args:
		prompt (str): The command promt.
	"""
	
	prompt = '(hbnb) '

	classes = {'BaseModel': BaseModel,
		'User': User,
		'Place': Place,
		'State': State,
		'City': City,
		'Amenity': Amenity,
		'Review': Review
	}

	def do_quit(self, line):
		"""Quit command to exit the program."""
		return True

	def do_EOF(self, line):
		"""EOF command to exit the program."""
		print("")
		return True

	def help_quit(self):
		"""Help for quit command."""
		print("Quit command to exit the program")

	def help_EOF(self):
		"""Help for EOF command"""
		print("EOF command to exit the program""")

	def emptyline(self):
		"""Override emptyline to do nothing on an empty line"""
		pass

	def do_create(self, arg):
		"""Create a new instance of BaseModel, save it, and prnts the id."""
		if not arg:
			print("** class name missing **")
			return
		if arg not in HBNBCommand.classes:
			print("** class doesn't exist **")
			return
		new_instance = HBNBCommand.classes[arg]()
		new_instance.save()
		print(new_instance.id)

	def do_show(self, arg):
		"""Prints the string representation of an instance base on the class name and id"""
		args = arg.split()
		if len(args) == 0:
			print("** class name missing **")
			return
		if args[0] not in HBNBCommand.classes:
			print("** class doesn't exist **")
			return
		if len(args) == 1:
			print("** instance id missing **")
			return
		key = "{}.{}".format(args[0], args[1])
		if key not in storage.all():
			print("** no instance found **")
			return
		print(storage.all()[key])

	def do_destroy(self, arg):
		"""Deletes an instance based on the class name and id."""
		args = arg.split()
		if len(args) == 0:
			print("** class name missing **")
			return
		if args[0] not in HBNBCommand.classes:
			print("** class doesn't exist **")
			return
		if len(args) == 1:
			print("** instance id missing **")
			return
		key = "{}.{}".format(args[0], args[1])
		if key not in storage.all():
			print("** no instance found **")
			return
		del storage.all()[key]
		storage.save()

	def do_all(self, arg):
		"""Prints all string representation of all instances of a given class.
		If no class is specified, prints all instantiated objects."""
		args = arg.split()
		if len(args) == 0:
			print([str(obj) for obj in storage.all().values()])
		elif args[0] in HBNBCommand.classes:
			print([str(obj) for key, obj in storage.all().items() if key.startswith(args[0])])
		else:
			print("** class doesn't exist **")

	def do_update(self, arg):
		"""Updates an instance based on the class name and id by adding or updating attribute"""
		args = arg.split()
		if len(args) == 0:
			print("** class name missing **")
			return
		if args[0] not in HBNBCommand.classes:
			print("** class doesn't exist **")
			return
		if len(args) == 1:
			print("** instance id missing **")
			return
		key = "{}.{}".format(args[0], args[1])
		if key not in storage.all():
			print("** no instance found **")
			return
		if len(args) == 2:
			print("** attribute name missing")
			return
		if len(args) == 3:
			print("** value missing **")
			return

		obj = storage.all()[key]
		attr_name = args[2]
		attr_value = args[3].strip('"')

		if hasattr(obj, attr_name):
			attr_type = type(getattr(obj, attr_name))
			try:
				attr_value = attr_type(attr_value)
			except ValueError:
				print("** invalid value **")
				return
		setattr(obj, attr_name, attr_value)
		obj.save()

	def default(self, line):
		 """Handle default commands <class name>.all(), <class name>.count(),
        <class name>.destroy(<id>), <class name>.show(<id>), and
        <class name>.update(<id>, <attribute name>, <attribute value>),
        <class name>.update(<id>, <dictionary representation>)"""
		args = line.split('.')
		if len(args) == 2:
			class_name, command = args[0], args[1].strip()
			if command == "all()":
				if class_name in HBNBCommand.classes:
					self.do_all(class_name)
				else:
					print("** class doesn't exist **")
			elif command == "count()":
				if class_name in HBNBCommand.classes:
					count = sum(1 for key in storage.all().keys()
							if key.startswith(class_name + '.'))
					print(count)
				else:
					print("** class doesn't exist **")
			elif command.startswith("show(") and command.endswith(")"):
				instance_id = command[5:-1].strip('"')
				self.do_show(f"{class_name} {instance_id}")
			elif command.startswith("destroy(") and command.endswith(")"):
				if class_name in HBNBCommand.classes:
					instance_id = command[8:-1].strip('"')
					self.do_destroy(f"{class_name} {instance_id}")
			elif command.startswith("update(") and command.endswith(")"):
				params = command[7:-1]
				if "," in params:
					try:
						obj_id, updates = params.split(',', 1)
						obj_id = obj_id.strip().strip('"')
						updates = updates.strip()
						if updates.A



if __name__ == "__main__":
	HBNBCommand().cmdloop()
