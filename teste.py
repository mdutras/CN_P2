'''
Arquivo usado para testes de implementação
'''
import numpy as np
import imageio
import matplotlib.pyplot as plt

def numera(M):
    print("numera")
    n,m = M.shape[0:2]
    I = np.zeros((n,m), dtype=int)
    counter = 0
    # TODO: numeração das equações
    for i in range(n):
        for j in range(m):
            if(np.sum(M[i,j]) != 255 * 3):
                I[i,j] = counter
                counter += 1
            else:
                I[i,j] = -1
    return I

def montagem(P,M):
    print("montagem")
    # numera as equações
    I = numera(M)
    n,m = M.shape[0:2]
    # calcula a quantidade de pixels indesejados
    N = np.count_nonzero(I >= 0)
    
    # TODO: constroi a matriz e os vetores independentes
    A  = np.eye(N) * 8
    br = np.zeros((N,))
    bg = np.zeros((N,))
    bb = np.zeros((N,))

    for i in range(n):
        for j in range(m):
            if(I[i,j] > -1):
                index = I[i,j]
                for k in [-1, 0, 1]:
                    for l in [-1, 0, 1]:
                        if((k == 0 and l == 0) or (i + k < 0 or i + k >= n or j + l < 0 or j + l >= m)):
                            continue
                        else:
                            if(I[i+k,j+l] > -1):
                                aux = I[i+k,j+l]
                                A[index,aux] = -1
                            else:
                                br[index] += P[i+k,j+l,0]
                                bg[index] += P[i+k,j+l,1]
                                bb[index] += P[i+k,j+l,2]
    return I,A,br,bg,bb

def retoque(P,M):
    print("retoque")
    # montagem do sistema
    I,A,br,bg,bb = montagem(P,M)
    retocada = np.copy(P)
    n,m = M.shape[0:2]
    counter = 0
    # TODO: cálculo das novas cores
    print("solving red")
    ansR = np.linalg.solve(A, br)
    print("solving green")
    ansG = np.linalg.solve(A, bg)
    print("solving blue")
    ansB = np.linalg.solve(A, bb)
    # TODO: construção da imagem retocada
    for i in range(n):
        for j in range(m):
            if(I[i,j] > -1):
                retocada[i,j,0] = ansR[counter]
                retocada[i,j,1] = ansG[counter]
                retocada[i,j,2] = ansB[counter]
                counter += 1
    return retocada

def main():
    print("Hello World")
    original = imageio.v2.imread("./original.png")
    mascara = imageio.v2.imread("./mascara.png")
    #retoque(img, mascara)
    retocada = retoque(original,mascara)
    plt.figure(figsize=(15,10))
    plt.imshow(retocada)
    plt.show()

if __name__ == "__main__":
    main()
