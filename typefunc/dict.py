def sub(dic1, dic2):
    # dic1 in dic2
    if tuple(dic1) <= tuple(dic2):
        for i in dic1:
            if i not in dic2 or dic1[i] != dic2[i]:
                return False
        return True
    else:
        return False


def parent(dic1, dic2):
    # dic2 in dic1
    return sub(dic2, dic1)


def key_sub(dic1, dic2):
    return tuple(dic1) <= tuple(dic2)


def key_parent(dic1, dic2):
    return tuple(dic2) <= tuple(dic1)


def update(dic1, dic2):
    # update 将dic2 的值更新到 dic1
    for i in dic2:
        dic1[i] = dic2[i]
    return dic1


def eupdate(dic1, dic2):
    for i in dic2:
        if i not in dic1:
            dic1[i] = dic2[i]
    return dic1


def sort(dic1, dic2):
    # 将两部字典的键修改至相同
    for i in dic1:
        if i not in dic2:
            dic2[i] = dic1[i]
    for i in dic2:
        if i not in dic1:
            dic1[i] = dic2[i]
    return dic1
