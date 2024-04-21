import cv2
import mediapipe as mp

# Inicialização das soluções do mediapipe para detecção de mãos
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Inicialização do modelo de detecção de mãos
hands = mp_hands.Hands()

# Inicialização da câmera
camera = cv2.VideoCapture(0)

# Configuração da resolução da imagem
resolution_x = 1280
resolution_y = 720
camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolution_x)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution_y)


def find_hands_coordinates(img, side_inverted = False):
    # Converte a imagem para RGB (mediapipe requer RGB)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Processamento da imagem para detecção de mãos
    result = hands.process(img_rgb)

    all_hands = [] # dicionário que irá armazenar as informações de todas as mãos

    # Verifica se há mãos detectadas na imagem
    if result.multi_hand_landmarks:
        # Desenha os pontos e conexões das mãos na imagem
        for side_hand, hand_marks in zip(result.multi_handedness, result.multi_hand_landmarks):
            # Coleta as coordenadas
            hand_info = {}
            coordinates = []
            for  mark in hand_marks.landmark:
                coord_x, coord_y, coord_z = (
                    int(mark.x * resolution_x),  # Largura
                    int(mark.y * resolution_y),  # Altura
                    int(mark.z * resolution_x),  # Profundidade
                )
                coordinates.append(
                    (coord_x, coord_y, coord_z)
                )  # Armazena todas as coordenadas da mão em uma lista

            hand_info["coordenadas"] = coordinates

            # checando se o lado está invertido 
            if side_inverted:
                # invertendo os valores
                if side_hand.classification[0].label == 'Left':
                   hand_info['lado'] = 'Right'
                else:
                    side_hand.classification[0].label = 'Right'
            else:
                hand_info['lado'] = side_hand.classification[0].label
                
            # acessando informação sobre qual é o lado da mão
            print(side_hand.classification[0].label)

            all_hands.append(hand_info)

            # Desenha os landmarks e conexões das mãos na imagem
            mp_draw.draw_landmarks(img, hand_marks, mp_hands.HAND_CONNECTIONS)

    return img, all_hands


# Loop para mostrar a imagem em tempo real
while True:
    # Captura de um frame da câmera
    success, img = camera.read()
    # invertendo a imagem
    img = cv2.flip(img, 1) # 1 - inverte a esquerda pela direita

    # Encontra e desenha as coordenadas das mãos na imagem
    img, all_hands = find_hands_coordinates(img)

    # Mostra a imagem em uma janela
    cv2.imshow("Imagem", img)

    # Aguarda um determinado tempo e verifica se a tecla "ESC" foi pressionada para sair do loop
    key = cv2.waitKey(1)
    if key == 27:
        break

# Libera a câmera e fecha todas as janelas
camera.release()
cv2.destroyAllWindows()
