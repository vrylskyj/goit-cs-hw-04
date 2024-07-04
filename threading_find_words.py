import threading
import os

# Функція для пошуку ключових слів у списку файлів
def search_files(files, keywords, results):
    local_results = {}
    for file_name in files:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
            found_keywords = [keyword for keyword in keywords if keyword in content]
            for keyword in found_keywords:
                if keyword not in local_results:
                    local_results[keyword] = []
                local_results[keyword].append(file_name)
    results.put(local_results)

# Головна функція для обробки файлів у різних потоках
def process_files_with_threads(file_list, num_threads, keywords):
    results_queue = threading.Queue()
    threads = []

    # Розділимо список файлів між потоками
    split_size = len(file_list) // num_threads
    file_chunks = [file_list[i:i + split_size] for i in range(0, len(file_list), split_size)]

    # Створимо та запустимо потоки
    for i in range(num_threads):
        thread = threading.Thread(target=search_files, args=(file_chunks[i], keywords, results_queue))
        threads.append(thread)
        thread.start()

    # Зачекаємо завершення всіх потоків
    for thread in threads:
        thread.join()

    # Зберігаємо результати з черги
    results = {}
    while not results_queue.empty():
        data = results_queue.get()
        for keyword, files in data.items():
            if keyword not in results:
                results[keyword] = []
            results[keyword].extend(files)

    return results

# Приклад використання:
if __name__ == '__main__':
    files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']  # Припустимо, це ваші файли
    keywords = ['keyword1', 'keyword2', 'keyword3']  # Пошук цих ключових слів
    num_threads = 2  # Кількість потоків для використання

    import time
    start_time = time.time()

    results = process_files_with_threads(files, num_threads, keywords)

    end_time = time.time()
    execution_time = end_time - start_time

    # Виведення результатів
    for keyword, found_files in results.items():
        print(f"Keyword: {keyword}, Found in files: {found_files}")

    print(f"Execution time: {execution_time} seconds")
