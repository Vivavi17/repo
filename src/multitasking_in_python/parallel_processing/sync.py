import csv
import time

from src.multitasking_in_python.parallel_processing.data_process import (
    generate_data,
    process_number,
)

if __name__ == "__main__":
    start = time.time()

    data = generate_data(1000000)
    for i in data:
        process_number(i)
    execute_time = time.time() - start
    results = ("sync", execute_time)
    with open("result.csv", "a") as fp:
        csv.writer(fp).writerow(results)
