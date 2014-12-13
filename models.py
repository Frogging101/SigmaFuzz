from django.db import models
import datetime

# Create your models here.

class Submission(models.Model):
    title = models.CharField(max_length=255)
    submissionDate = models.DateTimeField(default=datetime.datetime(2034,01,18,23,40))
    indexDate = models.DateTimeField(auto_now_add=True)
    #Rating
    artist = models.CharField(max_length=255)
    submitter = models.CharField(max_length=255) #Users later maybe
    #Tags
    description = models.TextField()
    source = models.URLField()
    imgSource = models.URLField()
    fileName = models.CharField(max_length=255,blank=True,null=True)
    #File size
    #Approved
    
    def thumbPath(self):
        if self.fileName is None:
            return "/static/nothumb.png"
        else:
            return "/static/thumbs/"+thumbPath
