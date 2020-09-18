from django.shortcuts import render
from guestbook import models
from django.http import HttpResponseRedirect


def list(request):
    result = models.fetchall()
    data = {"guestbook_list": result}
    return render(request, "guestbook/list.html", data)


def deleteform(request):
    no = request.GET["no"]
    data = {"no":no}
    return render(request, "guestbook/deleteform.html", data)


def delete(request):
    obj = request.POST.dict()
    obj.pop("csrfmiddlewaretoken")
    result = models.delete(obj)
    return HttpResponseRedirect("/guestbook")


def insert(request):
    obj = request.POST.dict()
    obj.pop("csrfmiddlewaretoken")
    result = models.insert(obj)
    return HttpResponseRedirect("/guestbook")


