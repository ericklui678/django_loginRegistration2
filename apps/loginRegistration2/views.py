from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

def index(request):
    print User.objects.all()
    return render(request, 'loginRegistration2/index.html')

def create(request):
    postData = {
        'first_name': request.POST['first_name'],
        'last_name': request.POST['last_name'],
        'email': request.POST['email'],
        'password': request.POST['password'],
        'confirm': request.POST['confirm'],
    }
    errors = User.objects.register(postData)
    if len(errors) == 0:
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['name'] = postData['first_name']
        return redirect('/success')
    else:
        for error in errors:
            messages.info(request, error)
        return redirect('/')

def login(request):
    postData = {
        'email': request.POST['email'],
        'password': request.POST['password']
    }
    errors = User.objects.login(postData)
    if len(errors) == 0:
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['name'] = User.objects.filter(email=postData['email'])[0].first_name
        return redirect('/success')
    for error in errors:
        messages.info(request, error)
    return redirect('/')

def success(request):
    context = {'users': User.objects.all().order_by('-created_at')}
    return render(request, 'loginRegistration2/success.html', context)
