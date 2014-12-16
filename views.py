from django.shortcuts import render
from django.template import loader,Context,RequestContext
from django.http import HttpResponse,Http404
from django.forms import ModelForm

from sigmafuzz.models import Submission
import sigmafuzz.tasks as tasks

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
    return HttpResponse(template.render(Context({'submissionList': submissionList})))

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
    return HttpResponse(template.render(Context({'submission': submission})))

def submissionArchive(request,subID):
    try:
        submission = Submission.objects.all().get(id=subID)
    except Submission.DoesNotExist:
        raise Http404
    tasks.archiveImg.delay(subID)
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
    return HttpResponse(template.render(Context({})))

def bot(request):
    template = loader.get_template('sigmafuzz/bot.html')
    return HttpResponse(template.render(Context({})))
