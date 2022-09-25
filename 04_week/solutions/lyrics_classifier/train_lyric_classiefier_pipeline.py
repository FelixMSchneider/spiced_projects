#nltk.download('omw-1.4')
#nltk.download("wordnet")
#nltk.download('stopwords')
# only done once! we have to download the WordNet database locally
import glob
import pylab as plt

# here I remove some duplicates
# first I run  "bash replace_sonderzeichen.sh" in oder to replace special characters in the filenames

def metrics(yt,yp):
    """
    This function returns a dataframe with the model evaluation metrics,
    and a heatmap of the confusion matrix
    """
    import seaborn as sns

    from sklearn.metrics import accuracy_score, precision_score, recall_score, balanced_accuracy_score
    from sklearn.metrics import confusion_matrix

    sns.heatmap(data=confusion_matrix(yt,yp),cmap='crest',annot=True)

    accuracy = round(accuracy_score(yt,yp),6)
    precision = round(precision_score(yt,yp),6)
    recall = round(recall_score(yt,yp),6)
    balanced_accuracy = round(balanced_accuracy_score(yt, yp),6)

    df_metric = pd.DataFrame({'score': [accuracy,precision,recall,balanced_accuracy]},
                            index = ['accuracy','precision','recall','balanced_accuracy'])
    return df_metric



def get_uniq_filelist(txt_folder="songs_txt_The-Rolling-Stones/"):

    unified_songlist=[]

    songlist=sorted(glob.glob(txt_folder+"*.txt"))

    songlist_part=[s.split("_")[2].split(".")[0] for s in songlist]

    uniq_soglist_part=sorted(list(set(songlist_part)))

    for s in uniq_soglist_part:
        l=glob.glob("songs_txt_"+s+"*")[0]
        unified_songlist.append(l)
    return unified_songlist


def get_corpus(songlist, verbose=False):
    CORPUS=[]

    for i,sfile in enumerate(songlist):
        with open(sfile, "r") as sf:
            try:
                if i%100==0:
                    if verbose: print("read song", i,"of ", len(songlist))
                A=sf.read()
                CORPUS.append(A)
            except:
                print("cannot read file: ", sfile)
                continue

    return CORPUS

def combine_corpus_and_get_labels(C1,C2, prefix1="stones", prefix2="queen"):
    CORPUS = C1 + C2
    l1,l2 = len(C1), len(C2)
    LABELS = [f"{prefix1}" for i in range(l1)] + [f"{prefix2}" for i in range(l2)]
    return CORPUS,LABELS


def preprocessing(X):
    import nltk
    from nltk.tokenize import TreebankWordTokenizer
    from nltk.stem import WordNetLemmatizer 
    import pandas as pd 

    
    CORPUS=X#[0]
    CORPUS = [s.lower() for s in CORPUS]
    
    tokenizer = TreebankWordTokenizer()
    lemmatizer = WordNetLemmatizer()

    CLEAN_CORPUS = [] # this is where my clean corpus will end 

    for doc in CORPUS:
        tokens = tokenizer.tokenize(text=doc)
        clean_doc = " ".join(lemmatizer.lemmatize(token) for token in tokens)
        CLEAN_CORPUS.append(clean_doc)
    
    from nltk.corpus import stopwords
    
    #feature_matrix=pd.DataFrame(CLEAN_CORPUS) 

    return CLEAN_CORPUS

if __name__ == "__main__":    
    
    songlist_stones = get_uniq_filelist()
    songlist_queen  = get_uniq_filelist("songs_txt_Queen/")
    
    CORPUS_STONES=get_corpus(songlist_stones)
    CORPUS_STONES=CORPUS_STONES#[0:300]
    CORPUS_QUEEN=get_corpus(songlist_queen)
    
    CORPUS,LABELS = combine_corpus_and_get_labels(CORPUS_STONES, CORPUS_QUEEN,"stones", "queen")
    
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    
    import pandas as pd 
    import numpy as np
    
    #X=pd.DataFrame(CORPUS)
    X=CORPUS
    Y=np.array(LABELS)
    
    #X_train,X_test,Y_train,Y_test = train_test_split(X,Y, test_size=0.33, random_state=42)
    X_train=X
    Y_train=Y 
    
    # In[4]:
    
    
    #transformer.transform(CORPUS)
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.feature_extraction.text import TfidfVectorizer
    from nltk.corpus import stopwords
    
    STOPWORDS = stopwords.words('english')
    
    
    #create a pipeline
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import FunctionTransformer
    
    transformer = FunctionTransformer(preprocessing)
    
    pipeline=Pipeline([('preprocessing', transformer),
                       ("vectorizer", TfidfVectorizer(
                                                      lowercase = True,
                                                     stop_words = STOPWORDS,
                                                  token_pattern = r"(?u)\b\w\w\w+\b", 
                                                    ngram_range = (1, 1)) ),
                       ('classifier', MultinomialNB())])
    
    
    from sklearn.utils import class_weight
   
    s_w = class_weight.compute_sample_weight('balanced', Y_train)
    
    pipeline.fit(X_train, Y_train, classifier__sample_weight=s_w)#, vectorizer__lowercase=False)
    
    import pickle
    pickle.dump(pipeline, open("Queen_Stones_Classifier_pipeline.pickle", "wb"))
    
