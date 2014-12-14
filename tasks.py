from celery import Celery
import re
import shutil
import urllib2
import imghdr
import sys

app = Celery('sf_tasks', broker='amqp://guest@localhost//')

@app.task
def archiveImg(submission):
    try:
        pattern = r"[^0-9A-Za-z.~]"
        artist = re.sub(pattern,'_',str(submission.artist))
        title = re.sub(pattern,'_',str(submission.title))
        subID = str(submission.id)

        try:
            resp = urllib2.urlopen(submission.imgSource)
        except urllib2.HTTPError:
            submission.archiveStatus = 3
            submission.archiveException = "HTTP Error "+str(resp.code)
            submission.save()
            return 0
        respdata = resp.read()
        extension = imghdr.what('',tempfiledata)
        if extension is None:
            submission.archiveStatus = 3
            submission.archiveException = "File type indeterminate"
            submission.save()
            return 0
        elif extension == "jpeg":
            extension = "jpg"

        filename = artist+'-'+title+'sf'+subID+'.'+extension
        shutil.move(tempfile,"/var/www/sigmafuzz/static/content/"+filename)
        submission.filename = filename
        submission.archiveStatus = 1
        submission.save()
    except:
        exc_type, exc_obj = sys.exc_info()[:2]
        submission.archiveStatus = 3
        submission.archiveException = exc_type.__name__
        submission.save()
