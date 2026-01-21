import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_last_received_message(driver, last_message):
    """
    Retorna o texto das mensagens RECEBIDAS no chat aberto
    
    """

    try:   # Seleciona o elemento CSS que é a caixa de texto na lista de contatos
        messages = driver.find_elements(
            By.CSS_SELECTOR,
            "[data-testid='conversation-panel-messages'] span[dir='ltr']"
        )
         
        # Caso o texto selecionado seja diferente do último texto selecionado ele iŕa clicar nesse elemento
        if messages != last_message:
            wait = WebDriverWait(driver, 20)
            contact = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='conversation-panel-messages'] span[dir='ltr']")))
            contact.click()

        container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='copyable-area']"))
        )
        # Capta as mensagens recebidas por nós
        mensagens_recebidas = container.find_elements(By.CSS_SELECTOR, "div.message-in")
        
        if not mensagens_recebidas:
            return None
        
        # Última mensagem enviada
        ultima = mensagens_recebidas[-1]
        texto = ultima.find_element(By.XPATH, ".//span[@dir='ltr']").text

        print(texto)
    
        if not texto:
            return None
        
        
        return texto.strip()
    
    except StaleElementReferenceException:
        return None

def send_message(driver, text):
    try:  # Tenta 
        wait = WebDriverWait(driver, 20)
        # Com input_box iremos clicar no input para poder inserir a mensagem da llm e enviar a mensagem
        input_box = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//footer//div[@role="textbox" and @contenteditable="true"]')
                )
            )
        input_box.click()              
        time.sleep(0.2)

        input_box.send_keys(text)
        time.sleep(0.1)

        input_box.send_keys(Keys.ENTER) 
        time.sleep(1)
        return
    except StaleElementReferenceException:
        time.sleep(0.5)
        

        raise Exception("Não foi possivel enviar a mensagem(stale element)")



def bot_loop(driver):
    last_message = None

    history = [
        {"role": "system", "content": "Você é um assistente."}
    ]

    print("Bot ativo! Aguardando mensagens")

    while True:
        try:
            msg = get_last_received_message(driver, last_message)

            # 🔒 validação forte
            if not msg or not msg.strip():
                time.sleep(1)
                continue

            if msg == last_message:
                time.sleep(1)
                continue

            print("Recebido:", msg)

            # ✅ só agora entra no histórico
            history.append({"role": "user", "content": msg})

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=history
            )

            assistant_reply = response.output_text

            # segurança extra
            if not assistant_reply or not assistant_reply.strip():
                print("Resposta vazia da LLM")
                continue

            send_message(driver, assistant_reply)

            history.append(
                {"role": "assistant", "content": assistant_reply}
            )

            last_message = msg

            # evita histórico infinito
            if len(history) > 20:
                history = [history[0]] + history[-18:]

            time.sleep(6)

        except Exception as e:
            print("Erro no loop:", e)
            time.sleep(5)
