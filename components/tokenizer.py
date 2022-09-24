import re


class Tokenizer:
    """
    class to help tokenize text into
    sentences or words.
    """

    alphabets = "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"

    @classmethod
    def tokenizeToSentences(cls, text: str):
        text = " " + text + "  "
        text = text.replace("\n", " ")
        text = text.replace("’", "")
        # ^^^ this is a brute force method to get rid of the apostrophes to help with apostrophe searches.
        # it is not a good method.
        text = re.sub(cls.prefixes, "\\1<prd>", text)
        text = re.sub(cls.websites, "<prd>\\1", text)
        if "Ph.D" in text:
            text = text.replace("Ph.D.", "Ph<prd>D<prd>")
        text = re.sub("\s" + cls.alphabets + "[.] ", " \\1<prd> ", text)
        text = re.sub(cls.acronyms + " " + cls.starters, "\\1<stop> \\2", text)
        text = re.sub(
            cls.alphabets + "[.]" + cls.alphabets + "[.]" + cls.alphabets + "[.]",
            "\\1<prd>\\2<prd>\\3<prd>",
            text,
        )
        text = re.sub(
            cls.alphabets + "[.]" + cls.alphabets + "[.]",
            "\\1<prd>\\2<prd>",
            text,
        )
        text = re.sub(
            " " + cls.suffixes + "[.] " + cls.starters,
            " \\1<stop> \\2",
            text,
        )
        text = re.sub(" " + cls.suffixes + "[.]", " \\1<prd>", text)
        text = re.sub(" " + cls.alphabets + "[.]", " \\1<prd>", text)
        if "”" in text:
            text = text.replace(".”", "”.")
        if '"' in text:
            text = text.replace('."', '".')
        if "!" in text:
            text = text.replace('!"', '"!')
        if "?" in text:
            text = text.replace('?"', '"?')
        text = text.replace(".", ".<stop>")
        text = text.replace("?", "?<stop>")
        text = text.replace("!", "!<stop>")
        text = text.replace("<prd>", ".")
        sentences = text.split("<stop>")
        sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]

        return sentences

    @classmethod
    def TokenizeToWords(cls, text: list[str]):
        if isinstance(text, str):
            text = [str]
        words = []
        for sentence in text:
            try:
                words += sentence.split(" ")
            except ValueError:
                pass

        return words
