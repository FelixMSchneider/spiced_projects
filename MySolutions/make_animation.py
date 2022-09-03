import imageio.v2 as io
import glob

outfolder="./figs/"

imagefiles=sorted(glob.glob(outfolder+"????.0_gap*.png"))

images=[]
for imfile in imagefiles:
    images.append(io.imread(imfile))

io.mimsave(outfolder+"output.gif", images, fps=20)






