import multiprocessing
from multiprocessing import Queue

# Функція для обробки файлів у процесі
def process_files(files, keywords, results_queue):
    results = []
    for file_name in files:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
            found_keywords = [keyword for keyword in keywords if keyword in content]
            results.append((file_name, found_keywords))
    results_queue.put(results)

# Головна функція для обробки файлів у різних процесах
def process_files_with_multiprocessing(file_list, num_processes, keywords):
    # Розділимо список файлів між процесами
    split_size = len(file_list) // num_processes
    file_chunks = [file_list[i:i + split_size] for i in range(0, len(file_list), split_size)]

    # Створимо чергу для зберігання результатів
    results_queue = Queue()

    # Створимо процеси
    processes = []
    for i in range(num_processes):
        process = multiprocessing.Process(target=process_files, args=(file_chunks[i], keywords, results_queue))
        processes.append(process)
        process.start()

    # Зіберемо всі результати з черги
    results = []
    for _ in range(num_processes):
        results.extend(results_queue.get())

    # Зачекаємо завершення всіх процесів
    for process in processes:
        process.join()

    return results

# Приклад використання:
if __name__ == '__main__':
    files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']  # Припустимо, це ваші файли
    keywords = ['keyword1', 'keyword2', 'keyword3']  # Пошук цих ключових слів

    results = process_files_with_multiprocessing(files, 2, keywords)  # Використовуємо 2 процеси

    # Виведення результатів
    for result in results:
        print(f"File: {result[0]}, Found keywords: {result[1]}")
