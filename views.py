from django.shortcuts import render
from django.template import loader,Context,RequestContext
from django.http import HttpResponse,Http404
from django.forms import ModelForm
from django.contrib.auth import authenticate, login

from sigmafuzz.models import Submission
import sigmafuzz.tasks

from celery.task.control import inspect

import datetime

class SubmitForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['title','artist','submitter','description','source','imgSource']
        labels = {'imgSource': u'Direct Image URL',}

# Create your views here.

def splash(request):
    template = loader.get_template('sigmafuzz/splash.html')
    return HttpResponse(template.render(Context({'timestamp': datetime.datetime.now().isoformat(' ')})))

def index(request):
    submissionList = Submission.objects.all()
    template = loader.get_template('sigmafuzz/index.html')
    return HttpResponse(template.render(RequestContext(request,{'submissionList': submissionList})))

def submit(request):
    if request.method == 'POST':
        form = SubmitForm(request.POST)
        form.is_valid()
        form.save()
        return HttpResponse("success",content_type="text/plain")
    else:
        template = loader.get_template('sigmafuzz/submit.html')
        form = SubmitForm()
        return HttpResponse(template.render(RequestContext(request,{'form': form.as_table()})))

def submissionView(request,subID):
    try:
        submission = Submission.objects.all().get(id=subID)
    except Submission.DoesNotExist:
        raise Http404
    template = loader.get_template('sigmafuzz/submission.html')
    return HttpResponse(template.render(RequestContext(request,{'submission': submission})))

def submissionArchive(request,subID):
    try:
        submission = Submission.objects.all().get(id=subID)
    except Submission.DoesNotExist:
        raise Http404
    sigmafuzz.tasks.archiveImg.delay(subID)
    response = HttpResponse(content="", status=303)
    response["Location"] = "http://"+request.META['HTTP_HOST']+"/s/"+str(subID)
    return response

def submissionArchiveErr(request,subID):
    try:
        submission = Submission.objects.all().get(id=subID)
    except Submission.DoesNotExist:
        raise Http404

    if submission.archiveStackTrace is not None:
        return HttpResponse(submission.archiveStackTrace,content_type="text/plain")
    else:
        return HttpResponse("No error.",content_type="text/plain")

def about(request):
    template = loader.get_template('sigmafuzz/about.html')
    return HttpResponse(template.render(RequestContext(request,{})))

def bot(request):
    template = loader.get_template('sigmafuzz/bot.html')
    return HttpResponse(template.render(RequestContext(request,{})))

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

#        if username is None or password is None:
#            return HttpResponse(template.render(RequestContext(request

        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            resp = HttpResponse(content="", status=303)
            resp["Location"] = "http://"+request.META['HTTP_HOST']+"/index/"
            return resp
        else:
            template=loader.get_template('sigmafuzz/login.html')
            return HttpResponse(template.render(RequestContext(request,{"error": "Invalid username or password"})))
    else:
        template = loader.get_template('sigmafuzz/login.html')
        return HttpResponse(template.render(RequestContext(request,{})))

def tasks(request):
    if request.method == "POST":
        if request.user.is_authenticated():
            sigmafuzz.tasks.testTask.delay(1,2)

    template = loader.get_template('sigmafuzz/tasks.html')
    i = inspect()
    workers = i.stats().keys()
    if len(workers) > 1:
        pass #warning maybe

    active = i.active()[workers[0]]
    reserved = i.reserved()[workers[0]]

    return HttpResponse(template.render(RequestContext(request,{"active": active, "reserved": reserved})))
