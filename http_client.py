import requests
import time
import random
import threading
import concurrent.futures
import json
import asyncio
import aiohttp
import csv

API_URL = "http://127.0.0.1:5000/sqrt"


#调用api，功能验证为串行，性能压测为异步io
async def call_api(session, number):
    start_time = time.time()
    async with session.post(API_URL, json={'number': number}) as response:
        end_time = time.time()
        delay = (end_time - start_time) * 1000  # 转换为毫秒
        if response.status == 200:
            result = await response.json()
            api_delay = result.get('delay') * 1000
            return {
                'input': number,
                'output': result.get('result'),
                'delay': delay,
                'api_delay': api_delay,
                'success': 100 <= delay <= 200
            }
        return {
            'input': number,
            'output': None,
            'delay': delay,
            'api_delay': None,
            'success': False
        }

async def validate_functionality():
    results = []
    async with aiohttp.ClientSession() as session:
        for _ in range(10000):
            number = random.randint(1, 1000000)
            result = await call_api(session, number)
            results.append(result)
    return results

async def performance_test(qps, duration=10):
    async def worker(lock):
        nonlocal success_count, total_count
        while time.time() < end_time:
            number = random.randint(1, 1000000)
            result = await call_api(session, number)
            async with lock:
                total_count += 1
                if result['success']:
                    success_count += 1
            await asyncio.sleep(1 / qps)  # 控制每个worker的请求速率，确保在每秒发送 qps 次请求。


    start_time = time.time()
    end_time = start_time + duration
    success_count = 0
    total_count = 0
    lock = asyncio.Lock()

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(worker(lock)) for _ in range(qps)]
        await asyncio.gather(*tasks)

    success_rate = (success_count / total_count) * 100 if total_count > 0 else 0
    return success_rate

async def main():
    # 功能验证
    results = await validate_functionality()
    with open('validation_results.json', 'w') as f:
        json.dump(results, f, indent=4)

    # 写入CSV文件
    with open('validation_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['input', 'output', 'delay', 'api_delay', 'success']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # 写入列标题
        for result in results:
            writer.writerow(result)  # 写入每一行数据

    success_cases = sum(result['success'] for result in results)
    print(f"Functional validation success rate: {success_cases / 10000 * 100}%")

    # 性能测试
    qps_values = [10, 100, 1000, 10000]
    for qps in qps_values:
        success_rate = await performance_test(qps)
        print(f"QPS: {qps}, Success Rate: {success_rate}%")
        if success_rate < 99.95:
            break

if __name__ == '__main__':
    asyncio.run(main())



# async def call_api(session, number):
#     start_time = time.time()
#     async with session.post(API_URL, json={'number': number}) as response:
#         end_time = time.time()
#         delay = (end_time - start_time) * 1000  # 转换为毫秒
#         if response.status == 200:
#             result = await response.json()
#             api_delay = result.get('delay') * 1000
#             return {
#                 'input': number,
#                 'output': result.get('result'),
#                 'delay': delay,
#                 'api_delay': api_delay,
#                 'success': 100 <= delay <= 200
#             }
#         return {
#             'input': number,
#             'output': None,
#             'delay': delay,
#             'api_delay': None,
#             'success': False
#         }
#
# async def validate_functionality():
#     results = []
#     async with aiohttp.ClientSession() as session:
#         tasks = [call_api(session, random.randint(1, 1000000)) for _ in range(10000)]
#         for result in await asyncio.gather(*tasks):
#             results.append(result)
#     return results
#
#
# async def performance_test(qps, duration=10):
#     async def worker():
#         nonlocal success_count, total_count
#         while time.time() < end_time:
#             number = random.randint(1, 1000000)
#             result = await call_api(session, number)
#             if result['success']:
#                 success_count += 1
#             total_count += 1
#
#     start_time = time.time()
#     end_time = start_time + duration
#     success_count = 0
#     total_count = 0
#
#     async with aiohttp.ClientSession() as session:
#         tasks = [asyncio.create_task(worker()) for _ in range(qps)]
#         await asyncio.gather(*tasks)
#
#     success_rate = (success_count / total_count) * 100
#     return success_rate
#
# async def main():
#     # 功能验证
#     results = await validate_functionality()
#     with open('validation_results.json', 'w') as f:
#         json.dump(results, f, indent=4)
#     success_cases = sum(result['success'] for result in results)
#     print(f"Functional validation success rate: {success_cases / 10000 * 100}%")
#
#     # 性能测试
#     qps_values = [10, 100, 1000, 10000]
#     for qps in qps_values:
#         success_rate = await performance_test(qps)
#         print(f"QPS: {qps}, Success Rate: {success_rate}%")
#         if success_rate < 99.95:
#             break
#
#
# if __name__ == '__main__':
#     asyncio.run(main())


# #api调用函数
# def call_api(number):
#     start_time = time.time()
#     response = requests.post(API_URL, json={'number': number})
#     end_time = time.time()
#     delay = (end_time - start_time) * 1000  #转换为毫秒
#     if response.status_code == 200:
#         result = response.json().get('result')
#         api_delay = response.json().get('delay') * 1000
#         return {
#             'input': number,
#             'output': result,
#             'delay': delay,
#             'api_delay': api_delay,
#             'success': 100 <= delay <= 200
#         }
#     return {
#         'input': number,
#         'output': None,
#         'delay': delay,
#         'api_delay': None,
#         'success': False
#     }
#
# #功能验证函数
# def validate_functionality():
#     results = []
#     for _ in range(10000):
#         number = random.randint(1, 1000000)
#         #number = random.randint(1, 20000)
#         result = call_api(number)
#         results.append(result)
#     return results
#
# #性能测试函数：在给定QPS和持续时间下测试api性能
# def performance_test(qps, duration=10):
#     lock = threading.Lock()  # 创建一个锁对象
#     def worker():
#         nonlocal success_count, total_count #明确外部变量
#         while time.time() < end_time:
#             number = random.randint(1, 1000000)
#             #number = random.randint(1, 20000)
#             result = call_api(number)
#             with lock:  # 使用锁确保操作的原子性
#                 if result['success']:
#                     success_count += 1
#                 total_count += 1
#
#     start_time = time.time()
#     end_time = start_time + duration
#     success_count = 0
#     total_count = 0
#
#     threads = []
#     for _ in range(qps):
#         thread = threading.Thread(target=worker)
#         thread.start()
#         threads.append(thread)
#
#     for thread in threads:
#         thread.join()
#
#     success_rate = (success_count / total_count) * 100
#     return success_rate
#
#
# def main():
#     #功能验证
#     results = validate_functionality()
#     with open('validation_results.json', 'w') as f:
#         json.dump(results, f, indent=4)
#     success_cases = sum(result['success'] for result in results)
#     print(f"Functional validation success rate: {success_cases / 10000 * 100}%")
#
#     #性能测试
#     qps_values = [10, 100, 1000, 10000]
#     for qps in qps_values:
#         success_rate = performance_test(qps)
#         print(f"QPS: {qps}, Success Rate: {success_rate}%")
#         if success_rate < 99.95:
#             break
#
#
# if __name__ == '__main__':
#     main()

"""
QPS（Queries Per Second）即每秒查询数，是衡量一个系统在一秒内能处理多少请求的指标。QPS 是衡量系统性能和吞吐量的重要参数。
每个线程都独立地运行，并且多个线程同时发起请求。这些线程并行运行的效果是：
如果我们创建了 10 个线程，并且每个线程在 1 秒内可以完成 1 个请求，那么这相当于系统处理了 10 QPS。
如果我们创建了 100 个线程，每个线程在 1 秒内完成 1 个请求，那么系统处理了 100 QPS。
通过调整线程数（QPS 值），我们模拟了系统在不同并发请求数下的表现。
"""