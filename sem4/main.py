import requests
from pathlib import Path
import time
import threading
import multiprocessing
import asyncio
import aiohttp
from random import randint


# Написать программу, которая считывает список из 10 URL-адресов и одновременно загружает данные с каждого адреса.
# После загрузки данных нужно записать их в отдельные файлы.
# Используйте потоки.
def download(url: str, type_: str):
    start_time = time.time()
    response = requests.get(url)
    filename = type_ + url.replace('https:', '').replace('.', '_').replace('/', '') + '.html'
    with open(f"./upload/{filename}", 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


def task1(urls: list[str]):
    start_time = time.time()
    threads = []
    for url in urls:
        thread = threading.Thread(target=download, args=[url, "thread_"])
        threads.append(thread)
        thread.start()
        # download(url, start_time) # 10.87

    for thread in threads:
        thread.join()  # 2.83
    print(f"Thread tasks took {time.time() - start_time:.2f} seconds")


# Написать программу, которая считывает список из 10 URLадресов и одновременно загружает данные с каждого адреса.
# После загрузки данных нужно записать их в отдельные файлы.
# Используйте процессы.
def task2(urls: list[str]):
    start_time = time.time()
    processes = []
    for url in urls:
        process = multiprocessing.Process(target=download, args=[url, "process_"])
        processes.append(process)
        process.start()

    for process in processes:
        process.join()  # 3.78
    print(f"Multiprocess tasks took {time.time() - start_time:.2f} seconds")


async def download_async(url: str, type_: str):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    filename = (type_ + url.replace('https:', '').replace('.', '_').replace('/', '')
                + '.html')
    with open(f"./upload/{filename}", 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


# Написать программу, которая считывает список из 10 URLадресов и одновременно загружает данные с каждого адреса.
# После загрузки данных нужно записать их в отдельные файлы.
# Используйте асинхронный подход.
async def task3(urls):
    start_time = time.time()
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download_async(url, 'async_'))
        tasks.append(task)
    await asyncio.gather(*tasks)  # 1.01
    print(f"Async tasks took {time.time() - start_time:.2f} seconds")


def count_words(file: Path):
    start_time = time.time()
    with open(file, encoding='utf-8') as f:
        text = f.read()
    print(f"In file {file.name} {len(text.split())} words - {time.time() - start_time:.2f} ")


# Создать программу, которая будет производить подсчет количества слов в каждом файле в указанной директории
# и выводить результаты в консоль.
# Используйте потоки.
def task4(path: Path):
    start_time = time.time()
    files = [file for file in path.iterdir() if file.is_file()]
    threads = []
    for file in files:
        thread = threading.Thread(target=count_words, args=[file])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print(f"Thread tasks took {time.time() - start_time:.2f} seconds")


# Создать программу, которая будет производить подсчет количества слов в каждом файле в указанной директории
# и выводить результаты в консоль.
# Используйте процессы.
def task5(path: Path):
    start_time = time.time()
    files = [file for file in path.iterdir() if file.is_file()]
    processes = []
    for file in files:
        process = multiprocessing.Process(target=count_words, args=[file])
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    print(f"Multiprocess tasks took {time.time() - start_time:.2f} seconds")


# Создать программу, которая будет производить подсчет количества слов в каждом файле в указанной директории
# и выводить результаты в консоль.
# Используйте асинхронный подход.
async def count_words_async(file: Path):
    start_time = time.time()
    with open(file, encoding='utf-8') as f:
        text = f.read()
    print(f"In file {file.name} {len(text.split())} words - {time.time() - start_time:.2f} ")


async def task6(path: Path):
    start_time = time.time()
    tasks = [asyncio.create_task(count_words_async(file)) for file in path.iterdir() if file.is_file()]
    await asyncio.gather(*tasks)
    print(f"Async tasks took {time.time() - start_time:.2f} seconds")


# Напишите программу на Python, которая будет находить сумму элементов массива из 1000000 целых чисел.
# Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
# Массив должен быть заполнен случайными целыми числами от 1 до 100.
# При решении задачи нужно использовать многопоточность, многопроцессорность и асинхронность.
# В каждом решении нужно вывести время выполнения вычислений.
async def get_sum_array_async(arr: list[int]):
    return sum(arr)


async def task7_async(arr: list[int]):
    start_time = time.time()
    arr_len_10 = len(arr) // 10
    result = await asyncio.gather(*[get_sum_array_async(arr[arr_len_10 * i:arr_len_10 * (i + 1)]) for i in range(10)])
    print(f"Async - sum arr = {sum(result)} - took {time.time() - start_time:.5f}")


def task7():
    arr = [randint(1, 100) for i in range(1_000_000)]
    asyncio.run(task7_async(arr))
    start_time = time.time()
    sum_arr = sum(arr)
    print(f"Noraml - sum arr = {sum_arr} - took {time.time() - start_time:.5f}")  # 2 times faster than async


def main():
    Path(Path.cwd() / 'upload').mkdir(exist_ok=True)
    urls = [
        'https://www.google.ru/',
        'https://gb.ru/',
        'https://ya.ru/',
        'https://www.python.org/',
        'https://habr.com/ru/all/',
        'https://mail.ru/',
        'https://www.yahoo.com/',
        'https://www.rambler.ru/',
        'https://www.wikipedia.org/',
        'https://pikabu.ru/'
    ]

    # task1(urls)  # 2.67s
    # task2(urls)  # 4.68s
    # loop = asyncio.get_event_loop() # Not working
    # loop.run_until_complete(task3) # Not working
    # asyncio.run(task3(urls))  # preferred - 1.09s
    path = Path(Path.cwd() / 'upload')
    # task4(path)  # 0.13s
    # task5(path)  # 5.48s
    # asyncio.run(task6(path))  # 0.13s
    task7()


if __name__ == '__main__':
    main()
