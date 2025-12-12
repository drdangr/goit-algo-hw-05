from typing import List, Tuple, Optional


def binary_search_with_upper_bound(arr: List[float], target: float) -> Tuple[int, Optional[float]]:
    """
    Виконує двійковий пошук у відсортованому масиві arr для значення target.

    Повертає:
        (iterations, upper_bound)
        iterations  - кількість ітерацій циклу пошуку
        upper_bound - найменший елемент з arr, який є >= target,
                      або None, якщо такого елемента немає.
    """
    left = 0
    right = len(arr) - 1
    iterations = 0

    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        mid_val = arr[mid]

        if mid_val < target:
            # Шукаємо правіше
            left = mid + 1
        else:
            # mid_val >= target — кандидат на upper bound, звужуємо діапазон зліва
            right = mid - 1

    # Після циклу:
    # left — індекс першого елемента, який >= target (якщо він існує)
    if 0 <= left < len(arr):
        upper_bound = arr[left]
    else:
        upper_bound = None

    return iterations, upper_bound

# Тестуємо функцію:
if __name__ == "__main__":
    data = [1.1, 2.5, 3.3, 4.8, 5.0, 7.2]

    print(binary_search_with_upper_bound(data, 4.0))
    # например: (3, 4.8)

    print(binary_search_with_upper_bound(data, 4.8))
    # (3, 4.8)

    print(binary_search_with_upper_bound(data, 0.5))
    # (1, 1.1)

    print(binary_search_with_upper_bound(data, 10.0))
    # (3, None) — верхньої межі немає