# Não esquecer de instalar a biblioteca do selenium: 
# Escrever "pip install selenium" no terminal

import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Model:
class VerificadorWebsite:
    def __init__(self):
        self.driver = None
        self.resultados = []
        self.capturas = []

    def abrir_navegador(self):
        if not self.driver:
            options = webdriver.ChromeOptions()
            # options.add_argument('--headless')  # Removendo o modo headless para visualizar a execução
            self.driver = webdriver.Chrome(options=options)

    def fechar_navegador(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def abrir_pagina_principal(self, url):
        try:
            self.abrir_navegador()
            self.driver.get(url)
            self.resultados.append(f"Abrindo página principal: {url}")
        except Exception as e:
            logging.error(f"Erro ao abrir a página principal: {e}")
            self.resultados.append(f"Erro ao abrir a página principal: {e}")

    def encontrar_subpaginas(self):
        subpaginas = []
        try:
            links = self.driver.find_elements(By.TAG_NAME, 'a')
            for link in links:
                href = link.get_attribute('href')
                text = link.text.strip() if link.text.strip() else href
                if href and href != "#":
                    subpaginas.append((text, href))
            self.resultados.append(f"Foram encontradas {len(subpaginas)} subpáginas.")
            return subpaginas
        except Exception as e:
            logging.error(f"Erro ao encontrar subpáginas: {e}")
            self.resultados.append(f"Erro ao encontrar subpáginas: {e}")
            return []

    def verificar_disponibilidade_subpagina(self, subpagina_text, subpagina_href):
        try:
            link_subpagina = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, subpagina_text))
            )
            link_subpagina.click()
            input("Interaja com a subpágina e pressione Enter para continuar...")
            return "Subpágina aberta com sucesso."
        except (NoSuchElementException, TimeoutException):
            logging.error(f"Subpágina '{subpagina_text}' não encontrada ou não clicável.")
            self.resultados.append(f"Subpágina '{subpagina_text}' não encontrada ou não clicável.")
            return "Subpágina não encontrada ou não clicável."
        except ElementClickInterceptedException:
            logging.error(f"Elemento clicável foi interceptado ao tentar acessar '{subpagina_text}'.")
            self.resultados.append(f"Elemento clicável foi interceptado ao tentar acessar '{subpagina_text}'.")
            return "Elemento clicável foi interceptado."
        except Exception as e:
            logging.error(f"Erro ao verificar a subpágina: {e}")
            self.resultados.append(f"Erro ao verificar a subpágina: {e}")
            return "Erro ao verificar a subpágina."

    def capturar_tela(self, nome_arquivo):
        if not os.path.exists("capturas"):
            os.makedirs("capturas")
        caminho_arquivo = os.path.join("capturas", nome_arquivo)
        self.driver.save_screenshot(caminho_arquivo)
        self.capturas.append(caminho_arquivo)


# View:
class InterfaceUsuarioVerificacao:
    def obter_url(self):
        return input("Digite a URL do site a ser verificado: ")

    def exibir_subpaginas_encontradas(self, subpaginas):
        if not subpaginas:
            logging.info("Não foram encontradas subpáginas.")
        else:
            print(f"Foram encontradas {len(subpaginas)} subpáginas.")
            for i, (subpagina_text, subpagina_href) in enumerate(subpaginas[:5], 1):
                print(f"{i}. {subpagina_text}")
            if len(subpaginas) > 5:
                print("* Existem mais subpáginas que podem ser verificadas.")

    def obter_escolha_subpagina(self):
        return input("Escolha o número da subpágina para verificar: ")

    def exibir_resultado_verificacao(self, resultado):
        logging.info(resultado)


# Controller:
class ControladorVerificacao:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def iniciar_verificacao(self):
        url = self.view.obter_url()
        self.model.abrir_pagina_principal(url)
        input("Navegue na página principal e pressione Enter para continuar...")
        self.model.capturar_tela("pagina_principal.png")
        self.model.resultados.append("Interação com a página principal concluída com sucesso.")

        subpaginas = self.model.encontrar_subpaginas()
        self.view.exibir_subpaginas_encontradas(subpaginas)

        if subpaginas:
            escolha = int(self.view.obter_escolha_subpagina()) - 1
            if 0 <= escolha < len(subpaginas):
                subpagina_text, subpagina_href = subpaginas[escolha]
                resultado_verificacao = self.model.verificar_disponibilidade_subpagina(subpagina_text, subpagina_href)
                self.model.capturar_tela(f"subpagina_{escolha + 1}.png")
                self.model.resultados.append(resultado_verificacao)
                self.view.exibir_resultado_verificacao(resultado_verificacao)
            else:
                logging.info("Escolha inválida.")

        self.model.fechar_navegador()
        self.gerar_relatorio()

    def gerar_relatorio(self):
        if not os.path.exists("relatorios"):
            os.makedirs("relatorios")
        with open("relatorios/relatorio_verificacao.txt", "w") as f:
            for resultado in self.model.resultados:
                f.write(f"{resultado}\n")
            f.write("Capturas de tela salvas:\n")
            for captura in self.model.capturas:
                f.write(f"{captura}\n")
        logging.info("Relatório de verificação guardado na pasta 'relatorios'")
        logging.info("Capturas de tela guardadas na pasta 'capturas'")
        print("Relatório de verificação guardado na pasta 'relatorios'")
        print("Capturas de tela guardadas na pasta 'capturas'")


# Inicialização e execução da aplicação
if __name__ == "__main__":
    model = VerificadorWebsite()
    view = InterfaceUsuarioVerificacao()
    controller = ControladorVerificacao(model, view)
    controller.iniciar_verificacao()