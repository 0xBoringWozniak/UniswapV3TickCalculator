from enum import Enum

from abc import abstractmethod, ABC


class LoaderType(Enum):
    CSV = 1
    JSON = 2
    SQL = 3
    PICKLE = 4


class Loader(ABC):


    def __init__(self, loader_type: LoaderType, *args, **kwargs) -> None:
        self.loader_type = loader_type
        self._data = None

    @abstractmethod
    def extract(self):
        raise NotImplementedError

    @abstractmethod
    def transform(self):
        raise NotImplementedError

    @abstractmethod
    def load(self):
        raise NotImplementedError

    @abstractmethod
    def read(self, with_run: bool = False):
        raise NotImplementedError
    
    def run(self):
        self.extract()
        self.transform()
        self.load()
