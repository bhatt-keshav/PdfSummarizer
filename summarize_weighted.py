import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import fitz
import re
import statistics
import math
import heapq

# ## Step 1: Load article  
os.chdir('C:\\esg')
# good format
jpm = fitz.open('jpm.pdf')
# interesting but good format
alibaba = fitz.open('alibaba.pdf')
# problematic format, good for testing
gs = fitz.open('gs.pdf')
docs = [jpm, alibaba, gs]

# Pages per document
for d in docs:
    d.pageCount    

# # JP Morgan and GoldManSachs documents are base, focus on former for the pilot
pageJpm = jpm.loadPage(8)
# In the textJpm object we do not remove anything e.g. numbers, punctuations, special characters
# from this raw text, since we will use this text to create summaries and weighted word frequencies 
textJpm = pageJpm.getText("text") 

# Instead of the text mode, the HTML mode could be used, an advantage of it is 
# that it can identify headings, but this might not always be the case
# the goldman sachs doc is such an example

# ## Step 2: Preprocessing to remove special characters and digits

# Remove roman numerals, kept numeral) as the pattern for generalization
processedJpm = re.sub(r'[x|ix|iv|v?i{0,3}]+\)', ' ', textJpm) 
# Remove extra spaces and newline,
# in the raw text \n is kept, since the terminal recognizes \n and prints out nicely
processedJpm = re.sub(r'\s+', ' ', processedJpm)
# Keeps only text, hence any special characters are removed
processedJpm = re.sub('[^a-zA-Z]', ' ', processedJpm)
# the processedJpm will be used to create weighted frequency histograms 
# these will be assigned to the raw text

# ## Step 3: Converting Text To Sentences
# the raw text is used, since the processed text doesn't contain punctuations
sentencesJpmText = sent_tokenize(textJpm)

# ## Step 4: Find Weighted Frequency of Occurrence
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(processedJpm.lower()):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

# # Find the frequency of the most occurring word
maxFreq = max(word_frequencies.values())

# # Replace the frequency by weighted/scaled frequency
# TODO: Check what is the effect with min-max scaling
word_frequencies_scaled = word_frequencies.copy()
for word in word_frequencies_scaled.keys():
    word_frequencies_scaled[word] = (word_frequencies_scaled[word]/maxFreq)              

# ## Step 5: Calculating Sentence Scores            

# Determine the nr of words/length per sentence and the mean length of the sentences
lengthPerSentence = [len(sent.split(' ')) for sent in sentencesJpmText] 
# Sentences longer than the mean length are not used to generate the summary
meanLength = math.ceil(statistics.mean(lengthPerSentence))

sentence_scores = {}
# If a word in a sentence of the text is in the word_frequencies object, 
# then add this word's score to the sentence's score
for sent in sentencesJpmText:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies_scaled.keys():            
            if len(sent.split(' ')) < meanLength:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies_scaled[word]
                else:
                    sentence_scores[sent] += word_frequencies_scaled[word]

# ## Step 6: Getting the Summary                    
# 1/3 of the top sentences with the highest scores are retrieved
nrSummarySentences = math.ceil(len(sentence_scores.keys())/3)
summary_sentences = heapq.nlargest(nrSummarySentences, sentence_scores, key=sentence_scores.get)
summary = ' '.join(summary_sentences)
print(summary)


#TRY    
# GoldmanSachs
pageGS = gs.loadPage(8)
textGS = pageGS.getText("text") 
# dictTextGS = pageGS.getText("dict") 
htmGS = pageGS.getText("html") 

try:
    iter(jpm)
    print('iteration will probably work')
except TypeError:
    print('not iterable')

gs.pageCount 
gs.metadata #not very useful as not always filled in a pdf
gs.getToC()  #not very useful as not always filled in a pdf

page = gs.loadPage(18)
#page = doc[0] #shortcut
doc.pageCount
text = page.getText("text")
allText = [pg.getText("text") for pg in jpm]
# os.system('cls')

with open('summary_weighted.txt', 'w') as f:
    print(summary, file=f)

# better to use html than dict
# dictJPM = page.getText("dict") 

# Working with HTML
# htmJpm = pageJpm.getText("html") 
# soupJpm = BeautifulSoup(htmJpm, 'html.parser')
# print(soupJpm.prettify())
# soupJpmText = soupJpm.get_text()
# # Removes all whitespace chars [\r\n\t\f\v ])
# soupJpmText = re.sub(r'\s+', ' ', soupJpmText)
# soupJpmText = soupJpmText.split("\n")
# soupJpmText = [p for p in soupJpmText.split("\n")]


doc = fitz.open()            # or a new PDF by fitz.open()
doc.insertPage(0, text=summary, fontsize=10)  # insert a new page in front of page n
doc.save("censored.pdf") 