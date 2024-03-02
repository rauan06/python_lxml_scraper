import scrapetube

from collections import Counter
import matplotlib.pyplot as plt

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.reduction  import ReductionSummarizer  as summarize
from sumy.nlp.stemmers import Stemmer

liked_videos = scrapetube.get_playlist('PLEa8hAzmCr2qlGcwiUAn52S0kgvZyenqA')

LANGUAGE = "english"
SENTENCES_COUNT = 10

summaries = ''
for videos in liked_videos:
    parser = PlaintextParser.from_string(videos['title']['accessibility']['accessibilityData']['label'], Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summary = summarize(stemmer)
    for sentence in summary(parser.document, SENTENCES_COUNT):
        summaries += str(sentence)

number = Counter()
word = ''
for i in range(len(summaries)):
    if summaries[i] == ' ':
        number[word] += 1
        word = ''
    else:
        word += summaries[i]

number = sorted(number.items(), key=lambda x: x[1], reverse=True)

plt.bar([y[0] for y in number], [x[0] for x in number])
plt.savefig('lol.png')
plt.show()
# parser = PlaintextParser.from_string(summaries, Tokenizer(LANGUAGE))
# stemmer = Stemmer(LANGUAGE)
# summary = summarize(stemmer)

# for sentence in summary(parser.document, 1):
#     print(sentence)