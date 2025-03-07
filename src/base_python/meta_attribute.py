from datetime import datetime


class AddAttributeMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs["created_at"] = datetime.now()
        return super().__new__(cls, name, bases, attrs)


if __name__ == "__main__":

    class First(metaclass=AddAttributeMeta): ...

    a, b = First(), First()
    assert a.__getattribute__("created_at")
    assert a.created_at == b.created_at == First.created_at

    class Second(metaclass=AddAttributeMeta): ...

    b = Second()
    assert a.created_at != b.created_at
