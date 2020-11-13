# -*- coding: utf-8 -*-
"""helper

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1weoDOMOdzf6muea5cvHhfiM_lAFqNiqC
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from sklearn.metrics import (
    precision_score, 
    recall_score, 
    f1_score, 
    classification_report,
    accuracy_score,
    roc_curve,
    confusion_matrix
)

class Tokenization():

  def __init__(self,df,pad_length=50):
    self.df = df
    self.pad_length = pad_length

    self.dictionary()

  def dictionary(self):    # Builds a dictionary of words
    corpus = self.df.apply(lambda s: s.split()).values

    vocab = {}
    i = 0
    for line in corpus:
        for word in line:
          if word not in vocab:
            vocab[word] = i
            i += 1            

    self.vocab = vocab


  def convert_to_numbers(self,X): #Converts text data into Number sequence
    corpus = X.apply(lambda s: s.split()).values
    vocab = self.vocab
    line_list = []
    corpus_list = []

    for line in corpus:
      for word in line:
        if word in vocab:
          line_list.append(vocab[word])
          
      if len(line_list) < self.pad_length:
        pad_length = self.pad_length - len(line_list)
        line_list = np.pad(line_list,(0,pad_length),mode='constant')
      else:
        line_list = np.asarray(line_list[0:self.pad_length])

      corpus_list.append(line_list)
      line_list = []

    return np.asarray(corpus_list)


  def convert_to_str(self,corpus): #Converts Number sequence into text data
    
    inv_vocab = {v: k for k, v in self.vocab.items()}

    line_list = []
    corpus_list = []

    for line in corpus:
      for num in line:
        if num in inv_vocab:       
          line_list.append(inv_vocab[num])

      corpus_list.append(line_list)
      line_list = []

    return np.asarray(corpus_list)

class Metrics():
  def __init__(self,y_true,y_pred,y_scores = None):
    self.y_true = y_true
    self.y_pred = y_pred
    self.y_scores = y_scores
  
  def cost_matrix(self):
    tn, fp, fn, tp = confusion_matrix(self.y_true,self.y_pred).ravel()
    array = np.asarray([[tp,fn],[fp,tn]])
    matrix_df = pd.DataFrame(array,columns=['Positive','Negative'],index=['Positive','Negative'])

    display(matrix_df)

  def scores(self):
    print("F1-score: ", f1_score(self.y_true,self.y_pred))
    print("Precision: ", precision_score(self.y_true,self.y_pred))
    print("Recall: ", recall_score(self.y_true,self.y_pred))
    print("Acuracy: ", accuracy_score(self.y_true,self.y_pred))
    print("-"*50)
    print(classification_report(self.y_true,self.y_pred))
    print("-"*50)

  def roc_curve(self):
    
    fig,ax = plt.subplots(dpi=100)
    fpr,tpr,th = roc_curve(self.y_true,self.y_scores)
    ax.plot(fpr,tpr,'r-')
    ax.set_title("ROC Plot")
    ax.set_xlabel("FPR")
    ax.set_ylabel("TPR")