from django.db import models
from users.models import User
from django.utils import timezone




class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    isbn = models.CharField(max_length=14)
    cover_pic = models.ImageField(upload_to="book_pics")

    def __str__(self):
        return self.title 
    


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    star = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return str(self.star)

