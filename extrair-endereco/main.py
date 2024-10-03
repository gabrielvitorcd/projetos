import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from fuctions import salvar_excel, extrair_dominio_email, criar_diretorio_e_mover_arquivos
# Aqui você pode importar as outras funções que já desenvolveu

# Função que verifica o sucesso da entrada


def verificar_entrada():

    if botao_verificar["text"] == "Inserir Busca do Google":
        global nome_diretorio
        nome_diretorio = entrada_busca.get()

        if not nome_diretorio:
            messagebox.showerror("ERROR", "Não inseriu o termo da busca")
            return

        label_busca.config(text='Insira o Link 1')
        botao_verificar.config(text='Avança')

        entrada_busca.delete(0, 'end')

    elif botao_verificar["text"] == "Avança":
        contagem = len(enderecos_do_google)
        label_busca.config(text=f'Insira o Link {contagem + 2}')
        endereco_pag_google = entrada_busca.get()

        if not endereco_pag_google:
            messagebox.showerror("ERROR", "Não inseriu nenhum link válido")
            return
        else:
            enderecos_do_google.append(endereco_pag_google)

        messagebox.showinfo(
            "SUCESSO", f"Link inserido com sucesso!")

        # Limpa a entrada para o próximo uso
        entrada_busca.delete(0, 'end')


def iniciar_extracao():
    # criando a lista com nomes das paginas para salvar depois
    for chave, links in enumerate(enderecos_do_google):
        numero_da_pagina_nome_arquivo = str(chave + 2)
        nome_das_paginas = 'pagina-' + numero_da_pagina_nome_arquivo + '.xlsx'
        nomes_dos_arquivos.append(nome_das_paginas)

        link_limpo, email_limpo = extrair_dominio_email(links)
        salvar_excel(link_limpo, email_limpo, numero_da_pagina_nome_arquivo)

    criar_diretorio_e_mover_arquivos(nome_diretorio, nomes_dos_arquivos)
    messagebox.showinfo(
        "SUCESSO", f"Extração Finalizada !")


enderecos_do_google = []
nomes_dos_arquivos = []

#  ====================================================================

# Janela principal
janela = tk.Tk()
janela.title("Extrator de Dados Google")
janela.geometry("400x300")

# Label para instrução de busca
label_busca = tk.Label(
    janela, text="Insira o Nome da Pasta")
label_busca.pack(pady=10)

# Caixa de entrada de texto para a busca
entrada_busca = tk.Entry(janela, width=40)
entrada_busca.pack(pady=5)

# Botão para verificar a entrada e continuar o processo
botao_verificar = tk.Button(
    janela, text="Inserir Busca do Google", command=verificar_entrada)
botao_verificar.pack(pady=10)

# Botão para iniciar a extração
botao_iniciar = tk.Button(
    janela, text="Iniciar Extração", command=iniciar_extracao)
botao_iniciar.pack(pady=10)


# Barra de progresso
progresso = ttk.Progressbar(
    janela, orient="horizontal", length=300, mode="determinate")
progresso.pack(pady=30)

#  ====================================================================
# MINHA DUVIDA

#  ====================================================================

# Loop principal da interface
janela.mainloop()
