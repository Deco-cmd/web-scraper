from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

options = Options()
# options.add_argument('--headless')

driver = webdriver.Chrome(options=options)
driver.get('https://www.luitex.com.br')

wait = WebDriverWait(driver, 15)

try:
    # Espera os cards dos produtos aparecerem
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'vtex-product-summary-2-x-container')))

    # Agora pega todos os cards e extrai nome e preço dentro de cada um
    produtos = driver.find_elements(By.CLASS_NAME, 'vtex-product-summary-2-x-container')

    with open('preco.csv', 'w', encoding='utf-8', newline='') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(["Produto", "Preço"])

        for i, produto in enumerate(produtos):
            try:
                nome = produto.find_element(By.CLASS_NAME, 'vtex-product-summary-2-x-brandName').text
                preco = produto.find_element(By.CLASS_NAME, 'luitex-luitex-theme-2-x-price--shelf').text
                print(f"{i+1}. Produto: {nome} | Preço: {preco}")
                writer.writerow([nome.strip(), preco.strip()])
            except Exception as e:
                print(f"Erro em produto {i+1}: {e}")

except Exception as e:
    print("Erro ao coletar dados:", e)
finally:
    input("Pressione Enter para sair...")
    driver.quit()
