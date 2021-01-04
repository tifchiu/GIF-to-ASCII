from PIL import Image
from jinja2 import Template
import argparse
import operator

def gifToText(filename, maxLen, outputFile, withColour, character):
    try:
        maxLen = int(maxLen)
    except:
        maxLen = 80
    
    # opening the file, and alerting the user if such file is not found
    try:
        img = Image.open(filename)
    except:
        exit("file not found: {}".format(filename))
    
    # Initializing variables based on properties of the file uploaded
    width, height = img.size
    aspectRatio = float(maxLen) / max(width,height)
    width = int(aspectRatio * width)
    height = int(aspectRatio * height)

    greyscale = "@MNZQUzj?+>;*-. " # characters to be used in the ASCII generation of the gif
    choiceFactor = float(len(greyscale)) / 3.0 / 256.0 # calculations to determine pixel color (?)
    strings = []

    try:
        while True:
            palette = img.getpalette()

            img.putpalette(palette)
            newImg = Image.new('RGB', img.size)
            newImg.paste(img)
            newImg = newImg.resize((width, height))
            string = ''

            for h in range(height):
                for w in range(width):
                    rgb = newImg.getpixel((w,h))
                    #print(rgb)
                    if withColour:
                        string += ("<span style=\"color:rgb({0}, {1}, {2});\">" + character + "</span>").format(rgb[0], rgb[1], rgb[2])
                    else:
                        string += greyscale[int(sum(rgb) * choiceFactor)]
                string += '\n'
            
            # really not sure what this next bit does

            if isinstance(string, bytes):
                string = string.decode('utf8')
            strings.append(string)
            img.seek(img.tell() + 1)
    except EOFError:
        pass

    with open('template.html') as tpl_f:
        template = Template(tpl_f.read())
        html = template.render(strings=strings)
    with open(outputFile, 'w') as out_f:
        if not isinstance('html', str):
            html = html.encode('utf8')
        out_f.write(html)


def main():
    # Parse command line input
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='GIF input file')
    parser.add_argument('-m', '--maxLen', help='Maximum width of the output GIF')
    parser.add_argument('-c', '--colour', action='store_true', default=False, help='Produce ASCII GIF with colour')

    parser.add_argument('-t', '--text', type=str, help='Character to produce coloured gif with')

    args = parser.parse_args()

    if not args.maxLen:
        args.maxLen = 80

    if not args.text:
        args.text = "&#9607;"
    
    
    gifToText(
        args.filename,
        args.maxLen,
        "output" + args.filename[:-4] + ".html",
        args.colour,
        args.text
    )

if __name__ == '__main__':
    main()
