# helpers/aiohttp_fetch.py
import asyncio
from contextlib import nullcontext

import aiohttp

from helpers.exceptions import CustomException, TooManyRequestsException
from helpers.loggers import logger

RETRY_LIMIT = 10

__all__ = [
    "aiohttp_fetch",
    "aiohttp_fetch_from_session",
]


# --- public functions ---
async def aiohttp_fetch(
    url,
    params=None,
    headers=None,
    semaphore=None,
    retry_limit=RETRY_LIMIT,
    sleep_time=2,
    pre_sleep=0,
):
    async with aiohttp.ClientSession() as session:
        return await _fetch_with_retry(
            session,
            url,
            params,
            headers,
            semaphore,
            retry_limit,
            sleep_time,
            pre_sleep,
        )


async def aiohttp_fetch_from_session(
    session,
    url,
    params=None,
    headers=None,
    semaphore=None,
    retry_limit=RETRY_LIMIT,
    sleep_time=2,
    pre_sleep=0,
):
    return await _fetch_with_retry(
        session,
        url,
        params,
        headers,
        semaphore,
        retry_limit,
        sleep_time,
        pre_sleep,
    )


# --- private functions ---
async def _fetch_with_retry(
    session,
    url,
    params=None,
    headers=None,
    semaphore=None,
    retry_limit=RETRY_LIMIT,
    sleep_time=2,
    pre_sleep=0,
):
    for retry in range(retry_limit):
        await asyncio.sleep(sleep_time * (retry + pre_sleep))
        try:
            return await _fetch_from_session(session, url, params, headers, semaphore)
        except TooManyRequestsException:
            await asyncio.sleep(3 * sleep_time * (retry + pre_sleep))
        except Exception as e:  # noqa pylint: disable=broad-except disable=invalid-name
            logger.warning(f"Error occurred while fetching {url}: {e}")
    return None


async def _fetch_from_session(session, url, params=None, headers=None, semaphore=None):
    async with semaphore if semaphore else nullcontext():
        async with session.get(url, params=params, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            elif response.status == 429:
                raise TooManyRequestsException()
            else:
                response_text = await response.text()
                raise CustomException(
                    f"Fetch {url=} failed with {response.status=}; {response.reason=}; {response_text=}"
                )


# --- additional functions ---
def _fetch_recent_erc20_transactions(*args, **kwargs):  # pylint: disable=unused-argument
    pass


def _fetch_transaction_details(*args, **kwargs):  # pylint: disable=unused-argument
    pass


async def _sliding_window(session, tx_list, max_concurrent=10):
    results = []
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_and_process(tx):
        try:
            result = await _fetch_transaction_details(session, tx, semaphore)
            results.append(result)
        except Exception as e:  # noqa pylint: disable=broad-except disable=invalid-name
            print(f"Error fetching {tx}: {e}")

    tasks = [fetch_and_process(tx) for tx in tx_list]
    await asyncio.gather(*tasks)

    return results


async def _get_erc20_tx_details(address, page_limit=1_000, result_limit=1_000, date_limit=None):
    async with aiohttp.ClientSession() as session:
        tx_list = await _fetch_recent_erc20_transactions(
            session,
            address=address,
            page_limit=page_limit,
            result_limit=result_limit,
            date_limit=date_limit,
        )
        responses = await _sliding_window(session, tx_list, max_concurrent=10)
        return tx_list, responses
