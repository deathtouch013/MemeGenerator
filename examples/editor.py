import cv2

img = cv2.imread('./templates/children_scare_from_rabbit.jpg')

texto = "diabloooooooooooooooooo"
ubicacion=(300,830)
font = cv2.FONT_HERSHEY_TRIPLEX
tamañoLetra = 2
colorLetra = (255,255,255)
grosorLetra = 1

cv2.putText(img,texto,ubicacion,font,tamañoLetra,colorLetra,grosorLetra)

cv2.imshow('imagen',img)
cv2.waitKey(0)
cv2.destroyAllWindows()