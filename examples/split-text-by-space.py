from PIL import Image, ImageDraw, ImageFont

def break_fix(text, width, font, draw):
    if not text:
        return
    lo = 0
    hi = len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        #t = text[:mid]
        t = text[0]
        for i in text[1:mid]:
            t = t + ' ' + i
         # calculate bbox for version 8.0.0
        new_box = draw.textbbox((0, 0), t, font)  # need 8.0.0
        

        w = new_box[2] - new_box[0]  # bottom-top
        h = new_box[3] - new_box[1]  # right-left

        #w, h = draw.textsize(t, font=font)
        if w <= width:
            lo = mid
        else:
            hi = mid - 1
    t = text[0]
    for i in text[1:lo]:
        t = t + ' ' + i
    #t = text[:lo]
    #w, h = draw.textsize(t, font=font)

    new_box = draw.textbbox((0, 0), t, font)  # need 8.0.0

    # `bbox` may have top/left margin so calculate real width/height
    w = new_box[2] - new_box[0]  # bottom-top
    h = new_box[3] - new_box[1]  # right-left

    yield t, w, h
    yield from break_fix(text[lo:], width, font, draw)

def fit_text(img, text, color, font):
    #Si se quisiera aplicar sobre una imagen habria que añadirle el offset sobre donde se van a colocar
    offset_x = 0
    offset_y = 0
    width = img.size[0] - 2
    draw = ImageDraw.Draw(img)
    pieces = list(break_fix(text.split(), width, font, draw))
    height = sum(p[2] for p in pieces)
    if height > img.size[1]:
        raise ValueError("text doesn't fit")
    y = (img.size[1] - height) // 2
    for t, w, h in pieces:
        x = (img.size[0] - w) // 2
        draw.text((offset_x + x, offset_y + y), t, font=font, fill=color)
        y += h

cadena = "abc efgh ijklmnñ opq rstv wxy z ab c def g"
img = Image.new('RGB', (128, 48), color='black')
Font = ImageFont.FreeTypeFont('/usr/share/fonts/liberation/LiberationSans-Regular.ttf', size=15)
fit_text(img, cadena, (255,255,0), Font)
img.save('split-text-by-space.png')