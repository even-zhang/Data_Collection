#!/usr/bin/python3
# -*- coding:utf8 -*-
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import time
import sqlite3



#根据所有字段名获得输入数据中字段名所在坐标，提取出对应字段名及内容存入字典
def location(term, sentence):
    dic = {}
    seq = []
    i = 0
    j = 0
    for word in term:
        if word in sentence:
            loc = sentence.index(word)
            le = len(word)
            seq.append([loc, le])
    seq.sort()
    while j < len(seq)-1:
        if (seq[j+1][0] >= seq[j][0]) and ((seq[j+1][1] + seq[j+1][0]) <= (seq[j][1] + seq[j][0])):
            seq = seq[:j + 1] + seq[j + 2:]
            j += 1
        elif (seq[j+1][0] <= seq[j][0]) and ((seq[j+1][1] + seq[j+1][0]) >= (seq[j][1] + seq[j][0])):
            seq = seq[j + 1:]
            j += 1
        else:
            j += 1

    while i<len(seq):
        if i != len(seq)-1:
            field_detail = sentence[seq[i][0]:seq[i+1][0]]
            field = field_detail[0:seq[i][1]]
            detail = field_detail[seq[i][1]:]
            dic[field] = detail
        else:
            field_detail = sentence[seq[i][0]:]
            field = field_detail[0:seq[i][1]]
            detail = field_detail[seq[i][1]:]
            dic[field] = detail
        i += 1
    return dic



def terms(request):
    mz = sqlite3.connect(r'C:\Users\User\Desktop\py\data_collection\db\mz.db', check_same_thread=False)
    cu = mz.cursor()
    uid = time.time()
    uid = str(uid)
    term = request.GET['terms']
    term = term.replace(' ', '')
    sentence = ''
    try:
        cu.execute("insert into grid (uid, terms, sentence) VALUES(?, ?, ?)", (uid, term, sentence))
    except:
        uid += 'unique'
        cu.execute("insert into grid (uid, terms, sentence) VALUES(?, ?, ?)", (uid, term, sentence))
    mz.commit()
    mz.close()
    return JsonResponse({'uid':uid})


def index(request):
    return render(request, 'form.html')


def seg(request):
    mz = sqlite3.connect(r'C:\Users\User\Desktop\py\data_collection\db\mz.db')
    cu = mz.cursor()
    uid = request.GET['uid']
    sentence = request.GET['sentence']
    sentence = sentence.replace(' |，|,', '')
    if uid != '' and sentence != '':
        cu.execute("select terms, sentence from grid where uid =?", (uid,))
        terms = cu.fetchall()
        term = terms[0][0].split(',')
        dic = location(term, sentence)
    mz.close()
    return JsonResponse(dic, json_dumps_params={'ensure_ascii': False}, )
