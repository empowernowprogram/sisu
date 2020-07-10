from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from enumfields import EnumField
from enumfields import Enum
from django.conf import settings
#from django.contrib.auth.models import User

from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount, HitCountMixin

from users.models import CustomUser

# Create your models here.
class Category(Enum):
  Harassment = 'Harassment'; 
  Discrimination = 'Discrimination'; 
  Politics = 'Politics';
  Conflict = 'Conflict';
  Miscellaneous = 'Miscellaneous';
  
  class Labels:
    Discrimination = 'Discrimination'; 
    Harassment = 'Harassment';
    Politics = 'Politics';
    Conflict = 'Employee Conflicts';
    Miscellaneous = 'Other Issues';
    
  def get_label(cat_name):
      if cat_name == "Harassment":
        return Category.Harassment
      
      if cat_name == "Discrimination":
        return Category.Discrimination
      
      if cat_name == "Politics":
        return Category.Politics
      
      if cat_name == "Conflict":
        return Category.Conflict
              
      if cat_name == "Miscellaneous":
        return Category.Miscellaneous
    
    
@python_2_unicode_compatible  
class Post(models.Model, HitCountMixin):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  text = models.TextField()
  short_desc = models.TextField()
  published_date = models.DateTimeField(blank=True, null=True)
  created_date = models.DateTimeField(default=timezone.now)
  category_name = EnumField(Category, max_length=30, default=Category.Harassment)
  hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')
        
  def publish_post(self):
    self.published_date = timezone.now()
    self.save()
  
  def __str__(self):
    return self.title
    
class Comment(models.Model):
  post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
  userprofile = models.ForeignKey('users.UserProfile', default=1, on_delete=models.CASCADE)
  author = models.CharField(max_length=200)
  text = models.TextField()
  created_date = models.DateTimeField(default=timezone.now)
  approved_comment = models.BooleanField(default=False)
  rec_value = models.IntegerField(default=2)
  
  def approve(self):
    self.approved_comment = True
    self.save()
  
  def approved_comments(self):
    return self.comments.filter(approved_comment=True)
    
  def __str__(self):
    return self.text
    
  
class PostPreferrence(models.Model):
  username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
  postpk = models.ForeignKey(Post, on_delete=models.CASCADE)
  ip_address = models.CharField(max_length=40)
  vote_value = models.IntegerField(default=0) #1 = yes, 2 = no
  vote_date = models.DateTimeField(default=timezone.now)
  
  def __str__(self):
    return str(self.username) + str(self.ip_address) + str(self.postpk)
    
  class Meta:
    unique_together = ("username", "postpk", "ip_address")

class ReplyToComment(models.Model):
  post = models.ForeignKey('Post', related_name='commentPost', on_delete=models.CASCADE)
  comment = models.ForeignKey('Comment', related_name='replyToComment', on_delete=models.CASCADE)
  author = models.CharField(max_length=200)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
  userprofile = models.ForeignKey('users.UserProfile', default=1, on_delete=models.CASCADE)
  text = models.TextField()
  created_date = models.DateTimeField(default=timezone.now)
  approved_comment = models.BooleanField(default=False)
  
  def approve(self):
    self.approved_comment = True
    self.save()
  
  def approved_comments(self):
    return self.comments.filter(approved_comment=True)
    
  def __str__(self):
    return self.text

#For recommendation
class Cluster(models.Model):
  name = models.CharField(max_length=200)
  users = models.ManyToManyField(CustomUser)
  
  def get_members(self):
        return "\n".join([u.username for u in self.users.all()])
 
class Resource(models.Model):
  title = models.CharField(max_length=200)
  category_name = EnumField(Category, max_length=30, default=Category.Harassment)
  res_url = models.URLField(max_length=250)      
  
  def __str__(self):
    return self.title