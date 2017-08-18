from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from time import gmtime, strftime, localtime
from django.contrib import messages
from models import * # Need this in order to run queries
from django.core.urlresolvers import reverse
import bcrypt


def index(request):
    print request.session.values()
    return render(request, 'logreg/index.html')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect(reverse('index'))
        else:
            request.session['user_id'] = User.objects.get(email = request.POST['user_email']).id
            messages.add_message(request, messages.INFO, 'Successfully Logged In!')
            return redirect(reverse('success'))
    else:        
        return redirect(reverse('index'))


def register(request):
        if request.method == "POST":
            errors = User.objects.reg_validator(request.POST)
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect(reverse('index'))
            else:
                messages.add_message(request, messages.INFO, 'Successfully registered!')

                new_user = User()
                new_user.first_name = request.POST["f_name"]
                new_user.last_name = request.POST["l_name"]
                new_user.email = request.POST["user_email"]
                new_user.password = bcrypt.hashpw(request.POST["pass"].encode(), bcrypt.gensalt())
                new_user.save()

                #since INSERT returns last row id we set this equal to session to log in
                request.session['user_id'] = User.objects.get(email = request.POST['user_email']).id
                print User.objects.last().id
                print User.objects.get(email = request.POST['user_email']).id
                return redirect(reverse('success'))
        else:        
            return redirect(reverse('index'))

    
def success(request):
    if 'user_id' in request.session:
        context = {
            "loggedin_user" : User.objects.get(id = request.session['user_id'])
        }
        print request.session.values()
        return render(request, 'logreg/success.html', context)
    else:
        return redirect(reverse('index'))

def logout(request):
    try:
        request.session.clear()
        return redirect(reverse('index'))
    except:
        return redirect(reverse('index'))

