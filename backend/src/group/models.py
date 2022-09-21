from django.db import models
from user.models import User

# Create your models here.
class GroupType(models.Model):
    grouptype = models.CharField(db_column='groupType', max_length=45)

    class Meta:
        managed = False
        db_table = 'group_type'


class Group(models.Model):
    groupname = models.CharField(db_column='groupName', max_length=45, blank=True, null=True)
    grouppurpose = models.CharField(db_column='groupPurpose', max_length=200, blank=True, null=True)
    grouptype = models.OneToOneField(GroupType, db_column='groupType', on_delete=models.CASCADE)
    createdat = models.DateTimeField(db_column='createdAt')
    deletedat = models.DateTimeField(db_column='deletedAt', blank=True, null=True)
    createdby = models.OneToOneField(User, db_column='createdBy', on_delete=models.CASCADE)
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'group'


class GroupToUser(models.Model):
    groupid = models.OneToOneField(Group, db_column='groupId', on_delete=models.CASCADE)
    userid = models.OneToOneField(User, db_column='userId', on_delete=models.CASCADE)
    isactive = models.IntegerField(db_column='isActive', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_to_user'
