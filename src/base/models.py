from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null= True)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank= True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    #Setting the foreign key: messages being child to Room model; on_delete=models.CASCADE means if the parent model is deleted, all the Messages in that ROoom gets deleted too
    body= models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.body[0:50]
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default= 'default.jpg', upload_to='profile-pics')

    def __str__(self):
        return f'{self.user.username} Profile'


