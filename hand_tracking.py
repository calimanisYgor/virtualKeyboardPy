import cv2
import mediapipe as mp

# acessando soluções do mediapipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# adicionando modelos de ML para leitura das mãos
hands = mp_hands.Hands()

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
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_marks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_marks, mp_hands.HAND_CONNECTIONS)
    cv2.imshow("Imagem", img)

    # aguarda um determinado tempo para que o código continue sendo executado
    key = cv2.waitKey(1)
    # tecal "ESC" é o número 27
    # A waitKey também aguarda uma tecla do teclado que será utilizada para encerrar o loop
    if key == 27:
        break
