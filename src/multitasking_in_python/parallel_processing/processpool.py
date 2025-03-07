import csv
import multiprocessing
import time

from src.multitasking_in_python.parallel_processing.data_process import (
    generate_data,
    process_number,
)


def processing_process_pool(data: list[int]) -> list[int]:
    with multiprocessing.Pool() as p:
        return p.map(process_number, data)


if __name__ == "__main__":
    data = generate_data(1000000)
    start = time.time()
    result = processing_process_pool(data)
    execute_time = time.time() - start
    results = ("processpool", execute_time)
    with open("result.csv", "a") as fp:
        csv.writer(fp).writerow(results)
