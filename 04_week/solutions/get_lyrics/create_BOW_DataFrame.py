import glob

#txt_folder="songs_txt_Queen/"
txt_folder="songs_txt_The-Rolling-Stones/"


# here I remove some duplicates
# first I run  "bash replace_sonderzeichen.sh" in oder to replace special characters in the filenames


def get_uniq_filelist(txt_folder="songs_txt_The-Rolling-Stones/"):
 
    unified_songlist=[]

    songlist=sorted(glob.glob(txt_folder+"*.txt"))

    songlist_part=[s.split("_")[2].split(".")[0] for s in songlist]

    uniq_soglist_part=sorted(list(set(songlist_part)))

    for s in uniq_soglist_part:
        l=glob.glob("songs_txt_"+s+"*")[0]
        unified_songlist.append(l)
    return unified_songlist


def get_corpus(songlist):
    CORPUS=[]

    for i,sfile in enumerate(songlist):
        with open(sfile, "r") as sf:
            try:
                if i%100==0: 
                    print("read song", i,"of ", len(songlist))
                A=sf.read()
                CORPUS.append(A)
            except:
                print("cannot read file: ", sfile)
                continue

    return CORPUS

def combine_corpus_and_get_labels(C1,C2, prefix1="stones", prefix2="queen"):
    CORPUS = C1 + C2
    l1,l2 = len(C1), len(C2)
    LABELS = [f"{prefix1}_{i}" for i in range(l1)] + [f"{prefix2}_{i}" for i in range(l2)] 
    return CORPUS,LABELS


songlist_stones = get_uniq_filelist()
songlist_queen  = get_uniq_filelist("songs_txt_Queen/")

CORPUS_STONES=get_corpus(songlist_stones)
CORPUS_QUEEN=get_corpus(songlist_queen)

CORPUS,LABELS = combine_corpus_and_get_labels(CORPUS_STONES, CORPUS_QUEEN,"stones", "queen")



########## now the fun beguns #####

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text
import pandas as pd




english_stop_words = text.ENGLISH_STOP_WORDS

count_vectorizer = CountVectorizer(
    #
    ###################################################################
    # convert all characters to lowercase before tokenizing
    #
    lowercase = True, 
    #
    ###################################################################
    # choose words to create features
    #
    analyzer = 'word',
    #
    ###################################################################
    # use built-in stop word list for English (default=None)
    #
    stop_words = english_stop_words,
    #
    ###################################################################
    # select tokens of 2 or more word characters (punctuation ignored) 
    #
    token_pattern = r"(?u)\b\w\w+\b",
    #
    ###################################################################
    # consider only unigrams of tokens
    #
    ngram_range = (1, 1)
    #
    ###################################################################  
)
vec = count_vectorizer.fit_transform(CORPUS)


count_matrix_skl = pd.DataFrame(
    vec.todense(), 
    columns=count_vectorizer.get_feature_names(), 
    index=LABELS
)

from sklearn.feature_extraction.text import TfidfTransformer
tf = TfidfTransformer(use_idf=False)

vec2 = tf.fit_transform(vec)
feature_matrix = pd.DataFrame(
    vec2.todense(), 
    columns=count_vectorizer.get_feature_names(), 
    index=LABELS
)



print(feature_matrix)

import pickle

pickle.dump(feature_matrix, open("FeatureMatrix.pickle","wb"))


FM=feature_matrix
FM["LABEL"]=FM.index
FM["LABEL"].apply(lambda x: "stones" in x)*1
FM["STONES"]=FM["LABEL"].apply(lambda x: "stones" in x)*1
FM=FM.drop("LABEL", axis=1)

from sklearn.linear_model import LogisticRegression


from sklearn.model_selection import train_test_split

FM_train, FM_test=train_test_split(FM)


Xtrain=FM_train.drop("STONES", axis=1)
Ytrain=FM_train["STONES"]

model = LogisticRegression()
model.fit(Xtrain, Ytrain)

Xtest=FM_test.drop("STONES", axis=1)
Ytest=FM_test["STONES"]
print(model.score(Xtrain,Ytrain))
print(model.score(Xtest,Ytest))



