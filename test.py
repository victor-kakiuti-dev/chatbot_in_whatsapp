from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com")

print("=" * 60)
print("INSTRUÇÕES:")
print("1. Faça login no WhatsApp Web escaneando o QR Code")
print("2. CLIQUE em uma conversa para abri-la")
print("3. Envie algumas mensagens de teste")
print("4. Pressione Enter aqui no terminal")
print("=" * 60)

input("\nPressione Enter DEPOIS de abrir uma conversa e enviar mensagens...")

time.sleep(2)  # Aguardar um pouco

print("\n=== PROCURANDO O CONTAINER DE MENSAGENS ===\n")

# Vamos tentar encontrar o container principal de mensagens
containers_possiveis = [
    "div[data-testid='conversation-panel-body']",
    "div[class*='copyable-area']",
    "div[tabindex='-1'][role='application']",
    "div[data-tab='10']",
    "#main",
]

container_mensagens = None
for seletor in containers_possiveis:
    try:
        elem = driver.find_element(By.CSS_SELECTOR, seletor)
        print(f"✓ Container encontrado com: {seletor}")
        container_mensagens = elem
        break
    except:
        print(f"✗ Não encontrado: {seletor}")

if not container_mensagens:
    print("\n⚠️  Nenhum container encontrado! Você abriu uma conversa?")
    input("Pressione Enter para fechar...")
    driver.quit()
    exit()

print(f"\n=== ANALISANDO MENSAGENS NO CONTAINER ===\n")

# Agora vamos procurar as mensagens dentro do container
try:
    # Tentar encontrar divs com role="row"
    mensagens_row = container_mensagens.find_elements(By.XPATH, ".//div[@role='row']")
    print(f"Mensagens com role='row': {len(mensagens_row)}")
    
    if len(mensagens_row) > 0:
        print("\n=== ANALISANDO AS 3 ÚLTIMAS MENSAGENS ===\n")
        
        for i, msg in enumerate(mensagens_row[-3:], 1):
            print(f"\n--- Mensagem {i} ---")
            print(f"Classes: {msg.get_attribute('class')}")
            
            # Ver se tem data-testid
            testid = msg.get_attribute('data-testid')
            if testid:
                print(f"data-testid: {testid}")
            
            # Tentar pegar texto de várias formas
            print("\nTentando extrair texto:")
            
            # Método 1: span com dir='ltr'
            try:
                spans_ltr = msg.find_elements(By.XPATH, ".//span[@dir='ltr']")
                if spans_ltr:
                    textos = [s.text for s in spans_ltr if s.text]
                    print(f"  Spans dir='ltr': {textos}")
            except Exception as e:
                print(f"  Spans dir='ltr': Erro - {e}")
            
            # Método 2: Qualquer span com texto
            try:
                spans = msg.find_elements(By.TAG_NAME, "span")
                textos_spans = [s.text for s in spans if s.text and len(s.text) > 2]
                if textos_spans:
                    print(f"  Todos spans com texto: {textos_spans[:3]}")  # Primeiros 3
            except:
                pass
            
            # Método 3: .text direto
            try:
                texto_completo = msg.text
                if texto_completo:
                    print(f"  Texto direto (.text): {texto_completo[:100]}")
            except:
                pass
            
            # Método 4: Verificar estrutura interna
            try:
                divs_internos = msg.find_elements(By.TAG_NAME, "div")
                print(f"  Total de divs internos: {len(divs_internos)}")
                
                # Verificar se algum tem classe específica de mensagem
                for div in divs_internos[:5]:  # Checar primeiros 5
                    classes = div.get_attribute('class')
                    if 'message' in classes.lower():
                        print(f"    Div com 'message': {classes}")
            except:
                pass
            
            # Mostrar HTML completo (primeiros 300 chars)
            print(f"\nHTML (primeiros 300 chars):")
            print(msg.get_attribute('outerHTML')[:300])
            print()

except Exception as e:
    print(f"Erro ao analisar mensagens: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
input("Pressione Enter para fechar o navegador...")
driver.quit()