class Observer:
    def update(self, message):
        raise NotImplementedError("This method should be implemented by subclasses")

class ResultObserver(Observer):
    def update(self, message):
        print(f"Notification: {message}")

class Observable:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)
