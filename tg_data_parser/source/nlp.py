import pke
from aiochan import Chan
from config import keywords_count


async def get_keywords(channel:Chan, text):
    extractor = pke.unsupervised.TopicRank()
    extractor.load_document(
        input=text,
        language='ru'
    )
    extractor.candidate_selection()
    extractor.candidate_weighting()
    keyphrases = extractor.get_n_best(n=keywords_count)
    channel.put(keyphrases)