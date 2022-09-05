import imageio.v2 as io
import glob

drop_India_China = False

if drop_India_China:
    outfolder="./figs_drop_China_India/"
else:
    outfolder="./figs/"


imagefiles=sorted(glob.glob(outfolder+"????_gap*.png"))

images=[]
for imfile in imagefiles:
    images.append(io.imread(imfile))

io.mimsave(outfolder+"output.gif", images, fps=20)






