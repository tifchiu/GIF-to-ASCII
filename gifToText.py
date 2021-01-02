from PIL import Image
from jinja2 import Template
import argparse
import operator

def gifToText(filename, maxLen, outputFile, withColour):
    try:
        maxLen = int(maxLen)
    except:
        maxLen = 80
    
    try:
        img = Image.open(filename)
    except:
        exit("file not found: {}".format(filename))
    
    width, height = img.size
    aspectRatio = float(maxLen) / max(width,height)
    width = int(aspectRatio * width)
    height = int(aspectRatio * height)

    palette = img.getpalette()
    greyscale = "MNHQ$OC?7>!:-;. "
    strings = []

    try:
        while True:
            img.putpalette(palette)
            newImg = Image.new('RGB', img.size)
            newImg.paste(img)
            newImg = newImg.resize((width, height))
            string = ''

            for h in range(height):
                for w in range(width):
                    rgb = newImg.getpixel((w,h))
                    if withColour:
                        # Using @ as a place holder. TO DO: let the user give a character they want to use
                        string += ("<span style=\"color:rgb({0}, {1}, {2});\">" + '@' + "</span>").format(rgb[0], rgb[1], rgb[2] / 255.0)
                    else:
                        string += greyscale[int(sum(rgb) / 3.0 / 256.0 * 16)]
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
    # We should just set default output file name
    #parser.add_argument('-o', help='Name of output file')
    parser.add_argument('-c', '--colour', action='store_true', default=False, help='Produce ASCII GIF with colour')

    args = parser.parse_args()

    if not args.maxLen:
        args.maxLen = 80
    
    
    gifToText(
        args.filename,
        args.maxLen,
        'out.html',
        args.colour
    )

if __name__ == '__main__':
    main()
