import tkinter as tk
import speedtest
import threading
from pythonping import ping

def medir_velocidade():
    response_list = ping('google.com', count=4)
    ping_time = response_list.rtt_avg_ms

    st = speedtest.Speedtest()

    tamanho_arquivo = 15_000_000

    download_speed = st.download() / 1_000_000
    upload_speed = st.upload() / 1_000_000

    return ping_time, download_speed, upload_speed

def piscar_status_label():
    if not medicao_concluida:
        current_text = status_label.cget("text")
        if current_text == "Medindo...":
            status_label.config(text="Medindo")
        else:
            status_label.config(text=current_text + ".")
        root.after(500, piscar_status_label)  # Chama a função novamente se a medição não estiver concluída

def atualizar_valores():
    global medicao_concluida
    ping, download, upload = medir_velocidade()
    ping_label.config(text=f"Ping: {ping} ms")
    download_label.config(text=f"Download: {download:.2f} Mbps")
    upload_label.config(text=f"Upload: {upload:.2f} Mbps")

    medicao_concluida = True  # Define que a medição está concluída
    status_label.config(text="Medição finalizada.")

    fechar_botao = tk.Button(root, text="Fechar", command=root.quit)
    fechar_botao.pack()

root = tk.Tk()
root.title("Medidor de Velocidade de Internet")
root.geometry("350x115")

ping_label = tk.Label(root, text="Ping: -- ms")
download_label = tk.Label(root, text="Download: -- Mbps")
upload_label = tk.Label(root, text="Upload: -- Mbps")
status_label = tk.Label(root, text="Medindo...")

ping_label.pack()
download_label.pack()
upload_label.pack()
status_label.pack()

medicao_concluida = False  # Inicialmente, a medição não está concluída

thread = threading.Thread(target=atualizar_valores)
thread.daemon = True
thread.start()

piscar_status_label()  # Inicie a função para criar o efeito de piscar

root.mainloop()
