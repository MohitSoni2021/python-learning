import threading;
import time;
from typing import Union, List;

def func1(a : int, b : int):
    time.sleep(5);
    print(f"Func1 : {a+b}");

def func2(a : int, b : int):
    time.sleep(2);
    print(f"Func2 : {a+b}");

# Creating thread for the function;
# Thread can be used only once, if we create below threads we can start them only once, if i tried to run twices it shows me the error;
func1Thread = threading.Thread(target=func1, args=(1,2));
func2Thread = threading.Thread(target=func2, args=(3, 5));

#running functions using thread;
func1Thread.start();
func1Thread.join();  # This join function tell that 1st run this thread and let other thread to wait, sequence execution;

func2Thread.start();
func2Thread.join();