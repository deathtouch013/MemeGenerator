import sys
from MemeGenerator.MemeGenerator import MemeGenerator

nargv = len(sys.argv)
meme = MemeGenerator()
path = "./result/meme-generado.png"
StringsBegin = 2
if sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print(meme.help)
    exit

if nargv >= 4 and sys.argv[2] == "-o":
    path = sys.argv[3]
    StringsBegin = 4


if sys.argv[1] == "info" and nargv == 3:
    print(meme.info(sys.argv[2]))

strings = []
aux = ""
for i in sys.argv[StringsBegin:]:
    if i == ";":
        strings.append(aux[:-1])
        aux = ""
        continue
    aux = aux + i + " "
strings.append(aux[:-1])
try:
    meme.saveMeme(sys.argv[1],strings,path)
except ValueError as e:
    print(e)
