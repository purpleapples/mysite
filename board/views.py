from django.shortcuts import render
from django.http import HttpResponseRedirect
from board import models


# Create your views here.
def list(request):

    page_arr = get_page_arr()
    # - 값일 경우 setting
    page_no = request.GET["page_no"]
    if page_no == '':
        page_no = 1

    page_no = int(page_no)

    # max 초과일 경우 setting
    if page_no < 0:
        page_no = 1
    if page_no > max(page_arr):
        page_no = max(page_arr)

    # page list 생성
    page_arr = page_arr[page_no: page_no+5]
    board_list = models.fetchlist(page_no)

    #  글쓰기 취소 시 사용
    request.session["page_no"] = page_no

    for board in board_list:
        board["indepth"] = " " * int(board["depth"])
    data = {"board_list": board_list, "page_arr": page_arr, "page_no": page_no}

    return render(request, "board/list.html", data)


def modify(request):
    no = request.GET["no"]
    result = models.select_one(no)
    data = {"board": result}
    return render(request, "board/modify.html", data)


def update(request):
    obj = request.POST.dict()
    obj.pop("csrfmiddlewaretoken")
    result = models.update(obj)
    return HttpResponseRedirect("/board")


def view(request):
    no = request.GET["no"]
    result = models.select_one(no)

    if request.session.get("user_info") != None:
        if result["user_no"] != request.session["user_info"]["no"]:
            models.update_hit(no)
    else:
        models.update_hit(no)

    data = {"board": result, "page_no": request.session["page_no"], "g_no": request.GET["g_no"]}
    return render(request, "board/view.html", data)


def write(request):
    return render(request, "board/write.html")


def insert(request):
    obj = request.POST.dict()
    obj.pop("csrfmiddlewaretoken")
    order_no = models.select_order(obj)
    obj["order_no"] = order_no
    result = models.update_order(obj)
    obj["order_no"] = int(order_no) + 1
    result = models.insert(obj)
    return HttpResponseRedirect("/board")


def delete(request):
    no = request.GET["no"]
    result = models.delete(int(no))
    return HttpResponseRedirect("/board")


def get_page_arr():
    count = models.count()["count"]
    page_count = (count // 5) if count % 5 == 0 else (count // 5) + 1


    page_arr = [*range(0, page_count+1)]
    return page_arr