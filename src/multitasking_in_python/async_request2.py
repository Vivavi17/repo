import asyncio
import json
from concurrent.futures import ProcessPoolExecutor

import aiofiles
from aiohttp import ClientSession, ClientTimeout


async def fetch_urls(filename: str, workers: int) -> None:
    """
    Создает 2 очереди:
        urls_queue - очередь считанных урлов
        responses_queue - очередь полученных ответов

    Запускает N workers для обработки урлов
    """
    urls_queue = asyncio.Queue()
    responses_queue = asyncio.Queue()
    executor = ProcessPoolExecutor()

    tasks = [
        read_urls(filename, urls_queue, workers),
        *[prepare_url(urls_queue, responses_queue, executor) for _ in range(workers)],
        write_response(responses_queue),
    ]
    await asyncio.gather(*tasks)


async def read_urls(filename: str, urls_queue: asyncio.Queue, workers: int) -> None:
    async with aiofiles.open(filename, "r") as file:
        while True:
            url = await file.readline()
            if not url:
                for _ in range(workers):
                    await urls_queue.put(None)
                break
            await urls_queue.put(url.rstrip())


async def prepare_url(
    urls_queue: asyncio.Queue,
    responses_queue: asyncio.Queue,
    executor: ProcessPoolExecutor,
) -> None:
    async with ClientSession() as session:
        while True:
            url = await urls_queue.get()
            if url is None:
                await responses_queue.put(None)
                break
            try:
                async with session.get(
                    url, timeout=ClientTimeout(total=30)
                ) as response:
                    if response.status != 200:
                        continue
                    content = await response.read()
            except Exception:
                continue
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(executor, prepare_result, url, content)
            await responses_queue.put(result)


def prepare_result(url: str, content: bytes):
    content = json.loads(content.decode())
    return json.dumps({"url": url, "content": content}) + "\n"


async def write_response(responses_queue: asyncio.Queue) -> None:
    async with aiofiles.open("result.json", "a") as result_f:
        while True:
            response = await responses_queue.get()
            if response is None:
                break
            await result_f.write(response)


async def main():
    workers = 5
    filename_urls = "url"
    await fetch_urls(filename_urls, workers)
