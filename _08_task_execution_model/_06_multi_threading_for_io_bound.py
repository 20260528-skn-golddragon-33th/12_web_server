"""동기 requests도 스레드 여러 개에서 호출하면 네트워크 대기를 겹칠 수 있다."""
import argparse
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import requests


# [스레드·프로세스] 각 작업자가 같은 동기 I/O 함수를 실행한다.
def io_task(url):
    # [블로킹] 각 작업자는 응답을 기다리지만, 다른 작업자의 요청은 진행할 수 있다.
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.status_code


def run(mode, url):
    # [스레드·프로세스] mode에 따라 두 종류의 실행자 중 하나를 선택한다.
    executor_type = ProcessPoolExecutor if mode == 'process' else ThreadPoolExecutor
    start = time.perf_counter()
    with executor_type(max_workers=2) as executor:
        # [동시 실행] map이 두 I/O 작업을 맡기며 결과는 입력 순서를 유지한다.
        statuses = list(executor.map(io_task, [url, url]))
    print(f'{mode}: 상태={statuses}, {time.perf_counter() - start:.2f}초')

    return statuses


# [프로세스] 자식이 이 파일을 불러올 때 작업을 다시 생성하지 않도록 한다.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['thread', 'process', 'both'], default='thread')
    parser.add_argument('--url', default='https://httpbin.org/delay/2')
    args = parser.parse_args()
    for mode in (['thread', 'process'] if args.mode == 'both' else [args.mode]):
        run(mode, args.url)