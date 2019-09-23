import abc


class Observer(metaclass=abc.ABCMeta):
    def __init__(self):
        self._subject = None
        self._observer_state = None

    @abc.abstractmethod
    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers = set()

    def attach(self, observer):
        self.observers.add(observer)

    def detach(self, observer):
        self.observers.discard(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self)
