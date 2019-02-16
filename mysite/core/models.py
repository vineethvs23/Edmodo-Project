from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

""" Classroom:  this class is model to store classroom names or classroom for different subjects
				it has only one column, that is called classname
	Newpost:	This is a model which stores the details of a post that a user does, this has 5 columns which are author,
				title, body of post , timestap and to which classroom it is from. NOTE: classroom is a foreign key, it it 
				added to this model from the Classroom model			"""



class College(models.Model):

	college_name = models.CharField(max_length=400,blank=True)
	invite_code = models.CharField(max_length=100,blank=True)

class Classroom(models.Model):

	classname = models.CharField(max_length = 150, default = "classroom name",blank=True)
	class_teacher = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
	college = models.ForeignKey(College,on_delete=models.CASCADE, blank = True)
	classroom_invite = models.CharField(max_length = 100, blank = True )

	def __str__(self):
		return self.classname



class Students(models.Model):

	classroom = models.ForeignKey(Classroom, on_delete = models.CASCADE, blank = True)
	user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True)
	enrolled = models.BooleanField(default = False)




class NewPost(models.Model):

	author = models.ForeignKey(User, on_delete=models.CASCADE, null = True )
	title = models.CharField(max_length=240, null=True, blank=True)
	body = models.TextField(null=True, blank=True)
	timestamp = models.DateTimeField(auto_now=True)
	classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null = True)
	

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural='New Posts'	



	


class Profile(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_type = models.IntegerField(choices=((1, ("teacher")),(2, ("student"))),default=2)
	about = models.TextField(null=True, blank=True)
	skills = models.TextField(null=True, blank=True)
	education = models.TextField(null=True, blank=True)
	followers = ArrayField(models.IntegerField(), null=True, blank=True)
	following = ArrayField(models.IntegerField(), null=True, blank=True)

	college = models.ForeignKey(College,on_delete=models.CASCADE,blank=True,default=True)


		



