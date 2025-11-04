# mp4-to-mp3

Projeto para extrair áudio de vídeos MP4 e transcrever automaticamente usando MoviePy e Whisper.

## Requisitos

*   Python >= 3.12
*   uv (gerenciador de ambientes e dependências)
*   moviepy >= 2.2.1
*   pyinstaller >= 6.16.0
*   whisper >= 1.1.10

## Instalação

```bash
# Instale o uv se ainda não tiver
pip install uv

# Crie o ambiente e instale as dependências
uv sync
```

## Estrutura dos scripts

*   **01\_extract\_audios.py**: Extrai o áudio de todos os arquivos MP4 da pasta `./videos` e salva em `./output/audios` como MP3.
*   **02\_transcribe\_audios.py**: Transcreve os arquivos de áudio (MP3/WAV) da pasta `./output/audios` e salva as transcrições em `./output/transcriptions`.
*   **app.py**: Interface gráfica (Tkinter) para selecionar vídeos ou pastas, definir pasta de saída e extrair áudios em lote.

## Como usar

### 1. Extração de Áudio (linha de comando)

Coloque seus vídeos MP4 na pasta `./videos` e execute:

```bash
python 01_extract_audios.py
```

Os arquivos MP3 serão salvos em `./output/audios`.

### 2. Transcrição de Áudio

Após extrair os áudios, execute:

```bash
python 02_transcribe_audios.py
```

As transcrições serão salvas em `./output/transcriptions`.

### 3. Interface Gráfica (somente extração de áudios)

Para usar a interface gráfica:

```bash
python app.py
```

*   Selecione arquivos ou uma pasta de vídeos.
*   Escolha a pasta de saída.
*   Clique em “Iniciar Conversão”.

## Empacotamento (se quiser gerar um .exe)

Para gerar um executável (usando pyinstaller):

```bash
pyinstaller --onefile app.py
```

## Observações

*   O Whisper usa GPU se disponível, senão CPU.
*   As pastas de entrada e saída são criadas automaticamente se não existirem.
*   O projeto pode ser facilmente adaptado para outros formatos de vídeo/áudio.
