import math, sys
import nltk
from pprint import pprint
import pandas as pd
import re
import time
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from matplotlib import rc
import seaborn as sns

class BayesianFilter:
    def __init__(self):
        self.words = set()  # 출현한 단어 기록
        self.word_dict = {}  # 카테고리마다의 출현 횟수 기록
        self.category_dict = {}  # 카테고리 출현 횟수 기록

    # 형태소 분석하기 -- (1)
    def split(self, text):
        
    # 영문자 이외 문자는 공백으로 변환
        only_english = re.sub('[^a-zA-Z]', ' ', text)
 
    # 소문자 변환
        no_capitals = only_english.lower().split()
 
    # 불용어 제거
        stops = set(stopwords.words('english'))
        no_stops = [word for word in no_capitals if not word in stops]
 
    # 어간 추출
        stemmer = nltk.stem.SnowballStemmer('english')
        results = [stemmer.stem(word) for word in no_stops]
 
    # 공백으로 구분된 문자열로 결합하여 결과 반환
        return results

    # 단어와 카테고리의 출현 횟수 세기 -- (2)
    def inc_word(self, word, category):
        # 단어를 카테고리에 추가하기
        if not category in self.word_dict:
            self.word_dict[category] = {}
        if not word in self.word_dict[category]:
            self.word_dict[category][word] = 0
        self.word_dict[category][word] += 1
        self.words.add(word)

    def inc_category(self, category):
        # 카테고리 계산하기
        if not category in self.category_dict:
            self.category_dict[category] = 0
        self.category_dict[category] += 1

    # 텍스트 학습하기 -- (3)
    def fit(self, text, category):
        """ 텍스트 학습 """
        word_list = self.split(text)
        for word in word_list:
            self.inc_word(word, category)
        self.inc_category(category)

    # 단어 리스트에 점수 매기기-- (4)
    def score(self, words, category):
        score = math.log(self.category_prob(category))
        for word in words:
            score += math.log(self.word_prob(word, category))
        return score

    # 예측하기 -- (5)
    def predict(self, text):
        best_category = None
        max_score = -sys.maxsize
        words = self.split(text)
        score_list = []
        for category in self.category_dict.keys():
            score = self.score(words, category)
            score_list.append((category, score))
            if score > max_score:
                max_score = score
                best_category = category
        return best_category, score_list

    # 카테고리 내부의 단어 출현 횟수 구하기
    def get_word_count(self, word, category):
        if word in self.word_dict[category]:
            return self.word_dict[category][word]
        else:
            return 0

    # 카테고리 계산
    def category_prob(self, category):
        sum_categories = sum(self.category_dict.values())
        category_v = self.category_dict[category]
        return category_v / sum_categories

    # 카테고리 내부의 단어 출현 비율 계산 -- (6)
    def word_prob(self, word, category):
        n = self.get_word_count(word, category) + 1  # -- (6a)
        d = sum(self.word_dict[category].values()) + len(self.words)
        return n / d