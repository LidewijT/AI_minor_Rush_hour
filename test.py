# from time import sleep
#
# def progress(percent=0, width=40):
#     # percent = percent
#     left = width * percent // 100
#     right = width - left
#
#     tags = "#" * left
#     spaces = " " * right
#     percents = f"{percent:.0f}%"
#
#     print("\r[", tags, spaces, "]", percents, sep="", end="", flush=True)
#
# # Example run
# for i in range(121):
#     progress(i/121)
#     sleep(0.05)
from tqdm import tqdm
import time


for i in tqdm (range (101),desc="Loading…", ncols=75):
	time.sleep(0.01)
    # a = 1

print("Complete.")
