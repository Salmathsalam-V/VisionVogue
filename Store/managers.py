from django.db import models
from . querysets import SoftDeleteQuerySet

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)

class AllObjectsManager(models.Manager):
    def get_queryset(self):
        return super(AllObjectsManager, self).get_queryset()