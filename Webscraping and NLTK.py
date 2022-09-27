from pytube import YouTube
from pytube import Playlist
import pandas as pd
import numpy as np
import os
import nltk

#Pega a playlist
urls = Playlist('https://www.youtube.com/playlist?list=PL5LaOD9b1OVddNJT2FOU2hTqTOxcGrNEN')

#####Cria os vetores para os dados
text = []
author = []
date = []
rating = []
title = []
views = []

#####Extrai as transcrições 
for url in urls:
    yt = YouTube(url)
    texto = yt.captions.get_by_language_code("pt-BR")
    texto = texto.generate_srt_captions()
    titulo = yt.title
print(texto)


# Exclui certos caracteres para poder colocar como titulo do txt
    excluir = "-!,._|/()"
    titulo = ''.join(x for x in titulo if x not in excluir)

print(titulo)

#####Coloca em txt, sendo que o titulo é o titulo do video
    documento = open('{n}.txt'.format(n = titulo), 'w')
    documento.write(texto)
    documento.close()

#####Salva em lista
    lista = open('{n}.txt'.format(n = titulo), 'r')
    lista = list(lista)
#Determina o intervalo em que estão os textos
    lista = lista[2::4]
#Tira \n
    lista = [s.rstrip() for s in lista]
#Concatena os itens em apenas um
    lista = [' '.join(lista)]
#Deleta os arquivos criados
    os.remove('{n}.txt'.format(n = titulo))
    text.extend(lista)
    
#####Coloca em lista
    author.append(yt.author)
    date.append(yt.publish_date)
    rating.append(yt.rating) #Nivel de aprovação
    title.append(yt.title)
    views.append(yt.views)

#Stopwords: palavras comuns que normalmente não contribuem para o significado de uma frase
stopwords = nltk.corpus.stopwords.words('portuguese')
np.transpose(stopwords)
    
#Remove Stopwords
def tira_stopWords(texto):
    frases = []
    for palavras in texto:
        semStop = [p for p in palavras.split() if p not in stopwords]
        frases.append(semStop)     
    return frases        

#Remove sufixos e prefixos de uma palavra: Stemming
def poe_stemmer(texto):
    stemmer = nltk.stem.RSLPStemmer()
    sem_stemmer = []
    for palavras in texto:
        com_Stemmer = [str(stemmer.stem(p)) for p in palavras.split() if p not in stopwords]
        sem_stemmer.append(com_Stemmer)
    return sem_stemmer

# Agora o texto está mais enxuto, com palavras mais simples, para melhor comparação
text_stemmer = poe_stemmer(text)

# Faz uma lista com as palavras
def busca_Palavras(frases):
    todas_Palavras = []
    for palavras in frases:
        todas_Palavras.extend(palavras)
    return todas_Palavras

# Agora o texto virou uma lista
palavras_busca = busca_Palavras(text_stemmer)

#
def busca_frequencia(palavras):
    palavras = nltk.FreqDist(palavras)
    return palavras

frequencia_busca = busca_frequencia(palavras_busca)

# Tira a repetição das palavras
def busca_palavras_unicas(frequencia):
    freq = frequencia.keys()
    return freq

palavras_unicas = busca_palavras_unicas(frequencia_busca)

#
def extrator_palavras(documento):
    doc = set(documento)
    caracteristicas = {}
    for palavras in palavras_unicas:
        caracteristicas ['%s' % palavras] = (palavras in doc)
    return caracteristicas

print('-----------------------------------Deu certo-----------------------------------')
