from celery import Celery
import re
import shutil
import urllib2
import imghdr
import sys
import os
import traceback
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sf_site.settings')

from sigmafuzz.models import Submission
from sigmafuzz.scrapers import furaffinity
import sigmafuzz.tasks.thumbs_tasks

app = Celery('sf_tasks', broker='amqp://guest@localhost//', backend="amqp")

app.conf.update(CELERY_ROUTES={'sigmafuzz.tasks.thumbs_tasks.genThumb': {'queue': 'thumbs'}})

@app.task(rate_limit="0.5/s")
def archiveImg(subID):
    submission = Submission.objects.all().get(id=subID)
    if submission.archiveStatus == 1 and os.path.exists("/var/www/sigmafuzz/static/content/"+str(submission.fileName)):
        return 1
    try:
        submission.archiveStatus = 2
        submission.archiveException = None
        submission.archiveStackTrace = None
        submission.save()
        pattern = r"[^0-9A-Za-z.~]"
        artist = re.sub(pattern,'_',str(submission.artist))
        title = re.sub(pattern,'_',str(submission.title))

        try: #Try and get it from the thumbnail site in case it's there already
            req = urllib2.Request("http://thumbs.sigmafuzz.net/dl/"+str(subID),headers={"User-Agent": "SigmaFuzz/dev (+http://www.sigmafuzz.net/bot)"})
            resp = urllib2.urlopen(req)
        except:
            req = urllib2.Request(submission.imgSource,headers={"User-Agent": "SigmaFuzz/dev (+http://www.sigmafuzz.net/bot)"})
            try:
                resp = urllib2.urlopen(req)
            except urllib2.HTTPError as e:
                submission.archiveStatus = 3
                submission.archiveException = "HTTP Error "+str(e.code)
                submission.save()
                return 0
        respdata = resp.read()
        extension = imghdr.what('',respdata)
        if extension is None:
            submission.archiveStatus = 3
            submission.archiveException = "File type indeterminate"
            submission.save()
            return 0
        elif extension == "jpeg":
            extension = "jpg"

        filename = artist+'-'+title+'-sf'+str(subID)+'.'+extension
        outFile = open("/var/www/sigmafuzz/static/content/"+filename,'wb')
        outFile.write(respdata)
        outFile.close()
        os.chmod("/var/www/sigmafuzz/static/content/"+filename,0644)
        submission.fileName = filename
        submission.archiveStatus = 1
        submission.save()
    except:
        exc_type = sys.exc_info()[0]
        submission.archiveStackTrace = "".join(traceback.format_exc())
        submission.archiveStatus = 3
        submission.archiveException = exc_type.__name__
        submission.save()

@app.task(rate_limit="2/s")
def FA_indexSubmission(ID):
    subDict = furaffinity.scrapeSubmission(ID)
    newSub = Submission(**subDict)
    newSub.submitter = "SigmaFuzz"
    newSub.save()
    genThumb.delay(newSub.id)

@app.task
def testTask(arg1, arg2):
    time.sleep(30)
    return arg1+arg2

def FA_indexArtist(artist):
    IDs = furaffinity.IDsFromGallery(artist)
    for ID in IDs:
        FA_indexSubmission.delay(ID)

@app.task
def genThumb(subID):
    if os.path.exists("/var/www/sigmafuzz/static/thumbs/"+str(subID)+".jpg"):
        return
    submission = Submission.objects.all().get(id=subID)
    result = sigmafuzz.tasks.thumbs_tasks.genThumb.delay(submission.imgSource,subID)
    retval = result.get()

    req = urllib2.Request(retval,headers={"User-Agent": "SigmaFuzz/dev (+http://www.sigmafuzz.net/bot)"})
    resp = urllib2.urlopen(req)

    data = resp.read()
    o = open('/var/www/sigmafuzz/static/thumbs/'+str(subID)+".jpg",'wb')
    o.write(data)
    o.close()
    os.chmod("/var/www/sigmafuzz/static/thumbs/"+str(subID)+".jpg",0644)

    submission.thumbnailed = True
    submission.save()
