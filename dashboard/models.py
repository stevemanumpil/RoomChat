from django.db import models
from landing.models import Account

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    participant = models.ManyToManyField(Account, related_name='room_participant')

    ROOM_TYPE = [
        ('Pr','Private'),
        ('Gr','Group'),
    ]

    tipe = models.CharField(
        max_length=255,
        choices=ROOM_TYPE,
        default='Pr'
    )

    def __str__(self):
        return f"{self.name}"

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='message_room')
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='message_sender')
    text = models.TextField()
    date_send = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text}"

# class Group(models.Model):
#     group_name = models.CharField(max_length=255)
#     group_photo = models.ImageField()
#     created_date = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who_create_the_group')
#     member = models.ManyToManyField(User, related_name='group_member')

#     def __str__(self):
#         return f"{self.group_name}"

# class PersonalChat(models.Model):
#     user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='person._1_or_2')
#     user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='person_2_or_1')

#     def __str__(self):
#         return f"{self.user1}, {self.user2}"

# class Message(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     text = models.TextField()
#     date_send = models.DateTimeField(auto_now_add=True)
#     group_id = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
#     pc_id = models.ForeignKey(PersonalChat, on_delete=models.CASCADE, blank=True, null=True)

#     def __str__(self):
#         return f"{self.text}"