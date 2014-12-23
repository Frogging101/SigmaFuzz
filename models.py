from django.db import models
import datetime

# Create your models here.

class Submission(models.Model):
    archiveStatusStrings = [
            "Not archived",
            "Archived",
            "Archiving",
            "Failed",
            "Pending",
            "Retrying"]

    archiveStatusColours = [
        "#555555",
        "green",
        "white",
        "red",
        "yellow",
        "brown"]

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
    approved = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    
    archiveStatus = models.IntegerField(default=0)
    archiveException = models.CharField(max_length=255, null=True, blank=True)
    archiveStackTrace = models.TextField(null=True, blank=True)
    archiveDate = models.DateTimeField(null=True, blank=True)

    thumbnailed = models.BooleanField(default=False)

    def thumbPath(self):
        if not self.thumbnailed:
            return "/static/nothumb.png"
        else:
            return "/static/thumbs/"+str(self.id)+".jpg"

    def imagePath(self):
        if self.fileName is None:
            return "/static/notarchived.png"
        else:
            return "/static/content/"+self.fileName

    def imageLink(self):
        if self.fileName is None:
            return self.source
        else:
            return "/static/content/"+self.fileName

    def archiveStatusString(self):
        return self.archiveStatusStrings[self.archiveStatus]
    def archiveStatusColour(self):
        return self.archiveStatusColours[self.archiveStatus]
