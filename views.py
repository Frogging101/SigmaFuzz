from django.shortcuts import render
from django.template import loader,Context,RequestContext
from django.http import HttpResponse
from django.forms import ModelForm

from sigmafuzz.models import Submission

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

def doSubmit(request):
    pass
