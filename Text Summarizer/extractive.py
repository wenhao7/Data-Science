# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import bs4 as bs
import urllib.request
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

def chunk_text(article_text, chunk_size=512):
    words = article_text.split(' ')
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def remove_duplicates(text):
    sentences = re.split('(?<=[.!?]) +', text)
    vectorizer = TfidfVectorizer().fit_transform(sentences)
    similarity_matrix = cosine_similarity(vectorizer)
    similar_pairs = np.argwhere(similarity_matrix > 0.8)
    indices_to_remove = [pair[1] for pair in similar_pairs if pair[0] != pair[1]]
    unique_sentences = [sentence for i, sentence in enumerate(sentences) if i not in indices_to_remove]   
    return ' '.join(unique_sentences)

### Read Article
def read_article(url):
# Scrape Wikipedia
    #scraped_data = urllib.request.urlopen("https://en.wikipedia.org/wiki/Bear")
    scraped_data = urllib.request.urlopen(url)
    article = scraped_data.read()
    parsed_article = bs.BeautifulSoup(article, 'lxml')
    paragraphs = parsed_article.find_all('p')
    
    article_text = ""
    for p in paragraphs:
        article_text += p.text
    
    #print("\n First 500 characters of Wikipedia article: \n", article_text[:500])
    return article_text

def read_text(text):
    parsed_article = bs.BeautifulSoup(text, 'lxml')
    
    paragraphs = parsed_article.find_all('p')
    
    article_text = ""
    for p in paragraphs:
        article_text += p.text
    
    #print("\n First 500 characters of Wikipedia article: \n", article_text[:500])
    return article_text

### Preprocessing
def preprocess(article_text):
    # Clean formatting
    article_text = re.sub(r'(\r\n?|\n)+', ' ', article_text)
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    #article_text = re.sub(r'\s+', ' ', article_text)
    
    chunks = chunk_text(article_text)
    
    return chunks

### Tokenization
def score_sentences(chunks, article_text, n):
    summaries = []
    for chunk in chunks:
        # Remove punctuations
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        cleaned_article_text = re.sub(r'[^a-zA-Z]', ' ', chunk)
        cleaned_article_text = re.sub(r'\s+', ' ', cleaned_article_text)
        
        #print("\n First 500 characters of cleaned text: \n", cleaned_article_text[:500])
        
        
        ### Tokenization
        # Tokenize cleaned sentences
        sentences = sent_tokenize(article_text)
        
        # Word Frequency Table
        stop_words = stopwords.words('english')
        
        freqTable = dict()
        words = word_tokenize(cleaned_article_text)
        
        for word in words:
            word = word.lower()
            if word in stop_words:
                continue
            if word in freqTable.keys():
                freqTable[word] += 1
            else:
                freqTable[word] = 1
        
        max_freq = max(freqTable.values())
        for word in freqTable.keys():
            freqTable[word] = (freqTable[word]/max_freq)
            
        ### Sentence scoring
        # Sentence scores
        sentenceValue = dict()
        for sent in sentences:
            for word, freq in freqTable.items():
                if word in sent.lower():
                    if len(sent.split(' ')) < 40:
                        if sent in sentenceValue:
                            sentenceValue[sent] += freq
                        else:
                            sentenceValue[sent] = freq
                    
        ### Summarizing
        # Return summary
        summary = ' '.join(heapq.nlargest(n, sentenceValue, key = sentenceValue.get))   
        summaries.append(summary)
    return summaries
                    
### Summarizing
def build_summary(summaries):
    summaries_nodup = remove_duplicates(' '.join(summaries))
    sentences = re.split('(?<=[.!?]) +', summaries_nodup)
    final_sentences = [sentence.capitalize() for sentence in sentences] 
    return final_sentences

# article_text = read_article()
# cleaned_article_text = preprocess(article_text)
# sentenceValue = score_sentences(article_text, cleaned_article_text)
# summary=build_summary(sentenceValue, 4)
# print(summary)