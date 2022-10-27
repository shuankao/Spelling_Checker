#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import re
from collections import Counter


def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))



def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N


def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

first_edit = {}
def candidates(word): 
    "Generate possible spelling corrections for word."
    global first_edit 
    first_edit = edits1(word)
    #print(set((known(first_edit)).union(known(edits2(word)))))
    return (known([word]) or (known(first_edit)) or (known(edits2())) or ['word unknown'])
    # or (known(edits3(second_edits)))



def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

splits = []
def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    global splits
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes+transposes+replaces+inserts)

second_edits = {}
def edits2(): 
    "All edits that are two edits away from `word`."
    global second_edits 
    second_edits = set(e2 for e1 in first_edit for e2 in edits1(e1))
    return second_edits

## 新增edit distance == 3，只做常見拼字錯誤 (‘c','v'), ('r''t') 轉換
# def edits3(words):
#     replace_accu = []
#     for word in words:
#         common_mis = 'cvrt'
#         replaces   = [L + c + R[1:]  for L, R in splits if R in common_mis for c in common_mis]
#         replace_accu += replaces
#     return set(replace_accu)

def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    import time
    start = time.perf_counter()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in WORDS)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, WORDS[w], right, WORDS[right]))
    dt = time.perf_counter() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]

spelltest(Testset(open('spell-testset1.txt'))) # Development set

### week7
st.title('SpellChecker')
option = st.selectbox('Choosing a word...',('','apple','banana','strawberry'))
text = st.text_input('Type your own!')
# st.write(text)
corrected_text = correction(text)
corrected_option = correction(option)
show_original = False
with st.sidebar:
    show_original = st.checkbox('Show original word')
if text:
    if show_original:
        st.write('Original word: {}'.format(corrected_text))
    if text == corrected_text:
        st.success('{} is the correct spelling!'.format(text))
    else:
        st.error('Correction: {}'.format(corrected_text))
elif option:
    if show_original:
        st.write('Original word: {}'.format(corrected_option))
    if option == corrected_option:
        st.success('{} is the correct spelling!'.format(option))
    else:
        st.error('Correction: {}'.format(corrected_option))








