import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
import json

class TestHBNBCommand(unittest.TestCase):
    """Unit tests for HBNBCommand class."""

    def setUp(self):
        """Set up test environment."""
        storage._FileStorage__objects = {}

    def tearDown(self):
        """Tear down test environment."""
        storage._FileStorage__objects = {}

    @patch('sys.stdout', new=StringIO())
    def test_quit(self, mock_stdout):
        """Test quit command."""
        self.assertTrue(HBNBCommand().onecmd("quit"))

    @patch('sys.stdout', new=StringIO())
    def test_EOF(self, mock_stdout):
        """Test EOF command."""
        self.assertTrue(HBNBCommand().onecmd("EOF"))

    @patch('sys.stdout', new=StringIO())
    def test_emptyline(self, mock_stdout):
        """Test empty line input."""
        self.assertFalse(HBNBCommand().onecmd(""))

    @patch('sys.stdout', new=StringIO())
    def test_create(self, mock_stdout):
        """Test create command."""
        HBNBCommand().onecmd("create BaseModel")
        self.assertTrue(len(mock_stdout.getvalue().strip()) > 0)
        obj_id = mock_stdout.getvalue().strip()
        self.assertIn(f"BaseModel.{obj_id}", storage.all())

    @patch('sys.stdout', new=StringIO())
    def test_create_missing_class(self, mock_stdout):
        """Test create command with missing class."""
        HBNBCommand().onecmd("create")
        self.assertEqual(mock_stdout.getvalue().strip(), "** class name missing **")

    @patch('sys.stdout', new=StringIO())
    def test_create_invalid_class(self, mock_stdout):
        """Test create command with invalid class."""
        HBNBCommand().onecmd("create InvalidClass")
        self.assertEqual(mock_stdout.getvalue().strip(), "** class doesn't exist **")

    @patch('sys.stdout', new=StringIO())
    def test_show(self, mock_stdout):
        """Test show command."""
        new_instance = BaseModel()
        new_instance.save()
        HBNBCommand().onecmd(f"show BaseModel {new_instance.id}")
        self.assertIn(str(new_instance), mock_stdout.getvalue().strip())

    @patch('sys.stdout', new=StringIO())
    def test_show_missing_class(self, mock_stdout):
        """Test show command with missing class."""
        HBNBCommand().onecmd("show")
        self.assertEqual(mock_stdout.getvalue().strip(), "** class name missing **")

    @patch('sys.stdout', new=StringIO())
    def test_show_invalid_class(self, mock_stdout):
        """Test show command with invalid class."""
        HBNBCommand().onecmd("show InvalidClass")
        self.assertEqual(mock_stdout.getvalue().strip(), "** class doesn't exist **")

    @patch('sys.stdout', new=StringIO())
    def test_show_missing_id(self, mock_stdout):
        """Test show command with missing id."""
        HBNBCommand().onecmd("show BaseModel")
        self.assertEqual(mock_stdout.getvalue().strip(), "** instance id missing **")

    @patch('sys.stdout', new=StringIO())
    def test_show_invalid_id(self, mock_stdout):
        """Test show command with invalid id."""
        HBNBCommand().onecmd("show BaseModel invalid_id")
        self.assertEqual(mock_stdout.getvalue().strip(), "** no instance found **")

    @patch('sys.stdout', new=StringIO())
    def test_destroy(self, mock_stdout):
        """Test destroy command."""
        new_instance = BaseModel()
        new_instance.save()
        HBNBCommand().onecmd(f"destroy BaseModel {new_instance.id}")
        self.assertNotIn(f"BaseModel.{new_instance.id}", storage.all())

    @patch('sys.stdout', new=StringIO())
    def test_destroy_missing_class(self, mock_stdout):
        """Test destroy command with missing class."""
        HBNBCommand().onecmd("destroy")
        self.assertEqual(mock_stdout.getvalue().strip(), "** class name missing **")

    @patch('sys.stdout', new=StringIO())
    def test_destroy_invalid_class(self, mock_stdout):
        """Test destroy command with invalid class."""
        HBNBCommand().onecmd("destroy InvalidClass")
        self.assertEqual(mock_stdout.getvalue().strip(), "** class doesn't exist **")

    @patch('sys.stdout', new=StringIO())
    def test_destroy_missing_id(self, mock_stdout):
        """Test destroy command with missing id."""
        HBNBCommand().onecmd("destroy BaseModel")
        self.assertEqual(mock_stdout.getvalue().strip(), "** instance id missing **")

    @patch('sys.stdout', new=StringIO())
    def test_destroy_invalid_id(self, mock_stdout):
        """Test destroy command with invalid id."""
        HBNBCommand().onecmd("destroy BaseModel invalid_id")
        self.assertEqual(mock_stdout.getvalue().strip(), "** no instance found **")

    @patch('sys.stdout', new=StringIO())
    def test_all(self, mock_stdout):
        """Test all command."""
        HBNBCommand().onecmd("create BaseModel")
        HBNBCommand().onecmd("all BaseModel")
        output = mock_stdout.getvalue().strip()
        self.assertIn("BaseModel", output)

    @patch('sys.stdout', new=StringIO())
    def test_all_invalid_class(self, mock_stdout):
        """Test all command with invalid class."""
        HBNBCommand().onecmd("all InvalidClass")
        self.assertEqual(mock_stdout.getvalue().strip(), "** class doesn't exist **")

    @patch('sys.stdout', new=StringIO())
    def test_update(self, mock_stdout):
        """Test update command."""
        new_instance = BaseModel()
        new_instance.save()
        HBNBCommand().onecmd(f"update BaseModel {new_instance.id} name 'Holberton'")
        self.assertEqual(new_instance.name, 'Holberton')

    @patch('sys.stdout', new=StringIO())
    def test_update_missing_class(self, mock_stdout):
        """Test update command with missing class."""
        HBNBCommand().onecmd("update")
        self.assertEqual(mock_stdout.getvalue().strip(), "** class name missing **")

    @patch('sys.stdout', new=StringIO())
    def test_update_invalid_class(self, mock_stdout):
        """Test update command with invalid class."""
        HBNBCommand().onecmd("update InvalidClass")
        self.assertEqual(mock_stdout.getvalue().strip(), "** class doesn't exist **")

    @patch('sys.stdout', new=StringIO())
    def test_update_missing_id(self, mock_stdout):
        """Test update command with missing id."""
        HBNBCommand().onecmd("update BaseModel")
        self.assertEqual(mock_stdout.getvalue().strip(), "** instance id missing **")

    @patch('sys.stdout', new=StringIO())
    def test_update_invalid_id(self, mock_stdout):
        """Test update command with invalid id."""
        HBNBCommand().onecmd("update BaseModel invalid_id")
        self.assertEqual(mock_stdout.getvalue().strip(), "** no instance found **")

    @patch('sys.stdout', new=StringIO())
    def test_update_missing_attribute(self, mock_stdout):
        """Test update command with missing attribute."""
        new_instance = BaseModel()
        new_instance.save()
        HBNBCommand().onecmd(f"update BaseModel {new_instance.id}")
        self.assertEqual(mock_stdout.getvalue().strip(), "** attribute name missing **")

    @patch('sys.stdout', new=StringIO())
    def test_update_missing_value(self, mock_stdout):
        """Test update command with missing value."""
        new_instance = BaseModel()
        new_instance.save()
        HBNBCommand().onecmd(f"update BaseModel {new_instance.id} name")
        self.assertEqual(mock_stdout.getvalue().strip(), "** value missing **")

    @patch('sys.stdout', new=StringIO())
    def test_update_dict(self, mock_stdout):
        """Test update command with a dictionary."""
        new_instance = BaseModel()
        new_instance.save()
        update_dict = '{"name": "Holberton", "age": 5}'
        HBNBCommand().onecmd(f"update BaseModel {new_instance.id} {update_dict}")
        self.assertEqual(new_instance.name, 'Holberton')
        self.assertEqual(new_instance.age, 5)

    @patch('sys.stdout', new=StringIO())
    def test_default_all(self, mock_stdout):
        """Test default all() command."""
        HBNBCommand().onecmd("BaseModel.all()")
        self.assertIn("BaseModel", mock_stdout.getvalue().strip())

    @patch('sys.stdout', new=StringIO())
    def test_default_count(self, mock_stdout):
        """Test default count() command."""
        HBNBCommand().onecmd("BaseModel.count()")
        self.assertEqual(mock_stdout.getvalue().strip(), "0")

    @patch('sys.stdout', new=StringIO())
    def test_default_show(self, mock

