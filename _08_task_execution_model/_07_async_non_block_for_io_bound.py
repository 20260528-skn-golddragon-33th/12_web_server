"""I/O 작업 두 개를 하나의 이벤트 루프에서 진행한다. 스레드 예제의 대안이다."""
import argparse
import asyncio
import time
import aiohttp


# [코루틴 함수] io_task는 비동기 I/O 한 건의 실행 절차를 정의한다.
async def io_task(session, url, n):
    print(f'I/O 작업 {n} 시작')
    # [대기·양보] HTTP 응답을 기다리는 동안 다른 태스크가 진행할 수 있다.
    async with session.get(url) as response:
        response.raise_for_status()
        # [대기·양보] 본문 수신을 기다릴 때 제어권을 넘기고, 받은 JSON을 Python 값으로 바꾼다.
        data = await response.json()
        print(f'I/O 작업 {n} 완료')
        return data


# [코루틴 함수] main은 두 I/O 작업을 하나의 이벤트 루프에서 조율한다.
async def main(url):
    start = time.perf_counter()
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
        # [코루틴 객체] 두 io_task(...) 호출은 실행 전 객체를 만든다.
        # [태스크·동시 실행] gather가 태스크로 예약하며, 결과는 입력 순서로 모인다.
        results = await asyncio.gather(io_task(session, url, 1), io_task(session, url, 2))
    print(f'응답 {len(results)}개, 총 소요시간 {time.perf_counter() - start:.2f}초')
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='https://httpbin.org/delay/2')
    # [이벤트 루프] 새 루프에서 main 코루틴을 실행하고, 끝나면 루프를 정리한다.
    asyncio.run(main(parser.parse_args().url))