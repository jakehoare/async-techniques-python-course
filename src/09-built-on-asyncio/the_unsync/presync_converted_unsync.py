from unsync import unsync
import asyncio
import datetime
import math

import aiohttp
import requests


def main():
    t0 = datetime.datetime.now()

    #loop = asyncio.get_event_loop() no required unsync


    tasks = [
        compute_some(),
        compute_some(),
        compute_some(),
        download_some(),
        download_some(),
        download_some_more(),
        download_some_more(),
        wait_some(),
        wait_some(),
        wait_some(),
        wait_some(),
    ]

    [t.result() for t in tasks]
    #loop.run_until_complete(asyncio.gather(*tasks)) removed for unsync

    dt = datetime.datetime.now() - t0
    print("Synchronous version done in {:,.2f} seconds.".format(dt.total_seconds()))

@unsync(cpu_bound=True)
# cpu_bound runs on multiprocessing
def compute_some():
    # no awaiting possible
    print("Computing...")
    for _ in range(1, 10_000_000):
        math.sqrt(25 ** 25 + .01)

@unsync
async def download_some():
    print("Downloading...")
    url = 'https://talkpython.fm/episodes/show/174/coming-into-python-from-another-industry-part-2'
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as resp:
            resp.raise_for_status()

            text = await resp.text()

    print("Downloaded (more) {:,} characters.".format(len(text)))

# decorator applied to regular method will run on thread not event loop
@unsync
def download_some_more():
    # no await so no advantage of async (threading would help)
    print("Downloading more ...")
    url = 'https://pythonbytes.fm/episodes/show/92/will-your-python-be-compiled'
    resp = requests.get(url)
    resp.raise_for_status()

    text = resp.text

    print("Downloaded {:,} characters.".format(len(text)))

# unsync decorator on async method runs in ambient event loop
@unsync
async def wait_some():
    print("Waiting...")
    for _ in range(1, 1000):
        await asyncio.sleep(.001)


if __name__ == '__main__':
    main()
