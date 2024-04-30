# virtualKeyboardPy

O virtualKeyboardPy é um projeto de visão computacional em Python que visa criar um teclado virtual acessível através das coordenadas das mãos. Este projeto é especialmente importante para acessibilidade, permitindo que pessoas com deficiências possam usar dispositivos digitais sem depender de teclados físicos.

## Visão Geral

O código em Python utiliza as bibliotecas OpenCV e MediaPipe, junto com os módulos do MediaPipe Hands, para detectar e rastrear as mãos em uma imagem de vídeo da câmera. Isso permite a interação com o teclado virtual, onde os gestos das mãos são mapeados para a digitação de texto e controle de aplicativos.

## 💻 Tecnologias Utilizadas

- **OpenCV**: Biblioteca para processamento de imagens e vídeos.
- **MediaPipe**: Framework para visão computacional, incluindo detecção de mãos.
- **TensorFlow**: Utilizado pelo MediaPipe para inferência de modelos de detecção.
- **Anaconda**: Ambiente de gerenciamento de pacotes que simplifica a instalação e configuração do projeto.

## Pré-Requisitos

Para executar este projeto, é necessário ter uma webcam instalada no computador.

## 🚀 Instalação

Para instalar as dependências necessárias, siga estes passos:

### Passo 1: Abra o Anaconda Navigator

### Passo 2: Abra o Prompt de Comando do Anaconda e execute os seguintes comandos:

```bash
pip install opencv-python
pip install mediapipe
pip install pynput
```

Estes comandos instalarão as bibliotecas OpenCV, MediaPipe e Pynput no ambiente virtual do Anaconda, garantindo que o projeto funcione corretamente.

## Executando o Projeto

Após instalar as dependências, você pode executar o projeto virtualKeyboardPy abrindo o arquivo principal em seu ambiente de desenvolvimento Python e executando-o. Certifique-se de que sua webcam esteja funcionando corretamente para capturar as coordenadas das mãos e interagir com o teclado virtual.
