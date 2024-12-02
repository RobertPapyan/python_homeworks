import random
import time


def execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time for {func.__name__}: {end_time - start_time:.6f} seconds")
        return result
    return wrapper


@execution_time
def create_file_with_random_numbers(filename):
    with open(filename, "w") as file:
        for _ in range(100):
            random_numbers = [random.randint(1, 100) for _ in range(20)]
            file.write(" ".join(map(str, random_numbers)) + "\n")


@execution_time
def process_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    filtered_data = []
    for line in lines:
        numbers = list(map(int, line.split()))
        filtered_numbers = list(filter(lambda x: x > 40, numbers))
        filtered_data.append(filtered_numbers)

    with open(filename, "w") as file:
        for filtered_numbers in filtered_data:
            file.write(" ".join(map(str, filtered_numbers)) + "\n")


def read_file_as_generator(filename):
    with open(filename, "r") as file:
        for line in file:
            yield line.strip()


@execution_time
def use_generator(filename):
    for line in read_file_as_generator(filename):
        print(line)  


if __name__ == "__main__":
    filename = "text.txt"
    create_file_with_random_numbers(filename)
    process_file(filename)
    use_generator(filename)
