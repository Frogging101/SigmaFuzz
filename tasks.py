from celery import Celery
import re
import shutil
import urllib2
import imghdr
import sys
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sf_site.settings')

from sigmafuzz.models import Submission

app = Celery('sf_tasks', broker='amqp://guest@localhost//')

@app.task
def archiveImg(subID):
    submission = Submission.objects.all().get(id=subID)
    if submission.archiveStatus == 1 or submission.archiveStatus == 2:
        return 1
    try:
        submission.archiveStatus = 2
        submission.save()
        pattern = r"[^0-9A-Za-z.~]"
        artist = re.sub(pattern,'_',str(submission.artist))
        title = re.sub(pattern,'_',str(submission.title))

        try:
            resp = urllib2.urlopen(submission.imgSource)
        except urllib2.HTTPError:
            submission.archiveStatus = 3
            submission.archiveException = "HTTP Error "+str(resp.code)
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

        filename = artist+'-'+title+'sf'+subID+'.'+extension
        outFile = open("/var/www/sigmafuzz/static/content/"+filename,'wb')
        outFile.write(respdata)
        outFile.close()
        submission.filename = filename
        submission.archiveStatus = 1
        submission.save()
    except:
        exc_type, exc_obj = sys.exc_info()[:2]
        submission.archiveStatus = 3
        submission.archiveException = exc_type.__name__
        submission.save()
