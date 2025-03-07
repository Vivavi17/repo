from src.base_python.import_singleton import object_singleton


class SingletonMeta(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super().__call__()
        return cls._instance[cls]


class SingletonNew:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


def singleton_decorator(cls):
    _instance = {}

    def create_object(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return create_object


if __name__ == "__main__":

    class FirstSingleton(metaclass=SingletonMeta): ...

    class SecondSingleton(metaclass=SingletonMeta): ...

    @singleton_decorator
    class BaseClass: ...

    a, b = FirstSingleton(), FirstSingleton()
    c, d = SecondSingleton(), SecondSingleton()
    assert a is b
    assert c is d
    assert a is not c

    a, b = SingletonNew(), SingletonNew()
    assert a is b

    a, b = BaseClass(), BaseClass()
    assert a is b

    a, b = object_singleton, object_singleton
    assert a is b
