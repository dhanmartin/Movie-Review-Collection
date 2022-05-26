from jsonfield import JSONField
from django.db import models
from django.conf import settings

class Bookmark(models.Model):
    class Meta:
        app_label = "app"
        db_table = "bookmark"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    folder = models.ForeignKey("Bookmark_folder", on_delete = models.CASCADE)
    data = JSONField(default=dict)


class Bookmark_folder(models.Model):
    class Meta:
        app_label = "app"
        db_table = "bookmark_folder"
        unique_together = ("user","name")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    name = models.CharField(max_length = 255)
