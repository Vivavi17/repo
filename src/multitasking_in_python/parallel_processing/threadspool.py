import csv
import time
from concurrent.futures import ThreadPoolExecutor

from src.multitasking_in_python.parallel_processing.data_process import (
    generate_data,
    process_number,
)


def processing_thread_pool(data: list[int]) -> list[int]:
    with ThreadPoolExecutor() as executor:
        return list(executor.map(process_number, data))


if __name__ == "__main__":
    data = generate_data(1000000)
    start = time.time()
    result = processing_thread_pool(data)
    execute_time = time.time() - start
    results = [("type", "time"), ("threads", execute_time)]
    with open("result.csv", "a") as fp:
        csv.writer(fp).writerows(results)
