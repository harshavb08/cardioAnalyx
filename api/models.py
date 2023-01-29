from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

 
def logged_user(request):
    current_user = request.user 
    return current_user

class Tag(models.Model):
    name = models.CharField(max_length=250)
    parent = models.ManyToManyField("Tag", related_name="parent_tag", blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Lieux(models.Model):
    name = models.CharField(max_length=250)
    parent = models.ManyToManyField("Lieux", related_name="parent_location", blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Categorie(models.Model):
    name = models.CharField(max_length=250)
    parent = models.ManyToManyField("Categorie", related_name="parent_categorie", blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Photo(models.Model):
    url = models.CharField(max_length=300)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.url

class Author(models.Model):
    firstname = models.CharField(max_length=155, null=True, blank=True)
    lastname = models.CharField(max_length=155, null=True, blank=True)
    temp_name = models.CharField(max_length=155, null=True, blank=True)
    facebook_id = models.CharField(max_length=155, null=True, blank=True)
    profile_photo = models.ForeignKey("Photo", on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.temp_name

        
class Annonce(models.Model):
    titre = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    prix = models.CharField(max_length=100, null=True, blank=True)
    contacts = models.CharField(max_length=300)
    categorie = models.ManyToManyField("Categorie", related_name="categorie", blank=True)
    tag = models.ManyToManyField("Tag", related_name="tag", blank=True)
    lieux = models.ManyToManyField("Lieux", related_name="lieux", blank=True)
    photo = models.ManyToManyField("Photo", related_name="photo", blank=True)
    author = models.ForeignKey("Author", on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.titre

