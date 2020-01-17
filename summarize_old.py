import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import fitz
import networkx as nx

os.chdir('C:\\esg')
jpm = fitz.open('jpm.pdf')
alibaba = fitz.open('alibaba.pdf')
gs = fitz.open('gs.pdf')
docs = [jpm, alibaba, gs]

for d in docs:
    d.pageCount    

allText = [pg.getText("text") for pg in jpm]
# del a[-1]
a = allText[1:-1] 

# sUMMARIZE ON THIS
text = jpm[5].getText("text")

    
#TRY    
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

txt = "welcome to the jungle"
txt.split(". ")