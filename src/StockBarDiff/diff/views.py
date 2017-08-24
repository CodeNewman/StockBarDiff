from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from stockbar_10jqka.line.stock_bar_query import *
import json

def query(request):
    query = stock_bar_query()
    val = query.query('600000',year='2017')
    p = val['stock_code']

    return HttpResponse(p)