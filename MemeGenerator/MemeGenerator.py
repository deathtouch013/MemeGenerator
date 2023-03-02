import json
from PIL import Image, ImageDraw, ImageFont
import itertools
import os
import io
import requests
from requests_testadapter import Resp

LOCAL_URI_PREFIX = 'meme://'
LOCAL_URI_PREFIX_LEN = LOCAL_URI_PREFIX.__len__()

class LocalMemeAdapter(requests.adapters.HTTPAdapter):
    def build_response_from_file(self, request):
        file_path = request.url[LOCAL_URI_PREFIX_LEN:]
        print(file_path)
        with open(file_path, 'rb') as file:
            buff = bytearray(os.path.getsize(file_path))
            file.readinto(buff)
            resp = Resp(buff)
            r = self.build_response(request, resp)

            return r

    def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):
        return self.build_response_from_file(request)

class MemeGenerator:

    def __init__(self):
        self.templatesPath = os.path.abspath('./MemeGenerator/templates.json')
        self.templates = json.load(open(self.templatesPath))

        self.fontsPath = os.path.abspath('./MemeGenerator/fonts.json')
        self.fonts = json.load(open(self.fontsPath))

        # Register session
        self.requests_session = requests.Session()
        self.requests_session.mount('meme://', LocalMemeAdapter())

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
    
    # @pre: imageID is not None
    def write_image(self, imageID, num_args, l_cadena, l_ancho, l_alto, l_offset_x, l_offset_y, l_rango, l_espaciado):
        imagePath = self.templates.get(imageID)["source"]
        print(f"write_image Options = " + imagePath)

        # Redundant check, imageID is not none
        # if imagePath is None:
        #     raise ValueError("imageID invalid")

        # Load from http request
        response = self.requests_session.get(imagePath, stream=True, allow_redirects=True, headers={'Accept-Encoding': ''})
        img_buf = io.BytesIO(bytes(response.content))
        img = Image.open(img_buf)

        print("Image loaded!")

        if num_args != len(l_cadena) or num_args != len(l_ancho) or num_args != len(l_alto) or num_args != len(l_offset_x) or num_args != len(l_offset_y) or num_args != len(l_rango) or num_args != len(l_espaciado):
            raise ValueError("All the list must have the same number of elements")
        for i in range(num_args):
            self.write_text(img,l_cadena[i], l_ancho[i], l_alto[i], l_offset_x[i], l_offset_y[i], l_rango[i], l_espaciado[i])
        return img
    
    def makeMeme(self, imageID, l_cadena):
        imageOptions = self.templates.get(imageID)["positionList"]
        print(f"makeMeme Options = {imageOptions}")

        width_list = []
        height_list = []
        offset_x_list = []
        offset_y_list = []
        range_list = []
        spacing_list = []

        for key in imageOptions:
            width_list.append(key["width"])
            height_list.append(key["height"])
            offset_x_list.append(key["x"])
            offset_y_list.append(key["y"])
            range_list.append(key["sizeRange"])
            spacing_list.append(key["lineSpacing"])
        
        if imageOptions is None:
            raise ValueError("imageID invalid")
        
        return self.write_image(imageID=imageID, num_args=len(imageOptions), l_cadena=l_cadena, l_ancho=width_list, l_alto=height_list, l_offset_x=offset_x_list, l_offset_y=offset_y_list, l_rango=range_list, l_espaciado=spacing_list)

    def help(self):
        title = "Meme Generator Commands"
        commands = ["info", "list", "create"]
        params = ["imageID", None, "imageID <strings>"]
        descriptions = ["Returns the number of strings that the imageID can take", "Returns the list of available imageIDs", "Creates a meme with the given imageID and the given strings, the strings must be separated by \';\'"]

        return (title, commands, params, descriptions)

    def listAvail(self):
        # Todo make an embed
        return ", ".join(self.templates.keys())
    
    def info(self,imageID):
        imageOptions = self.templates.get(imageID)["positionList"]
        
        if imageOptions is None:
            return "Thats not a valid imageID!"

        return f"Format: `!meme create {imageID} {';'.join([f' string{i} ' for i in range(len(imageOptions))])}`"
    
    def saveMeme(self, imageID, l_cadena, path):
        img = self.makeMeme(imageID,l_cadena)
        img.save(path)
    
    def reload(self):
        self.__init__()