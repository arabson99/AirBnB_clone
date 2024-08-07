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
        prompt (str): The command prompt.
    """

    prompt = '(hbnb) '

    classes = {
        'BaseModel': BaseModel,
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
        print("EOF command to exit the program")

    def emptyline(self):
        """Override emptyline to do nothing on an empty line"""
        pass

    def do_create(self, arg):
        """Create a new instance of BaseModel, save it, and print the id."""
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
        """Prints the string representation of an instance based on the class name and id"""
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
            print([str(obj) for key, obj in storage.all().items()
                   if key.startswith(args[0] + '.')])
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
            print("** attribute name missing **")
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
        <class name>.destroy(<id>), and <class name>.update(<id>, <attribute name>, <attribute value>)"""
        args = line.split('.')
        if len(args) != 2:
            print("*** Unknown syntax:", line)
            return

        class_name, command = args[0], args[1].strip()
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if command == "all()":
            self.do_all(class_name)
        elif command == "count()":
            self.count(class_name)
        elif command.startswith("show(") and command.endswith(")"):
            self.show_by_id(class_name, command)
        elif command.startswith("destroy(") and command.endswith(")"):
            self.destroy_by_id(class_name, command)
        elif command.startswith("update(") and command.endswith(")"):
            self.update_by_id(class_name, command)
        else:
            print("*** Unknown syntax:", line)

    def count(self, class_name):
        """Count the number of instances of a class"""
        count = sum(1 for key in storage.all().keys() if key.startswith(class_name + '.'))
        print(count)

    def show_by_id(self, class_name, command):
        """Show an instance by ID"""
        instance_id = command[5:-1].strip('"')
        key = f"{class_name}.{instance_id}"
        if key in storage.all():
            print(storage.all()[key])
        else:
            print("** no instance found **")

    def destroy_by_id(self, class_name, command):
        """Destroy an instance by ID"""
        instance_id = command[8:-1].strip('"')
        key = f"{class_name}.{instance_id}"
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def update_by_id(self, class_name, command):
        """Update an instance by ID"""
        params = command[7:-1]
        if "," in params:
            try:
                obj_id, updates = params.split(',', 1)
                obj_id = obj_id.strip().strip('"')
                updates = updates.strip()
                if updates.startswith('{') and updates.endswith('}'):
                    update_dict = json.loads(updates.replace("'", '"'))
                    self._update_dict(class_name, obj_id, update_dict)
                else:
                    attr_name, attr_value = updates.split(',', 1)
                    attr_name = attr_name.strip().strip('"')
                    attr_value = attr_value.strip().strip('"')
                    self.do_update(f"{class_name} {obj_id} {attr_name} {attr_value}")
            except ValueError:
                print("** invalid dictionary format **")

    def _update_dict(self, class_name, obj_id, update_dict):
        """Update an instance using a dictionary"""
        key = f"{class_name}.{obj_id}"
        if key not in storage.all():
            print("** no instance found **")
            return
        obj = storage.all()[key]
        for attr_name, attr_value in update_dict.items():
            if hasattr(obj, attr_name):
                attr_type = type(getattr(obj, attr_name))
                try:
                    attr_value = attr_type(attr_value)
                except ValueError:
                    print("** invalid value **")
                    return
            setattr(obj, attr_name, attr_value)
        obj.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()

