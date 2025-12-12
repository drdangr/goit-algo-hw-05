import timeit
from typing import Callable


def boyer_moore_search(text: str, pattern: str) -> int:
    """
    Пошук підрядка алгоритмом Боєра–Мура.
    Повертає індекс першого входження або -1, якщо підрядок не знайдено.
    """
    m = len(pattern)
    n = len(text)

    if m == 0:
        return 0
    if m > n:
        return -1

    # Таблиця зсувів (bad character rule)
    skip = {pattern[i]: m - i - 1 for i in range(m - 1)}
    default_shift = m

    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i  # збіг знайдено

        bad_char = text[i + m - 1]
        i += skip.get(bad_char, default_shift)

    return -1


def kmp_search(text: str, pattern: str) -> int:
    """
    Пошук підрядка алгоритмом Кнута–Морріса–Пратта.
    Повертає індекс першого входження або -1.
    """
    m = len(pattern)
    n = len(text)

    if m == 0:
        return 0
    if m > n:
        return -1

    # Обчислення префікс-функції (масив lps)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    # Основний цикл пошуку
    i = 0  # індекс у text
    j = 0  # індекс у pattern

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                return i - j  # знайдено
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return -1


def rabin_karp_search(text: str, pattern: str) -> int:
    """
    Пошук підрядка алгоритмом Рабіна–Карпа.
    Повертає індекс першого входження або -1.
    """
    m = len(pattern)
    n = len(text)

    if m == 0:
        return 0
    if m > n:
        return -1

    base = 256
    mod = 10**9 + 7

    # base^(m-1) % mod для "викидання" першого символу з хеша
    h = 1
    for _ in range(m - 1):
        h = (h * base) % mod

    pattern_hash = 0
    window_hash = 0

    # Початкові хеші
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        window_hash = (window_hash * base + ord(text[i])) % mod

    # Пересувне вікно
    for i in range(n - m + 1):
        if pattern_hash == window_hash:
            # Додаткова перевірка на збіг
            if text[i:i + m] == pattern:
                return i

        if i < n - m:
            window_hash = (window_hash - ord(text[i]) * h) % mod
            window_hash = (window_hash * base + ord(text[i + m])) % mod
            window_hash = (window_hash + mod) % mod

    return -1


# Функція для вимірювання часу виконання

def measure_time(
    func: Callable[[str, str], int],
    text: str,
    pattern: str,
    number: int = 10
) -> float:
    """
    Вимірює середній час виконання функції пошуку.
    number – скільки разів запускаємо для усереднення.
    """
    t = timeit.timeit(lambda: func(text, pattern), number=number)
    return t / number

def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Вибір підрядків для тестування

def choose_existing_substring(text: str, length: int = 20) -> str:
    """
    Беремо підрядок десь із середини тексту, щоб він точно існував.
    """
    if len(text) <= length:
        return text
    start = len(text) // 3
    end = start + length
    return text[start:end]

# Вибір абсурдного підрядка, якого немає в тексті

def choose_fake_substring() -> str:
    """
    Абсурд, якого немає в текстах.
    """
    return "qwerty_uiop_1234567890"

# Бенчмарк для одного тексту та набору алгоритмів

def benchmark_for_text(
    text_name: str,
    text: str,
    pattern_exist: str,
    pattern_fake: str,
    algorithms: dict,
    number: int = 10,
):
    results = []
    ''' 
    Виконує бенчмарк для заданого тексту та підрядків.
    '''
    for algo_name, algo_func in algorithms.items():
        t_exist = measure_time(algo_func, text, pattern_exist, number=number)
        t_fake = measure_time(algo_func, text, pattern_fake, number=number)

        results.append((text_name, algo_name, "exists", t_exist))
        results.append((text_name, algo_name, "fake", t_fake))

    return results

# Тестуємо алгоритми на двох текстах

if __name__ == "__main__":
    
    article1_path = "data/article1.txt"
    article2_path = "data/article2.txt"

    text1 = load_text(article1_path)
    text2 = load_text(article2_path)

    # Обираємо підрядки
    existing_pattern_1 = choose_existing_substring(text1, length=25)
    existing_pattern_2 = choose_existing_substring(text2, length=25)

    fake_pattern_1 = choose_fake_substring()
    fake_pattern_2 = choose_fake_substring()

    algorithms = {
        "Boyer-Moore": boyer_moore_search,
        "KMP": kmp_search,
        "Rabin-Karp": rabin_karp_search,
    }

    results = []  # сюди складемо всі заміри
    results += benchmark_for_text("article1", text1, existing_pattern_1, fake_pattern_1, algorithms)
    results += benchmark_for_text("article2", text2, existing_pattern_2, fake_pattern_2, algorithms)
    
    # вивід у консоль
    print(f"{'Text':10} | {'Algorithm':12} | {'Case':8} | Time (s)")
    print("-" * 50)
    for text_name, algo_name, case, t in results:
        print(f"{text_name:10} | {algo_name:12} | {case:8} | {t:.6f}")
