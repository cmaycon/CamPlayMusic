import cv2
import os
import time
from detector import SalaDetector
from music_player import MusicPlayer

# CONFIGS
RTSP_URL = "rtsp://usuario:senha@IP:porta/cam/realmonitor?channel=1&subtype=0" # URL RTSP da câmera de monitoramento
MUSICA_PATH = "musicas/music.mp3"
TEMPO_LIMITE = 60 #segundos. Após esse tempo sem detecção de uma pessoa na sala, a música é pausada

# Cores ANSI para o terminal
VERDE = '\033[92m'
AMARELO = '\033[93m'
VERMELHO = '\033[91m'
AZUL = '\033[94m'
RESET = '\033[0m'
NEGRITO = '\033[1m'

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_dashboard(status, som, ocioso, player):
    limpar_terminal()
    print(f"{AZUL}{NEGRITO}=== MONITORAMENTO INTELBRAS IA ==={RESET}")
    
    # Status e Som
    cor_status = VERDE if "PRESENTE" in status else (AMARELO if "AGUARDANDO" in status else VERMELHO)
    print(f"Status: {cor_status}{NEGRITO}{status}{RESET}")
    
    # BARRA DE PROGRESSO DA MÚSICA
    if som:
        atual, total = player.get_progresso()
        percentual = min(atual / total, 1.0)
        largura_barra = 20
        preenchido = int(largura_barra * percentual)
        barra = "█" * preenchido + "░" * (largura_barra - preenchido)
        
        # Formatar tempo
        min_at, seg_at = divmod(int(atual), 60)
        min_tot, seg_tot = divmod(int(total), 60)
        
        print(f"Música: {VERDE}🎵 TOCANDO{RESET}")
        print(f"Progresso: [{barra}] {min_at:02}:{seg_at:02} / {min_tot:02}:{seg_tot:02}")
    else:
        print(f"Música: {VERMELHO}🔇 OFF{RESET}")

    print(f"Tempo Ocioso: {ocioso}s / {TEMPO_LIMITE}s")
    print(f"{AZUL}----------------------------------{RESET}")

    print("Pressione 'q' na janela da câmera para sair.")

def main():
    detector = SalaDetector(RTSP_URL)
    player = MusicPlayer(MUSICA_PATH)
    
    cv2.namedWindow("Camera Intelbras", cv2.WINDOW_NORMAL)
    
    ultimo_status_texto = ""
    ultimo_segundo = -1

    try:
        while True:
            # Pega os tempos
            alguem_na_sala, frame = detector.detectar_pessoa()
            ocioso = detector.tempo_ocioso()
            tempo_visto = detector.tempo_presenca_continua()

            # Após 5 segundos detectando movimento na sala, o status muda e a música toca
            if alguem_na_sala:
                if tempo_visto >= 5:
                    player.play()
                    status_atual = "PESSOA PRESENTE"
                else:
                    status_atual = f"ANALISANDO... ({tempo_visto}s)"
            elif ocioso >= TEMPO_LIMITE: # Tempo definido no início do código
                player.stop()
                status_atual = "SALA VAZIA"
            else:
                status_atual = "AGUARDANDO TIMEOUT"

            # Só atualiza o terminal se o status mudar OU se o segundo do cronômetro mudar
            if status_atual != ultimo_status_texto or ocioso != ultimo_segundo or (player.tocando and int(time.time()) % 1 == 0):
                exibir_dashboard(status_atual, player.tocando, ocioso, player)
                ultimo_status_texto = status_atual
                ultimo_segundo = ocioso

            if frame is not None:
                cv2.imshow("Camera Intelbras", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    finally:
        detector.fechar()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
