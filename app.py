import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy import VideoFileClip

def extrair_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path, codec='mp3', bitrate='320k', logger=None)
    audio.close()
    video.close()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Extrator de Áudio (MP4 → MP3)")
        self.root.geometry("600x400")

        self.video_paths = []
        self.output_dir = ""

        # Botões
        frame = tk.Frame(root)
        frame.pack(pady=10)
        tk.Button(frame, text="Selecionar Arquivo Único", command=self.selecionar_arquivo).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Selecionar Pasta Com Vários Arquivos", command=self.selecionar_pasta).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Pasta de Saída", command=self.selecionar_saida).grid(row=0, column=2, padx=5)

        # Lista
        self.lista = tk.Listbox(root, width=80, height=10)
        self.lista.pack(pady=10)

        # Barra de progresso
        self.progress = ttk.Progressbar(root, length=500, mode="determinate")
        self.progress.pack(pady=10)

        # Botão iniciar
        self.btn_iniciar = tk.Button(root, text="Iniciar Conversão", command=self.iniciar_conversao)
        self.btn_iniciar.pack(pady=10)

        # Status
        self.status = tk.Label(root, text="Aguardando seleção...", anchor="w")
        self.status.pack(fill="x", padx=10, pady=5)

    def selecionar_arquivo(self):
        arquivo = filedialog.askopenfilename(title="Selecione um vídeo", filetypes=[("Arquivos MP4", "*.mp4")])
        if arquivo:
            self.video_paths = [arquivo]
            self.atualizar_lista()

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta com vídeos")
        if pasta:
            self.video_paths = [os.path.join(pasta, f) for f in os.listdir(pasta) if f.lower().endswith(".mp4")]
            self.atualizar_lista()

    def selecionar_saida(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta para salvar os áudios")
        if pasta:
            self.output_dir = pasta
            self.status.config(text=f"Pasta de saída: {pasta}")

    def atualizar_lista(self):
        self.lista.delete(0, tk.END)
        for path in self.video_paths:
            self.lista.insert(tk.END, os.path.basename(path))

    def iniciar_conversao(self):
        if not self.video_paths:
            messagebox.showwarning("Aviso", "Nenhum vídeo selecionado.")
            return
        if not self.output_dir:
            messagebox.showwarning("Aviso", "Selecione a pasta de saída.")
            return

        self.progress["value"] = 0
        self.progress["maximum"] = len(self.video_paths)
        self.status.config(text="Processando...")

        # Desabilita botão e força atualização da GUI
        self.btn_iniciar.config(state="disabled")
        self.root.update_idletasks()  # <- ESSENCIAL

        threading.Thread(target=self.processar_videos, daemon=True).start()
        
        self.btn_iniciar.config(state="normal")
        self.root.update_idletasks()  # <- ESSENCIAL

    def processar_videos(self):
        for i, video_path in enumerate(self.video_paths, start=1):
            nome_audio = os.path.splitext(os.path.basename(video_path))[0] + ".mp3"
            audio_path = os.path.join(self.output_dir, nome_audio)

            self.status.config(text=f"Extraindo áudio: {os.path.basename(video_path)}")
            try:
                extrair_audio(video_path, audio_path)
            except Exception as e:
                self.status.config(text=f"Erro: {e}")

            self.progress["value"] = i
            self.root.update_idletasks()  # Força atualização da GUI

        self.status.config(text="Conversão concluída!")
        messagebox.showinfo("Finalizado", f"Áudios salvos em:\n{self.output_dir}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()