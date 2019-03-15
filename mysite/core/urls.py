from django.conf.urls import url
from django.urls import path
from core import views



urlpatterns = [
		path("index_teacher/<slug:username>/",views.index_teacher),
		path("index_student/<slug:username>/",views.index_student),
		path("signup/",views.signup),
		path("signin/",views.signin),
		path("logout/",views.signout),
		path("profile/<slug:username>/",views.editprofile),
		path("classroom/<slug:username>/",views.create_classroom),
		path("join_classroom/<slug:username>/",views.join_classroom),
		path("publish_post/",views.create_post),

]