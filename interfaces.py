from abc import ABC, abstractmethod

# Definição da Interface ISubpagina
class ISubpagina(ABC):
    @property
    @abstractmethod
    def texto(self):
        pass

    @property
    @abstractmethod
    def url(self):
        pass
