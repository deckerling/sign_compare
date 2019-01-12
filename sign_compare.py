#!/usr/bin/env python3

# sign_compare.py
#
# Copyright 2019 E. Decker
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A simple tool to compare (linguistic) signs."""

import os
import tkinter as tk


class SignCreator(tk.Frame):
    """GUI-frame to create (and save) new signs."""
    
    def __init__(self, master):
        tk.Frame.__init__(self)
        tk.Button(self, font='Arial 16', text='Back', width=7,
                  command=self.__del__).pack()
        tk.Label(self, font='Arial 16',
                 text='Enter a name (signifier) for the new sign: ').pack()
        self.entry = tk.Entry(self, font='Arial 16', width=15)
        self.entry.pack()
        tk.Button(self, font='Arial 16', text='Save', width=7,
                  command=self.save_sign).pack()

    def __del__(self):
        self.forget()
        ROOT_FRAME.pack()

    def save_sign(self):
        if not os.path.exists('sc_files'):
            os.makedirs('sc_files')
        if self.entry.get():
            # Changes the background colour of "self.entry" to green if the
            # entry was accepted (and the file saved) and to red if not.
            try:
                open('sc_files/'+self.entry.get()+'.txt', 'a').close()
                self.entry.delete(0, 'end')
                self.entry['bg'] = 'green'
            except OSError:
                self.entry['bg'] = 'red'


class FeatureAdder(tk.Frame):
    """GUI-frame to select an already created sign and to add features to it."""
    
    def __init__(self, master):
        tk.Frame.__init__(self)
        tk.Button(self, font='Arial 16', text='Back', width=7, command=
                  self.__del__).pack()
        if os.path.exists('sc_files') and os.listdir('sc_files'):
            self.label = tk.Label(self, font='Arial 16',
                                  text='Select the sign that should gain a feature: ')
            self.label.pack()
            self.sign_listbox = tk.Listbox(self, font='Arial 16', height=12,
                                           width=15)
            self.sign_listbox.pack()
            self.ok_button = tk.Button(self, font='Arial 16', text='Ok',
                                       width=7, command=self.select_sign)
            self.ok_button.pack()
            for sign in os.listdir('sc_files'):
                self.sign_listbox.insert('end', sign[:-4])
        else:
            tk.Label(self, font='Arial 16',
                     text='There are no signs saved!').pack()

    def __del__(self):
        try:
            self.forget()
            ROOT_FRAME.pack()
        except tk.TclError:
            pass

    def select_sign(self):
        self.label['text'] = 'Enter a new feature to add to the sign \"'+self.sign_listbox.get('active')+'\": '
        self.sign_listbox.forget()
        self.ok_button.forget()
        self.entry = tk.Entry(self, font='Arial 16', width=25)
        self.entry.pack()
        self.ok_button = tk.Button(self, font='Arial 16', text='Save', width=7,
                                   command=self.add_feature).pack()

    def add_feature(self):
        if self.entry.get():
            # Changes the background colour of "self.entry" to green if the
            # entry was accepted (and the feature saved) and to red if not.
            try:
                # If "self.entry.get()" ends with '.txt' or '.sign' the program
                # will add the content of that sign/file to the "edited_file".
                # If that sign/file does not exist an exception will be raised
                # and nothing will be added to "edited_file".
                if self.entry.get()[-4:] == '.txt':
                    with open('sc_files/'+self.entry.get(),
                              'r') as file_to_add:
                        features_to_add = file_to_add.read()
                elif self.entry.get()[-5:] == '.sign':
                    with open('sc_files/'+self.entry.get()[:-4]+'txt',
                              'r') as file_to_add:
                        features_to_add = file_to_add.read()
                else:
                    features_to_add = self.entry.get()+';'
                with open('sc_files/'+self.sign_listbox.get('active')+'.txt',
                          'a') as edited_file:
                    edited_file.write(features_to_add)
                self.entry.delete(0, 'end')
                self.entry['bg'] = 'green'
            except IOError:
                self.entry['bg'] = 'red'


class FeatureRemover(tk.Frame):
    """GUI-frame to select an already created sign and to remove features from
        it."""
    
    def __init__(self, master):
        tk.Frame.__init__(self)
        tk.Button(self, font='Arial 16', text='Back', width=7,
                  command=self.__del__).pack() 
        if os.path.exists('sc_files') and os.listdir('sc_files'):
            self.label = tk.Label(self, font='Arial 16',
                                  text='Select the sign that should lose a feature: ')
            self.label.pack()
            self.sign_listbox = tk.Listbox(self, font='Arial 16', height=12,
                                           width=15)
            self.sign_listbox.pack()
            self.ok_button = tk.Button(self, font='Arial 16', text='Ok',
                                       width=7, command=self.select_sign)
            self.ok_button.pack()
            for sign in os.listdir('sc_files'):
                self.sign_listbox.insert('end', sign[:-4])
        else:
            tk.Label(self, font='Arial 16',
                     text='There are no signs saved!').pack()

    def __del__(self):
        try:
            self.forget()
            ROOT_FRAME.pack()
        except tk.TclError:
            pass

    def select_sign(self):
        self.file_name = self.sign_listbox.get('active')
        try:
            with open('sc_files/'+self.file_name+'.txt', 'r') as file_with_features:
                feature_string = file_with_features.read()
            # Checks if there are features saved for the selected sign.
            if ';' in feature_string:
                self.label['text'] = 'Select the feature of the sign\n\"'+self.file_name+'\" you want to remove. '
                self.sign_listbox.delete(0, 'end')
                self.ok_button['text'] = 'Remove'
                self.ok_button['command'] = self.remove_feature
                self.feature_list = feature_string.split(';')
                self.feature_list.remove('')
                for i in range(len(self.feature_list)):
                    self.sign_listbox.insert('end', self.feature_list[i])
            else:
                self.sign_listbox.forget()
                self.ok_button.forget()
                self.label['text']='There are no features saved for the sign \"'+self.file_name+'\"!'
        except IOError:
            pass

    def remove_feature(self):
        """Removes a selected feature from the selected sign by rebuilding the
            file's (i.e. the sign's) content from the "sign_listbox" after the
            selected feature was removed from there."""
        try:
            self.feature_list.remove(self.sign_listbox.get('active'))
            new_file_content = ''
            for i in range(len(self.feature_list)):
                new_file_content += self.feature_list[i]+';'
            with open('sc_files/'+self.file_name+'.txt', 'w') as edited_file:
                edited_file.write(new_file_content)
            self.sign_listbox.delete('active')
        except IOError:
            pass
        except ValueError:
            self.__del__()


class SignComparer(tk.Frame):
    """GUI-frame to compare two already created signs by calculating the Dice
        coefficient and the Jaccard index."""

    def __init__(self, master):
        tk.Frame.__init__(self)
        tk.Button(self, font='Arial 16', text='Back', width=7,
                  command=self.__del__).pack()
        if os.path.exists('sc_files') and os.listdir('sc_files'):
            tk.Label(self, font='Arial 16',
                     text='Select one sign in each box to compare: ').pack()
            boxFrame = tk.Frame(self)
            boxFrame.pack()
            self.sign_listbox_0 = tk.Listbox(boxFrame, font='Arial 16',
                                             height=12, width=15,
                                             exportselection=0)
            self.sign_listbox_0.pack(side='left')
            self.sign_listbox_1 = tk.Listbox(boxFrame, font='Arial 16',
                                             height=12, width=15,
                                             exportselection=0)
            self.sign_listbox_1.pack(side='left')
            tk.Button(self, font='Arial 16', text='Compare', width=10,
                      command=self.calculate_similarity).pack()
            self.dice_label_0 = tk.Label(self, font='Arial 16')
            self.dice_label_0.pack()
            self.dice_label_1 = tk.Label(self, font='Arial 18 bold')
            self.dice_label_1.pack()
            self.jaccard_label_0 = tk.Label(self, font='Arial 16')
            self.jaccard_label_0.pack()
            self.jaccard_label_1 = tk.Label(self, font='Arial 18 bold')
            self.jaccard_label_1.pack()
            for sign in os.listdir('sc_files'):
                self.sign_listbox_0.insert('end', sign[:-4])
                self.sign_listbox_1.insert('end', sign[:-4])
        else:
            tk.Label(self, font='Arial 16',
                     text='There are no signs saved!').pack()

    def __del__(self):
        try:
            self.forget()
            ROOT_FRAME.pack()
        except tk.TclError:
            pass

    def calculate_similarity(self):
        try:
            with open('sc_files/'+self.sign_listbox_0.get('active')+'.txt',
                      'r') as file_with_features_0:
                feature_string_0 = file_with_features_0.read()
            with open('sc_files/'+self.sign_listbox_1.get('active')+'.txt',
                      'r') as file_with_features_1:
                feature_string_1 = file_with_features_1.read()
            feature_list_0 = feature_string_0.split(';')
            feature_list_1 = feature_string_1.split(';')
            feature_list_0.remove('')
            feature_list_1.remove('')
            try:
                x = len(set(feature_list_0)&set(feature_list_1))
                y = len(set(feature_list_0))+len(set(feature_list_1))
                dice_coefficient = 2*x/y
                jaccard_index = x/(y-x)
                self.dice_label_0['text'] = 'Dice coefficient of the signifieds of the signs\n\"'+self.sign_listbox_0.get('active')+'\" and \"'+self.sign_listbox_1.get('active')+'\": '
                self.dice_label_1['text'] = dice_coefficient
                self.jaccard_label_0['text'] = 'And their Jaccard index: '
                self.jaccard_label_1['text'] = jaccard_index
            # Raises an exception if both signs have no features.
            except ZeroDivisionError:
                self.dice_label_0['text'] = 'Couldn\'t compare the signs\n\"'+self.sign_listbox_0.get('active')+'\" and \"'+self.sign_listbox_1.get('active')+'\":\nThere are no features saved for them!'
                self.dice_label_1['text'] = ''
                self.jaccard_label_0['text'] = ''
                self.jaccard_label_1['text'] = ''
        except IOError:
            pass


def create_sign():
    ROOT_FRAME.forget()
    SignCreator(ROOT).pack()


def add_feature():
    ROOT_FRAME.forget()
    FeatureAdder(ROOT).pack()


def remove_feature():
    ROOT_FRAME.forget()
    FeatureRemover(ROOT).pack()


def compare_signs():
    ROOT_FRAME.forget()
    SignComparer(ROOT).pack()


ROOT = tk.Tk()
ROOT.title('sign_compare')

ROOT_FRAME = tk.Frame(ROOT)
tk.Button(ROOT_FRAME, font='Arial 16', text='New sign', width=28,
          command=create_sign).pack()
tk.Button(ROOT_FRAME, font='Arial 16', text='Add feature(s)', width=28,
          command=add_feature).pack()
tk.Button(ROOT_FRAME, font='Arial 16', text='Remove feature(s)', width=28,
          command=remove_feature).pack()
tk.Button(ROOT_FRAME, font='Arial 16', text='Compare signs', width=28,
          command=compare_signs).pack()
ROOT_FRAME.pack()

ROOT.mainloop()
