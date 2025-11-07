import whisper
import torch
import os
import time
from tqdm import tqdm

def transcrever_whisper(audio_path: str, idioma: str = "pt", show_progress: bool = True) -> str:
    # Detecta GPU automaticamente
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Device:", device)

    # Carrega o modelo Whisper no device correto
    modelo = whisper.load_model("small", device=device)
    
    if show_progress:
        # Opção 1: Usar tqdm para barra de progresso
        print(f"Transcrevendo: {os.path.basename(audio_path)}")
        start_time = time.time()
        
        # Whisper não tem callback nativo, mas podemos mostrar progresso estimado
        # baseado no tamanho do áudio
        import librosa
        duration = librosa.get_duration(path=audio_path)
        estimated_time = duration / 10  # Estimativa: Whisper processa ~10x em tempo real
        
        with tqdm(total=100, desc="Transcrevendo", unit="%") as pbar:
            resultado = modelo.transcribe(audio_path, language=idioma)
            pbar.update(100)
        
        elapsed_time = time.time() - start_time
        print(f"Concluído em {elapsed_time:.2f}s")
    else:
        resultado = modelo.transcribe(audio_path, language=idioma)
    
    return resultado["text"]

def transcrever_com_callback(audio_path: str, idioma: str = "pt") -> str:
    """Opção 2: Usar callback personalizado para progresso detalhado"""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Device:", device)
    
    modelo = whisper.load_model("small", device=device)
    
    # Simula progresso baseado nos segmentos
    print(f"Transcrevendo: {os.path.basename(audio_path)}")
    
    class ProgressCallback:
        def __init__(self, total_segments):
            self.total_segments = total_segments
            self.processed = 0
            
        def update(self, segment):
            self.processed += 1
            progress = (self.processed / self.total_segments) * 100
            print(f"\rProgresso: {progress:.1f}% ({self.processed}/{self.total_segments})", end="", flush=True)
    
    # Carrega áudio para estimar segmentos
    audio = whisper.load_audio(audio_path)
    estimated_segments = len(audio) // (16000 * 30)  # Estimativa: segmentos de 30s
    
    callback = ProgressCallback(estimated_segments)
    resultado = modelo.transcribe(audio_path, language=idioma, verbose=True)  # verbose=True mostra segmentos
    
    print("\nTranscrição concluída!")
    return resultado["text"]

if __name__ == "__main__":
    input_dir = "./output/audios"
    output_dir = "./output/transcriptions"

    # Cria pasta de saída, se não existir
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.lower().endswith((".mp3", ".wav")):  # Apenas áudio
            audio_path = os.path.join(input_dir, file)
            
            # Escolha o método de progresso:
            # Opção 1: Barra de progresso simples
            texto = transcrever_whisper(audio_path, show_progress=True)
            
            # Opção 2: Progresso detalhado com callback
            # texto = transcrever_com_callback(audio_path)
            
            # Opção 3: Sem progresso (original)
            # texto = transcrever_whisper(audio_path, show_progress=False)

            # Salva transcrição
            txt_path = os.path.join(output_dir, os.path.splitext(file)[0] + ".txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(texto)
