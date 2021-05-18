from django.db import models
from django.conf import settings
from django.utils.text import slugify


# Create your models here.
class Image(models.Model):
    # User object that bookmarked image FK one to many,a user can post multiple image, each image posted by single user.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="images_created",
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to="images/%Y/%m/%d/")
    description = models.TextField(blank=True)
    created = models.DateField(
        auto_now_add=True, db_index=True
    )  # Database index created for this field
    """
    Consider setting db_index=True for fields that you query frequently using filter(),
    exclude(), order_by(). ForeignKey fields or fields with unique = True imply creation of an index.
    """
    # Many to Many Relationship
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="images_liked", blank=True
    )
    """
    When you define a ManyToManyField, Django creates an intermediary join table using the primary keys of 
    both models. The ManyToManyField can be defined in either of the two related models.
    
    The relationship can be named. 
    """

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Generate slug automatically
        super().save(*args, **kwargs)
