"""
Module to get the frequencies of the audit parameters
"""
import re
import json
import string
import nltk
from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer
from nltk.data import find
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import gensim
# nltk.download()

model = gensim.models.Word2Vec(brown.sents())
WORD_TWO_VEC_SAMPLE = str(find('models/word2vec_sample/pruned.word2vec.txt'))
model = gensim.models.KeyedVectors.load_word2vec_format(WORD_TWO_VEC_SAMPLE, binary=False)

FILE_PATH_SCRAPPED_DATA = r"C:\\Users\\ammittal\\Desktop\\fer.txt"
FILE_PATH_STOPWORDS = r"C:\\Users\\ammittal\\Desktop\\stop_words.json"
FILE_PATH_LOCATION=r"C:\\Users\\ammittal\\Desktop\\keywords_comp.json"
ENCODING_EXTNS = 'utf-8'

pos_dict = {"JJ": "a", "JJR": "a", "JJS": "a",
            "NN": "n", "NNS": "n", "NNP": "n",
            "NNPS": "n", "PRP": "n", "PRP$": "n",
            "WP": "n", "WP$": 'n',"RB": "v",
            "RBR": "v", "RBS": "v", "VB": "v",
            "VBD": "v", "VBG": "v",
            "VBN": "v", "VBP": "v", "VBZ": "v",
            "WRB": 'n' }

with open(FILE_PATH_SCRAPPED_DATA,encoding=ENCODING_EXTNS) as file:
    text_data=file.read()
file.close()

def remove_emoji(string_text):
    """
    Removes the emojis if present in the text
    """
    emoji_pattern = re.compile("["
                           u"U0001F600-U0001F64F"
                           u"U0001F300-U0001F5FF"
                           u"U0001F680-U0001F6FF"
                           u"U0001F1E0-U0001F1FF"
                           u"U00002702-U000027B0"
                           u"U000024C2-U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string_text)

def decontracted(phrase):
    """
    Decontracting the text
    """
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

def tfidfvect(lemmatizer_list):
    """
    Converting the words to vectors using tfidf

    """
    data_frame = pd.DataFrame({"list_of_words": lemmatizer_list})
    data_frame['list_of_words']=data_frame['list_of_words'].str.cat(sep=',')
    data_frame = data_frame.drop(data_frame.index.to_list()[1:] ,axis = 0 )
    tfidf = TfidfVectorizer()
    vectors_list = tfidf.fit_transform(data_frame["list_of_words"].values)
    df1 = pd.DataFrame(vectors_list.toarray(),columns = tfidf.get_feature_names_out())
    return df1

def extracted_keywords_from_audit_parameters(posmotag):
    """
    Extract the list of keywords from audit parameters
    """
    keywords=np.unique(np.array(posmotag).flatten())
    string_keywords=' '.join(keywords)
    return np.unique(preprocessing(string_keywords,pos_dict))


def preprocessing(text,position_dict):
    """
    Removing and cleaning of unwanted data
    """
    lower_text=text.lower()
    lower_text=lower_text.replace("\u200d"," ")
    puncts_to_remove=string.punctuation
    punct_list=[]
    for i in puncts_to_remove:
        punct_list.append(i)
    punct_list.append("'")
    punct_list.append("\n")
    punct_removed=''.join([i for i in lower_text if i not in punct_list])
    digits_removed=''.join([i for i in punct_removed if not i.isdigit()])
    space_removed=" ".join(digits_removed.split())
    replace_rep=re.sub(r'(!|.)1+', '', space_removed)
    remove_emojis=remove_emoji(replace_rep)
    decontracted_text=decontracted(remove_emojis)
    tokenized_words=decontracted_text.split(" ")
    with open(FILE_PATH_STOPWORDS,encoding=ENCODING_EXTNS) as stop_words_file:
        data=json.load(stop_words_file)
    stop_words_file.close()
    stop_words=data['en']
    filtered_words = [w for w in tokenized_words if not w.lower() in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmatized_words=[lemmatizer.lemmatize(i) for i in filtered_words]
    lemmatized_words_final=[]
    for i in lemmatized_words:
        try:
            lemmatized_words_final.append(lemmatizer.lemmatize(i,
            pos=position_dict[nltk.pos_tag([i])[0][1]]))
        except KeyError:
            lemmatized_words_final.append(i)
    return lemmatized_words_final
lemmatized_words_list=preprocessing(text_data,pos_dict)
print("Lemmatized Words:-",lemmatized_words_list)

def find_density(lemmatized_words):
    """
    Find the densities/weightage of extracted keywords
    """
    density_df=tfidfvect(lemmatized_words).T
    return density_df

def find_similar_keywords(posmotag,threshold,unmapped_list):
    """
    Finds similarity score and filter the
    similar words to add them to the final frequencies
    """
    extracted_keywords=extracted_keywords_from_audit_parameters(posmotag)
    similiar_words={}
    for i in extracted_keywords:
        similiar_words[i]=[]
    count=0
    for i in extracted_keywords:
        for j in lemmatized_words_list:
            try:
                if model.similarity(i,j)>threshold:
                    if j not in similiar_words[i]:
                        similiar_words[i].append(j)
                        count=count+1
                else:
                    unmapped_list.append(j)
            except KeyError:
                pass
    # frequency=count/len(similiar_words)
    frequency=count
    # return similiar_words,frequency
    return frequency,unmapped_list

def audit_frequency(file_location):
    """
    Calculates the average frquencies
    for corresponding audit parameters
    """
    threshold=float(input("Please enter the threshold:-"))
    with open(file_location,encoding=ENCODING_EXTNS) as file_path:
        data_keywords_dict=json.load(file_path)
    file_path.close()
    uniques_keys=list(data_keywords_dict.keys())
    dict_frequency={}
    unmapped_dict={}
    for i in uniques_keys:
        unmapped_list=[]
        dict_frequency[i],unmapped_list2=find_similar_keywords(data_keywords_dict[i],threshold,unmapped_list)
        unmapped_dict[i]=unmapped_list2
    return dict_frequency,unmapped_dict

dict_frequency,unmapped_dict=audit_frequency(FILE_PATH_LOCATION)
print("DICT FREQUENCY:-",dict_frequency)
keys=list(unmapped_dict.keys())
for i in keys:
    print(i)
    print(unmapped_dict[i])
    print()
