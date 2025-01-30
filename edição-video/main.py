import tkinter as tk
from tkinter import filedialog
import ffmpeg
import os


# Variável para armazenar o caminho do vídeo selecionado
video_caminho = None

def selecionar_video():
    """Abre a janela para selecionar um vídeo"""
    global video_caminho  # Usa a variável global
    caminho = filedialog.askopenfilename(
        filetypes=[("Arquivos de vídeo", "*.mkv *.mp4"), ("Todos os arquivos", "*.*")]
    )
    if caminho:
        video_caminho = caminho  # Armazena o caminho do vídeo selecionado
        nome_arquivo = os.path.basename(caminho)  # Extrai o nome do arquivo
        label_video.config(text=f"Vídeo selecionado:\n{nome_arquivo}")
    return caminho


def cortar_video(input_file, output_file, start_time, duration):
    """Corta um trecho do vídeo e converte para o formato 9:16 (1080x1920)"""
    ffmpeg.input(input_file, ss=start_time, t=duration).output(output_file, vf='scale=1080:1920', vcodec='libx264', acodec='aac', strict='-2').run()

def iniciar_corte():
    """Inicia o corte do vídeo selecionado"""
    if video_caminho:  # Verifica se o vídeo foi selecionado
        # Obtém os valores das caixas de texto
        start_time = entrada_inicio.get()  # Tempo de início
        duration = entrada_final.get()  # Tempo final
        if start_time and duration:
            output_video = "corte.mp4"  # Nome do arquivo de saída
            cortar_video(video_caminho, output_video, start_time, duration)
            label_video.config(text=f"Vídeo cortado e salvo como {output_video}")
        else:
            label_video.config(text="Por favor, insira o tempo de início e duração do corte")
    else:
        label_video.config(text="Por favor, selecione um vídeo primeiro")

# Criar a janela
root = tk.Tk()
root.title("Selecionar e Cortar Vídeo")

# Botão para escolher o vídeo
btn_selecionar = tk.Button(root, text="Selecionar Vídeo", command=selecionar_video)
btn_selecionar.grid(row=0, column=0, columnspan=2, pady=10)

# Label para mostrar o caminho do vídeo
label_video = tk.Label(root, text="Nenhum vídeo selecionado", wraplength=400)
label_video.grid(row=1, column=0, columnspan=2, pady=10)

# Label e caixa de texto para o tempo de início
label_inicio = tk.Label(root, text="Tempo de início (hh:mm:ss):")
label_inicio.grid(row=2, column=0, padx=10, pady=5, sticky="e")  # Alinhado à direita

entrada_inicio = tk.Entry(root)
entrada_inicio.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

# Label e caixa de texto para o tempo final
label_final = tk.Label(root, text="Tempo Duração(segundos)")
label_final.grid(row=3, column=0, padx=10, pady=5, sticky="e")  # Alinhado à direita

entrada_final = tk.Entry(root)
entrada_final.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

# Botão para iniciar o corte, abaixo das caixas de entrada
btn_iniciar_corte = tk.Button(root, text="Iniciar Corte", command=iniciar_corte)
btn_iniciar_corte.grid(row=4, column=0, columnspan=2, pady=10)

# Ajustar as colunas para expandirem
root.grid_columnconfigure(1, weight=1)

# Iniciar a interface gráfica
root.mainloop()
