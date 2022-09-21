from django.db import models
from group.models import Group


class Expense(models.Model):
    expensename = models.CharField(db_column='expenseName', max_length=100)
    totalamount = models.IntegerField(db_column='totalAmount')
    addedby = models.IntegerField(db_column='addedBy')
    createdtime = models.DateTimeField(db_column='createdTime')
    deletedby = models.IntegerField(db_column='deletedBy', blank=True, null=True)
    deletedat = models.DateTimeField(db_column='deletedAt', blank=True, null=True)
    issettled = models.IntegerField(db_column='isSettled')
    is_active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expense'


class ExpenseGroupUser(models.Model):
    expenseid = models.ForeignKey(Expense, models.CASCADE, db_column='expenseId')
    groupid = models.ForeignKey(Group, models.CASCADE, db_column='groupId', null=True)
    paidby = models.IntegerField(db_column='paidBy')
    amountshared = models.IntegerField(db_column='amountShared')
    amountowedby = models.IntegerField(db_column='amountOwedBy')
    issettled = models.IntegerField(db_column='isSettled', blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expense_group_user'
