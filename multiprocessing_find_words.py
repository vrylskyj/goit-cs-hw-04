import multiprocessing
from multiprocessing import Queue

# Функція для обробки файлів у процесі
def process_files(files, keywords, results):
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

# Головна функція для обробки файлів у різних процесах
def process_files_with_multiprocessing(file_list, num_processes, keywords):
    results_queue = Queue()

    # Розділимо список файлів між процесами
    split_size = len(file_list) // num_processes
    file_chunks = [file_list[i:i + split_size] for i in range(0, len(file_list), split_size)]

    # Створимо та запустимо процеси
    processes = []
    for i in range(num_processes):
        process = multiprocessing.Process(target=process_files, args=(file_chunks[i], keywords, results_queue))
        processes.append(process)
        process.start()

    # Зачекаємо завершення всіх процесів
    for process in processes:
        process.join()

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
    num_processes = 2  # Кількість процесів для використання

    import time
    start_time = time.time()

    results = process_files_with_multiprocessing(files, num_processes, keywords)

    end_time = time.time()
    execution_time = end_time - start_time

    # Виведення результатів
    for keyword, found_files in results.items():
        print(f"Keyword: {keyword}, Found in files: {found_files}")

    print(f"Execution time: {execution_time} seconds")
