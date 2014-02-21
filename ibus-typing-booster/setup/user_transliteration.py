# -*- coding: utf-8 -*-
# vim:et sts=4 sw=4
#
# ibus-typing-booster - The Tables engine for IBus
#
# Copyright (c) 2012-2013 Anish Patil <apatil@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import os
import os.path as path
import sys
import re
import codecs
import sqlite3
import time
from gi.repository import Translit


class LangDictTable:
    '''
        Class that specifies accent rules that needs to be appied for each language
        If user has specified user dictionary then that can be overiden by default mapping
    '''
    def __init__(self,dict_name,lang_dict=None):
        self.lang = dict_name
        self.lang_table = lang_dict

    def get_lang_table(self):
        if self.lang_table:
            return self.lang_table
        else:
            return self.get_sys_lang_table()

    def get_sys_lang_table(self):
        if self.lang == 'mr_IN.dic':
            return self.get_mr_table()

    def get_mr_table(self):
        table = dict({
            (u'ā', 'aa'),
            (u'ṭ', 't'),
            (u'ḍ', 'd'),
            (u'ē', 'e'),
            (u'ĕ', 'ey'),
            (u'ẖ', 'ha'),
            (u'ṛ', 'da'),
            (u'ġ', 'gan'),
            (u'ī', 'ee'),
            (u'ḵ', 'k'),
            (u'ḷ', 'l'),
            (u'ṁ', '-mm'),
            (u'ṅ', 'nn'),
            (u'ṇ', 'na'),
            (u'', 'a'),
            (u'ō', 'o'),
            (u'ṣ', 'sh'),
            (u'ŏ', 'oy'),
            (u'ḥ', 'tah'),
            (u'ś', 'she'),
            (u'ṟ', 'rr'),
            (u'ū', 'u'),
            (u'ñ', 'dnya'),
            (u'n̄' , 'n')
        })
        return table

class LatinConvert:
    def __init__(self,
                 user_dict,
                 hunspell_dict,
                 aff_file,
                 dict_name):
        self.user_db = user_dict
        self.hunspell_dict = hunspell_dict
        self.aff_file = aff_file
        self.trans = Translit.Transliterator.get("icu", "en")
        self.conv_table = LangDictTable(dict_name)
        self.lang_table = self.conv_table.get_lang_table()

    def read_hunspell_dict(self):
        aff_buffer = None
        encoding = None
        dict_buffer = None
        try:
            aff_buffer = open(
                self.aff_file).read().replace('\r\n', '\n')
        except:
            import traceback
            traceback.print_exc()
        if aff_buffer:
            encoding_pattern = re.compile(
                r'^[\s]*SET[\s]+(?P<encoding>[-a-zA-Z0-9_]+)[\s]*$',
                re.MULTILINE|re.UNICODE)
            match = encoding_pattern.search(aff_buffer)
            if match:
                encoding = match.group('encoding')
                print "load_dictionary(): encoding=%(enc)s found in %(aff)s" %{
                    'enc': encoding, 'aff': self.aff_file}
        try:
            dict_buffer = codecs.open(
                self.hunspell_dict).read().decode(encoding).replace('\r\n', '\n')
        except:
            print "load_dictionary(): loading %(dic)s as %(enc)s encoding failed, fall back to ISO-8859-1." %{
                'dic': self.hunspell_dict, 'enc': encoding}
            encoding = 'ISO-8859-1'
            try:
                dict_buffer = codecs.open(
                    self.hunspell_dict).read().decode(encoding).replace('\r\n', '\n')
            except:
                print "load_dictionary(): loading %(dic)s as %(enc)s encoding failed, giving up." %{
                    'dic': self.hunspell_dict, 'enc': encoding}
        if dict_buffer[0] == u'\ufeff':
            dict_buffer = dict_buffer[1:]
        return dict_buffer

    def get_words(self):
        buff = self.read_hunspell_dict()
        word_pattern = re.compile(r'^[^\s]+.*?(?=/|$)', re.MULTILINE|re.UNICODE)
        words = word_pattern.findall(buff)
        nwords = int(words[0])
        words = words[1:]
        return words

    def trans_word(self,word):
        try:
            return self.trans.transliterate(word)[0]
        except:
            print "Error while transliteration"

    def remove_accent(self,word):
        word = word.decode('utf-8')
        new_word  = []
        # To- Do use list compression
        for char in word:
            if self.lang_table.has_key(char):
                new_word.append(self.lang_table[char])
            elif char in[ u'\u0325', u'\u0310',u'\u0304', u'\u0315',u'\u0314']:
                pass
            else:
                new_word.append(char)
        return ''.join(new_word)

    def get_converted_words(self):
        words = self.get_words()
        icu_words = map(self.trans_word,words)
        ascii_words = map(self.remove_accent,icu_words)
        return ascii_words

    def insert_into_db(self):
        words = self.get_converted_words()
        sql_table_name = "phrases"
        try:
            conn = sqlite3.connect(self.user_db)
            sql = "INSERT INTO %s (input_phrase, phrase, user_freq, timestamp) values(:input_phrase, :phrase, :user_freq, :timestamp);" % (sql_table_name)
            sqlargs = []
            map(lambda x: sqlargs.append(
                {'input_phrase': x.decode('utf-8'),
                 'phrase': x.decode('utf-8'),
                 'user_freq': 0,
                 'timestamp': time.time()}),
                words)
            conn.executemany(sql,sqlargs)
            conn.commit()
        except:
            import traceback
            traceback.print_exc()

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description='translit')
    parser.add_argument('-u', '--userdictionary',
                        nargs='?',
                        type=str,
                        default='',
                        help='user dictionary')
    parser.add_argument('-d', '--hunspelldict',
                        nargs='?',
                        type=str,
                        default='',
                        help='hunspell file path')
    return parser.parse_args()


def main():
    args = parse_args()
    user_dict = args.userdictionary
    hunspell_dict = args.hunspelldict
    dict_name = args.hunspelldict
    if user_dict:
        #check whether user dict exists in the path
        home_path = os.getenv ("HOME")
        tables_path = path.join (home_path, ".local/share/ibus-typing-booster")
        user_dict = path.join (tables_path, user_dict)
        if not path.exists(user_dict):
            sys.stderr.write(
                "The user database %(udb)s does not exist .\n" %{'udb': user_dict})
            sys.exit(1)
    if hunspell_dict:
        # Not sure how to get hunspell dict path from env
        hunspell_path = "/usr/share/myspell/"
        hunspell_dict = path.join(hunspell_path,hunspell_dict)
        if not path.exists(hunspell_dict):
            sys.stderr.write(
                "The hunspell dictionary  %(hud)s does not exists .\n" %{'hud': hunspell_dict})
            sys.exit(1)
    aff_name = hunspell_dict.replace('.dic','.aff')
    lt = LatinConvert(user_dict,
                      hunspell_dict,
                      aff_name,
                      dict_name)
    lt.insert_into_db()

if __name__ == '__main__':
    main()