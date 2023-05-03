import pke
import spacy
from aiochan import Chan
from config import keywords_count


async def get_keywords(channel: Chan, text):
    extractor = pke.unsupervised.TopicRank()
    extractor.load_document(
        input=text,
        language='ru'
    )
    extractor.candidate_selection()
    extractor.candidate_weighting()
    keyphrases = extractor.get_n_best(n=keywords_count)
    channel.put(keyphrases)


def get_similar(word1, word2):
    # ставлю порог сходства 0.4 если сходство больше то попадает в категорию
    nlp = spacy.load('ru_core_news_sm')
    words = f"{word1} {word2}"
    tokens = nlp(words)
    token1, token2 = tokens[0], tokens[1]
    print("Similarity:", token1.similarity(token2))
