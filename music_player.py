import pygame
from mutagen.mp3 import MP3

class MusicPlayer:
    def __init__(self, caminho_musica):
        pygame.mixer.init()
        self.caminho = caminho_musica
        self.tocando = False
        audio = MP3(caminho_musica)
        self.duracao_total = audio.info.length

    def get_progresso(self):
        if not self.tocando:
            return 0, self.duracao_total
        
        posicao_absoluta = pygame.mixer.music.get_pos() / 1000.0
        posicao_relativa = posicao_absoluta % self.duracao_total
        
        return posicao_relativa, self.duracao_total

    def play(self):
        if not self.tocando:
            pygame.mixer.music.load(self.caminho)
            pygame.mixer.music.play(-1)
            self.tocando = True

    def stop(self):
        if self.tocando:
            pygame.mixer.music.stop()
            self.tocando = False