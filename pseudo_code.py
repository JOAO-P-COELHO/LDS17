# Não esquecer de instalar a biblioteca do selenium: 
# Escrever "pip install selenium" no termnail

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Edge(service=s, options=options)

# Model:
class VerificadorWebsite:
    def __init__(self):
        # Configuração do WebDriver
        self.driver = webdriver.Chrome()  # Certifique-se de ter o ChromeDriver no PATH ou especifique o caminho diretamente

    def verificar_disponibilidade(self, url):
        try:
            self.driver.get(url)
            # Verificar se a página principal foi carregada corretamente
            return True
        except Exception as e:
            print(f"Erro ao carregar a página: {e}")
            return False

    def verificar_navegacao_subpaginas(self):
        # Exemplo: navegando para a página de "Sobre" do Google
        try:
            link_sobre = self.driver.find_element(By.LINK_TEXT, "Sobre")
            link_sobre.click()
            time.sleep(2)
            return True
        except NoSuchElementException as e:
            print(f"Erro ao navegar para a subpágina: {e}")
            return False

    def realizar_pesquisa(self, termo_pesquisa):
        try:
            search_box = self.driver.find_element(By.NAME, "q")
            search_box.send_keys(termo_pesquisa)
            search_box.send_keys(Keys.RETURN)
            time.sleep(2)  # Esperar um pouco para os resultados carregarem
            return True
        except NoSuchElementException as e:
            print(f"Erro ao realizar a pesquisa: {e}")
            return False

    def fechar_driver(self):
        self.driver.quit()

# View:
class InterfaceUsuarioVerificacao:
    def exibir_resultado_verificacao(self, resultado):
        if resultado:
            print("Operação realizada com sucesso.")
        else:
            print("Falha na operação.")

# Controller:
class ControladorVerificacao:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def iniciar_verificacao(self):
        # Verificação de disponibilidade da página principal
        resultado_disponibilidade = self.model.verificar_disponibilidade("https://www.google.com")
        self.view.exibir_resultado_verificacao(resultado_disponibilidade)

        if not resultado_disponibilidade:
            return  # Se a página não estiver disponível, não continuar

        # Verificação de navegação das subpáginas (este passo é opcional e depende da estrutura do site)
        # resultado_navegacao = self.model.verificar_navegacao_subpaginas()
        # self.view.exibir_resultado_verificacao(resultado_navegacao)

        # Verificação de pesquisa no site
        resultado_pesquisa = self.model.realizar_pesquisa("Universidade Aberta")
        self.view.exibir_resultado_verificacao(resultado_pesquisa)

        # Adiciona um tempo de espera para manter o navegador aberto
        print("Verificação completa. O navegador permanecerá aberto por 60 segundos para inspeção.")
        time.sleep(60)

        # Fechar o driver no final (comentado para manter o Chrome aberto)
        # self.model.fechar_driver()


# Inicialização e execução da aplicação
if __name__ == "__main__":
    model = VerificadorWebsite()
    view = InterfaceUsuarioVerificacao()
    controller = ControladorVerificacao(model, view)
    controller.iniciar_verificacao()
    # controller.fechar_driver()  # Descomente esta linha para fechar o navegador manualmente após a inspeção
