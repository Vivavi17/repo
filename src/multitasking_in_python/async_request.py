import asyncio
import json

import aiofiles
from aiohttp import ClientSession, ClientTimeout


async def fetch_urls(filename: str) -> None:
    semaphore = asyncio.Semaphore(5)

    async with (
        aiofiles.open(filename, "r") as f,
        aiofiles.open("result.json", "a") as result_f,
        ClientSession() as session,
    ):
        urls = await get_urls(f)
        while urls:
            tasks = [
                asyncio.create_task(fetch_url(url, session, semaphore)) for url in urls
            ]
            responses = await asyncio.gather(*tasks)
            await result_f.writelines(responses)
            urls = await get_urls(f)


async def get_urls(file, len_lines: int = 100) -> list[str]:
    urls = [await file.readline() for _ in range(len_lines)]
    return [url.strip() for url in urls if url]


async def fetch_url(url: str, session: ClientSession, semaphore: asyncio.Semaphore):
    async with semaphore:
        try:
            async with session.get(url, timeout=ClientTimeout(total=30)) as response:
                if response.status != 200:
                    return
                content = await response.read()
        except Exception:
            return
    content = json.loads(content.decode())
    return json.dumps({"url": url, "content": content}) + "\n"


async def main():
    filename_urls = "url"
    await fetch_urls(filename_urls)


asyncio.run(main())
