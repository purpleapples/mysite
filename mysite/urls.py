"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
import main.views as main_views
import board.views as board_views
import user.views as user_views
import guestbook.views as guestbook_views
urlpatterns = [
    path('admin/', admin.site.urls),

    # main
    path('main/', main_views.index),

    # board
    path('board/', board_views.list),
    path('board/modify', board_views.modify),
    path('board/update', board_views.update),
    path('board/view', board_views.view),
    path('board/write', board_views.write),
    path('board/writeReply', board_views.writeReply),
    path('board/insert', board_views.insert),
    path('board/delete', board_views.delete),

    # user
    path('user/joinform', user_views.joinform),
    path('user/insert', user_views.insert),
    path('user/updateform', user_views.updateform),
    path('user/update', user_views.update),
    path('user/joinsuccess', user_views.joinsuccess),
    path('user/loginform', user_views.loginform),
    path('user/login', user_views.login),

    path('user/logout', user_views.logout),


    # guestbook
    path('guestbook/', guestbook_views.list),
    path('guestbook/deleteform', guestbook_views.deleteform),
    path('guestbook/delete', guestbook_views.delete),
    path('guestbook/insert', guestbook_views.insert),

]
