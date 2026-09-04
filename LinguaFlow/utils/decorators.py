from time import time

def calc_execution_time(func):
    """
        Decorator to calculate the execution time of a function.
    """
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        execution_time = end_time - start_time
        print(f"\nExecution time of {func.__name__}: {execution_time:.6f} seconds\n")
        return result
    return wrapper