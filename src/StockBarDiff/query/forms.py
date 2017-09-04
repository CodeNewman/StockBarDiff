'''
Created on Aug 30, 2017

@author: Coder_J
'''
from django import forms

class AddForm(forms.Form):
    '''
    classdocs
    '''

    rate = forms.FloatField()
