from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.
def index(request):
    # return redirect('index')
    return render(request, 'tabletest/index.html')


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")