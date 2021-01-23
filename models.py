from django.conf import settings
from django.db import models
from django.utils import timezone
# Create your models here.
class Book(models.Model):
    isbn = models.CharField(max_length=30)
    title  = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.IntegerField()


class Comment(models.Model):
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    rating = models.FloatField()
    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text   


class Record(models.Model):
    commented =  models.BooleanField(default=False)
    book_key = models.ForeignKey('book.Book', on_delete=models.CASCADE, related_name='record')       
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)