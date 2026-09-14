"""CPU 작업을 스레드/프로세스로 비교한다. 일반 CPython 3.12(GIL 활성) 기준이다."""
import argparse
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def calculate(iterations):
    total = 0
    for i in range(iterations):
        total += i
    return total


def run(mode, iterations):
    # [스레드·프로세스] mode에 따라 동일한 CPU 작업의 실행자를 선택한다.
    executor_type = ProcessPoolExecutor if mode == 'process' else ThreadPoolExecutor
    start = time.perf_counter()
    # [병렬·동시성] 프로세스는 CPU 병렬 실행이 가능하지만 스레드는 GIL 영향을 받는다.
    # map 결과는 작업 완료 순서와 관계없이 입력 순서로 모인다.
    with executor_type(max_workers=2) as executor:
        results = list(executor.map(calculate, [iterations, iterations]))
    print(f'{mode}: 결과={results}, {time.perf_counter() - start:.2f}초')
    return results


# [프로세스] 자식이 이 파일을 불러올 때 작업을 다시 생성하지 않도록 한다.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['thread', 'process', 'both'], default='both')
    parser.add_argument('--iterations', type=int, default=5000000)
    args = parser.parse_args()
    for mode in (['thread', 'process'] if args.mode == 'both' else [args.mode]):
        run(mode, args.iterations)
    # 작업이 작으면 프로세스 시작 비용 때문에 더 느릴 수 있다.