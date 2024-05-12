def split_order(order: str):
    olst = order.split()
    objs = []
    is_text = 0
    for i in olst:
        if i.startswith('"'):
            objs.append('')
            is_text = 1
            i = i[1:]
        if i.endswith('"'):
            is_text = 0
            i = i[:-1]
        if is_text:
            objs[-1] = objs[-1] + " " + i
        else:
            objs.append(i)
    return objs


def get_order(text=""):
    order = input(text)
    return split_order(order)
