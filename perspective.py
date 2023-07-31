#===============================================================================
# Trabalho 4
#-------------------------------------------------------------------------------
# Autor: Eduarda Simonis Gavião
# UNICAMP
#===============================================================================
# Importando bibliotecas
import sys
import numpy as np
import cv2
import scipy

# TRABALHANDO COM PERSPECTIVA
#===============================================================================
PERSPECTIVA_IMAGE =  'baboon_perspectiva.png'

#obtenção da matriz de transformção
def getPerspectiveTransform(inputPoints,outPoints):
    a = np.zeros((8, 8))
    b = np.zeros((8))

    #criando um sistema com coeficientes da matriz
    for i in range(4):
        a[i][0] = a[i+4][3] = inputPoints[i][0]
        a[i][1] = a[i+4][4] = inputPoints[i][1]
        a[i][2] = a[i+4][5] = 1
        a[i][3] = a[i][4] = a[i][5] = 0
        a[i+4][0] = a[i+4][1] = a[i+4][2] = 0
        a[i][6] = -inputPoints[i][0]*outPoints[i][0]
        a[i][7] = -inputPoints[i][1]*outPoints[i][0]
        a[i+4][6] = -inputPoints[i][0]*outPoints[i][1]
        a[i+4][7] = -inputPoints[i][1]*outPoints[i][1]
        b[i] = outPoints[i][0]
        b[i+4] = outPoints[i][1]

    #resolvendo o sistema linear e obtendo os coeficientes
    x = np.linalg.solve(a, b)
    x.resize((9,), refcheck=False)
    x[8] = 1 

    #entrega a matriz de transformação
    return x.reshape((3,3))

# funções auxiliares para trabalhar com as coordenadas horizontais e verticais.
def transform(img):
    image = np.zeros((img.shape[0],img.shape[1],img.shape[2]), dtype='uint8')
    for i in range(img.shape[0]):
        y,x= np.where(img[i]!=0)
        if(len(y)==0 or len(x)==0):
            image[:,i] = img[i]
            continue
        image[:,i]=img[i]
    return image
#função de transformação, recebe a matriz, a imagem original e o tamanho da imagem de saida
def perspective(M,img,dsize):
    
    R,C = dsize #identifica o tamanho da imagem de saída
    dst = np.zeros((R,C,img.shape[2])) # cria uma iamgem vazia com as dimensões obtidas
    #utiliza de dois laços para percorrer a imagem de saída
    for i in range(dst.shape[0]):
        for j in range(dst.shape[1]):
            res = np.dot(M,[i,j,1]) #cria um vetor de coordenadas
            i2,j2,_ = (res / res[2]).astype(int)
            if i2 >= 0 and i2 < dst.shape[0]:
                if j2 >= 0 and j2 < dst.shape[1]:
                    dst[i,j] = img[j2,i2] #passa os valores para a imagem de saída

    return transform(dst)


def main ():
    img = cv2.imread(PERSPECTIVA_IMAGE,cv2.COLOR_BGR2RGB)
        #verifica se é possível abrir a imagem
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # pontos de origem
    pt_A = [37, 51]
    pt_D = [342,42]
    pt_C = [485,467]
    pt_B = [73,380]
    # pontos de saída
    pt_ALinha = [0, 0]
    pt_DLinha = [511,0]
    pt_CLinha = [511,511]
    pt_BLinha = [0,511]
    inputPoints= np.float32([pt_A,pt_B,pt_C,pt_D])
    outPoints=np.float32([pt_ALinha,pt_BLinha,pt_CLinha,pt_DLinha])
    destination_size = (img.shape[0], img.shape[1])
    r,c = destination_size
    # Obtem a matriz de transformação via OpenCv
    mCV = cv2.getPerspectiveTransform(inputPoints,outPoints)
    # realiza a transformação via opem cv
    outCV = cv2.warpPerspective(img,mCV,(r, c))
    #obtem a matriz de transformação manualmente utilizando da função criada
    M = getPerspectiveTransform(outPoints,inputPoints)
    #realiza a transformação a partir da função criada
    out= perspective(M,img,(r,c))
    #imprime ambas as matrizes para verificar se estão iguais
    #print(mCV)
    #print(M)
    #apresenta as imagens
    cv2.imshow('Original',img)
    cv2.imshow("OpenCV",outCV)
    cv2.imshow("Manual",out)
    filename='perspectivaManual.png'
    cv2.imwrite(filename,out) 
    cv2.waitKey()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    main()
        