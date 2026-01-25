import psutil
import os

print(f"Memory percent used: {psutil.virtual_memory().percent}%")

process = psutil.Process(os.getpid())
memory_use = process.memory_info().rss / (1024 * 1024) # in MiB
print(f"Current process memory use: {memory_use:.2f} MiB")

available_memory = psutil.virtual_memory().available / (1024**3)
print(f"Available system memory: {available_memory:.1f} GB")