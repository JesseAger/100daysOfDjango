from django.db import models

# Create your models here.

class Room(models.Model):
    # host =
    # topic =
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank= True)
    # participants =
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
class Message(models.Model):
    # user =
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    #Setting the foreign key: messages being child to Room model; on_delete=models.CASCADE means if the parent model is deleted, all the Messages in that ROoom gets deleted too
    body= models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body[0:50]


