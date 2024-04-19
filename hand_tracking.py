import cv2
import mediapipe

# realizando a conexão com a webcam
camera = cv2.VideoCapture(0)

# aumentando a resolução da imagem 
resolution_x = 1280
resolution_y = 720
camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolution_x)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution_y)

# mostrando em tempo real a imagem
while True:
    # O primeiro deles é o sucesso (true ou false) e o segundo é a imagem da camera
    sucess, img = camera.read() 

    cv2.imshow('Imagem', img)

    # aguarda um determinado tempo para que o código continue sendo executado
    key = cv2.waitKey(1)
    # tecal "ESC" é o número 27
    # A waitKey também aguarda uma tecla do teclado que será utilizada para encerrar o loop   
    if key == 27:
        break