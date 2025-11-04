import whisper

def transcrever_whisper(audio_path: str, idioma: str = "pt") -> str:
    # Usa GPU se disponível, senão CPU
    device = "cuda" if whisper.available_devices() else "cpu"
    print('Device: ', device)
    modelo = whisper.load_model("small", device=device)
    resultado = modelo.transcribe(audio_path, language=idioma)
    return resultado["text"]

if __name__ == "__main__":
    import os

    input_dir = "./output/audios"
    output_dir = "./output/transcriptions"

    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.lower().endswith((".mp3", ".wav")):  # Apenas áudio
            print(f"Transcrevendo: {file}")
            audio_path = os.path.join(input_dir, file)
            texto = transcrever_whisper(audio_path)

            # Salva transcrição
            txt_path = os.path.join(output_dir, os.path.splitext(file)[0] + ".txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(texto)
