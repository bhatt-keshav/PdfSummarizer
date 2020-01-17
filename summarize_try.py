import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# import PyPDF2
# pdfFileObj = open('C:/esg/jpm.pdf', 'rb')
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# nrPgs = pdfReader.numPages

# for pg in range(nrPgs):
#     print(pg)

# pageObj = pdfReader.getPage(31)
# pageObj.extractText()

# import textract
# text = textract.process("C:/esg/jpm.pdf", method='pdfminer')

# from tika import parser

# raw = parser.from_file('sample.pdf')
# print(raw['content'])

# # does not work
# import pdftotext

# # Load your PDF
# with open("lorem_ipsum.pdf", "rb") as f:
#     pdf = pdftotext.PDF(f)

# # working
# from tika import parser

# raw = parser.from_file("C:/esg/jpm.pdf")
# raw = str(raw)

# safe_text = raw.encode('utf-8', errors='ignore')

# safe_text = str(safe_text).replace("\n", "").replace("\\", "")
# print('--- safe text ---' )
# print( safe_text )
# good
import fitz
doc = fitz.open("C:/esg/jpm.pdf")
doc.pageCount # 0 -31, displays 32
doc.metadata
doc.getToC()
page = doc.loadPage(1)
#page = doc[0] #shortcut
text = page.getText("text")
dic = page.getText("dict") #quite useful, as in a native py env
xml = page.getText("xml") #not so useful


