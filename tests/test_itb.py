# -*- coding: utf-8 -*-
# vim:et sts=4 sw=4
#
# ibus-typing-booster - A completion input method for IBus
#
# Copyright (c) 2016 Mike FABIAN <mfabian@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

'''
This file implements the test cases for the unit tests of ibus-typing-booster
'''

import sys
import unicodedata
import unittest
import subprocess

from gi import require_version
require_version('IBus', '1.0')
from gi.repository import IBus

sys.path.insert(0, "../engine")
from hunspell_table import *
import tabsqlitedb
import itb_util
sys.path.pop(0)

class ItbTestCase(unittest.TestCase):
    def setUp(self):
        self.bus = IBus.Bus()
        self.db = tabsqlitedb.TabSqliteDb(user_db_file = ':memory:')
        self.engine = TypingBoosterEngine(
            self.bus,
            '/com/redhat/IBus/engines/table/typing_booster/engine/0',
            self.db,
            unit_test = True)
        self.backup_original_settings()
        self.set_default_settings()

    def tearDown(self):
        self.restore_original_settings()
        del self.engine

    def backup_original_settings(self):
        self.orig_emoji_prediction_mode = (
            self.engine.get_emoji_prediction_mode())
        self.orig_off_the_record_mode = (
            self.engine.get_off_the_record_mode())
        self.orig_auto_commit_characters = (
            self.engine.get_auto_commit_characters())
        self.orig_tab_enable = (
            self.engine.get_tab_enable())
        self.orig_inline_completion = (
            self.engine.get_inline_completion())
        self.orig_remember_last_used_preedit_ime = (
            self.engine.get_remember_last_used_preedit_ime())
        self.orig_page_size = (
            self.engine.get_page_size())
        self.orig_lookup_table_orientation = (
            self.engine.get_lookup_table_orientation())
        self.orig_min_char_complete = (
            self.engine.get_min_char_complete())
        self.orig_show_number_of_candidates = (
            self.engine.get_show_number_of_candidates())
        self.orig_show_status_info_in_auxiliary_text = (
            self.engine.get_show_status_info_in_auxiliary_text())
        self.orig_add_space_on_commit = (
            self.engine.get_add_space_on_commit())
        self.orig_current_imes = (
            self.engine.get_current_imes())
        self.orig_dictionary_names = (
            self.engine.get_dictionary_names())
        self.orig_qt_im_module_workaround = (
            self.engine.get_qt_im_module_workaround())
        self.orig_keybindings = (
            self.engine.get_keybindings())

    def restore_original_settings(self):
        self.engine.set_emoji_prediction_mode(
            self.orig_emoji_prediction_mode)
        self.engine.set_off_the_record_mode(
            self.orig_off_the_record_mode)
        self.engine.set_auto_commit_characters(
            self.orig_auto_commit_characters)
        self.engine.set_tab_enable(
            self.orig_tab_enable)
        self.engine.set_inline_completion(
            self.orig_inline_completion)
        self.engine.set_remember_last_used_preedit_ime(
            self.orig_remember_last_used_preedit_ime)
        self.engine.set_page_size(
            self.orig_page_size)
        self.engine.set_lookup_table_orientation(
            self.orig_lookup_table_orientation)
        self.engine.set_min_char_complete(
            self.orig_min_char_complete)
        self.engine.set_show_number_of_candidates(
            self.orig_show_number_of_candidates)
        self.engine.set_show_status_info_in_auxiliary_text(
            self.orig_show_status_info_in_auxiliary_text)
        self.engine.set_add_space_on_commit(
            self.orig_add_space_on_commit)
        self.engine.set_current_imes(
            self.orig_current_imes)
        self.engine.set_dictionary_names(
            self.orig_dictionary_names)
        self.engine.set_qt_im_module_workaround(
            self.orig_qt_im_module_workaround)
        self.engine.set_keybindings(
            self.orig_keybindings)

    def set_default_settings(self):
        self.engine.set_emoji_prediction_mode(False)
        self.engine.set_off_the_record_mode(False)
        self.engine.set_auto_commit_characters('')
        self.engine.set_tab_enable(False)
        self.engine.set_inline_completion(False)
        self.engine.set_remember_last_used_preedit_ime(False)
        self.engine.set_page_size(6)
        self.engine.set_min_char_complete(1)
        self.engine.set_show_number_of_candidates(False)
        self.engine.set_add_space_on_commit(True)
        self.engine.set_current_imes(['NoIME'])
        self.engine.set_dictionary_names(['en_US'])
        self.engine.set_qt_im_module_workaround(False)
        self.engine.set_keybindings({
            'cancel': ['Escape'],
            'commit_candidate_1': [],
            'commit_candidate_1_plus_space': ['1', 'KP_1', 'F1'],
            'commit_candidate_2': [],
            'commit_candidate_2_plus_space': ['2', 'KP_2', 'F2'],
            'commit_candidate_3': [],
            'commit_candidate_3_plus_space': ['3', 'KP_3', 'F3'],
            'commit_candidate_4': [],
            'commit_candidate_4_plus_space': ['4', 'KP_4', 'F4'],
            'commit_candidate_5': [],
            'commit_candidate_5_plus_space': ['5', 'KP_5', 'F5'],
            'commit_candidate_6': [],
            'commit_candidate_6_plus_space': ['6', 'KP_6', 'F6'],
            'commit_candidate_7': [],
            'commit_candidate_7_plus_space': ['7', 'KP_7', 'F7'],
            'commit_candidate_8': [],
            'commit_candidate_8_plus_space': ['8', 'KP_8', 'F8'],
            'commit_candidate_9': [],
            'commit_candidate_9_plus_space': ['9', 'KP_9', 'F9'],
            'enable_lookup': ['Tab', 'ISO_Left_Tab'],
            'lookup_related': ['Mod5+F12'],
            'lookup_table_page_down': ['Page_Down', 'KP_Page_Down', 'KP_Next'],
            'lookup_table_page_up': ['Page_Up', 'KP_Page_Up', 'KP_Prior'],
            'next_dictionary': ['Mod1+Down', 'Mod1+KP_Down'],
            'next_input_method': ['Control+Down', 'Control+KP_Down'],
            'previous_dictionary': ['Mod1+Up', 'Mod1+KP_Up'],
            'previous_input_method': ['Control+Up', 'Control+KP_Up'],
            'select_next_candidate': ['Tab', 'ISO_Left_Tab', 'Down', 'KP_Down'],
            'select_previous_candidate': ['Shift+Tab', 'Shift+ISO_Left_Tab', 'Up', 'KP_Up'],
            'setup': ['Mod5+F10'],
            'speech_recognition': [],
            'toggle_emoji_prediction': ['Mod5+F6'],
            'toggle_input_mode_on_off': [],
            'toggle_off_the_record': ['Mod5+F9'],
        })

    def test_dummy(self):
        self.assertEqual(True, True)

    def test_single_char_commit_with_space(self):
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'a ')

    def test_single_char_commit_with_arrow_right(self):
        self.engine.do_process_key_event(IBus.KEY_b, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_Right, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'b')

    def test_char_space_period_space(self):
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_period, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'a . ')

    def test_direct_input(self):
        self.engine.set_current_imes(['NoIME', 't-latn-post'])
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_quotedbl, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'a" ')

    def test_latn_post(self):
        self.engine.set_current_imes(['t-latn-post', 'NoIME'])
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_quotedbl, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'ä ')

    def test_autocommit_characters(self):
        self.engine.set_current_imes(['NoIME', 't-latn-post'])
        self.engine.set_auto_commit_characters('.')
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_semicolon, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_period, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_b, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'a;. b ')

    def test_set_page_size(self):
        self.engine.set_page_size(3)
        self.assertEqual(
            self.engine.get_lookup_table().mock_page_size,
            3)
        self.engine.set_page_size(5)
        self.assertEqual(
            self.engine.get_lookup_table().mock_page_size,
            5)

    def test_complete_word_from_us_english_dictionary(self):
        self.engine.set_current_imes(['NoIME', 't-latn-post'])
        self.engine.set_dictionary_names(['en_US'])
        self.engine.do_process_key_event(IBus.KEY_c, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_r, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_u, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.assertEqual(self.engine._candidates[0][0], 'cerulean')
        self.engine.do_process_key_event(IBus.KEY_F1, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'cerulean ')

    def test_commit_with_arrows(self):
        self.engine.set_current_imes(['NoIME', 't-latn-post'])
        self.engine.set_dictionary_names(['en_US'])
        self.engine.do_process_key_event(IBus.KEY_f, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_o, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_o, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'foo ')
        self.engine.do_process_key_event(IBus.KEY_b, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_r, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'foo ')
        self.assertEqual(self.engine.mock_committed_text_cursor_pos, 4)
        self.assertEqual(self.engine.mock_preedit_text, 'bar')
        self.assertEqual(self.engine.mock_preedit_text_cursor_pos, 3)
        self.assertEqual(self.engine.mock_preedit_text_visible, True)
        self.engine.do_process_key_event(IBus.KEY_Left, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_Left, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_Left, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'foo ')
        self.assertEqual(self.engine.mock_preedit_text, 'bar')
        self.assertEqual(self.engine.mock_preedit_text_cursor_pos, 0)
        self.assertEqual(self.engine.mock_preedit_text_visible, True)
        self.engine.do_process_key_event(IBus.KEY_Left, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'foo bar')
        self.assertEqual(self.engine.mock_committed_text_cursor_pos, 3)
        self.assertEqual(self.engine.mock_preedit_text, '')
        self.assertEqual(self.engine.mock_preedit_text_cursor_pos, 0)
        self.assertEqual(self.engine.mock_preedit_text_visible, False)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'foo  bar')
        self.assertEqual(self.engine.mock_committed_text_cursor_pos, 4)
        self.engine.do_process_key_event(IBus.KEY_b, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_z, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_Left, 0,
                                         IBus.ModifierType.CONTROL_MASK)
        self.assertEqual(self.engine.mock_committed_text, 'foo  bar')
        self.assertEqual(self.engine.mock_committed_text_cursor_pos, 4)
        self.assertEqual(self.engine.mock_preedit_text, 'baz')
        self.assertEqual(self.engine.mock_preedit_text_cursor_pos, 0)
        self.assertEqual(self.engine.mock_preedit_text_visible, True)
        self.engine.do_process_key_event(IBus.KEY_Left, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'foo baz bar')
        self.assertEqual(self.engine.mock_committed_text_cursor_pos, 3)
        self.assertEqual(self.engine.mock_preedit_text, '')
        self.assertEqual(self.engine.mock_preedit_text_cursor_pos, 0)
        self.assertEqual(self.engine.mock_preedit_text_visible, False)

    def test_emoji_related_tab_enable_cursor_visible_escape(self):
        self.engine.set_current_imes(['NoIME'])
        self.engine.set_dictionary_names(['en_US'])
        self.engine.set_emoji_prediction_mode(True)
        self.engine.set_tab_enable(True)
        self.engine.do_process_key_event(IBus.KEY_c, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_m, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_Tab, 0, 0)
        self.assertEqual(self.engine._candidates[0][0], 'camel')
        self.assertEqual(self.engine._candidates[5][0], '🐫')
        self.assertEqual(self.engine._candidates[5][2],
                         'bactrian camel')
        self.engine.do_candidate_clicked(5, 3, 0)
        self.assertEqual(self.engine._candidates[0][0], '🐫')
        self.assertEqual(self.engine._candidates[1][0], '🐪')
        self.assertEqual(
            self.engine.get_lookup_table().cursor_visible,
            False)
        self.engine.do_process_key_event(IBus.KEY_Down, 0, 0)
        self.assertEqual(
            self.engine.get_lookup_table().cursor_visible,
            True)
        self.engine.do_process_key_event(IBus.KEY_Down, 0, 0)
        self.assertEqual(
            self.engine.get_lookup_table().cursor_visible,
            True)
        self.assertEqual(
            self.engine.get_string_from_lookup_table_cursor_pos(),
            '🐪')
        self.engine.do_process_key_event(IBus.KEY_Escape, 0, 0)
        self.assertEqual(
            self.engine.get_lookup_table().cursor_visible,
            False)
        self.assertEqual(
            self.engine.get_lookup_table().get_cursor_pos(),
            0)
        self.assertEqual(
            self.engine.get_string_from_lookup_table_cursor_pos(),
            '🐫')
        self.engine.do_process_key_event(IBus.KEY_Escape, 0, 0)
        self.assertEqual(
            self.engine.get_lookup_table().cursor_visible,
            False)
        self.assertEqual(
            self.engine.get_lookup_table().get_cursor_pos(),
            0)
        self.assertEqual(self.engine._candidates[0][0], 'camel')
        self.assertEqual(self.engine._candidates[5][0], '🐫')
        self.assertEqual(self.engine._candidates[5][2],
                         'bactrian camel')
        self.engine.do_process_key_event(IBus.KEY_Down, 0, 0)
        self.assertEqual(
            self.engine.get_lookup_table().cursor_visible,
            True)
        self.assertEqual(
            self.engine.get_string_from_lookup_table_cursor_pos(),
            'camel')
        self.engine.do_process_key_event(IBus.KEY_Escape, 0, 0)
        self.assertEqual(
            self.engine.get_lookup_table().cursor_visible,
            False)
        self.assertEqual(
            self.engine.get_lookup_table().get_cursor_pos(),
            0)
        self.assertEqual(
            self.engine.get_string_from_lookup_table_cursor_pos(),
            'camel')
        self.engine.do_process_key_event(IBus.KEY_Escape, 0, 0)
        self.assertEqual(
            self.engine.get_lookup_table().get_number_of_candidates(),
            0)
        self.assertEqual(self.engine._candidates, [])
        self.assertEqual(self.engine.mock_preedit_text, 'camel')
        self.assertEqual(self.engine.mock_preedit_text_cursor_pos, 5)
        self.assertEqual(self.engine.mock_preedit_text_visible, True)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'camel ')
        self.assertEqual(self.engine.mock_preedit_text, '')
        self.assertEqual(self.engine.mock_preedit_text_cursor_pos, 0)
        self.assertEqual(self.engine.mock_preedit_text_visible, False)

    def test_marathi_and_britisch_english(self):
        self.engine.set_current_imes(['mr-itrans', 'NoIME'])
        self.engine.set_dictionary_names(['mr_IN', 'en_GB'])
        self.assertEqual(
            self.engine.get_current_imes(), ['mr-itrans', 'NoIME'])
        self.assertEqual(
            self.engine.get_dictionary_names(), ['mr_IN', 'en_GB'])
        self.engine.do_process_key_event(IBus.KEY_g, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_u, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_r, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_u, 0, 0)
        self.assertEqual(self.engine.mock_preedit_text, 'गुरु')
        self.engine.do_process_key_event(IBus.KEY_Down, 0,
                                         IBus.ModifierType.CONTROL_MASK)
        self.assertEqual(self.engine.mock_preedit_text, 'guru')
        self.engine.do_process_key_event(IBus.KEY_Down, 0,
                                         IBus.ModifierType.CONTROL_MASK)
        self.assertEqual(self.engine.mock_preedit_text, 'गुरु')
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine.mock_preedit_text, '')
        self.assertEqual(self.engine.mock_committed_text, 'गुरु ')

    def test_korean(self):
        if not itb_util.get_hunspell_dictionary_wordlist('ko_KR')[0]:
            # No Korean dictionary file could be found, skip this
            # test.  On some systems, like 'Arch' or 'FreeBSD', there
            # is no ko_KR.dic hunspell dictionary available, therefore
            # there is no way to run this test on these systems.
            # On systems where a Korean hunspell dictionary is available,
            # make sure it is installed to make this test case run.
            # In the ibus-typing-booster.spec file for Fedora,
            # I have a “BuildRequires:  hunspell-ko” for that purpose
            # to make sure this test runs when building the rpm package.
            return
        self.engine.set_current_imes(['ko-romaja'])
        self.engine.set_dictionary_names(['ko_KR'])
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_y, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_o, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_g, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_h, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_s, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_y, 0, 0)
        self.assertEqual(self.engine.mock_preedit_text, '안녕하세이')
        candidates = [unicodedata.normalize('NFC', x[0])
                      for x in self.engine._candidates]
        self.assertEqual(True, '안녕하세요' in candidates)
        self.engine.do_process_key_event(IBus.KEY_o, 0, 0)
        self.assertEqual(self.engine.mock_preedit_text, '안녕하세요')
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine.mock_preedit_text, '')
        self.assertEqual(self.engine.mock_committed_text, '안녕하세요 ')
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_y, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_o, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_g, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_h, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_s, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_y, 0, 0)
        self.assertEqual(self.engine.mock_preedit_text, '안녕하세이')
        candidates = [unicodedata.normalize('NFC', x[0])
                      for x in self.engine._candidates]
        self.assertEqual(True, '안녕하세요' in candidates)
        self.assertEqual('안녕하세요', candidates[0])

    def test_accent_insensitive_matching_german_dictionary(self):
        self.engine.set_current_imes(['NoIME', 't-latn-post'])
        self.engine.set_dictionary_names(['de_DE'])
        self.engine.do_process_key_event(IBus.KEY_A, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_p, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_g, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_u, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_h, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        self.assertEqual(
            unicodedata.normalize('NFC',
                                  self.engine._candidates[0][0]),
            'Alpenglühen')
        self.engine.do_process_key_event(IBus.KEY_F1, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'Alpenglühen ')

    def test_accent_insensitive_matching_german_database(self):
        self.engine.set_current_imes(['t-latn-post', 'NoIME'])
        self.engine.set_dictionary_names(['de_DE'])
        # Type “Glühwürmchen”
        self.engine.do_process_key_event(IBus.KEY_G, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_u, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_quotedbl, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_h, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_w, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_u, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_quotedbl, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_r, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_m, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_c, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_h, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        # The German hunspell recognizes this as a correct word
        # (although it is not in the dictionary as a single word
        # it is created by rules). Therefore, it must be
        #  the first candidate here:
        self.assertEqual(
            unicodedata.normalize('NFC',
                                  self.engine._candidates[0][0]),
            'Glühwürmchen')
        # user_freq must be 0 because this word has not been found in
        # the user database, it is only a candidate because it is a
        # valid word according to hunspell:
        self.assertEqual(self.engine._candidates[0][1], 0)
        # Commit with F1:
        self.engine.do_process_key_event(IBus.KEY_F1, 0, 0)
        # Type “Glühwürmchen” again:
        self.engine.do_process_key_event(IBus.KEY_G, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_u, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_quotedbl, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_h, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_w, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_u, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_quotedbl, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_r, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_m, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_c, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_h, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        # Again it should be the first candidate:
        self.assertEqual(
            unicodedata.normalize('NFC',
                                  self.engine._candidates[0][0]),
            'Glühwürmchen')
        # But now user_freq must be > 0 because the last commit
        # added this word to the user database:
        self.assertTrue(self.engine._candidates[0][1] > 0)
        # Commit with F1:
        self.engine.do_process_key_event(IBus.KEY_F1, 0, 0)
        self.assertEqual(
            self.engine.mock_committed_text,
            'Glühwürmchen Glühwürmchen ')
        # Type “Gluhwurmchen” (without the accents):
        self.engine.do_process_key_event(IBus.KEY_G, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_u, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_h, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_w, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_u, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_r, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_m, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_c, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_h, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        # The first candidate should be “Glühwürmchen” again now
        # because the input phrases are added without accents into the
        # user database and before matching against the user database
        # accents are removed from the input phrase:
        self.assertEqual(
            unicodedata.normalize('NFC',
                                  self.engine._candidates[0][0]),
            'Glühwürmchen')
        # Commit with F1:
        self.engine.do_process_key_event(IBus.KEY_F1, 0, 0)
        self.assertEqual(
            self.engine.mock_committed_text,
            'Glühwürmchen Glühwürmchen Glühwürmchen ')

    def test_accent_insensitive_matching_french_dictionary(self):
        self.engine.set_current_imes(['NoIME', 't-latn-post'])
        self.engine.set_dictionary_names(['fr_FR'])
        self.engine.do_process_key_event(IBus.KEY_d, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_i, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_f, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_f, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_r, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_m, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_m, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        self.assertEqual(
            unicodedata.normalize('NFC',
                                  self.engine._candidates[0][0]),
            'différemment')
        self.engine.do_process_key_event(IBus.KEY_F1, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'différemment ')

    def test_emoji_triggered_by_underscore_when_emoji_mode_is_off(self):
        self.engine.set_current_imes(['NoIME'])
        self.engine.set_dictionary_names(['en_US'])
        self.engine.set_emoji_prediction_mode(False)
        # Without a leading underscore, no emoji should match:
        self.engine.do_process_key_event(IBus.KEY_c, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_m, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.assertEqual(self.engine._candidates[0][0], 'camel')
        self.assertEqual(False, self.engine._candidates[5][0] == '🐫')
        self.engine.do_process_key_event(IBus.KEY_F1, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'camel ')
        # Now again with a leading underscore an emoji should match.
        self.engine.do_process_key_event(IBus.KEY_underscore, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_c, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_m, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.assertEqual(self.engine._candidates[0][0], '_camel')
        self.assertEqual(self.engine._candidates[5][0], '🐫')
        self.assertEqual(self.engine._candidates[5][2],
                         'bactrian camel')
        self.engine.do_process_key_event(IBus.KEY_F6, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'camel 🐫 ')

    def test_selecting_non_existing_candidates(self):
        '''
        Test case for: https://bugzilla.redhat.com/show_bug.cgi?id=1630349

        Trying to use the 1-9 or F1-F9 keys to select candidates beyond
        the end of the candidate list should not cause ibus-typing-booster
        to stop working.
        '''
        self.engine.set_current_imes(['NoIME'])
        self.engine.set_dictionary_names(['en_US'])
        self.engine.do_process_key_event(IBus.KEY_B, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_r, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_c, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_o, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.assertEqual(self.engine._candidates, [('Barcelona', 0, '', False, False)])
        self.engine.do_process_key_event(IBus.KEY_2, 0, 0)
        # Nothing should be committed:
        self.assertEqual(self.engine.mock_committed_text, '')
        self.assertEqual(self.engine.mock_preedit_text, 'Barcelona2')
        self.engine.do_process_key_event(IBus.KEY_BackSpace, 0, 0)
        self.assertEqual(self.engine.mock_preedit_text, 'Barcelona')
        self.assertEqual(self.engine._candidates, [('Barcelona', 0, '', False, False)])
        self.engine.do_process_key_event(IBus.KEY_1, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'Barcelona ')
        self.assertEqual(self.engine.mock_preedit_text, '')

    def test_add_space_on_commit(self):
        '''Test new option to avoid adding spaces when committing by label
        (1-9 or F1-F9 key) or by mouse click.  See:
        https://github.com/mike-fabian/ibus-typing-booster/issues/39
        '''
        self.engine.set_current_imes(['NoIME'])
        self.engine.set_dictionary_names(['en_US'])
        self.engine.do_process_key_event(IBus.KEY_t, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_s, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_t, 0, 0)
        self.assertEqual(self.engine.mock_preedit_text, 'test')
        self.assertEqual(self.engine.mock_committed_text, '')
        self.assertEqual(self.engine._candidates[0][0], 'test')
        self.engine.do_process_key_event(IBus.KEY_1, 0, 0)
        self.assertEqual(self.engine.mock_preedit_text, '')
        # By default a space should be added:
        self.assertEqual(self.engine.mock_committed_text, 'test ')
        # Now set the option to avoid the extra space:
        self.engine.set_keybindings({
            'commit_candidate_1': ['1', 'KP_1'],
            'commit_candidate_1_plus_space': ['F1'],
        })
        self.engine.do_process_key_event(IBus.KEY_t, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_s, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_t, 0, 0)
        self.assertEqual(self.engine.mock_preedit_text, 'test')
        self.assertEqual(self.engine.mock_committed_text, 'test ')
        self.assertEqual(self.engine._candidates[0][0], 'test')
        self.engine.do_process_key_event(IBus.KEY_1, 0, 0)
        self.assertEqual(self.engine.mock_preedit_text, '')
        # No space should be added now:
        self.assertEqual(self.engine.mock_committed_text, 'test test')

    def test_tab_enable_key_binding_changed(self):
        self.engine.set_current_imes(['NoIME', 't-latn-post'])
        self.engine.set_dictionary_names(['en_US'])
        self.engine.set_tab_enable(True)
        self.engine.set_keybindings({
            'enable_lookup': ['Insert'], # changed from default Tab
        })
        self.engine.do_process_key_event(IBus.KEY_t, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_s, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_t, 0, 0)
        # Tab should trigger a commit now instead of enabling the
        # lookup (which is what Tab would do by default):
        self.engine.do_process_key_event(IBus.KEY_Tab, 0, 0)
        self.assertEqual(len(self.engine._candidates), 0)
        self.assertEqual(self.engine.mock_preedit_text, '')
        self.assertEqual(self.engine.mock_committed_text, 'test\t')
        self.engine.do_process_key_event(IBus.KEY_c, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_r, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_u, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_Insert, 0, 0)
        self.assertEqual(self.engine._candidates[0][0], 'cerulean')
        self.engine.do_process_key_event(IBus.KEY_F1, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'test\tcerulean ')

    def test_digits_used_in_keybindings(self):
        self.engine.set_current_imes(['hi-itrans'])
        self.engine.set_dictionary_names(['hi_IN'])
        self.engine.do_process_key_event(IBus.KEY_0, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_1, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_2, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_3, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_4, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_5, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_6, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_7, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_8, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_9, 0, 0)
        # As digits are used in the default key bindings,
        # the typed digits should be transliterated to
        # Hindi digits and committed immediately:
        self.assertEqual(len(self.engine._candidates), 0)
        self.assertEqual(self.engine.mock_preedit_text, '')
        self.assertEqual(self.engine.mock_committed_text, '०१२३४५६७८९')
        # Now remove all digits from the key bindings and type
        # the same digits again:
        self.engine.set_keybindings({
            'commit_candidate_1': [],
            'commit_candidate_1_plus_space': ['F1'],
            'commit_candidate_2': [],
            'commit_candidate_2_plus_space': ['F2'],
            'commit_candidate_3': [],
            'commit_candidate_3_plus_space': ['F3'],
            'commit_candidate_4': [],
            'commit_candidate_4_plus_space': ['F4'],
            'commit_candidate_5': [],
            'commit_candidate_5_plus_space': ['F5'],
            'commit_candidate_6': [],
            'commit_candidate_6_plus_space': ['F6'],
            'commit_candidate_7': [],
            'commit_candidate_7_plus_space': ['F7'],
            'commit_candidate_8': [],
            'commit_candidate_8_plus_space': ['F8'],
            'commit_candidate_9': [],
            'commit_candidate_9_plus_space': ['F9'],
        })
        self.engine.do_process_key_event(IBus.KEY_0, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_1, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_2, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_3, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_4, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_5, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_6, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_7, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_8, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_9, 0, 0)
        # The newly typed digits should be in the preedit now
        # and the committed text should still be unchanged:
        self.assertEqual(self.engine.mock_preedit_text, '०१२३४५६७८९')
        self.assertEqual(self.engine.mock_committed_text, '०१२३४५६७८९')
        # Commit:
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine.mock_preedit_text, '')
        self.assertEqual(self.engine.mock_committed_text, '०१२३४५६७८९०१२३४५६७८९ ')

    def test_commit_candidate_1_without_space(self):
        self.engine.set_current_imes(['NoIME', 't-latn-post'])
        self.engine.set_dictionary_names(['en_US'])
        self.engine.set_keybindings({
            'commit_candidate_1': ['Right'],
        })
        self.engine.do_process_key_event(IBus.KEY_c, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_r, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_u, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.assertEqual(self.engine._candidates[0][0], 'cerulean')
        self.engine.do_process_key_event(IBus.KEY_F1, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'cerulean ')
        self.engine.do_process_key_event(IBus.KEY_c, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_r, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_u, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.assertEqual(self.engine._candidates[0][0], 'cerulean')
        self.engine.do_process_key_event(IBus.KEY_Right, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'cerulean cerulean')

    def test_toggle_candidate_case(self):
        self.engine.set_current_imes(['NoIME', 't-latn-post'])
        self.engine.set_dictionary_names(['en_US'])
        self.engine.do_process_key_event(IBus.KEY_c, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_r, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_u, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.assertEqual(self.engine._candidates[0][0], 'cerulean')
        self.engine.do_process_key_event(IBus.KEY_Shift_L, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_Shift_L, 0, IBus.ModifierType.RELEASE_MASK)
        self.assertEqual(self.engine._candidates[0][0], 'Cerulean')
        self.engine.do_process_key_event(IBus.KEY_Shift_R, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_Shift_R, 0, IBus.ModifierType.RELEASE_MASK)
        self.assertEqual(self.engine._candidates[0][0], 'CERULEAN')
        self.engine.do_process_key_event(IBus.KEY_F1, 0, 0)
        self.assertEqual(self.engine.mock_committed_text, 'CERULEAN ')

    def test_sinhala_wijesekera(self):
        self.engine.set_current_imes(['si-wijesekera', 'NoIME'])
        self.engine.set_dictionary_names(['en_US'])
        self.engine.do_process_key_event(IBus.KEY_v, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_k, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_s, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_I, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.assertEqual(self.engine.mock_preedit_text, 'ඩනිෂ්ක')
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine.mock_preedit_text, '')
        self.assertEqual(self.engine.mock_committed_text, 'ඩනිෂ්ක ')
        self.engine.do_process_key_event(IBus.KEY_k, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_j, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_S, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_k, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.assertEqual(self.engine.mock_preedit_text, 'නවීන්')
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine.mock_preedit_text, '')
        self.assertEqual(self.engine.mock_committed_text, 'ඩනිෂ්ක නවීන් ')
