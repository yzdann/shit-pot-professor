import uuid
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import get_object_or_404


class University(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Universities'


class Field(models.Model):
    name = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    slug = models.SlugField(max_length=5)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.area}"

    def get_absolute_url(self):
        return reverse('all', args=[str(self.slug)])

    @classmethod
    def name_and_area_by(cls, slug):
        field = get_object_or_404(Field, slug=slug)
        field_name = field.name
        field_area = field.area
        return field_name, field_area


class Professor(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    score = models.BigIntegerField(default=0)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
