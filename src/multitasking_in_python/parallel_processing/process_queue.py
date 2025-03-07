import csv
import multiprocessing
import time

from src.multitasking_in_python.parallel_processing.data_process import (
    generate_data,
    process_number,
)


def worker(input_queue):
    while True:
        num = input_queue.get()
        if num is None:
            break
        process_number(num)


if __name__ == "__main__":
    data = generate_data(1000000)
    start = time.time()

    input_queue = multiprocessing.Queue()

    num_processes = multiprocessing.cpu_count()
    processes = []

    for _ in range(num_processes):
        p = multiprocessing.Process(target=worker, args=(input_queue,))
        processes.append(p)
        p.start()

    for i in data:
        input_queue.put(i)

    for _ in range(num_processes):
        input_queue.put(None)

    for p in processes:
        p.join()

    execute_time = time.time() - start
    results = ("processqueue", execute_time)
    with open("result.csv", "a") as fp:
        csv.writer(fp).writerow(results)
