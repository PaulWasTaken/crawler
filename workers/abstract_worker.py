from abc import abstractmethod, ABC


class AbstractWorker(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError
