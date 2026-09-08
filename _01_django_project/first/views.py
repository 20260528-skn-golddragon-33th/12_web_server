from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse('Hello, world!')

def greeting(request):
    return HttpResponse(f'<h1>사람이 미래다</h1>')

def foo(request):
    return HttpResponse('<h1>🦑Foooooooooooooooooooo🦑</h1>')


def bar(request):
    return HttpResponse('''
    <html>
    <head>
      <title>🐳Bar Page🐳</title>
    </head>
    <body>
      <h1>🐳Bar Page🐳</h1>
      <p>🐳This is a bar page🐳</p>
    </body>
    </html>
    ''')