# Python program to illustrate the concept 
# of threading 
# importing the threading module 
import threading 

import concurrent.futures

def foo(bar):
    print('hello {}'.format(bar))
    return 'foo'

def cube(num): 
    """ 
    function to print cube of given num 
    """
    print("Cube: {}".format(num * num * num)) 

    return num * num * num

with concurrent.futures.ThreadPoolExecutor() as executor:
    future = executor.map(cube, range(3))
    print(future)
    cubes = [x for x in future]

    print(cubes)
    # return_value = future.result()
    # print(return_value)
  
def print_square(num): 
    """ 
    function to print square of given num 
    """
    print("Square: {}".format(num * num)) 
    return num * num
  
# if __name__ == "__main__": 
#     # creating thread 
#     t1 = threading.Thread(target=print_square, args=(10,)) 
#     t2 = threading.Thread(target=print_cube, args=(10,)) 
  
#     # starting thread 1 
#     t1.start() 
#     # starting thread 2 
#     t2.start() 
  
#     # wait until thread 1 is completely executed 
#     val1 = t1.join() 
#     # wait until thread 2 is completely executed 
#     val2 = t2.join() 

    print(val1)
    print(val2)
  
    # both threads completely executed 
    print("Done!") 