import SzQlib

if __name__ == '__main__':
    for i in SzQlib.path.listdir("."):
        print("file:", i)
        f = open(i)
        print(f.read())
        f.close()
