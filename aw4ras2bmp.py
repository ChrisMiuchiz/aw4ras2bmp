#ChrisMiuchiz
#Written for Python 3.6.0
import sys

def to4bytes(integer):
    bytes = [0,0,0,0]
    if integer <= 0xFFFFFFFF:
        i=3
        while integer>0:
            bytes[i]=(integer&0xFF)
            integer = integer^0xFF
            integer = integer>>8
            i -= 1
        return list(reversed(bytes))
    else:
        print("to4bytes error")

def readbytes(contents, address, bytenum):
    result = 0
    i = bytenum-1
    while i >= 0:
        result = result + int(contents[address+i])*256**i
        i -= 1
    return result

def getraspixel(ptype, filecontents, address):
    if ptype == "r":
        pixelbytes = [((filecontents[address+1]&0xF8)>>3)]
        redpixel = round((pixelbytes[0]*255)/31)
        return redpixel
    elif ptype == "g":
        pixelbytes = [(filecontents[address+1]&0x7),(filecontents[address]&0xE0)>>5]
        greenpixel = round((((pixelbytes[0]<<3)+pixelbytes[1])*255)/63)
        return greenpixel
    elif ptype == "b":
        pixelbytes = [filecontents[address]&0x1F]
        bluepixel = round((pixelbytes[0]*255)/31)
        return bluepixel

if len(sys.argv) != 2:
    print("Usage: aw4ras2bmp <input RAS file>")
    infile = input("Enter input RAS file: ")
else:
    infile=str(sys.argv[1])
try:
    rasfile = open(infile, "rb")
except:
    print("Error opening file.")
    quit()
destfile = str(infile[:len(infile)-3])+"bmp"

rascontents = rasfile.read()
rasfile.close()
width = readbytes(rascontents, 0x5, 2)
height = readbytes(rascontents, 0x7, 2)
print("Input filename:",infile)
print("Width:",width)
print("Height:",height)
outfile = open(destfile, "wb")

i=0x0D #Starting point
pixels = []

#make pixel array
while i < len(rascontents):
    pixels.append(getraspixel("b", rascontents, i))
    pixels.append(getraspixel("g", rascontents, i))
    pixels.append(getraspixel("r", rascontents, i))
    i+=2
    
#write bmp file
out_size = to4bytes(54+len(pixels))
out_width = to4bytes(width)
out_height = to4bytes(0x100000000-height)

bmpheader = [0x42, 0x4D]
bmpheader.extend(out_size)
bmpheader.extend([0x00, 0x00, 0x00, 0x00, 0x36, 0x00, 0x00, 0x00,
                  0x28, 0x00, 0x00, 0x00])#DIB
bmpheader.extend(out_width)
bmpheader.extend(out_height)
bmpheader.extend([0x01, 0x00, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x13, 0x0B, 0x00, 0x00, 0x13, 0x0B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

outfile.write(bytearray(bmpheader))
outfile.write(bytearray(pixels))
outfile.close()

