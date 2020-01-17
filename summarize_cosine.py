import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
# nltk.download('punkt') # one time execution
import re
import os
import fitz
import networkx as nx
import statistics
# ### Using extractive summarization
# Steps: Input article → split into sentences → remove stop words → build a similarity matrix → generate rank based on matrix → pick top N sentences for summary.

# ## Step 1: Load article  
os.chdir('C:\\esg')
# good format
jpm = fitz.open('jpm.pdf')

# # JP Morgan and GoldManSachs documents are base, focus on former for the pilot
pageJpm = jpm.loadPage(8)
# In the textJpm object we do not remove anything e.g. numbers, punctuations, special characters
# from this raw text, since we will use this text to create summaries and weighted word frequencies 
textJpm = pageJpm.getText("text") 

# Split Text into Sentences
sentencesJpmText = sent_tokenize(textJpm)

# ## Download and extract GloVe Word Embeddings
word_embeddings = {}
f = open('glove.6B.100d.txt', encoding='utf-8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
f.close()

len(word_embeddings)

# ## Text Preprocessing

# Remove roman numerals, kept numeral) as the pattern, for generalization
processedJpm = re.sub(r'[x|ix|iv|v?i{0,3}]+\)', ' ', textJpm) 
# Make everything lowercase
processedJpm = processedJpm.lower()
# Make sentences now
processedSentences = sent_tokenize(processedJpm)

# Remove stop words from the sentences
stop_words = stopwords.words('english')
relevantWordsPerSentenceJpm = []
for sent in processedSentences:
    wordInSentence = ' '.join([word for word in nltk.word_tokenize(sent) if word not in stop_words])   
    relevantWordsPerSentenceJpm.append(wordInSentence)

# ## Vector Representation of Sentences
sentence_vectors = []
for sen in relevantWordsPerSentenceJpm:
    if len(sen) != 0:        
        # summing happens per element 
        # all elements are in rows 100r, 0 col
        v = sum([word_embeddings.get(w, np.zeros((100,))) for w in sen.split()])/(len(sen.split()))
    else:
        v = np.zeros((100,))
    sentence_vectors.append(v)

# ## Similarity Matrix Preparation  
from sklearn.metrics.pairwise import cosine_similarity
# cosine_similarity = 1 - cosine_distance

similarity_matrix = np.zeros((len(sentencesJpmText), len(sentencesJpmText)))

for i in range(len(sentencesJpmText)):
  for j in range(len(sentencesJpmText)):
    if i != j:
        # cosine similarity returns a (1,1) numpy array, by doing [0,0] the element inside is returned
      similarity_matrix[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]

# ## Applying PageRank Algorithm
nx_graph = nx.from_numpy_array(similarity_matrix)
scores = nx.pagerank(nx_graph)

# ## Summary Extraction
ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentencesJpmText)), reverse=True)

# This extracts top 10 sentences as the summary
summaryTop10 = ''
for i in range(5):
    item = str(i) + ' ' + ranked_sentences[i][1] + '\n'
    summaryTop10 += item
    # summaryTop10 = summaryTop10.join(str(i) + ranked_sentences[i][1])
  
  print(i, ranked_sentences[i][1])

# but is better to extract 4 top dissimilar sentences as summary
print(1, ranked_sentences[0][1], 2, ranked_sentences[5][1], 3, ranked_sentences[10][1], 4, ranked_sentences[15][1])

ranks = []
for i in range(22):    
#   print(ranked_sentences[i][0])
    ranks.append(ranked_sentences[i][0])

avg = statistics.mean(ranks)
max(ranks) - min(ranks)
next(i for i, x in enumerate(ranks) if x <= avg)


# TRY
x = [np.asarray([0.1, 0.2, 0.3], dtype=np.float32), np.asarray([0.3, 0.4, 0.5], dtype=np.float32), np.asarray([0.3, 0.4, 0.5], dtype=np.float32)]

sentence_vectors[0].shape
a = np.asarray([0.3, 0.4, 0.5, 0.3, 0.4, 0.5])
cosine_similarity(x[0].reshape(1,3), x[1].reshape(1,3))[0,0]
sum(x)


np.arange(6).reshape(2,3).shape
x[0].shape

len(sentence_vectors[0])
word_embeddings.get('water').shape

# Keeps only text, hence any special characters are removed
processedJpm = re.sub('[^a-zA-Z]', ' ', processedJpm)
# Remove extra spaces and newline,
# in the raw text \n is kept, since the terminal recognizes \n and prints out nicely
processedJpm = re.sub(r'\s+', ' ', processedJpm)
# Remove the stopwords 
# make alphabets lowercase
clean_sentences = [s.lower() for s in clean_sentences]

with open('summary_glove_1234.txt', 'w') as f:
    # print(1, ranked_sentences[0][1], 2, ranked_sentences[5][1], 3, ranked_sentences[10][1], 4, ranked_sentences[15][1], file=f)
    print(summaryTop10, file=f)