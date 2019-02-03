import sys, random, argparse
import numpy as np
import math

from PIL import Image

#70 levels of gray
greyscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^ `'. "
greyscale2 = '@%#*+=-:. '

def getAverageL(image):
    #return average grayscale value of an image
    im = np.array(image)#get as numpy array
    w,h = im.shape
    return np.average(im.reshape(w*h))

#import pdb; pdb.set_trace()
def convertImageToAscii(fileName, cols, scale, moreLevels):
    #return m*n list of images given image and dimensions (in rows and columns)
    # declare globals
    global gscale1, gscale2
    # open image and convert to grayscale
    image = Image.open(fileName).convert('L') # store the image dimensions
    W, H = image.size[0], image.size[1]
    print("input image dims: %d x %d" % (W, H))
    w = W/cols # compute tile width
    # compute tile height based on the aspect ratio and scale of the font
    h = w/scale
    # compute number of rows to use in the final grid
    rows = int(H/h)

    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))

    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    # an ASCII image is a list of character strings
    aimg = []
    # generate the list of tile dimensions
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)

        # correct the last tile
        if j == rows-1:
            y2 = H
        # append an empty string
        aimg.append("")
        for i in range(cols):
            # crop the image to fit the tile
            x1 = int(i*w)
            x2 = int((i+1)*w)
            # correct the last tile
            if i == cols-1:
                x2 = W
            # crop the image to extract the tile into another Image object
            img = image.crop((x1, y1, x2, y2))
            # get the average luminance
            avg = int(getAverageL(img))
            # look up the ASCII character for grayscale value (avg)
            if moreLevels:
                gsval = greyscale1[int((avg*69)/255)]
            else:
                gsval = greyscale2[int((avg*9)/255)]
                # append the ASCII character to the string
            aimg[j] += gsval
    # return text image
    return aimg

def main():
    #create parser
    desc = "This program converts image into ASCII art."
    parser = argparse.ArgumentParser(description = desc)
    #add expected arguments
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--morelevels', dest='moreLevels', action='store_true')

    args = parser.parse_args()#parse arguments
    imgFile = args.imgFile
    outFile = 'out.txt'
    if args.outFile:
        outFile = args.outFile
    # set scale default as 0.43, which suits a courier font
    scale = 0.43
    if args.scale:
        scale = float(args.scale)
    #set cols
    cols = 80
    if args.cols:
        cols = int(args.cols)
    print('Taking your image and making it nUmBeRs mY DooD')
    aimg = convertImageToAscii(imgFile, cols, scale, args.moreLevels)

    f = open(outFile, 'w')
    for row in aimg:
        f.write(row + '\n')
    f.close()#clean up
    print("ASCII art written to %s" % outFile)

#call main
if __name__ == '__main__':
    main()
