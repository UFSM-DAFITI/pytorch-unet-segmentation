# -*- coding: utf-8 -*-
import sys

if __name__ == "__main__":
    if (len(sys.argv) < 2):
      print(f"Usage : python ",sys.argv[0]," imageurl")
      print(f"Example : python ",sys.argv[0]," https://static.dafiti.com.br/p/GAP-Camiseta-GAP-Batman-Preta-1662-3358368-3-zoom.jpg")
    else:
      import torch
      import numpy as np
      from PIL import Image
      import urllib.request
      from unet_segmentation.prediction.display import daftpunk
      #esse import é feito a partir das pastas do projeto
      
      url = urllib.parse.quote(sys.argv[1],safe=':/')
      
      urllib.request.urlretrieve(url, "foto.jpg")

      '''Realiza a segmentação semântica da imagem em foto.jpg. O resultado da 
      predição é um dicionário indexado pelo tipo de roupa detectado. Por exemplo, 
      para extrair a máscara de uma calça da foto, utiliza-se

      mascaras = daftpunk(model, 'foto.jpg')
      mascaradacalca = mascaras["trousers"]

      As roupas possíveis podem ser
      "trousers" -> calças, 
      "skirt" -> saias, 
      "top" -> camisas,camisetas,
      "dress" -> vestidos, 
      "outwear" -> casacos(?) ou 
      "shorts" -> shorts, calção
      '''

      if torch.cuda.is_available():
        model = torch.load('unet.pt')
         #esse unet_iter_1300000.pt (modelo treinado) e mudar o nome para unet.pt deve ser feito o download no link https://drive.google.com/file/d/1sC_puW3pc6P75KTi2hJxgjgUiZo3zl1Q/view
        mascaras = daftpunk(model, 'foto.jpg')
       #Aqui só precisa colocar o nome da imagem e ela precisa estar no mesmo path do algoritmo, ela precisa ser um formato JPEG (se for PNG vai apontar que da erro com o canal alpha)
      else:
        model = torch.load('unet.pt', map_location=torch.device('cpu'))
        mascaras = daftpunk(model, 'foto.jpg', device ='cpu')
      # daft : alterei a função e agora ela realiza a predição e salva as classes encontradas em um dicionário. Para acessar uma máscara em específico,
      # utilize mascaras[coisa] em que coisa pode ser "trousers", "skirt", "top", "dress", "outwear" ou "shorts"

      #carregando imagem e mascara
      imagem = Image.open('foto.jpg')
      mascara = mascaras["top"]
      left,upper,right,lower = mascara.getbbox()

      def shirt_rescaling(image, newsize, left,right,lower,upper, newleft, newright, newlower,newupper):
        scaling_y = (lower - upper)/(newlower - newupper)
        translate_y = upper - scaling_y*newupper

        scaling_x = (right - left)/(newright - newleft)
        translate_x = right - scaling_x*newright

        result = image.transform(newsize, Image.AFFINE, (scaling_x, 0, translate_x, 0, scaling_y, translate_y))
        return result

      '''Utiliza metahuman.png como o background de uma imagem e coloca a camiseta 
      segmentada por cima. Os parâmetros newuper, newlower, newleft e newright precisam 
      ser atribuídos manualmente de acordo com o avatar utilizado. Salva a imagem no 
      arquivo gordola.png'''

      background = Image.open('metahuman.png')

      newsize = background.size 

      newupper = 155
      newlower = 400
      newleft = 130
      newright = 425

      scaled = shirt_rescaling(imagem, newsize, left,right,lower,upper, newleft, newright, newlower,newupper)
      scaled_mask = shirt_rescaling(mascaras["top"], newsize, left,right,lower,upper, newleft, newright, newlower,newupper)

      # paste image giving dimensions
      background.paste(scaled, (0, 0),scaled_mask)

      background.save('gordola.png')
 
