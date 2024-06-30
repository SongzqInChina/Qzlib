def 阶乘(num):
    if num == 1:
        return 1
    else:
        return num * 阶乘(num - 1)


def 组合数(n, m):
    return 阶乘(n) / (阶乘(m) * 阶乘(n - m))

print(组合数(9, 3))