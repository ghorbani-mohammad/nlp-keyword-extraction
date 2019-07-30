# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from hazm import *
import os
import sys
from collections import OrderedDict
import numpy as np


"""Showing whole matrix not just truncated"""
# np.set_printoptions(threshold=sys.maxsize)


"""We use hazm library for pos tagging"""
tagger = POSTagger(model='resources/postagger.model')
tags = tagger.tag(word_tokenize('ما بسیار کتاب می‌خوانیم'))


class TextRank4Keyword:
    """Extract keywords and keyphrase from text"""
    def __init__(self):
        self.d = 0.85  # damping coefficient, usually is .85
        self.min_diff = 1e-5  # convergence threshold  0.00001
        self.steps = 10  # iteration steps
        self.node_weight = None  # save keywords and its weight
        self.normalizer = Normalizer()
        self.stop_words = [line.rstrip('\n') for line in open('Stop_words.txt', encoding="utf8")]

    def normalize_text(self, text):
        return self.normalizer.normalize(text)

    def get_sentences(self, file_text):
        return sent_tokenize(file_text)

    def prepare_sentences(self, sentences, candid_pos):
        pured_sentences = []
        for sentence in sentences:
            pured_sentence = []
            tokens = word_tokenize(sentence)
            tags = tagger.tag(tokens)
            for i, token in enumerate(tokens):
                if token in self.stop_words:
                    continue
                else:
                    if tags[i][1] in candid_pos:
                        token = token.replace(u'\u200c', ' ')
                        pured_sentence.append(token)
            pured_sentences.append(pured_sentence)
        return pured_sentences

    def get_vocab(self, sentences):
        """Get all tokens"""
        vocab = OrderedDict()
        i = 0
        for sentence in sentences:
            for word in sentence:
                if word not in vocab:
                    vocab[word] = i
                    i += 1
        return vocab

    def get_token_pairs(self, window_size, sentences):
        """Build token_pairs from windows in sentences"""
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i + 1, i + window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs

    def symmetrize(self, a):
        return a + a.T - np.diag(a.diagonal())

    def get_matrix(self, vocab, token_pairs):
        """Get normalized matrix"""
        vocab_size = len(vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word1, word2 in token_pairs:
            i, j = vocab[word1], vocab[word2]
            g[i][j] = 1
        g = self.symmetrize(g)
        norm = np.sum(g, axis=0)
        g_norm = np.divide(g, norm, where=norm != 0)  # this is ignore the 0 element in norm
        return g_norm

    def calculate_score(self, vocab, matrix):
        pr = np.array([1] * len(vocab))
        previous_pr = 0
        for epoch in range(self.steps):
            pr = (1 - self.d) + self.d * np.dot(matrix, pr)
            if abs(previous_pr - sum(pr)) < self.min_diff:
                break
            else:
                previous_pr = sum(pr)
        node_weight = dict()
        for word, index in vocab.items():
            node_weight[word] = pr[index]
        return node_weight

    def get_keywords(self, file_name, node_weights, number=10):
        out_file = open('./Output/WordOut_' + file_name, 'w', encoding="utf8")
        node_weight = OrderedDict(sorted(node_weights.items(), key=lambda t: t[1], reverse=True))
        for i, (key, value) in enumerate(node_weight.items()):
            out_file.write(key + ' - ' + str(value)+'\n')
            if i > number:
                break
        out_file.close()

    def get_phrases(self, sentences, candid_pattern):
        all_candid_phrases = []
        for sentence in sentences:
            sentence_candid_phrases = []
            tokens = word_tokenize(sentence)
            tagss = tagger.tag(tokens)
            candid_phrase = []
            for i, token in enumerate(tokens):
                if (token not in self.stop_words) and (tagss[i][1] in candid_pattern):
                    token = token.replace(u'\u200c', ' ')
                    candid_phrase.append(token)
                else:
                    if len(candid_phrase) > 1 and (tagss[i][1] == 'N' or tagss[i][1] == 'Ne' or True):
                        sentence_candid_phrases.append(candid_phrase)
                    candid_phrase = []
            all_candid_phrases.append(sentence_candid_phrases)
        return all_candid_phrases

    def score_phrase(self, all_phrases, scores):
        phrases_score = dict()
        for sentence_phrases in all_phrases:
            for phrase in sentence_phrases:
                score = 0
                phrase_string = ''
                count = len(phrase)
                for word in phrase:
                    score = score + scores[word]
                    phrase_string += ' '+word
                phrases_score[phrase_string] = score/count
        return phrases_score

    def get_keyphrases(self, file_name, phrase_weights, number=10):
        out_file = open('./Output/PhraseOut_' + file_name, 'w', encoding="utf8")
        node_weight = OrderedDict(sorted(phrase_weights.items(), key=lambda t: t[1], reverse=True))
        for i, (key, value) in enumerate(node_weight.items()):
            out_file.write(key + ' - ' + str(value) + '\n')
            if i > number:
                break
        out_file.close()

def analyze_files():
    dir_path = './Input'
    all_files = os.listdir(dir_path)
    txt_files = list(filter(lambda x: x[-4:] == '.txt', all_files))
    for file in txt_files:
        input_file = open(dir_path+'/'+file, "r", encoding="utf8", errors="ignore")
        text = input_file.read()
        tr4w = TextRank4Keyword()
        text_normalized = tr4w.normalize_text(text)
        sentences = tr4w.get_sentences(text_normalized)
        sentences_processed = tr4w.prepare_sentences(sentences, ['N', 'V', 'Ne', 'AJ', 'AJe'])
        vocab = tr4w.get_vocab(sentences_processed)
        token_pairs = tr4w.get_token_pairs(4, sentences_processed)
        matrix = tr4w.get_matrix(vocab, token_pairs)
        scores = tr4w.calculate_score(vocab, matrix)
        tr4w.get_keywords(file, scores)
        phrases = tr4w.get_phrases(sentences, ['N', 'Ne', 'AJ', 'AJe'])
        phrases_score = tr4w.score_phrase(phrases, scores)
        tr4w.get_keyphrases(file, phrases_score)
        input_file.close()


analyze_files()

