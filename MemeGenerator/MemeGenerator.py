import json
from PIL import Image, ImageDraw, ImageFont
import itertools


class MemeGenerator:
    imagesPath = './MemeGenerator/images.json'
    images = json.load(open(imagesPath))
    configPath = './MemeGenerator/configuration.json'
    #orden: numero de argumentos, ancho, alto, offset_x, offset_y, rango de tamaño de letra, espaciado entre lineas
    configuration = json.load(open(configPath))
    fontsPath = './MemeGenerator/fonts.json'
    fonts = json.load(open(fontsPath))

    def break_fix(self, text, width, font, draw):
        if not text:
            return
        lo = 0
        hi = len(text)
        mid = (lo + hi + 1) // 2
        esMayor = False
        #se va a la posicion inicial y se va mirando las posiciones anteriores o posteriores 
        #sumando o restando 1 hasta que encontremos la que hace el with mas grande de lo que
        #se puede escribir
        while mid <= hi and mid >= lo:
            t = text[0]
            for i in text[1:mid]:
                t = t + ' ' + i
            new_box = draw.textbbox((0, 0), t, font)
            

            w = new_box[2] - new_box[0]  # bottom-top
            h = new_box[3] - new_box[1]  # right-left

            if w <= width:
                if esMayor:
                    break
                mid = mid + 1
                
            else:
                mid = mid - 1
                esMayor = True
        t = text[0]
        for i in text[1:mid]:
            t = t + ' ' + i

        new_box = draw.textbbox((0, 0), t, font)

        w = new_box[2] - new_box[0]  # bottom-top
        if w > width:
            raise ValueError("text doesn't fit")
        h = new_box[3] - new_box[1]  # right-left

        yield t, w, h
        yield from self.break_fix(text[mid:], width, font, draw)

    def fit_text(self, img, text, color, font, ancho, alto, offset_x, offset_y, espaciado):
        #Si se quisiera aplicar sobre una imagen habria que añadirle el offset sobre donde se van a colocar
        width = ancho - 2
        draw = ImageDraw.Draw(img)
        t = text.split() #OJO es importante para que se divida en lineas por espacios
        pieces = list(self.break_fix(t, width, font, draw))
        height = sum(p[2] for p in pieces)
        if height > alto:
            raise ValueError("text doesn't fit")
        y = (alto - height) // 2
        for t, w, h in pieces:
            x = (ancho - w) // 2
            draw.text((offset_x + x, offset_y + y), t, font=font, fill=color, stroke_width=3, stroke_fill='black')
            #draw.text((offset_x + x, offset_y + y), t, font=font, fill=color)
            #TODO revisar este espaciado es para que no se peguen las letras entre ellas y poner mas diferencia entre ellas para que no se toque
            y += h + espaciado

    def try_fit_text(self, img, text, font, ancho, alto):
        width = ancho - 2
        draw = ImageDraw.Draw(img)
        t = text.split() #OJO es importante para que se divida en lineas por espacios
        try:
            pieces = list(self.break_fix(t, width, font, draw))
        except:
            raise ValueError("text doesn't fit")
        height = sum(p[2] for p in pieces)
        if height > alto:
            raise ValueError("text doesn't fit")

    def write_text(self, img, cadena, ancho, alto, offset_x, offset_y, rango, espaciado):
        #TODO optimizar con busqueda binaria
        for size in range(rango[0], rango[1]):
            Font = ImageFont.FreeTypeFont('./fonts/LiberationSans-Regular.ttf', size=size)
            try:
                self.try_fit_text(img, cadena, Font, ancho, alto)
            except:
                break
                
            selected_size = size

        arial = ImageFont.FreeTypeFont('./fonts/LiberationSans-Regular.ttf', size=selected_size)
        self.fit_text(img, cadena, (255,255,255), arial, ancho, alto,  offset_x, offset_y, espaciado)
        return img
    
    def write_image(self, imageID, argmuentos, l_cadena, l_ancho, l_alto, l_offset_x, l_offset_y, l_rango, l_espaciado):
        imagePath = self.images.get(imageID)
        if imagePath is None:
            raise ValueError("imageID invalid")
        img = Image.open(imagePath)
        if argmuentos != len(l_cadena) or argmuentos != len(l_ancho) or argmuentos != len(l_alto) or argmuentos != len(l_offset_x) or argmuentos != len(l_offset_y) or argmuentos != len(l_rango) or argmuentos != len(l_espaciado):
            raise ValueError("All the list must have the same number of elements")
        for i in range(argmuentos):
            self.write_text(img,l_cadena[i], l_ancho[i], l_alto[i], l_offset_x[i], l_offset_y[i], l_rango[i], l_espaciado[i])
        return img
    
    def makeMeme(self, imageID, l_cadena):
        imageOptions = self.configuration.get(imageID)
        if imageOptions is None:
            raise ValueError("imageID invalid")
        return self.write_image(imageID, imageOptions[0], l_cadena, imageOptions[1], imageOptions[2], imageOptions[3], imageOptions[4], imageOptions[5], imageOptions[6])

    def help(self):
        title = "Meme Generator Commands"
        commands = ["info", "list", "create"]
        params = ["imageID", None, "imageID <strings>"]
        descriptions = ["Returns the number of strings that the imageID can take", "Returns the list of available imageIDs", "Creates a meme with the given imageID and the given strings, the strings must be separated by \';\'"]

        return (title, commands, params, descriptions)

    def listAvail(self):
        return ", ".join(self.images.keys())
    
    def info(self,imageID):
        arguments = self.configuration.get(imageID)
        if arguments is None:
            return "Thats not a imageID"
        return "The number of strings is " + str(arguments[0])
    
    def saveMeme(self, imageID, l_cadena, path):
        img = self.makeMeme(imageID,l_cadena)
        img.save(path)
    
    def reload(self):
        self.images = json.load(open(self.imagesPath))
        self.configuration = json.load(open(self.configPath))
        self.fonts = json.load(open(self.fontsPath)) 