import random
import string
import time
from collections import Counter
from threading import Thread, Lock
from multiprocessing import Process, Manager


def generate_large_text_file(filename, size_in_mb):
    words = ["apple", "banana", "orange", "grape", "pineapple", "kiwi", "strawberry", "blueberry", "mango"]
    with open(filename, 'w') as f:
        for _ in range(size_in_mb * 10000): 
            sentence = " ".join(random.choices(words, k=random.randint(5, 15)))
            f.write(sentence + "\n")


def count_words_sequential(filename):
    with open(filename, 'r') as f:
        word_counts = Counter(f.read().split())
    return word_counts


def count_words_multithreading(filename):
    lock = Lock()
    word_counts = Counter()

    def process_chunk(chunk):
        nonlocal word_counts
        local_counts = Counter(chunk.split())
        with lock:
            word_counts.update(local_counts)

    with open(filename, 'r') as f:
        lines = f.readlines()

    threads = []
    num_threads = 4
    chunk_size = len(lines) // num_threads

    for i in range(num_threads):
        chunk = lines[i * chunk_size:(i + 1) * chunk_size]
        thread = Thread(target=process_chunk, args=(" ".join(chunk),))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return word_counts


def count_words_multiprocessing(filename):
    def process_chunk(chunk, result_list):
        result_list.append(Counter(chunk.split()))

    with open(filename, 'r') as f:
        lines = f.readlines()

    manager = Manager()
    result_list = manager.list()
    processes = []
    num_processes = 4
    chunk_size = len(lines) // num_processes

    for i in range(num_processes):
        chunk = lines[i * chunk_size:(i + 1) * chunk_size]
        process = Process(target=process_chunk, args=(" ".join(chunk), result_list))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    word_counts = Counter()
    for result in result_list:
        word_counts.update(result)

    return word_counts


def compare_execution_times(filename):

    start_time = time.perf_counter()
    sequential_counts = count_words_sequential(filename)
    sequential_time = time.perf_counter() - start_time


    start_time = time.perf_counter()
    threading_counts = count_words_multithreading(filename)
    threading_time = time.perf_counter() - start_time


    start_time = time.perf_counter()
    multiprocessing_counts = count_words_multiprocessing(filename)
    multiprocessing_time = time.perf_counter() - start_time

    print(f"Sequential Time: {sequential_time:.6f} seconds,\nWords: {sequential_counts}")
    print(f"Multithreading Time: {threading_time:.6f} seconds,\nWords: {threading_counts}")
    print(f"Multiprocessing Time: {multiprocessing_time:.6f} seconds,\nWords: {multiprocessing_counts}")

    print(f"Speedup (Threading): {sequential_time / threading_time:.2f}x")
    print(f"Speedup (Multiprocessing): {sequential_time / multiprocessing_time:.2f}x")


if __name__ == "__main__":
    filename = "large_text_file.txt"
    generate_large_text_file(filename, size_in_mb=10)  
    compare_execution_times(filename)
