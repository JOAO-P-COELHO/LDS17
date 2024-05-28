from interfaces import ISubpagina

# Implementação da Subpagina que herda de ISubpagina
class Subpagina(ISubpagina):
    def __init__(self, texto, url):
        self._texto = texto
        self._url = url

    @property
    def texto(self):
        return self._texto

    @property
    def url(self):
        return self._url
