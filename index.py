# Importar as bibliotecas necessárias
import cv2
import numpy as np
from vidgear.gears import CamGear
import os
from PIL import Image

# Definir a área de interesse (ROI) na imagem
# Você pode modificar esses valores de acordo com sua necessidade
x = 1515 # coordenada x do canto superior esquerdo da ROI
y = 450 # coordenada y do canto superior esquerdo da ROI
w = 200 # largura da ROI
h = 200 # altura da ROI

path = 'videos'
files = [f for f in os.listdir(path) if f.endswith('.mp4')]
number = 1

for i in files:
    print(i)
    input_file = "videos/" + i
    # output_file = "video.mp4"
    # input_video = ffmpeg.input(input_file)

    # # Converter o arquivo de entrada para o formato mp4 com o codec h.264
    # output_video = ffmpeg.output(input_video, output_file, codec="libx264")

    # # Executar o processo de conversão
    # ffmpeg.run(output_video)

    # Criar um objeto CamGear com o caminho do arquivo de vídeo como fonte
    # Você pode modificar esse valor de acordo com o nome do seu arquivo
    # Você também pode usar um loop para iterar sobre vários arquivos
    cam = CamGear(source=input_file).start()

    # Criar uma variável para armazenar o quadro anterior
    prev_frame = None

    # Criar um loop infinito para processar os quadros do vídeo
    while True:

        # Ler o quadro atual do objeto CamGear
        frame = cam.read()
        # Verificar se o quadro é válido
        if frame is None:
            # Se o quadro for inválido, significa que o vídeo terminou
            break

        # Converter o quadro para escala de cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Extrair a ROI do quadro
        roi = gray[y:y+h, x:x+w]

        # Verificar se o quadro anterior é válido
        if prev_frame is not None:
            # Se o quadro anterior for válido, comparar a ROI com a ROI anterior
            diff = cv2.absdiff(roi, prev_frame)
            
            # Aplicar um limiar para binarizar a diferença
            thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
            
            # Contar o número de pixels brancos na imagem binarizada
            count = np.count_nonzero(thresh)
            # Verificar se o número de pixels brancos é maior que um limiar
            # Você pode modificar esse valor de acordo com sua sensibilidade
            if count > 1515:
                # Se o número de pixels brancos for maior que o limiar, significa que houve um movimento na ROI
                # Desenhar um retângulo vermelho na ROI para indicar o movimento
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                img = Image.fromarray (frame, 'RGB')
                img.save ('movimento'+str(number)+'.png') 
                # Imprimir uma mensagem na tela
                print("Movimento detectado " + str(number) + " na ROI do vídeo " + i)
                number += 1

        # Atualizar o quadro anterior com a ROI atual
        prev_frame = roi.copy()

        # Mostrar o quadro na janela
        cv2.imshow("Frame", frame)

        # Esperar por uma tecla para interromper o loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # Liberar os recursos
    cam.stop()
    cv2.destroyAllWindows()
