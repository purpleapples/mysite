from django.shortcuts import render
from user import models
from django.http import HttpResponseRedirect


def joinform(request):
    return render(request, "user/joinform.html")


def insert(request):
    obj = request.POST.dict()
    obj.pop("csrfmiddlewaretoken")
    result = models.insert(obj)

    return HttpResponseRedirect("/user/joinsuccess")


def update(request):
    obj = request.POST.dict()
    obj.pop("csrfmiddlewaretoken")
    result = models.update(obj)
    update_info = models.select_one(obj["no"])
    request.session["user_info"] = update_info
    return HttpResponseRedirect("/main")


def updateform(request):
    return render(request, "user/updateform.html")


def joinsuccess(request):
    return render(request, "user/joinsuccess.html")


def loginform(request):
    return render(request, "user/loginform.html")


def login(request):
    obj = request.POST.dict()
    obj.pop("csrfmiddlewaretoken")
    result = models.login(obj)
    user_info = ""
    if len(result) == 0:
        data = {"login_result": 0}
        return render(request, "user/loginform.html", data)
    else:
        user_info = models.login(obj)[0]
        request.session['user_info'] = user_info
        return HttpResponseRedirect("/main")


def logout(request):

    request.session["user_info"] = None
    return HttpResponseRedirect("/main")
