import cv2
import mediapipe as mp
import os

# CONSTANTES DE CORES QUE VÃO SER UTILIZADAS
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (255, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (0, 0, 255)
AZUL_CLARO = (255, 255, 0)

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
notepad = False
chrome = False
calculadora = False
teclas = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", " "],
]
offset = 50
contador = 0
texto = ">"


def find_hands_coordinates(img, side_inverted=False):
    """
    Encontra e desenha as coordenadas das mãos na imagem.

    Args:
        img: Imagem de entrada.
        side_inverted: Indica se o lado das mãos está invertido.

    Returns:
        img: Imagem com as coordenadas das mãos desenhadas.
        all_hands: Lista de informações das mãos encontradas.
    """
    # Converte a imagem para RGB (mediapipe requer RGB)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Processamento da imagem para detecção de mãos
    result = hands.process(img_rgb)

    all_hands = []  # Lista que armazenará informações de todas as mãos

    # Verifica se há mãos detectadas na imagem
    if result.multi_hand_landmarks:
        # Desenha os pontos e conexões das mãos na imagem
        for side_hand, hand_marks in zip(
            result.multi_handedness, result.multi_hand_landmarks
        ):
            # Coleta as coordenadas
            hand_info = {}
            coordinates = []
            for mark in hand_marks.landmark:
                coord_x, coord_y, coord_z = (
                    int(mark.x * resolution_x),  # Largura
                    int(mark.y * resolution_y),  # Altura
                    int(mark.z * resolution_x),  # Profundidade
                )
                coordinates.append(
                    (coord_x, coord_y, coord_z)
                )  # Armazena as coordenadas
            hand_info["coordenadas"] = coordinates

            # Verifica e ajusta o lado da mão conforme necessário
            if side_inverted:
                if side_hand.classification[0].label == "Left":
                    hand_info["lado"] = "Right"
                else:
                    hand_info["lado"] = "Left"
            else:
                hand_info["lado"] = side_hand.classification[0].label

            all_hands.append(hand_info)

            # Desenha os landmarks e conexões das mãos na imagem
            mp_draw.draw_landmarks(img, hand_marks, mp_hands.HAND_CONNECTIONS)

    return img, all_hands


def raised_fingers(hand):
    """
    Verifica quais dedos estão levantados em uma mão.

    Args:
        hand: Informações da mão.

    Returns:
        fingers: Lista de booleanos indicando quais dedos estão levantados.
    """
    fingers = []

    for finger_tip in [8, 12, 16, 20]:
        fingers.append(
            hand["coordenadas"][finger_tip][1] < hand["coordenadas"][finger_tip - 2][1]
        )

    return fingers


def print_buttons(img, position, letter, size=50, rectangle_color=BRANCO):
    # desenhando o retangulo do teclado
    cv2.rectangle(
        img,
        position,
        (position[0] + size, position[1] + size),
        rectangle_color,
        cv2.FILLED,
    )
    # adicionando uma borda
    cv2.rectangle(img, position, (position[0] + size, position[1] + size), AZUL, 1)
    # escrevendo as letras
    cv2.putText(
        img,
        letter,
        (position[0] + 15, position[1] + 30),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        PRETO,
        2,
    )
    return img


# Loop para mostrar a imagem em tempo real
while True:
    # Captura de um frame da câmera
    success, img = camera.read()
    # Inverte a imagem horizontalmente
    img = cv2.flip(img, 1)

    # Encontra e desenha as coordenadas das mãos na imagem
    img, all_hands = find_hands_coordinates(img)

    if len(all_hands) == 1:
        info_finger_hand1 = raised_fingers(all_hands[0])
        # só aparece o teclado se for a mão esquerda
        if all_hands[0]["lado"] == "Left":
            # acessando coordenadas do indicador
            indicador_x, indicador_y, indicador_z = all_hands[0]["coordenadas"][8]
            cv2.putText(
                img,
                f"Distancia camera: {indicador_z}",
                (850, 50),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                BRANCO,
                2,
            )

            # inserindo as letras no teclado virtual
            for indice_linha, linha_teclado in enumerate(teclas):
                for indice, letra in enumerate(linha_teclado):
                    # mecanismo para alternar entre maiusculo e minusculo
                    if sum(info_finger_hand1) <= 1:
                        letra = letra.lower()
                    img = print_buttons(
                        img, (offset + indice * 80, offset + indice_linha * 80), letra
                    )
                    # checar se as coordenadas do indicador estão posicionadas dentro da região da tecla
                    if (
                        offset + indice * 80 < indicador_x < 100 + indice * 50
                        and offset + indice_linha * 80
                        < indicador_y
                        < 100 + indice_linha * 80
                    ):
                        # modificando a cor da tecla se o dedo estiver em cima
                        img = print_buttons(
                            img,
                            (offset + indice * 80, offset + indice_linha * 80),
                            letra,
                            rectangle_color=VERDE,
                        )
                        if indicador_z < -85:
                            contador = 1
                            escreve = letra
                            img = print_buttons(
                                img,
                                (offset + indice * 80, offset + indice_linha * 80),
                                letra,
                                rectangle_color=AZUL_CLARO,
                            )
            if contador:
                contador += 1
                if contador == 3:
                    texto += escreve
                    contador = 0

        # só executa se for a mão direita
        if all_hands[0]["lado"] == "Right":
            # abrindo o notepad com o indicador
            if info_finger_hand1 == [True, False, False, False] and notepad == False:
                notepad = True
                os.startfile(r"C:\Windows\notepad.exe")

            # abrindo o chrome com o indicador e o dedo médio
            if info_finger_hand1 == [True, True, False, False] and chrome == False:
                chrome = True
                os.startfile(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

            # abrindo a calculadora com o indicador e o dedo médio e anelar
            if info_finger_hand1 == [True, True, True, False] and calculadora == False:
                calculadora = True
                os.startfile(r"C:\Windows\System32\calc.exe")

            # fechando o bloco de notas quando todos os dedos estiverem abaixados
            if info_finger_hand1 == [False, False, False, False] and notepad == True:
                notepad = False
                os.system("TASKKILL /IM notepad.exe")

            # Encerrando o loop caso o dedo indicador e o minimo estejam levantados
            if info_finger_hand1 == [True, False, False, True]:
                break

    # Mostra a imagem em uma janela
    cv2.imshow("Imagem", img)

    # Aguarda um determinado tempo e verifica se a tecla 'ESC' foi pressionada para sair do loop
    key = cv2.waitKey(1)
    if key == 27:
        break

# Libera a câmera e fecha todas as janelas
camera.release()
cv2.destroyAllWindows()
