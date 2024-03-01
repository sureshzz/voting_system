"""
URL configuration for voting_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from users import views
from registration import views as registration_views
from superadmin import views as admin_views
from candidates import views as candidates_views
from login import views as login_views

urlpatterns = [
    path('',views.home,name="home"),
    path('register/',registration_views.register,name="register"),
    path('cregister/',candidates_views.cregister,name="cregister"),
    path('auth/',login_views.auth,name="auth"),
    path('vote/',views.vote,name="vote"),
    path('cinfo/',candidates_views.cinfo,name="cinfo"),
    path('votecount/',views.votecount,name="votecount"),
    path('delete/',admin_views.deletecandidate,name="votecount"),
    path('adminlogin/',admin_views.adminlogin,name="adminlogin"),
    # path('click/',registration_views.click,name="click"),
]
