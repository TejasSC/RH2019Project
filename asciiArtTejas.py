import sys, random, argparse
import numpy as np
import math

from PIL import Image
# inspired by GeeksForGeeks' implementation

#70 shades of gray
shortScale = '@%#*+=-:. '
longScale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^ `'. "

def calcAvgGrey(image):
    #return average grayscale value of an image
    im = np.array(image)#get as numpy array
    width, height = im.shape
    return np.average(im.reshape(width * height))

#import pdb; pdb.set_trace()
def transformPicture(fileName, cols, scale, moreLevels):
    #return m*n list of images given image and dimensions (in rows and columns)
    # declare globals
    global gscale1, gscale2
    # open image and convert to grayscale
    picture = Image.open(fileName).convert('L') # store the image dimensions
    width, height = picture.size[0], picture.size[1]
    print("input image dims: %d x %d" % (width, height))
    tile_width = width/cols # tile width
    # compute tile height based on the aspect ratio and scale of the font
    tile_height = tile_width/scale
    # compute number of rows to use in the final grid
    rows = int(height/tile_height)

    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (tile_width, tile_height))

    if cols > width or rows > height:
        print("Image too small for specified cols!")
        exit(0)

    # an ASCII image is a list of character strings
    ascii_image = []
    # generate the list of tile dimensions
    for j in range(rows):
        yA = int(j*tile_height)
        yB = int((j+1)*tile_height)

        # correct the last tile
        if j == rows-1:
            yB = height
        # append an empty string
        ascii_image.append("")
        for i in range(cols):
            # crop the image to fit the tile
            xA = int(i*tile_width)
            xB = int((i+1)*tile_width)
            # correct the last tile
            if i == cols-1:
                xB = height
            # crop the image to extract the tile into another Image object
            img = picture.crop((xA, yA, xB, yB))
            # get the average luminance
            avg_luminance = int(calcAvgGrey(img))
            # look up the ASCII character for grayscale value (avg)
            if moreLevels:
                grey_shade = longScale[int((avg_luminance*69)/255)]
            else:
                grey_shade = shortScale[int((avg_luminance*9)/255)]
                # append the ASCII character to the string
            ascii_image[j] += grey_shade
    # return text image
    return ascii_image

def main():
    #create parser
    desc = "This program transforms an image into an ASCII artwork."
    parser = argparse.ArgumentParser(description = desc)
    #add expected arguments
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--morelevels', dest='moreLevels', action='store_true')

    args = parser.parse_args()#parse args
    imgFile = args.imgFile
    outFile = 'out.txt'
    if args.outFile:
        outFile = args.outFile
    scale = 0.43 #courier font
    if args.scale:
        scale = float(args.scale)
    #set cols
    cols = 80
    if args.cols:
        cols = int(args.cols)
    print('Taking your image and making it nUmBeRs mY DooD')
    ascii_image = transformPicture(imgFile, cols, scale, args.moreLevels)

    #method to write new image file to the output file
    f = open(outFile, 'w')
    for row in ascii_image:
        f.write(row + '\n')
    f.close()
    #confirmation that the file was written successfully
    print("ASCII art written to %s" % outFile)

#call main
if __name__ == '__main__':
    main()
