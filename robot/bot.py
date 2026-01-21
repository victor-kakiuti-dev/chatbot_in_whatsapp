import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
# from openai import OpenAI
# from dotenv import load_dotenv
# import os

# load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_last_received_message(driver):
    """
    Retorna o texto das mensagens RECEBIDAS no chat aberto
    
    """

    try:
        messages = driver.find_elements(
            By.CSS_SELECTOR,
            "span._ao3e"
        )
        
    
        if not messages:
            return None
        
        
        return messages[1].text.strip()
    
    except StaleElementReferenceException:
        return None

def send_message(driver, text):
    try:
        wait = WebDriverWait(driver, 20)
    
        contact = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span._ao3e")))
        
        contact.click()
        input_box = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//footer//div[@role="textbox" and @contenteditable="true"]')
                )
            )
        input_box.click
        input_box.send_keys(text)
        input_box.send_keys("\n")
        return
    except StaleElementReferenceException:
        time.sleep(0.5)
        

        raise Exception("Não foi possivel enviar a mensagem(stale element)")



def bot_loop(driver):
    last_message = None

    print("Bot ativo! Aguardando mensagens")

    while True:
        try:
            msg = get_last_received_message(driver)

            if  msg != last_message:
                print('Recebido: ', msg)
                

                if msg.lower() == 'ping':
                    send_message(driver, "pong")

                last_message = msg

                time.sleep(2.5)

  

        except Exception as e:
            print("Erro no loop:", e)
            time.sleep(5)

    
