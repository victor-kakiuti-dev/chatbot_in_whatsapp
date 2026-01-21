from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_whatsapp(driver, timeout=60):
    """
    Aguarda o WhatsApp Web estar totalmente carregado e logado
    """
    wait = WebDriverWait(driver, timeout)

    # Esse seletor aparece quando a lista de chats carrega
    wait.until(
        EC.presence_of_element_located(
            (By.ID, "pane-side")
        )
    )

    print("WhatsApp Web carregado e pronto")