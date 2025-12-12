class HashTable:
    def __init__(self, size):
        self.size = size
        # В каждой ячейке сразу список (может быть пустым)
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        key_hash = self.hash_function(key)
        key_value = [key, value]

        # Эта проверка по сути лишняя, т.к. у нас там всегда список, но оставим как в конспекте
        if self.table[key_hash] is None:
            self.table[key_hash] = list([key_value])
            return True
        else:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        key_hash = self.hash_function(key)
        if self.table[key_hash] is not None:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    def delete(self, key):
        key_hash = self.hash_function(key)
        bucket = self.table[key_hash]

        if not bucket:          # пустой список => нечего удалять
            return False

        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                return True

        return False


# Тестуємо нашу хеш-таблицю:
if __name__ == "__main__":
    H = HashTable(5)
    elements = ("apple", "orange", "banana", "grape")
    print(f'\nElements to insert: {elements}\n')
    print(' --- Insertion and Retrieval Tests ---') 
    i = 0
    for el in elements:
        i = i+1
        print(f'\ninsert "{el}" {i * 10}')
        H.insert(el, i * 10)        
        print(f'now try to get "{el}" hash: {H.get(el)}')

    print('\n --- Deletion Tests ---\n')    
    print(f'try to delete "orange": {H.delete("orange")}')  # True
    print(f'try to get "orange": {H.get("orange")}')     # None
    print(f'try to delete "orange": {H.delete("orange")}')  # False — уже удалён
