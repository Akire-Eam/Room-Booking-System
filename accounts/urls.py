"""ORB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('login/',views.loginPage, name='loginPage'),
    path('login/upmportal/', views.portal_seamless_auth, name='seamlessAuth'),
    # path('google_login/', include('social_django.urls', namespace='social')),
    path('logout/', views.logOutPage, name="logout"),
    path('login/failed/', views.failed_login, name='failedLogin'),

    path('profile/', views.viewProfile, name="profile"),
    path('profile/edit-profile/',views.editProfile, name='editProfile'),

    # admin pages
    path('manage/',views.manageUsers,name='manageUsers'),
    path('manage/add-user/', views.AddUserPage, name='AddUserPage'),
    path('manage/users/',views.users,name='users'),
    path('manage/edit/<int:pk>',views.editUser, name='editUser'),
    path('manage/edit/change-pass/<int:pk>/',views.changePass,name='changePass'),
    path('delete/<int:pk>',views.deleteUser.as_view(), name='deleteUser'),

    # Custom Django Admin
    path('accounts/referenceaccount/import', views.importReferenceTable, name='importReferenceTable'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
