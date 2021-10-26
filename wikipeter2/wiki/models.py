from typing import Any, Dict, Tuple
from django.db import models
from django.contrib.auth.models import User
from django.db.models import constraints
from django.db.models.constraints import CheckConstraint
from django.urls import reverse

from time import time

# Create your models here.

class Class(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_created = models.DateField(auto_now_add=True, null=False)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("class-detail", kwargs={'class_id': self.id})

    class Meta:
        verbose_name = "Klasse"


class ClassCategory(models.Model):
    # combination of title and target_class is unique
    title = models.CharField(max_length=155)
    target_class = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="Klasse")
    date_created = models.DateField(auto_now_add=True, null=False)

    def __str__(self) -> str:
        return self.target_class.name + " - " + self.title

    def get_absolute_url(self):
        return reverse("category-detail", kwargs={'category_id': self.pk})

    class Meta:
        verbose_name = "Kategorie"
        constraints = [
            models.UniqueConstraint(fields=['title', 'target_class'], name="unique_category_in_class")
        ]
    


class MasterCategory(models.Model):
    title = models.CharField(max_length=100, unique=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("master-category-detail", kwargs={"master_category_id": self.pk})

    class Meta:
        verbose_name = "Haupt-Kategorie"


# TODO: add random numbers after filename in uploads 
# dir to avoid hackers do download files on trys 
# and don't leak files of some unpublished posts
class WikiFile(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Name")
    upload_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Datei"
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        # no detail view avail...
        return reverse("members-files")


class Post(models.Model):
    title = models.CharField(max_length=255, null=False, default="", verbose_name="Titel")
    # on_delete=models.CASCADE will delete all posts if user(author) has been deleted
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ClassCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kategorie")
    master_category = models.ForeignKey(MasterCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Haupt-Kategorie")
    short_description = models.TextField(null=False, default="", verbose_name="Kurzbeschreibung")
    content = models.TextField(null=False, default="", verbose_name="Inhalt")
    post_date = models.DateField(auto_now_add=True, null=False)

    def author_full_name(self) -> str:
        # why does + " " + self.author.last_name not work ??
        return self.author.first_name + " " + self.author.last_name

    def __str__(self) -> str:
        return self.title

    def __eq__(self, o: object) -> bool:
        if type(o) == type(Post):
            return self.pk == o.pk
        else:
            return False    

    # why do i have to implement this method, and is it right how i've done this
    def __hash__(self) -> int:
        return (self.title, self.post_date, self.short_description).__hash__()

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Beitrag"
        constraints = [
            models.UniqueConstraint(fields=['title', 'category'], name="unique_post_in_category"),
            models.UniqueConstraint(fields=['title', 'master_category'], name="unique_post_in_master_category")
        ]


class WikiPostFile(models.Model):
    wiki_file = models.ForeignKey(WikiFile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    #def delete(self, using: Any, keep_parents: bool) -> Tuple[int, Dict[str, int]]:
    #    self.wiki_file.delete()
    #       return super().delete(using=using, keep_parents=keep_parents)

    def __str__(self) -> str:
        return self.wiki_file.name

    def get_absolute_url(self):
        # no detail view avail...
        return reverse("members-files")


class SpecialSiteContent(models.Model):
    site_name = models.CharField(primary_key=True, unique=True, max_length=255)
    content = models.TextField(null=False, verbose_name='Inhalt')

    def __str__(self) -> str:
        return self.site_name
