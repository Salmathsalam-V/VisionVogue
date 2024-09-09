from django.db import models

class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        self.update(is_deleted=True)

    def hard_delete(self):
        super(SoftDeleteQuerySet, self).delete()
