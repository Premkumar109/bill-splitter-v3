from django.db import models
from utils.helpers import validate_email


class User(models.Model):
    googleid = models.CharField(db_column='googleId', max_length=45, blank=True, null=True)
    firstname = models.CharField(db_column='firstName', max_length=45, blank=True, null=True)
    lastname = models.CharField(db_column='lastName', max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45)
    pictureurl = models.CharField(db_column='pictureUrl', max_length=300, blank=True, null=True)
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user'

    def save(self, *args, **kwargs):
        if validate_email(email=self.email):
            super(User, self).save(*args, **kwargs)
            return True
        else:
            return False

    def update(self, **kwargs):
        if 'email' in kwargs and validate_email(kwargs['email']):
            super(User, self).update(**kwargs)
            return True
        elif 'email' not in kwargs:
            super(User, self).update(**kwargs)
            return True
        else:
            return False
