from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.conf import settings

def register(request):
    form = UserCreationForm()
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            auth.login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render_to_response('registration/registration_form.html', {'form': form}, RequestContext(request),)


