import cv2
import time
from ultralytics import YOLO

class SalaDetector:
    def __init__(self, url_rtsp):
        self.model = YOLO('yolov8n.pt')
        self.cap = cv2.VideoCapture(url_rtsp)
        self.ultimo_movimento = 0
        self.primeira_deteccao = 0

    def detectar_pessoa(self):
        ret, frame = self.cap.read()
        if not ret: return False, None
        
        results = self.model.predict(frame, classes=[0], conf=0.5, verbose=False)
        tem_pessoa = len(results[0].boxes) > 0
        
        agora = time.time()
        if tem_pessoa:
            self.ultimo_movimento = agora
            if self.primeira_deteccao == 0:
                self.primeira_deteccao = agora
        else:
            if agora - self.ultimo_movimento > 2:
                self.primeira_deteccao = 0
            
        return tem_pessoa, frame

    def tempo_presenca_continua(self):
        """Retorna há quantos segundos a pessoa está sendo vista."""
        if self.primeira_deteccao == 0: return 0
        return int(time.time() - self.primeira_deteccao)

    def tempo_ocioso(self):
        if self.ultimo_movimento == 0: return 0
        return int(time.time() - self.ultimo_movimento)

    def fechar(self):
        self.cap.release()