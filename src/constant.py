#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Hou Shaohui, Wang Yong
# 
# Author:     Hou Shaohui <houshao55@gmail.com>
# Maintainer: Hou Shaohui <houshao55@gmail.com>
#             Wang Yong <lazycat.manatee@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from nls import _

LANGUAGE_OCR_DICT = {
    "af" : "tesseract-ocr-afr",
    "ar" : "tesseract-ocr-ara",
    "az" : "tesseract-ocr-aze",
    "be" : "tesseract-ocr-bel",
    "bn" : "tesseract-ocr-ben",
    "bg" : "tesseract-ocr-bul",
    "ca" : "tesseract-ocr-cat",
    "cs" : "tesseract-ocr-ces",
    "zh-CN" : "tesseract-ocr-chi-sim",
    "zh-TW" : "tesseract-ocr-chi-tra",
    "da" : "tesseract-ocr-dan",
    "de" : "tesseract-ocr-deu",
    "gr" : "tesseract-ocr-ell",
    "en" : "tesseract-ocr-eng",
    "eo" : "tesseract-ocr-epo",
    "et" : "tesseract-ocr-est",
    "eu" : "tesseract-ocr-eus",
    "fi" : "tesseract-ocr-fin",
    "fr" : "tesseract-ocr-fra",
    "gl" : "tesseract-ocr-glg",
    "iw" : "tesseract-ocr-heb",
    "hi" : "tesseract-ocr-hin",
    "hr" : "tesseract-ocr-hrv",
    "id" : "tesseract-ocr-ind",
    "is" : "tesseract-ocr-isl",
    "it" : "tesseract-ocr-ita",
    "ja" : "tesseract-ocr-jpn",
    "kn" : "tesseract-ocr-kan",
    "ko" : "tesseract-ocr-kor",
    "lv" : "tesseract-ocr-lav",
    "lt" : "tesseract-ocr-lit",
    "mk" : "tesseract-ocr-mkd",
    "mt" : "tesseract-ocr-mlt",
    "ms" : "tesseract-ocr-msa",
    "nl" : "tesseract-ocr-nld",
    "no" : "tesseract-ocr-nor",
    "pl" : "tesseract-ocr-pol",
    "pt" : "tesseract-ocr-por",
    "ro" : "tesseract-ocr-ron",
    "ru" : "tesseract-ocr-rus",
    "sk" : "tesseract-ocr-slk",
    "sl" : "tesseract-ocr-slv",
    "es" : "tesseract-ocr-spa",
    "sq" : "tesseract-ocr-sqi",
    "sr" : "tesseract-ocr-srp",
    "sw" : "tesseract-ocr-swa",
    "sv" : "tesseract-ocr-swe",
    "ta" : "tesseract-ocr-tam",
    "te" : "tesseract-ocr-tel",
    "th" : "tesseract-ocr-tha",
    "tr" : "tesseract-ocr-tur",
    "vi" : "tesseract-ocr-vie",
    }

LANGUAGES = [
    ('af', _('Afrikaans')),
    ('ar', _('Arabic')),
    ('az', _('Azerbaijani')),
    ('be', _('Belarusian')),
    ('bg', _('Bulgarian')),
    ('bn', _('Bengali')),
    ('ca', _('Catalan')),
    ('cs', _('Czech')),
    ('cy', _('Welsh')),
    ('da', _('Danish')),
    ('de', _('German')),
    ('en', _('English')),
    ('eo', _('Esperanto')),
    ('es', _('Spanish')),
    ('et', _('Estonian')),
    ('eu', _('Basque')),
    ('fa', _('Persian')),
    ('fi', _('Finnish')),
    ('fr', _('French')),
    ('ga', _('Irish')),
    ('gl', _('Galician')),
    ('gr', _('Greek')),
    ('gu', _('Gujarati')),
    ('hi', _('Hindi')),
    ('hr', _('Croatian')),
    ('ht', _('Haitian')),
    ('hu', _('Hungaric')),
    ('hy', _('Armenian')),
    ('id', _('Indonesian')),
    ('is', _('Icelandic')),
    ('it', _('Italian')),
    ('iw', _('Hebrew')),
    ('ja', _('Japanese')),
    ('ka', _('Georgian')),
    ('kn', _('Kannada')),
    ('ko', _('Korean')),
    ('la', _('Latin')),
    ('lt', _('Lithuanian')),
    ('lv', _('Latvian')),
    ('mk', _('Macedonian')),
    ('ms', _('Malay')),
    ('mt', _('Maltese')),
    ('nl', _('Dutch')),
    ('no', _('Norwegian')),
    ('pl', _('Polish')),
    ('pt', _('Portuguese')),
    ('ro', _('Romanian')),
    ('ru', _('Russian')),
    ('sk', _('Slovak')),
    ('sl', _('Slovenian')),
    ('sq', _('Albanian')),
    ('sr', _('Serbian')),
    ('sv', _('Swedish')),
    ('sw', _('Swahili')),
    ('ta', _('Tamil')),
    ('te', _('Telugu')),
    ('th', _('Thai')),
    ('tl', _('Filipino')),
    ('tr', _('Turkish')),
    ('uk', _('Ukrainian')),
    ('ur', _('Urdu')),
    ('vi', _('Vietnamese')),
    ('yi', _('Yiddish')),
    ('zh-CN', _('Chinese')),
    ]

TRAYAREA_TOP = 0
TRAYAREA_BOTTOM = 0