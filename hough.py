import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

def cargarImagenes(directory):
    images = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(('.png', '.jpg', '.jpeg'))]
    return [cv2.imread(image, 0) for image in images]

def deteccionBordes(image):
    edges = cv2.Canny(image, 50, 150)
    return edges

def resize(image, scale_percent=50):
    ancho = int(image.shape[1] * scale_percent / 100)
    alto = int(image.shape[0] * scale_percent / 100)
    return cv2.resize(image, (ancho, alto))

def houghm(image):
    alto, ancho = image.shape
    diag_len = int(np.sqrt(alto**2 + ancho**2))
    
    rhos = np.linspace(-diag_len, diag_len, 2*diag_len)
    thetas = np.deg2rad(np.arange(-90, 90))  
    acumulador = np.zeros((2*diag_len, len(thetas)))  

    cos_thetas = np.cos(thetas)
    sin_thetas = np.sin(thetas)

    for y in range(alto):
        for x in range(ancho):
            if image[y, x] > 0:  
                for theta_idx in range(len(thetas)):
                    rho = int(x * cos_thetas[theta_idx] + y * sin_thetas[theta_idx])
                    rho_idx = rho + diag_len  
                    acumulador[rho_idx, theta_idx] += 1 
    
    return acumulador, thetas, rhos

def detectarLineas(acumulador, thetas, rhos, threshold=100):
    lineas = []
    for rho_idx in range(acumulador.shape[0]):
        for theta_idx in range(acumulador.shape[1]):
            if acumulador[rho_idx, theta_idx] > threshold:
                rho = rhos[rho_idx]
                theta = thetas[theta_idx]
                lineas.append((rho, theta))
    return lineas

def dibujarLineas(image, lineas):
    imagenYa = np.copy(image)
    for rho, theta in lineas:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(imagenYa, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return imagenYa

def graficoHough(acumulador, filename=None):
    plt.imshow(acumulador, cmap='hot')
    plt.title('Espacio de Hough')
    plt.xlabel('Theta')
    plt.ylabel('Rho')
    if filename:
        plt.savefig(filename)
    else:
        plt.show()

def guardar(images, result_filename="result.jpg"):
    imagenGuardada = np.concatenate(images, axis=1)
    cv2.imwrite(result_filename, imagenGuardada)

if __name__ == "__main__":
    directory = 'D:/Anna Beristain/Documents/practica1.2/imagenes/'
    
    images = cargarImagenes(directory)
    imagenesResultado = []

    for i, image in enumerate(images):
        image = resize(image, 50)  

        edges = deteccionBordes(image)

        acumulador, thetas, rhos = houghm(edges)

        lineas = detectarLineas(acumulador, thetas, rhos)

        imagenYa = dibujarLineas(image, lineas)
        imagenesResultado.append(imagenYa)

        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(imagenYa, cmap='gray')
        plt.title('Líneas Detectadas')

        plt.subplot(1, 2, 2)
        graficoHough(acumulador)

        plt.show()

        hough_filename = f"hough_space_{i}.jpg"
        graficoHough(acumulador, filename=hough_filename)

    guardar(imagenesResultado)
