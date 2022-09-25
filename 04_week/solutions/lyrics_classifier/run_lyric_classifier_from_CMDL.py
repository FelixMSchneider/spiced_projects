import argparse
import sys  

# initialize the argument parser
parser = argparse.ArgumentParser(description='lyrics classifier')

parser.add_argument('-f', '--file', help='path to the song lyrics to predict')
parser.add_argument('-w', '--write', help='song line to predict')
args = parser.parse_args()

# get the pickled model (trained model)

if args.file or args.write:
    import pickle
    from train_lyric_classiefier_pipeline import preprocessing
    pipeline=pickle.load(open("/home/felix/spiced/04_week/scripts/classifie_lyrics/Queen_Stones_Classifier_pipeline.pickle", "rb"))

# get the lyrics from a txt file (option `-f`)
if args.file:
        with open(args.file, 'r') as lyrics_file:
                prediction =       pipeline.predict([lyrics_file.read()])
                proba      = pipeline.predict_proba([lyrics_file.read()])
# get the lyrics from the terminal (option `-w`)
elif args.write:
        print(args.write)
        prediction =       pipeline.predict([args.write])
        proba      = pipeline.predict_proba([args.write])

else:
    parser.print_help(sys.stderr)
    sys.exit(1)


if prediction[0] == "queen": predstr= "Queen"
if prediction[0] == "stones": predstr= "the Rolling Stones"



print("the lyrics are probably belong to : ", predstr)
print("")
print("    the probabilities are: ")
print("    ",round(proba[0][0]*100,1), "% : Queen" )
print("    ",round(proba[0][1]*100,1), "% : the Rolling Stones" )



