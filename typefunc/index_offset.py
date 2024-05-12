from typing import Iterable


class offset:
    def __init__(self, iterable):
        self.iterable = iterable
        self.start = 0

    def offset(self, lenght):
        data = self.iterable[self.start: self.start + lenght]
        self.start += lenght
        return data

    def offseter(self, lenght):
        data = self.iterable[self.start: self.start + lenght]
        self.start += lenght
        return self.__class__(data)

    def isend(self):
        return self.start >= len(self.iterable)

    def __iter__(self):
        return self.iterable[self.start:]

    def __getitem__(self, item):
        return self.iterable[item]

    def __len__(self):
        return len(self.iterable)

    def __setitem__(self, key, value):
        self.iterable[key] = value

    def n_offset(self, lenght):
        return self.iterable[self.start: self.start + lenght]

    def back(self, lenght):
        data = self.iterable[self.start - lenght: self.start]
        self.start -= lenght
        return data
    
    def n_back(self, lenght):
        data = self.iterable[self.start - lenght: self.start]
        return data
    
    def backer(self, lenght):
        data = self.iterable[self.start - lenght: self.start]
        self.start -= lenght
        return self.__class__(data)
    
    def n_offseter(self, lenght):
        data = self.iterable[self.start - lenght: self.start]
        return self.__class__(data)
    
    def n_backer(self, lenght):
        data = self.iterable[self.start - lenght: self.start]
        return self.__class__(data)

    def to(self, _Type):
        try:
            return _Type(self.iterable)
        except TypeError as e:
            raise e from None
        except Exception as e:
            raise e from None

    # >
    def __gt__(self, lenght):
        """
        offset.offset(lenght)
        :param lenght: an int value of lenght 
        :return: Iterable
        """
        return self.offset(lenght)
    
    # < 
    def __lt__(self, lenght):
        """
        offset.offset(lenght)
        :param lenght: an int value of lenght 
        :return: Iterable
        """
        return self.back(lenght)
    
    # >=
    def __ge__(self, lenght):
        """
        offset.n_offset(lenght)
        :param lenght: an int value of lenght 
        :return: Iterable
        """
        return self.n_offset(lenght)
    
    # <=
    def __le__(self, lenght):
        """
        offset.offset(lenght)
        :param lenght: an int value of lenght 
        :return: Iterable
        """
        return self.n_back(lenght)
    
    # +
    def __add__(self, lenght):
        """
        start += lenght
        :param lenght: an int value of lenght 
        :return: None
        """
        self.start += lenght
    
    # -
    def __sub__(self, lenght):
        """
        start -= lenght
        :param lenght: an int value of lenght
        :return: None
        """
        self.start -= lenght

    # +=
    def __iadd__(self, lenght):
        """
        start += lenght
        :param lenght: an int value of lenght
        :return: None
        """
        self.start += lenght
        return self

        