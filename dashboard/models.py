from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Group(models.Model):
    group_name = models.CharField(max_length=255)
    group_photo = models.ImageField()
    created_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who_create_the_group')
    member = models.ManyToManyField(User, related_name='group_member')

    def __str__(self):
        return f"{self.group_name}"

class PersonalChat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='person_1_or_2')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='person_2_or_1')

    def __str__(self):
        return f"{self.user1}, {self.user2}"

class Message(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_send = models.DateTimeField()
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    pc_id = models.ForeignKey(PersonalChat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text}"