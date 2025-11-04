from moviepy import VideoFileClip

def extrair_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path, codec='mp3', bitrate='320k')
    audio.close()
    video.close()

if __name__ == "__main__":
    import os
    
    # Pastas
    input_dir = "./videos"
    output_dir = "./output/audios"

    # Garante que a pasta de saída existe
    os.makedirs(output_dir, exist_ok=True)

    # Percorre todos os arquivos mp4 da pasta
    for file in os.listdir(input_dir):
        print('Processando: ', file)
        if file.lower().endswith(".mp4"):
            video_path = os.path.join(input_dir, file)
            audio_name = os.path.splitext(file)[0] + ".mp3"
            audio_path = os.path.join(output_dir, audio_name)

            print(f"Extraindo áudio de: {file}")
            extrair_audio(video_path, audio_path)
            print(f"Áudio salvo em: {audio_path}")
