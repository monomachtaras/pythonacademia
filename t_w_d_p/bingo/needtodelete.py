class TestClass(object):

    __var = 6
    _var = 6
    var = 6

    def __init__(self):
        self.__var = 46
        self._var = 45
        self.var = 44

    def __str__(self):
        return str(self.__var) + str(self._var) + str(self.var)

x = 6
class TestClass2(TestClass):

    __var = 6
    _var = 6
    var = 6

    def __init__(self):
        super.__init__()
        self.__var = 46
        self._var = 45
        self.var = 44

    def __str__(self):
        return str(self.__var) + str(self._var) + str(self.var)

def func():
    print(x)
    tc = TestClass()
    print(tc._var)
    tc._var = 0
    print(tc)
