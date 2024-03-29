from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    isAdmin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'first_name: {self.first_name}, last_name: {self.last_name}, email: {self.email}'

class File(models.Model):
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="files", on_delete=models.CASCADE)

class Report(models.Model):
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name="reports", on_delete=models.CASCADE)
    file = models.ForeignKey(File, related_name="reports", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    content = models.TextField()
    path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)

