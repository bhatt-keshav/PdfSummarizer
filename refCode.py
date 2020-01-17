file = open('medium.txt', "r")
filedata = file.readlines() 
article = filedata[0].split(". ") #splits on .
sentences = []

# for sentence in article:
#     print(sentence)
#     sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" ")) #replace everything not alphabetic with space
#     # sentences.pop() 
# return sentences

def read_article(file_name):
    file = open(file_name, "r")
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []   
    for sentence in article:
        print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
        sentences.pop() 
    return sentences

a = read_article('medium.txt')    