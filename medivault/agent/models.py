from django.db import models
from accounts.models import Profile
# Create your models here.




class Agent(models.Model):
    name=models.CharField(max_length=30)
    profile=models.OneToOneField(Profile,on_delete=models.CASCADE,related_name='agent')
    created_at=models.DateTimeField(auto_now_add=True)
    memory=models.TextField(blank=True,null=True)


class HumanAIConversation(models.Model):
    sender=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='conversations')
    ai_agent=models.ForeignKey(Agent,on_delete=models.CASCADE,related_name='conversations')
    created_at=models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=30,blank=True,null=True)

    def __str__(self):
        return f'{self.sender.user.username} started {self.name}'



class Message(models.Model):
    sender=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='messages')
    SENDER=[
        ("human",'HUMAN'),
        ("agent","AGENT")
    ]
    sender_type=models.CharField(max_length=30,choices=SENDER,blank=True,null=True)
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.user.username}  text : {self.text[:50]}"
    




# class Agent2AgentConversation(models.Model):
#     name=models.CharField(max_length=30,blank=True,null=True)
#     sender=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='sender_agent_conversation')
#     reciever=models.ForeignKey(Profile,on_delete=models.CASCADE,)    
   
 
      