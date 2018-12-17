from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    class Meta:
        verbose_name_plural = "Categories"

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    name = models.CharField(max_length=55)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.name)


class Budget(models.Model):
    name = models.CharField(max_length=55)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.name)


class Operation(models.Model):
    datetime = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    parent_budget = models.ForeignKey(Budget,
                                      on_delete=models.DO_NOTHING,
                                      null=True,
                                      blank=True,
                                      related_name='parent_budget')

    child_budget = models.ForeignKey(Budget,
                                     on_delete=models.DO_NOTHING,
                                     null=True,
                                     blank=True,
                                     related_name='child_budget')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(max_length=250, null=True, blank=True)

    def __str__(self):
        return str(self.pk)
