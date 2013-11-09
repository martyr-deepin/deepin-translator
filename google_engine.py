#! /usr/bin/env python
# -*- coding: utf-8 -*-

from netlib import Curl
public_curl = Curl()


def parse_dummy_list(dlist):
    while ",," in dlist or "[," in dlist:
        dlist = dlist.replace(",,", ",None,").replace("[,", "[None,")
    try:    
        return eval(dlist)
    except SyntaxError:
        return []

 
def get_sample_result(glist):
    '''
    翻译详细: a[5]
    
    原始字符:      a[5][<i>][0]
    句子ID:       a[5][<i>][1]
    可选翻译:      a[5][<i>][2] | 判断长度， 取每一列表的[0], 取出翻译后字符: a[5][<i>][2][0][0]
    字符位置(pos): a[5][<i>][3] | 取出[0], 并判断是否为None     

    In [104]: print a[4][1]
    ['reparents', [5], 1, 0, 1000, 1, 2, 0]

    In [105]: print a[5][1]
    ['reparents', 5, [['reparents', 1000, 1, 0]], [[13, 22]], '']    

    '''    
    try:
        return  ''.join([dl[0] for dl in glist[0]])
    except:
        return "翻译失败"
    
def google_translate(text, sl="auto", tl="zh-CN", encoding="UTF-8"):
    target_language = tl
    source_language = sl
    input_encoding = output_encoding = encoding
    data = dict(client="t",
                hl="zh-CN",
                sl=source_language,
                tl=target_language,
                ie=input_encoding,
                oe=output_encoding,
                otf=1,
                ssel=0,
                pc=1,
                uptl=target_language,
                sc=2,
                q=text)    
    url = "http://translate.google.cn/translate_a/t"
    dummy_list = public_curl.request(url, data)
    plist = parse_dummy_list(dummy_list)
    result = get_sample_result(plist)
    return result.decode(encoding)

def google_voice(text, tl="en", encoding="UTF-8"):
    data = dict(ie=encoding,
                tl=tl,
                total=1,
                idx=0,
                textlen=len(text),
                prev="input",
                q=text
                )
    return public_curl.request(data)


LANGUAGES = [
    ('af', u'\u5e03\u5c14\u8bed(\u5357\u975e\u8377\u5170\u8bed)'),
    ('ar', u'\u963f\u62c9\u4f2f\u8bed'),
    ('auto', u'\u68c0\u6d4b\u8bed\u8a00'),
    ('az', u'\u963f\u585e\u62dc\u7586\u8bed'),
    ('be', u'\u767d\u4fc4\u7f57\u65af\u8bed'),
    ('bg', u'\u4fdd\u52a0\u5229\u4e9a\u8bed'),
    ('bn', u'\u5b5f\u52a0\u62c9\u8bed'),
    ('bs', u'\u6ce2\u65af\u5c3c\u4e9a\u8bed'),
    ('ca', u'\u52a0\u6cf0\u7f57\u5c3c\u4e9a\u8bed'),
    ('ceb', u'\u5bbf\u52a1\u8bed'),
    ('cs', u'\u6377\u514b\u8bed'),
    ('cy', u'\u5a01\u5c14\u58eb\u8bed'),
    ('da', u'\u4e39\u9ea6\u8bed'),
    ('de', u'\u5fb7\u8bed'),
    ('en', u'\u82f1\u8bed'),
    ('eo', u'\u4e16\u754c\u8bed'),
    ('es', u'\u897f\u73ed\u7259\u8bed'),
    ('et', u'\u7231\u6c99\u5c3c\u4e9a\u8bed'),
    ('eu', u'\u5df4\u65af\u514b\u8bed'),
    ('fa', u'\u6ce2\u65af\u8bed'),
    ('fi', u'\u82ac\u5170\u8bed'),
    ('fr', u'\u6cd5\u8bed'),
    ('ga', u'\u7231\u5c14\u5170\u8bed'),
    ('gl', u'\u52a0\u5229\u897f\u4e9a\u8bed'),
    ('gu', u'\u53e4\u5409\u62c9\u7279\u8bed'),
    ('hi', u'\u5370\u5730\u8bed'),
    ('hmn', u'\u82d7\u8bed'),
    ('hr', u'\u514b\u7f57\u5730\u4e9a\u8bed'),
    ('ht', u'\u6d77\u5730\u514b\u91cc\u5965\u5c14\u8bed'),
    ('hu', u'\u5308\u7259\u5229\u8bed'),
    ('hy', u'\u4e9a\u7f8e\u5c3c\u4e9a\u8bed'),
    ('id', u'\u5370\u5c3c\u8bed'),
    ('is', u'\u51b0\u5c9b\u8bed'),
    ('it', u'\u610f\u5927\u5229\u8bed'),
    ('iw', u'\u5e0c\u4f2f\u6765\u8bed'),
    ('ja', u'\u65e5\u8bed'),
    ('jw', u'\u5370\u5c3c\u722a\u54c7\u8bed'),
    ('ka', u'\u683c\u9c81\u5409\u4e9a\u8bed'),
    ('km', u'\u9ad8\u68c9\u8bed'),
    ('kn', u'\u5361\u7eb3\u8fbe\u8bed'),
    ('ko', u'\u97e9\u8bed'),
    ('la', u'\u62c9\u4e01\u8bed'),
    ('lo', u'\u8001\u631d\u8bed'),
    ('lt', u'\u7acb\u9676\u5b9b\u8bed'),
    ('lv', u'\u62c9\u8131\u7ef4\u4e9a\u8bed'),
    ('mk', u'\u9a6c\u5176\u987f\u8bed'),
    ('mr', u'\u9a6c\u62c9\u5730\u8bed'),
    ('ms', u'\u9a6c\u6765\u8bed'),
    ('mt', u'\u9a6c\u8033\u4ed6\u8bed'),
    ('nl', u'\u8377\u5170\u8bed'),
    ('no', u'\u632a\u5a01\u8bed'),
    ('pl', u'\u6ce2\u5170\u8bed'),
    ('pt', u'\u8461\u8404\u7259\u8bed'),
    ('ro', u'\u7f57\u9a6c\u5c3c\u4e9a\u8bed'),
    ('ru', u'\u4fc4\u8bed'),
    ('sk', u'\u65af\u6d1b\u4f10\u514b\u8bed'),
    ('sl', u'\u65af\u6d1b\u6587\u5c3c\u4e9a\u8bed'),
    ('sq', u'\u963f\u5c14\u5df4\u5c3c\u4e9a\u8bed'),
    ('sr', u'\u585e\u5c14\u7ef4\u4e9a\u8bed'),
    ('sv', u'\u745e\u5178\u8bed'),
    ('sw', u'\u65af\u74e6\u5e0c\u91cc\u8bed'),
    ('ta', u'\u6cf0\u7c73\u5c14\u8bed'),
    ('te', u'\u6cf0\u5362\u56fa\u8bed'),
    ('th', u'\u6cf0\u8bed'),
    ('tl', u'\u83f2\u5f8b\u5bbe\u8bed'),
    ('tr', u'\u571f\u8033\u5176\u8bed'),
    ('uk', u'\u4e4c\u514b\u5170\u8bed'),
    ('ur', u'\u4e4c\u5c14\u90fd\u8bed'),
    ('vi', u'\u8d8a\u5357\u8bed'),
    ('yi', u'\u610f\u7b2c\u7eea\u8bed'),
    ('zh-CN', u'\u4e2d\u6587(\u7b80\u4f53)'),
    ('zh-TW', u'\u4e2d\u6587(\u7e41\u4f53)')
    ]
