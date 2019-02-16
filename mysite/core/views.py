from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from core.models import Classroom,NewPost,Profile,College,Students
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
	
# Create your views here.

def index_teacher(request,username):
	
	user = request.user
	classrooms = Classroom.objects.filter(class_teacher = user)
	all_posts = NewPost.objects.filter(author = user)

	return render(request,"index_teacher.html",{"classrooms":classrooms,"all_posts":all_posts})

def index_student(request,username):

	user = request.user
	all_posts = NewPost.objects.all()
	students = Students.objects.filter(user = user)






	return render(request, "index_student.html",{"students":students, "user":user,"all_posts":all_posts})



def signup(request):
	
	if request.method == "POST":
		
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get("email")
		user_type=request.POST.get("user_type")
		user_type=int(user_type)
		college = request.POST.get("college")
		print("this is college idss")
		print(college)
		invite_code = request.POST.get("invite_code")
		
		if User.objects.filter(username = username).exists():

			print("user already exists")
			user = User.objects.get(username = username)
			return render(request,'signup.html',{'show':'username already taken'})

		else:
			# teacher
			if user_type ==1:
				
				college_invite = College.objects.get(pk = college)
				if college_invite.invite_code == invite_code:
					print("in the if method")
					user = User.objects.create_user(username, email, password)
					print("user created")
					user_profile = Profile(user = user,college = college_invite, user_type = user_type)
					user_profile.save()
					print("profile created")
					login(request, user)
					return redirect(f"/core/index_teacher/{user.username}/")

				else:

					return render(request,"signup.html",{"error":"Invite code is wrong"})

			# student
			elif user_type == 2:

				user = User.objects.create_user(username, email, password)
				user_profile = Profile(user = user, user_type = user_type)
				user_profile.save()
				login(request, user)
				return redirect(f"/core/index_student/{user.username}/")		


	colleges = College.objects.all()
	print(colleges)

	return render(request,"signup.html",{"colleges":colleges})


def signin(request):

	user = request.user
	#user_profile = Profile.objects.get(user = user)
	#print(user.is_authenticated)
	

	if user.is_authenticated:
		
		user_profile = Profile.objects.get(user = user)
		# print(user_profile.user_type)
		if user_profile.user_type == 1:

			url=f"/core/index_teacher/{user.username}/"
			return redirect(url)

		else:

			url=f"/core/index_student/{user.username}/"
			return redirect(url)


	if request.method == "POST":


		username = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(request, username = username , password = password)


		if user is None:

			return render (request,'signin.html',{'error':"User Name or Password Might be Wrong"})

		if user is not None:
			user_profile = Profile.objects.get(user = user)
			print("here")
			login(request, user)
			print("done")
			if user_profile.user_type == 1:
		
				url=f"/core/index_teacher/{user.username}/"
				return redirect(url)

			else:
					
				url=f"/core/index_student/{user.username}/"
				return redirect(url)		

	return render(request, "signin.html")

def signout(request):	
	logout(request)
	return redirect('/core/signin/')


def editprofile(request,username):

	user = request.user
	profile = Profile.objects.get(user = user)

	if not user.is_authenticated:
		return redirect('/core/signin/')

	if request.method == "POST":
		firstname = request.POST.get('firstname', "Add your First Name")
		lastname = request.POST.get('lastname', "Add your Last Name")
		email = request.POST.get('email', "xyz@xyz.xyz")
		about = request.POST.get('aboutuser', "Add About")
		skills = request.POST.get('userskills', "Add Skills")
		education = request.POST.get('usereducation', "Add Your Education")

		user.first_name = firstname
		user.last_name = lastname
		user.save()
		profile.about = about,
		profile.skills = skills,
		profile.education = education
			
		profile.save()

		if profile.user_type == 1:

			return redirect(f"/core/index_teacher/{user.username}/")	

		elif profile.user_type == 2:

			return redirect(f"/core/index_student/{user.username}/")	

	
	return render(request, 'edit.html',{"user_profile":profile})

def create_classroom(request,username):

	user = request.user	
	
	if request.method == "POST":

		classname = request.POST.get("classname", "name this classroom")
		classroom_invite = request.POST.get("classroom_invite")
		college = Profile.objects.get(user = user)
		college = college.college
		new_classroom = Classroom(
			classname = classname,
			 classroom_invite = classroom_invite,
			   class_teacher = user, college = college)
		new_classroom.save()
	
	old_classrooms = Classroom.objects.filter(class_teacher = user)

	return render(request,"classroom.html",{"old_classrooms":old_classrooms})

def join_classroom(request,username):

	user = request.user
	college = Profile.objects.get(user = user)
	college = college.college
	all_classrooms = Classroom.objects.filter(college = college)

	if request.method == "POST":
		
		invite_code = request.POST.get("classroom_invite") 
		#print(invite_code)
		selected_classroom_id = request.POST.get("classroom","select classroom")
		selected_classroom_instance = Classroom.objects.get(pk = selected_classroom_id)

		

		if invite_code == selected_classroom_instance.classroom_invite:
			#print(invite_code)
			student = Students(classroom = selected_classroom_instance, user = user, enrolled = True)
			all_students = Students.objects.filter(user = user)
			classname_list = [] 
			for student_check in all_students:
				classname_list.append(student_check.classroom.classname)

			if (selected_classroom_instance.classname not in classname_list) or (student_check==[]): 
				#print("inside")
				student.save()

		return redirect(f'/core/index_student/{user.username}/',)

	return render(request, "join_classroom.html",{"classrooms":all_classrooms, "user":user})

def create_post(request):
	user = request.user

	if request.method == "POST":
		author = user

		title = request.POST.get("title", "Give a title")
		body = request.POST.get("body", "Enter Content")
		classroom_id = request.POST.get("classroom","select classroom")
		classroom = Classroom.objects.get(pk = classroom_id)
		new_post = NewPost(title = title,body = body,author = author, classroom = classroom)
		new_post.save()

		

	return redirect(f"/core/index_teacher/{user.username}/")	


		
