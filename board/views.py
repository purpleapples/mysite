from django.shortcuts import render
from django.http import HttpResponseRedirect
from board import models


# Create your views here.
def list(request):


    # - 값일 경우 setting
    if "page_no" not in request.GET.keys():
        page_no = request.session['page_no']
    else:
        page_no = request.GET["page_no"]

    if page_no == '':
        page_no = 1
    if int(page_no) <= 0:
        page_no = 1
    page_no = int(page_no)

    page_arr, page_no = get_page_arr(page_no)
    # page list 생성
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
    params = request.GET.dict()
    result = models.select_one(no)

    if request.session.get("user_info") != None:
        if result["user_no"] != request.session["user_info"]["no"]:
            models.update_hit(no)
    else:
        models.update_hit(no)

    data = {"board": result, "page_no": request.session["page_no"], **params}
    print('data', data)
    return render(request, "board/view.html", data)


def writeReply(request):
    g_no = request.GET['g_no']
    parent_no = request.GET['parent_no']
    depth = request.GET['depth']
    data = {'g_no': g_no, 'parent_no': parent_no, 'depth': depth}
    return render(request, "board/write.html", data)


def write(request):
    data = {'g_no': 0}
    return render(request, "board/write.html", data)


def insert(request):

    # 본글 과 댓글 분기

    # 댓글 작성
    # 1. 업데이트할 순서 번호 찾기
    # 2. 업데이트할 순서번호 부터 +1
    # 3. 순서 번호로 insert
    obj = request.POST.dict()
    obj.pop("csrfmiddlewaretoken")
    if obj['g_no'] == 0:
        result = models.insert(obj)
    else:
        o_no, order_update_yn = models.select_order(obj)
        o_no = int(o_no['o_no'])

        if order_update_yn:
            models.update_order(o_no)
            obj['o_no'] = o_no
        else:
            obj['o_no'] = o_no + 1

        print(obj, o_no)
        result = models.insertReply(obj)

    return HttpResponseRedirect("/board")


def delete(request):
    no = request.GET["no"]
    result = models.delete(int(no))
    return HttpResponseRedirect("/board")


def get_page_arr(page_no) -> dict:
    # 1 page 수 조회 후  dict 로 setting
    page_arr = []
    count = models.count()["count"]
    if page_no == '':
        page_no = 1
    count = int(count)
    page_no = int(page_no)
    if count < 5 or page_no < 1:
        page_no = 1
        page_arr = [*range(1, 2)]
    else:
        page_num = count // 5 if count % 5 == 0 else count // 5 + 1
        if page_no >= page_num:
            page_no = int(page_num)
            page_arr = [*range(page_no - 5, page_no+1)]
            page_arr = [x for x in page_arr if x > 0 and x <= page_no]
            if len(page_arr) == 0:
                page_arr = [*range(1, 2)]
        else:
            page_num = count // 5 if count % 5 == 0 else count // 5 + 1
            page_arr = [x for x in [*range(page_no, page_no + 5)] if x <= page_num]
    return page_arr, page_no