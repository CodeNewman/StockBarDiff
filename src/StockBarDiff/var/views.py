from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def do_work(request):
    '''    '''
    return HttpResponse("Hello")
#     args = {
# #         'index':'index',
# #         'code':'code',
#         'result':'result'
#         }
#     return render(request, 'var.html', args)