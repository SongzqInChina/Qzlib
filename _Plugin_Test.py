import inspect


def d():
    # for i in (inspect.stack()):
    # print(i)
    print(inspect.stack()[0].function)


def c(): d()


def b(): c()


def a(): b()


a()

print(inspect.stack()[0].function)
