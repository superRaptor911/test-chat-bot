import time
import psutil
import sys
import pandas as pd
import pickle

def time_elapsed(start):
    end = time.time()
    return (end - start) * 1000

def eval_performance(fn):
    start = time.time()
    val = fn()
    time_taken = time_elapsed(start)
    print(f"Time taken by {fn.__name__} : {time_taken:.2f} ms")
    return val


def print_total_memory_usage():
    mem = psutil.Process().memory_info().rss 
    print(f"memory_usage is : {obj_size_fmt(mem)}")


def get_memory_usage(obj):
    # Calculate the size of the dictionary object itself
    size = sys.getsizeof(obj)

    # If the object is a dictionary, calculate the size of its values recursively
    if isinstance(obj, dict):
        for key, value in obj.items():
            size += sys.getsizeof(key)
            size += get_memory_usage(value)

    # If the object is a list, tuple, or set, calculate the size of its elements recursively
    elif isinstance(obj, (list, tuple, set)):
        for elem in obj:
            size += get_memory_usage(elem)

    return size

def obj_size_fmt(num):
    if num<10**3:
        return "{:.2f}{}".format(num,"B")
    elif ((num>=10**3)&(num<10**6)):
        return "{:.2f}{}".format(num/(1.024*10**3),"KB")
    elif ((num>=10**6)&(num<10**9)):
        return "{:.2f}{}".format(num/(1.024*10**6),"MB")
    else:
        return "{:.2f}{}".format(num/(1.024*10**9),"GB")

def memory_usage(global_vars):
    memory_usage_by_variable=pd.DataFrame({k:get_memory_usage(v)\
            for (k,v) in global_vars.items()},index=['Size'])
    memory_usage_by_variable=memory_usage_by_variable.T
    memory_usage_by_variable=memory_usage_by_variable\
            .sort_values(by='Size',ascending=False).head(10)

    memory_usage_by_variable['Size']=memory_usage_by_variable['Size'].apply(lambda x: obj_size_fmt(x))
    return memory_usage_by_variable


def pickle_object(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

def unpickle_object( path):
    with open(path, 'rb') as f:
        return pickle.load(f)
