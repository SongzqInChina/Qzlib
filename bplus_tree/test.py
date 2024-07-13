#
# # 创建B+树实例
# tree = BplusTree(t=4)  # 设置树的阶数为4
#
# number = 1000
#
# # 准备测试数据
# data_size = 10000
# data = [(i, f'value_{i}') for i in range(data_size)]
#
# # 测试插入操作
# insert_time = timeit.timeit(lambda: [tree.insert(key, value) for key, value in data], number=number)
# print(f"Insert {data_size} elements took {insert_time:.6f} seconds")
#
# # 测试搜索操作
# search_time = timeit.timeit(lambda: [tree.search(i) for i in range(data_size)], number=number)
# print(f"Search {data_size} elements took {search_time:.6f} seconds")
#
# # 测试删除操作
# delete_time = timeit.timeit(lambda: [tree.delete(i) for i in range(data_size)], number=number)
# print(f"Delete {data_size} elements took {delete_time:.6f} seconds")
import time
import timeit
import numpy as np
from decimal import Decimal
from bplustree import BplusTree

tree = BplusTree(5)
for i in range(100):
    tree.insert(i, f"Value({i})")

for i in range(100):
    print(tree.search(i).result)

# number = 10000
#
# lst = [0] * number
# ary = np.zeros(number)
#
#
#
# def ary_set_time():
#     for k in range(number):
#         ary[k] = 1000
#
#
# def ary_get_time():
#     for k in range(number):
#         ary[k]
#
#
# def lst_set_time():
#     global lst
#     for v in range(number):
#         lst[v] = 1000
#
#
# def lst_get_time():
#     for index in range(number):
#         lst[index]
#
# sep_time = 3
#
# while True:
#     lst, ary = [0] * number, np.zeros(number)
#
#     ary_set = (Decimal(timeit.timeit(ary_set_time, number=number)))
#     ary_get = (Decimal(timeit.timeit(ary_get_time, number=number)))
#
#     lst_set = (Decimal(timeit.timeit(lst_set_time, number=number)))
#     lst_get = (Decimal(timeit.timeit(lst_get_time, number=number)))
#
#     print(ary_set, ary_get, lst_set, lst_get, sep='\n')
#
#     print(ary_set / ary_get, lst_set / lst_get, sep='\n')
#
#     if ary_set > lst_set:
#         print("lst_set速度大于ary_set")
#     else:
#         print("ary_set速度大于lst_set")
#
#     if ary_get > lst_get:
#         print("lst_get速度大于ary_get")
#     else:
#         print("ary_get速度大于lst_get")
#
#     time.sleep(sep_time)
