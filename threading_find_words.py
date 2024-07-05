import threading
import os

def search_files(files, keywords, results):
    local_results = {}
    for file_name in files:
        try:
            file_path = os.path.join(os.getcwd(), file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                found_keywords = [keyword for keyword in keywords if keyword in content]
                for keyword in found_keywords:
                    if keyword not in local_results:
                        local_results[keyword] = []
                    local_results[keyword].append(file_name)
        except Exception as e:
            print(f"Error processing file {file_name}: {str(e)}")
    results.put(local_results)

def process_files_with_threads(file_list, num_threads, keywords):
    results_queue = threading.Queue()
    threads = []

    split_size = len(file_list) // num_threads
    file_chunks = [file_list[i:i + split_size] for i in range(0, len(file_list), split_size)]

    for i in range(num_threads):
        thread = threading.Thread(target=search_files, args=(file_chunks[i], keywords, results_queue))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    results = {}
    while not results_queue.empty():
        data = results_queue.get()
        for keyword, files in data.items():
            if keyword not in results:
                results[keyword] = []
            results[keyword].extend(files)

    return results

if __name__ == '__main__':
    files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']
    keywords = ['keyword1', 'keyword2', 'keyword3']
    num_threads = 2

    import time
    start_time = time.time()

    results = process_files_with_threads(files, num_threads, keywords)

    end_time = time.time()
    execution_time = end_time - start_time

    for keyword, found_files in results.items():
        print(f"Keyword: {keyword}, Found in files: {found_files}")

    print(f"Total files processed: {len(files)}")
    print(f"Execution time: {execution_time} seconds")
