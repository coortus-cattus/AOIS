import sys

# Русский алфавит
RU_ALPHABET = {ch: i for i, ch in enumerate(
    "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")}

# Размер таблицы
TABLE_SIZE = 20


def compute_V(key: str) -> int:
    """Вычисляет значение V по первым двум буквам ключа (русские буквы)."""
    key = key.upper()
    if len(key) < 2 or key[0] not in RU_ALPHABET or key[1] not in RU_ALPHABET:
        raise ValueError(f"Недопустимый ключ: {key}")
    return RU_ALPHABET[key[0]] * 33 + RU_ALPHABET[key[1]]


def hash_func(V: int) -> int:
    """Хеш-функция h(V) = V % H"""
    return V % TABLE_SIZE



class AVLNode:
    def __init__(self, key, value):
        self.key = key  # ID
        self.value = value  # данные
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """AVL дерево: для цепочек"""

    def insert(self, root, key, value):
        if not root:
            return AVLNode(key, value)
        if key < root.key:
            root.left = self.insert(root.left, key, value)
        elif key > root.key:
            root.right = self.insert(root.right, key, value)
        else:
            raise ValueError("Дубликат ключа в AVL")

        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))
        balance = self.get_balance(root)

        # Балансировка
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        return root

    def delete(self, root, key):
        if not root:
            return root
        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            # Удаляемый узел найден
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            temp = self.get_min(root.right)
            root.key = temp.key
            root.value = temp.value
            root.right = self.delete(root.right, temp.key)
        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))
        balance = self.get_balance(root)
        # Балансировка
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        return root

    def search(self, root, key):
        if not root or root.key == key:
            return root
        if key < root.key:
            return self.search(root.left, key)
        return self.search(root.right, key)

    def get_min(self, node):
        while node.left:
            node = node.left
        return node

    def get_height(self, root):
        return root.height if root else 0

    def get_balance(self, root):
        return self.get_height(root.left) - self.get_height(root.right) if root else 0

    def left_rotate(self, z):
        y = z.right
        T = y.left
        y.left = z
        z.right = T
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T = y.right
        y.right = z
        z.left = T
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def inorder(self, root):
        if root:
            yield from self.inorder(root.left)
            yield (root.key, root.value)
            yield from self.inorder(root.right)



class HashTable:
    def __init__(self, size=TABLE_SIZE):
        self.size = size
        self.table = [None] * size
        self.trees = [AVLTree() for _ in range(size)]

    def insert(self, key: str, value):
        V = compute_V(key)
        h = hash_func(V)
        tree = self.trees[h]
        try:
            self.table[h] = tree.insert(self.table[h], key, value)
        except ValueError:
            print(f"Ключ {key} уже существует!", file=sys.stderr)

    def search(self, key: str):
        V = compute_V(key)
        h = hash_func(V)
        node = self.trees[h].search(self.table[h], key)
        return node.value if node else None

    def delete(self, key: str):
        V = compute_V(key)
        h = hash_func(V)
        self.table[h] = self.trees[h].delete(self.table[h], key)

    def display(self):
        for i in range(self.size):
            print(f"[{i}] ->", end=' ')
            entries = list(self.trees[i].inorder(self.table[i]))
            for k, v in entries:
                print(f"{k}: {v}", end='; ')
            print()


def menu():
    ht = HashTable()

    actions = {
        "1": "Добавить запись",
        "2": "Найти по ключу",
        "3": "Удалить по ключу",
        "4": "Показать таблицу",
        "5": "Выйти"
    }

    while True:
        print("\n===== МЕНЮ ХЕШ-ТАБЛИЦЫ =====")
        for k, v in actions.items():
            print(f"{k}. {v}")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            key = input("Введите ключ (фамилию): ").strip()
            value = input("Введите значение (описание): ").strip()
            try:
                ht.insert(key, value)
                print(f"Запись '{key}' добавлена.")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "2":
            key = input("Введите ключ для поиска: ").strip()
            result = ht.search(key)
            if result is not None:
                print(f"Найдено: {result}")
            else:
                print("Запись не найдена.")

        elif choice == "3":
            key = input("Введите ключ для удаления: ").strip()
            ht.delete(key)
            print(f"Попытка удаления записи с ключом '{key}' выполнена.")

        elif choice == "4":
            print("\nСодержимое хеш-таблицы:")
            ht.display()

        elif choice == "5":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    menu()

