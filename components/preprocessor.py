import json
from emoji import UNICODE_EMOJI
from .tokenizer import Tokenizer


def getProcessedData(data: str) -> list[str]:
    """
    processed data in the database is stored in
    the form of sentence. This function helps
    covert it into list of words.
    """
    if isinstance(data, list):
        return data

    return data.split(" ")


class PreProcessText:
    """
    processes raw scraped data and converts
    it into the required format.
    """

    def __init__(self, language="en"):
        self.language = language
        stopwords_file = open(r"components\json_files\stopwords.json")
        punctuations_file = open(r"components\json_files\punctuations.json")
        self.stopwords = json.load(stopwords_file)[language]
        self.punctuations = json.load(punctuations_file)[language]

    def _removeStopwords(self, sentence: str):
        sentence = sentence.lower()
        for word in self.stopwords:
            pattern = f" {word} "
            if pattern in sentence:
                sentence = sentence.replace(pattern, " ")
            if sentence == "":
                return None

        return sentence

    def removeStopwords(self, sentences: list[str]):
        output = []
        for sentence in sentences:
            temp = self._removeStopwords(sentence)
            if temp:
                output.append(temp)

        return output

    def _removePunctuations(self, sentence: str):
        sentence = sentence.lower()
        for punctuation in self.punctuations:
            sentence = sentence.replace(punctuation, "")

        return sentence

    def removePunctutaions(self, sentences: list[str]):
        if isinstance(sentences, str):
            sentences = [sentences]
        output = []
        for sentence in sentences:
            output.append(self._removePunctuations(sentence))

        return output

    # def removeEmojis(self, sentences: list[str]):
    #     if isinstance(sentences, str):
    #         sentences = [sentences]
    #     output = []
    #     for sentence in sentences:
    #         ...

    def process(self, text):

        text = text.lower()
        sentences = self.removePunctutaions(text)
        sentences = self.removeStopwords(sentences)
        words = Tokenizer.TokenizeToWords(sentences)

        return words
