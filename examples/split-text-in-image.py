from PIL import Image, ImageDraw, ImageFont

def break_fix(text, width, font, draw):
    if not text:
        return
    lo = 0
    hi = len(text)
    mid = (lo + hi + 1) // 2
    esMayor = False
    while mid <= hi and mid >= lo:
        t = text[0]
        for i in text[1:mid]:
            t = t + ' ' + i
        # calculate bbox for version 8.0.0
        new_box = draw.textbbox((0, 0), t, font)  # need 8.0.0
        

        w = new_box[2] - new_box[0]  # bottom-top
        h = new_box[3] - new_box[1]  # right-left

        #w, h = draw.textsize(t, font=font)
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
    #t = text[:lo]
    #w, h = draw.textsize(t, font=font)

    new_box = draw.textbbox((0, 0), t, font)  # need 8.0.0

    # `bbox` may have top/left margin so calculate real width/height
    w = new_box[2] - new_box[0]  # bottom-top
    if w > width:
        raise ValueError("text doesn't fit")
    h = new_box[3] - new_box[1]  # right-left

    yield t, w, h
    yield from break_fix(text[mid:], width, font, draw)

def fit_text(img, text, color, font, ancho, alto, offset_x, offset_y, espaciado):
    #Si se quisiera aplicar sobre una imagen habria que añadirle el offset sobre donde se van a colocar
    #width = img.size[0] - 2
    width = ancho - 2
    draw = ImageDraw.Draw(img)
    t = text.split() #OJO es importante para que se divida en lineas por espacios
    pieces = list(break_fix(t, width, font, draw))
    height = sum(p[2] for p in pieces)
    #if height > img.size[1]:
    if height > alto:
        raise ValueError("text doesn't fit")
    #y = (img.size[1] - height) // 2
    y = (alto - height) // 2
    for t, w, h in pieces:
        #x = (img.size[0] - w) // 2
        x = (ancho - w) // 2
        draw.text((offset_x + x, offset_y + y), t, font=font, fill=color, stroke_width=2, stroke_fill='black')
        #draw.text((offset_x + x, offset_y + y), t, font=font, fill=color)
        #TODO revisar este espaciado es para que no se peguen las letras entre ellas y poner mas diferencia entre ellas para que no se toque
        y += h + espaciado

def try_fit_text(img, text, font, ancho, alto):
    width = ancho - 2
    draw = ImageDraw.Draw(img)
    t = text.split() #OJO es importante para que se divida en lineas por espacios
    try:
        pieces = list(break_fix(t, width, font, draw))
    except:
        raise ValueError("text doesn't fit")
    height = sum(p[2] for p in pieces)
    #if height > img.size[1]:
    if height > alto:
        raise ValueError("text doesn't fit")

#img = Image.new('RGB', (128, 48), color='black')
img = Image.open('./templates/children_scare_from_rabbit.jpg')
cadena = "masako viendo a kuniko meterse donde no le llaman"
#cadena = "m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m"
ancho = 130
alto = 175
offset_x = 193
offset_y = 400
espaciado = 2
for size in range(10, 100):
    Font = ImageFont.FreeTypeFont('/usr/share/fonts/liberation/LiberationSans-Regular.ttf', size=size)
    try:
        if size == 42:
            print('a')
        try_fit_text(img, cadena, Font, ancho, alto)
    except:
        break
        
    selected_size = size

    print(Font.size)

arial = ImageFont.FreeTypeFont('/usr/share/fonts/liberation/LiberationSans-Regular.ttf', size=selected_size)
#fit_text(img, cadena, (255,255,255), arial, 160, 100,  170, 450)
fit_text(img, cadena, (255,255,255), arial, ancho, alto,  offset_x, offset_y, espaciado)
img.save('split-text-in-image.png')