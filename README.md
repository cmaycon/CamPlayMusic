# CamPlayMusic :sound::video_camera:
Projeto criado com o objetivo de automatizar um sistema de som ambiente em uma determinada sala.\
O algoritmo é baseado na detecção de movimento de uma câmera de monitoramento (Intelbras, por exemplo).

## :thinking: Como funciona?
Quando há presença de uma pessoa no campo de visão dessa câmera, a música configurada começa a tocar.\
Enquanto for detectado a presença, a reprodução estará em loop.

Quando não há presença de ninguém no campo de visão da câmera, após poucos segundos a música para automaticamente.

## :man_technologist: Como executar?
### 1. Instale o Python

É preciso ter o Python instalado na máquina - recomendado versão **3.13.7** ou superior (baixe somente do [site oficial](https://www.python.org/)).

### 2. Instale as Bibliotecas

Instale as bibliotecas necessárias listadas no arquivo `requirements.txt`.\
**Dica:** abra o prompt de comando dentro da pasta do projeto e digite `pip install -r requirements.txt`.\
Não esqueça de ativar a `venv`, caso esteja utilizando.

### 3. Configure sua Câmera

No arquivo `main.py`, é necessário inserir a URL RTSP da câmera de monitoramento que irá realizar as detecções.

Esta URL, geralmente da Intelbras, segue o padrão `rtsp://usuario:senha@IP:porta/cam/realmonitor?channel=1&subtype=0`, onde os campos **usuario**, **senha**, **IP**, **porta** e **channel** precisam ser preenchidos manualmente, conforme a câmera e o DVR alvo.

Como encontro o URL da minha câmera IP RTSP? [Saiba Mais](https://forum.intelbras.com.br/viewtopic.php?t=56068)

### 4. Arquivo de Áudio

É necessário ter um arquivo de áudio dentro da pasta `musicas` para o script funcionar corretamente.\
Adicione uma música de sua preferência. Renomei-o como `music.mp3`

### 5. Execute

Para executar, digite no prompt (com o caminho da pasta já selecionado) `python main.py`.

## :smiley: Uso e Contribuição

Sinta-se à vontade para utilizar esse algoritmo e adaptá-lo para o seu caso, ou realizar alterações que podem melhorá-lo ainda mais!
