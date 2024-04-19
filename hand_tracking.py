import cv2
import mediapipe as mp

# Inicialização das soluções do mediapipe para detecção de mãos
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Inicialização do modelo de detecção de mãos
hands = mp_hands.Hands()

# Inicialização da captura de vídeo da webcam
camera = cv2.VideoCapture(0)

# Configuração da resolução da imagem da câmera
resolution_x = 1280
resolution_y = 720
camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolution_x)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution_y)

# Loop para mostrar a imagem em tempo real
while True:
    # Captura de um frame da câmera
    success, img = camera.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Processamento da imagem para detecção de mãos
    result = hands.process(img_rgb)

    # Verificação se há mãos detectadas na imagem
    if result.multi_hand_landmarks:
        # Desenho dos pontos e conexões das mãos na imagem
        for hand_marks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_marks, mp_hands.HAND_CONNECTIONS)

    # Exibição da imagem em uma janela chamada "Imagem"
    cv2.imshow("Imagem", img)

    # Aguarda um determinado tempo e verifica se a tecla "ESC" foi pressionada para sair do loop
    key = cv2.waitKey(1)
    if key == 27:  # "ESC" é o número 27 na tabela ASCII
        break

# Liberação dos recursos utilizados
camera.release()
cv2.destroyAllWindows()
