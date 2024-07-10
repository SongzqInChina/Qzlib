import timeit
import random
from cpp import MutableTuple  # 假设你的自定义可变元组定义在这里

# 初始化列表和可变元组
lst = list(range(1000))
mt = MutableTuple(*range(1000))

# 测试插入操作
print(timeit.timeit('lst.insert(500, 9999)', globals=globals(), number=1000))
print(timeit.timeit('mt.insert(500, 9999)', globals=globals(), number=1000))
print()
# 测试删除操作
print(timeit.timeit('lst.pop(500)', globals=globals(), number=1000))
print(timeit.timeit('mt.pop(500)', globals=globals(), number=1000))
print()
# 测试更新元素
print(timeit.timeit('lst[500] = 8888', globals=globals(), number=1000))
print(timeit.timeit('mt[500] = 8888', globals=globals(), number=1000))
print()
# 测试索引访问
print(timeit.timeit('lst[500]', globals=globals(), number=1000))
print(timeit.timeit('mt[500]', globals=globals(), number=1000))
print()
# 测试切片操作
print(timeit.timeit('lst[100:200]', globals=globals(), number=1000))
print(timeit.timeit('mt[100:200]', globals=globals(), number=1000))
