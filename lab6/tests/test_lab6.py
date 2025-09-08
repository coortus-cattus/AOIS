import io
import unittest
from unittest.mock import patch


from lab6.main import (
    compute_V,
    AVLTree,
    HashTable,
    menu
)


class TestHashHelpers(unittest.TestCase):
    def test_compute_V_regular(self):
        self.assertEqual(compute_V("АБ"), 0 * 33 + 1)
        self.assertEqual(compute_V("ЯЯ"), 31 * 33 + 31)  # Я = 31 (нет Ё)

    def test_compute_V_short_key(self):
        with self.assertRaises(ValueError):
            compute_V("А")

    def test_compute_V_invalid_char(self):
        with self.assertRaises(ValueError):
            compute_V("AЯ")  # латиница


class TestAVLTree(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()
        self.root = None

    def test_insert_and_search(self):
        self.root = self.tree.insert(self.root, 10, "A")
        self.root = self.tree.insert(self.root, 20, "B")
        self.root = self.tree.insert(self.root, 30, "C")
        self.assertEqual(self.tree.search(self.root, 20).value, "B")

    def test_insert_duplicate_raises(self):
        self.root = self.tree.insert(self.root, 5, "A")
        with self.assertRaises(ValueError):
            self.root = self.tree.insert(self.root, 5, "B")

    def test_delete_node_with_two_children(self):
        self.root = self.tree.insert(self.root, 50, "A")
        self.root = self.tree.insert(self.root, 30, "B")
        self.root = self.tree.insert(self.root, 70, "C")
        self.root = self.tree.insert(self.root, 60, "D")
        self.root = self.tree.insert(self.root, 80, "E")
        self.root = self.tree.delete(self.root, 70)
        self.assertIsNone(self.tree.search(self.root, 70))

    def test_delete_nonexistent_key(self):
        self.root = self.tree.insert(self.root, 10, "A")
        self.root = self.tree.delete(self.root, 99)  # не должно упасть
        self.assertIsNotNone(self.root)

    def test_left_left_rotation(self):
        self.root = self.tree.insert(self.root, 30, "A")
        self.root = self.tree.insert(self.root, 20, "B")
        self.root = self.tree.insert(self.root, 10, "C")
        self.assertEqual(self.root.key, 20)

    def test_right_right_rotation(self):
        self.root = self.tree.insert(self.root, 10, "A")
        self.root = self.tree.insert(self.root, 20, "B")
        self.root = self.tree.insert(self.root, 30, "C")
        self.assertEqual(self.root.key, 20)

    def test_left_right_rotation(self):
        self.root = self.tree.insert(self.root, 30, "A")
        self.root = self.tree.insert(self.root, 10, "B")
        self.root = self.tree.insert(self.root, 20, "C")
        self.assertEqual(self.root.key, 20)

    def test_right_left_rotation(self):
        self.root = self.tree.insert(self.root, 10, "A")
        self.root = self.tree.insert(self.root, 30, "B")
        self.root = self.tree.insert(self.root, 20, "C")
        self.assertEqual(self.root.key, 20)


class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.ht = HashTable()

    def test_insert_and_search(self):
        self.ht.insert("Иванов", "Инженер")
        result = self.ht.search("Иванов")
        self.assertEqual(result, "Инженер")

    def test_delete_existing_key(self):
        self.ht.insert("Петров", "Менеджер")
        self.ht.delete("Петров")
        result = self.ht.search("Петров")
        self.assertIsNone(result)

    def test_delete_nonexistent_key(self):
        self.ht.delete("Несуществующий")  # просто не упадёт

    def test_insert_invalid_key_raises(self):
        with self.assertRaises(ValueError):
            self.ht.insert("A", "Ошибка")


class TestMenu(unittest.TestCase):
    def test_menu_add_and_exit(self):
        inputs = ["1", "Иванов", "Инженер", "5"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                menu()
                output = fake_out.getvalue()
                self.assertIn("Запись 'Иванов' добавлена.", output)
                self.assertIn("Выход из программы.", output)

    def test_menu_search(self):
        inputs = ["1", "Петров", "Менеджер", "2", "Петров", "5"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                menu()
                output = fake_out.getvalue()
                self.assertIn("Найдено: Менеджер", output)

    def test_menu_delete(self):
        inputs = ["1", "Сидоров", "Аналитик", "3", "Сидоров", "5"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                menu()
                output = fake_out.getvalue()
                self.assertIn("Попытка удаления записи с ключом 'Сидоров' выполнена.", output)


if __name__ == "__main__":
    unittest.main()

  