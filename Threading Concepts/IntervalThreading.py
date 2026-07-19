## Run function after some delay

from threading import Timer

Timer(5, print, args=["Hello"]).start();