from django.db import models
from django.conf import settings
from django.utils import timezone


class Categories(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_global = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Categories"
        unique_together = ("user", "name")

    def __str__(self):
        return f"{self.name}"
    


class Subjects(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = 'Subject'
        verbose_name_plural = "Subjects"
        unique_together = ("user", "name")

    def __str__(self):
        return f"{self.name} created by ({self.user.full_name})"
    

    
class Topic(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    total_revisions = models.PositiveIntegerField(default=0)
    last_revised = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = 'Topic'
        unique_together = ("subject", "title")

    def __str__(self):
        return f"{self.title}"
    

class RevisionLog(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="revision_log")
    revised_at = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-revised_at"]
        verbose_name = 'Revision Log'
        verbose_name_plural = "Revision Logs"

    def __str__(self):
        return f"From Subject : {self.topic.subject.name} Topic {self.topic.title} - {self.revised_at}"




