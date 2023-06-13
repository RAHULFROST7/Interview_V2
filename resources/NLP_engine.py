import spacy
import nltk
import gensim
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import numpy as np
from math import ceil, floor
import warnings
from typing import NewType

nlp = spacy.load('en_core_web_lg')
actualAnswer = NewType('actualAnswer', list)
givenAnswer = NewType('givenAnswer', str)

class Nlp_eng_SimCalc:
    def __init__(self):
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        warnings.filterwarnings("ignore", category=UserWarning)

    @staticmethod
    def preprocess_sentence(text: str):
        stop_words = set(stopwords.words("english"))
        words = text.split()
        words = [w for w in words if w not in stop_words]
        return " ".join(words)

    def getScore(self, sentence1: actualAnswer, sentence2: givenAnswer):
        processed_sentence2 = self.preprocess_sentence(sentence2.lower())
        score_list = []
        tokens2 = set(nltk.word_tokenize(sentence2.lower()))

        vectorizer = TfidfVectorizer()
        sentence1_tfidf = vectorizer.fit_transform([self.preprocess_sentence(s.lower()) for s in sentence1])
        sentence2_tfidf = vectorizer.transform([processed_sentence2])

        for i in range(0, len(sentence1)):
            final_score = 0

            doc1 = nlp(sentence1[i])
            doc2 = nlp(processed_sentence2)
            spacy_similarity_score = doc1.similarity(doc2)

            cosine_similarity_score = cosine_similarity(sentence1_tfidf[i], sentence2_tfidf)[0][0]

            try:
                tokens1 = word_tokenize(sentence1[i])
                tokens2 = word_tokenize(processed_sentence2)
                model = gensim.models.Word2Vec([tokens1, tokens2], min_count=2)
                word_vectors = {word: model.wv[word] for word in model.wv.index_to_key}
                vector1 = np.mean([word_vectors[word] for word in tokens1 if word in word_vectors], axis=0)
                vector2 = np.mean([word_vectors[word] for word in tokens2 if word in word_vectors], axis=0)
                sim_score = cosine_similarity([vector1], [vector2])[0][0]
            except:
                sim_score = 0

            tokens1 = set(nltk.word_tokenize(sentence1[i].lower()))
            jaccard_similarity_score = len(tokens1.intersection(tokens2)) / len(tokens1.union(tokens2))

            weighted_score = (0.5 * spacy_similarity_score) + (0.3 * jaccard_similarity_score) + (
                    0.2 * cosine_similarity_score)

            average_similarity_score = spacy_similarity_score * .15 + (
                    jaccard_similarity_score + cosine_similarity_score + (weighted_score + sim_score) * .15) / 2
            final_score = ceil(average_similarity_score * 100)
            score_list.append(final_score)

        result = max(score_list)
        return (
            np.random.randint(8, 30)
            if 10 < result < 50
            else (
                np.random.randint(95, 100)
                if result > 100
                else (
                    floor(result * 1.15)
                    if 60 < result < 75
                    else (
                        floor(result * 0.6)
                        if 50 < result < 70
                        else (0 if result < 0 else result)
                    )
                )
            )
        )
