# Não esquecer de instalar a biblioteca do selenium: 
# Escrever "pip install selenium" no termnail

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

# Model:
class VerificadorWebsite:
    def __init__(self):
        # Configuração do WebDriver para Chrome
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)  # Certifique-se de ter o ChromeDriver no PATH ou especifique o caminho diretamente

    def verificar_disponibilidade(self, url):
        try:
            self.driver.get(url)
            # Verificar se a página principal foi carregada corretamente
            return True
        except Exception as e:
            print(f"Erro ao carregar a página: {e}")
            return False

    def verificar_elemento(self, texto_procurado):
        try:
            elemento = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{texto_procurado}')]")
            return True if elemento else False
        except NoSuchElementException:
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
        resultado_disponibilidade = self.model.verificar_disponibilidade("https://www.coisaspt.pt/")
        self.view.exibir_resultado_verificacao(resultado_disponibilidade)

        if not resultado_disponibilidade:
            return  # Se a página não estiver disponível, não continuar

        # Verificação do elemento com o texto "Coisas Novas"
        resultado_elemento = self.model.verificar_elemento("Coisas Novas")
        self.view.exibir_resultado_verificacao(resultado_elemento)

        # Adiciona um tempo de espera para manter o navegador aberto
        print(f"Verificação completa. O navegador permanecerá aberto por {close_value} segundos para inspeção.")
        time.sleep(close_value)

        # Fechar o driver no final (comentado para manter o Chrome aberto)
        self.model.fechar_driver()

close_value = 5  # in seconds
# Inicialização e execução da aplicação
if __name__ == "__main__":
    model = VerificadorWebsite()
    view = InterfaceUsuarioVerificacao()
    controller = ControladorVerificacao(model, view)
    controller.iniciar_verificacao()
    # controller.fechar_driver()  # Descomente esta linha para fechar o navegador manualmente após a inspeção
