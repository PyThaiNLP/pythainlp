#text='hello everyone i am subarna lamsal from nepal'
#num=int(input("Enter the number of n_grams required"))
def n_grams(text,ngram_num,i=0):
    while (len(text[i:i+ngram_num])==ngram_num):
        print(text[i:i+ngram_num])
        i=i+1

#n_grams(text.split(),num)

#PARAMETERS
# text---> the given text
# ngram_num ---> the no.of n_grams required 
# for example: 1 for unigram, 2 for bigram, 3 for trigram and so on.. 