import time
def time_func(f_source):
    def wrapper(*args, **kwargs):
        
        init = time.time()
        
        response = f_source(*args, **kwargs)
        
        t = time.time() - init
        print('{t}s')
        
        return response
    return wrapper