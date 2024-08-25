import pyautogui
import cv2
import pytesseract
from time import sleep
import re

def distancia_corrida_1():
    
    tela_app = pyautogui.screenshot()
    tela_app.save('analiseimage/distancia_corrida.png')

    #abrindo
    arquivo_img = cv2.imread('analiseimage/distancia_corrida.png')

    
    #copiando a imagem altura / largura
    copia = arquivo_img[130:172, 485:578]

    
    #salvando a imagem copiada
    cv2.imwrite('analiseimage/dados_distancia.png', copia)

    try:
        texto_obtido = pytesseract.image_to_string('analiseimage/dados_distancia.png').strip()

        numero = int(re.search(r'\d+', texto_obtido).group())

        return numero

    except (ValueError,AttributeError):
        return False


def valor_corrida_1():
    tela_app = pyautogui.screenshot()
    tela_app.save('analiseimage/valor_corrida.png')

    #abrindo
    arquivo_img = cv2.imread('analiseimage/valor_corrida.png')

    #copiando a imagem altura / largura
    copia = arquivo_img[335:450, 700:878]
    
    
    #salvando a imagem copiada
    cv2.imwrite('analiseimage/so_preco.png', copia)


    texto_obtido = pytesseract.image_to_string('analiseimage/so_preco.png').strip()

  
    try:
        # Usando expressão regular para encontrar os números
        numeros = re.findall(r'\d+,\d+', texto_obtido)

        # Convertendo os números extraídos para float e somando-os
        soma = sum(float(numero.replace(',', '.')) for numero in numeros)

        return soma
    except (ValueError,AttributeError):
        return False

def aceitar_corrida():
    #clicar na corrida
    pyautogui.moveTo(x=644,y=272,duration=0.4)
    pyautogui.click()

    sleep(1.5)

    #clicar e arrastar o aceitar/ inicio Point(x=521, y=701)
    pyautogui.moveTo(x=521,y=701,duration=0.4)

    #clicar e arrastar o aceitar/ fim Point(x=843, y=708)
    pyautogui.dragTo(x=843,y=708, duration=0.4, button='left')




def destino_final():
    ...

def alarme_com_alerta():

    from pydub import AudioSegment
    from pydub.playback import play
    import tkinter as tk
    from threading import Thread

    # Função para parar o alarme
    def parar_alarme():
        global playing
        playing = False
        root.destroy()  # Fecha a janela quando o botão é clicado

    # Função para reproduzir o alarme
    def alarme():
        global playing
        # Carrega o arquivo de áudio
        alarme_audio = AudioSegment.from_file("mp3/alarm-clock-short-6402.mp3")
        
        playing = True
        while playing:
            play(alarme_audio)

    # Função para iniciar o alarme em uma thread separada
    def iniciar_alarme():
        alarme_thread = Thread(target=alarme)
        alarme_thread.start()

    # Criando a janela principal
    root = tk.Tk()
    root.title("Alarme")
    root.geometry("800x400")  # Define o tamanho da janela

    # Definindo a cor de fundo da janela
    root.configure(bg='red')

    # Criando um frame para centralizar o botão
    frame = tk.Frame(root, bg='red')
    frame.pack(expand=True)

    # Criando um botão para parar o alarme
    botao_parar = tk.Button(frame, text="TOCOU A BOA", command=parar_alarme, height=2, width=20, font=("Arial", 14), bg='white', fg='black')
    botao_parar.pack(pady=20)

    # Iniciando o alarme em uma thread separada
    iniciar_alarme()

    # Rodando o loop principal da janela
    root.mainloop()


def atualizar_corridas():
    
    # Define as coordenadas iniciais e finais para o movimento do mouse
    x_inicial, y_inicial = 663, 238
    x_final, y_final = 636, 502

    # Move o mouse para a coordenada final ao longo de 0.3 segundo
    pyautogui.moveTo(x_inicial, y_inicial,duration=0.4)

    # Clica e arrasta o mouse da coordenada inicial para a coordenada final ao longo de 1 segundo
    pyautogui.dragTo(x_final, y_final, duration=0.4, button='left')

    #Usar scroll mouse para cima/
    pyautogui.scroll(100)

contador = 1
while True:
    print(f'Consulta {contador}')
    contador += 1 

   
    atualizar_corridas()
    sleep(2)
    pyautogui.scroll(200)

    distancia = distancia_corrida_1()
    preco = valor_corrida_1()

    if distancia == False and preco == False:
        sleep(3)
        pyautogui.scroll(200)
        distancia = distancia_corrida_1()
        preco = valor_corrida_1()
    if distancia <= 16 and preco > 20:
        pyautogui.moveTo(x=644,y=272,duration=0.4)
        pyautogui.click()
        aceitar_corrida()
        alarme_com_alerta()
        break        
       
    if distancia and preco:
        print(f'Distancia da corrida [{distancia}]')
        print(f'Preco da corrida [{preco}]')
        print('NADABOM')
    else:    
        print('Nao consegui pegar os dados')


#abrir config
#melhorar leitura