from django.db import models

class Users(models.Model):
    userName = models.CharField(max_length=256)

    class Meta(object):
        app_label = 'users'
        default_related_name = 'userName'

        def __unicode__(self):
            return self.userName
