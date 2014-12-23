from django.shortcuts import render
from django.template import loader,Context,RequestContext
from django.http import HttpResponse,Http404,HttpResponseForbidden,HttpResponseNotAllowed
from django.forms import ModelForm
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie

from sigmafuzz.models import Submission
import sigmafuzz.tasks.sf_tasks

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

@ensure_csrf_cookie
def index(request,page):
    perPage = 100 #this should be centrally configured at some point

    if page == '':
        page = 0
    else:
        page = max(0,int(page)-1)

    submissions = Submission.objects.all().order_by('-id')
    start = page*perPage
    end = (page+1)*perPage

    if request.GET.get('napp') == 'on':
        napp = "checked"
    else:
        napp = ""
    if request.GET.get('narc') == 'on' or 'opt' not in request.GET:
        narc = "checked"
    else:
        narc = ""

    if narc != "checked":
        submissions = submissions.filter(archiveStatus=1)
    if napp != "checked":
        submissions = submissions.filter(approved=True)

    template = loader.get_template('sigmafuzz/index.html')
    return HttpResponse(template.render(RequestContext(
        request,{'submissionList': submissions[start:end],
            'page': page,
            'napp': napp,
            'narc': narc,
            'get': request.GET})))

def submit(request):
    if request.method == 'POST':
        if "submit" in request.POST:
            form = SubmitForm(request.POST)
            form.is_valid()
            form.save()
            return HttpResponse("success",content_type="text/plain")
        
        elif "fa_crawl_artist" in request.POST and request.user.is_superuser:
            ca = sigmafuzz.tasks.sf_tasks.FA_indexArtist(request.POST["artist"])
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

def submissionArchival(request,subID):
    try:
        submission = Submission.objects.all().get(id=subID)
    except Submission.DoesNotExist:
        raise Http404

    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    if request.user.is_superuser:
        response = HttpResponse(content="", status=303)
        response["Location"] = "http://"+request.META['HTTP_HOST']+"/s/"+str(subID)

        if request.POST.get("set") == "true" or request.POST.get("set") is None:
            sigmafuzz.tasks.sf_tasks.archiveImg.delay(subID)
        elif request.POST.get("set") == "false":
            pass #Unarchive
        elif request.POST.get("set") is None: #Already caught above, but ultimately should be caught here
            pass
        return response
    else:
        return HttpResponseForbidden()

def submissionApproval(request,subID):
    try:
        submission = Submission.objects.all().get(id=subID)
    except Submission.DoesNotExist:
        raise Http404

    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    if request.user.is_superuser:
        response = HttpResponse(content="", status=303)
        response["Location"] = "http://"+request.META['HTTP_HOST']+"/s/"+str(subID)

        if request.POST.get("set") == "true":
            submission.approved = True
        elif request.POST.get("set") == "false":
            submission.approved = False
        else:
            submission.approved = not submission.approved
        submission.save()
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
            if 'test' in request.POST:
                sigmafuzz.tasks.sf_tasks.testTask(1,2)
            elif 'genthumb' in request.POST:
                sigmafuzz.tasks.sf_tasks.genThumb.delay(request.POST['id'])

    template = loader.get_template('sigmafuzz/tasks.html')
    i = inspect()
    workers = i.stats().keys()
    if len(workers) > 1:
        pass #warning maybe

    active = i.active()[workers[0]]
    reserved = i.reserved()[workers[0]]
    scheduled = [e['request'] for e in i.scheduled()[workers[0]]]

    pending = reserved+scheduled

    return HttpResponse(template.render(RequestContext(request,{"active": active, "pending": pending})))
