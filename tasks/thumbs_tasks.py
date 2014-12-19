from celery import Celery
import urllib2
import subprocess
import os

app = Celery('thumbs_tasks', backend="amqp")

app.conf.update(CELERY_ROUTES={'sigmafuzz.tasks.thumbs_tasks.genThumb': {'queue': 'thumbs'}})

#Generates a thumbnail and puts it in a directory
#Where a webserver should expose it, at the following
#URL:
URL = "http://thumbs.sigmafuzz.net/"
thumbsURL = URL+"thumbs/"

#Original files are kept here
dlURL = URL+"dl/"
#Up to this many:
dlKeep = 2000

#FS directory where the stuff goes
webroot = "/var/www/sf_thumbs/"
webroot_dl = webroot+"dl/"
webroot_thumbs = webroot+"thumbs/"

@app.task
def genThumb(imageURL,subID):
    if not os.path.exists(webroot_dl):
        os.makedirs(webroot_dl)
        os.chmod(webroot_dl, 0755)
    if not os.path.exists(webroot_thumbs):
        os.makedirs(webroot_thumbs)
        os.chmod(webroot_thumbs, 0755)

    if not os.path.exists(webroot_dl+str(subID)):
        req = urllib2.Request(imageURL,headers={"User-Agent": "SigmaFuzz/dev (+http://www.sigmafuzz.net/bot)"})
        resp = urllib2.urlopen(req)
        data = resp.read()

        o = open(webroot_dl+str(subID),'wb')
        o.write(data)
        o.close()
    if not os.path.exists(webroot_thumbs+str(subID)+".jpg"):
        subprocess.call(["convert",webroot_dl+str(subID),"-resize","250x170",webroot_thumbs+str(subID)+".jpg"])
    return thumbsURL+str(subID)+".jpg"
