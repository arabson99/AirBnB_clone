import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.base_model import BaseModel
from models import storage

class TestHBNBCommand(unittest.TestCase):
    def setUp(self):
        """Set up a clean environment before each test."""
        self.console = HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User name=\"John\"")
            self.user_id1 = f.getvalue().strip()
            self.console.onecmd("create User name=\"Jane\"")
            self.user_id2 = f.getvalue().strip()

    def tearDown(self):
        """Clean up after each test."""
        storage.reset()

    def test_do_create(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User name=\"Alice\"")
            output = f.getvalue().strip()
            self.assertTrue(len(output) > 0)
            self.assertIn(output, storage.all())

    def test_do_show(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"show User {self.user_id1}")
            output = f.getvalue().strip()
            self.assertIn('User', output)
            self.assertIn(self.user_id1, output)
    
    def test_do_destroy(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"destroy User {self.user_id2}")
            output = f.getvalue().strip()
            self.assertNotIn(self.user_id2, storage.all())

    def test_do_all(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all User")
            output = f.getvalue().strip()
            self.assertIn(self.user_id1, output)
            self.assertIn(self.user_id2, output)

    def test_do_update(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"update User {self.user_id1} name \"John Doe\"")
            updated_user = storage.all()[f"User.{self.user_id1}"]
            self.assertEqual(updated_user.name, "John Doe")

    def test_default_show(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"User.show({self.user_id1})")
            output = f.getvalue().strip()
            self.assertIn('User', output)
            self.assertIn(self.user_id1, output)

    def test_default_destroy(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"User.destroy({self.user_id2})")
            output = f.getvalue().strip()
            self.assertNotIn(self.user_id2, storage.all())

    def test_default_update(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"User.update({self.user_id1}, name, \"John Doe\")")
            updated_user = storage.all()[f"User.{self.user_id1}"]
            self.assertEqual(updated_user.name, "John Doe")

    def test_default_update_dict(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"User.update({self.user_id1}, {{'name': 'John Doe'}})")
            updated_user = storage.all()[f"User.{self.user_id1}"]
            self.assertEqual(updated_user.name, "John Doe")

    def test_help(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("help show")
            output = f.getvalue().strip()
            self.assertIn("Prints the string representation", output)

if __name__ == '__main__':
    unittest.main()

