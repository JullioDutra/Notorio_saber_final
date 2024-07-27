# models.py

from django.db import models

class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel_images/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.caption if self.caption else f"Image {self.id}"
