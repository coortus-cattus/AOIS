import unittest
from ..main import HashTable, compute_V, hash_func

class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.ht = HashTable()
        # Тестовые данные
        self.test_data = [
            ("Иванов", "Инженер"),
            ("Петров", "Врач"),
            ("Сидоров", "Учитель"),
            ("Кузнецов", "Программист"),
            ("Васильев", "Бухгалтер"),
        ]

    def test_compute_V(self):
        self.assertEqual(compute_V("АА"), 0)  # А=0, А=0 => 0*33 + 0 = 0
        self.assertEqual(compute_V("АБ"), 1)  # А=0, Б=1 => 0*33 + 1 = 1
        self.assertEqual(compute_V("БА"), 33)  # Б=1, А=0 => 1*33 + 0 = 33
        self.assertEqual(compute_V("ЯЯ"), 1120)  # Я=32 => 32*33 + 32 = 1088 + 32 = 1120

    def test_hash_func(self):
        self.assertEqual(hash_func(0), 0)
        self.assertEqual(hash_func(19), 19)
        self.assertEqual(hash_func(20), 0)
        self.assertEqual(hash_func(39), 19)
        self.assertEqual(hash_func(1120), 0)  # 1120 % 20 = 0

    def test_insert_and_search(self):
        for key, value in self.test_data:
            self.ht.insert(key, value)
        
        # Проверяем поиск существующих записей
        self.assertEqual(self.ht.search("Иванов"), "Инженер")
        self.assertEqual(self.ht.search("Петров"), "Врач")
        self.assertEqual(self.ht.search("Сидоров"), "Учитель")
        
        # Проверяем поиск несуществующей записи
        self.assertIsNone(self.ht.search("Несуществующий"))

    def test_delete(self):
        for key, value in self.test_data:
            self.ht.insert(key, value)
        
        # Удаляем запись и проверяем, что её больше нет
        self.ht.delete("Петров")
        self.assertIsNone(self.ht.search("Петров"))
        
        # Проверяем, что остальные записи на месте
        self.assertEqual(self.ht.search("Иванов"), "Инженер")
        self.assertEqual(self.ht.search("Сидоров"), "Учитель")

    def test_display(self):
        for key, value in self.test_data:
            self.ht.insert(key, value)
        
        # Просто проверяем, что метод не вызывает ошибок
        try:
            self.ht.display()
        except Exception as e:
            self.fail(f"Метод display вызвал исключение: {e}")

    def test_collision_handling(self):
        # Создаём ключи, которые дают одинаковый хеш
        # Подберём такие ключи, что V1 % 20 == V2 % 20
        key1 = "АА"  # V=0, h=0
        key2 = "БЩ"  # Б=1, Щ=26 => V=1*33 + 26=59 => h=59%20=19 (не подходит)
        # Найдём другой ключ: например, "АФ" (А=0, Ф=20) => V=0*33+20=20 => h=0
        key2 = "АФ"
        
        self.assertEqual(hash_func(compute_V(key1)), hash_func(compute_V(key2)))
        
        self.ht.insert(key1, "Значение1")
        self.ht.insert(key2, "Значение2")
        
        # Проверяем, что оба значения сохранились
        self.assertEqual(self.ht.search(key1), "Значение1")
        self.assertEqual(self.ht.search(key2), "Значение2")

if __name__ == "__main__":
    unittest.main()