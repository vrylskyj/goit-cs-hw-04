import threading

# Функція для пошуку ключових слів у списку файлів
def search_files(files, keywords):
    results = []
    for file_name in files:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
            found_keywords = [keyword for keyword in keywords if keyword in content]
            results.append((file_name, found_keywords))
    return results

# Головна функція для обробки файлів у різних потоках
def process_files_with_threads(file_list, num_threads, keywords):
    # Розділимо список файлів між потоками
    split_size = len(file_list) // num_threads
    file_chunks = [file_list[i:i + split_size] for i in range(0, len(file_list), split_size)]

    # Створимо потоки
    threads = []
    results = []

    for i in range(num_threads):
        thread = threading.Thread(target=lambda idx=i: results.extend(search_files(file_chunks[idx], keywords)))
        threads.append(thread)
        thread.start()

    # Зачекаємо завершення всіх потоків
    for thread in threads:
        thread.join()

    return results

# Приклад використання:
if __name__ == '__main__':
    files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']  # Припустимо, це ваші файли
    keywords = ['keyword1', 'keyword2', 'keyword3']  # Пошук цих ключових слів

    results = process_files_with_threads(files, 2, keywords)  # Використовуємо 2 потоки

    # Виведення результатів
    for result in results:
        print(f"File: {result[0]}, Found keywords: {result[1]}")
