from django.db import models
from django.db import connection

# Create your models here.

#cursor = connection.cursor()

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()
    
    def __unicode__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()
    
    def __unicode__(self):
        return self.title
 
############################


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    duration = models.IntegerField()
    creator_email = models.EmailField()     
       
    def __unicode__(self): 
        return self.name

    
class User(models.Model):
    email = models.EmailField()     
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    device_id = models.CharField(max_length=200)
       
    def __unicode__(self): 
        return (self.first_name + self.last_name)
    
    
class Event_User(models.Model):
    user_id = models.ForeignKey(User) 
    event_id =  models.ForeignKey(Event) 
   
    def __unicode__(self): 
        return (self)
    
    
class Event_Times(models.Model):
    event_id = models.ForeignKey(Event) 
    open_time_slots = models.DateTimeField()
    open_dates = models.DateTimeField()
    
    def __unicode__(self): 
        return (self)