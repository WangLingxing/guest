from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from sign.models import Event, Guest


def index(request):
    return render(request, 'index.html')


# 登录
def login_action(request):
    """
    登录动作
    :param request:
    :return: 登录成功重定向发布会页面，失败提示病render index页面
    """
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)  # 若不为空则用户认证通过，否则返回None
        if user is not None:
            auth.login(request, user)  # 登录
            # response.set_cookie('user', sername, 3600) # 添加浏览器cookies
            request.session['user'] = username  # 将session信息记录到浏览器
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})


@login_required
def event_manage(request):
    """
     发布会管理
    :param request:
    :return:
    """
    event_list = Event.objects.all()
    # username = request.COOKIES.get('user', '')  # 读取cookies
    username = request.session.get('user', '')  # 读取浏览器session
    return render(request, 'event_manage.html', {'user': username,
                                                 'events': event_list})


@login_required
def search_name(request):
    """
    发布会名称模糊搜索
    :param request:
    :return:
    """
    username = request.session.get('user', '')
    search_name = request.GET.get('name', '')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, 'event_manage.html', {'user': username,
                                                 'events': event_list})


@login_required
def guest_manage(request):
    """
    嘉宾页面
    :param request:
    """
    username = request.session.get('user', '')
    guest_list = Guest.objects.get_queryset().order_by('id')
    paginator = Paginator(guest_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，获取第一页内容
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果page不在范围，取最后一页
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'guest_manage.html', {'user': username,
                                                 'guests': contacts})


@login_required
def search_guest(request):
    """
    嘉宾名字、手机号模糊搜索
    :param request:
    :return:
    """
    username = request.session.get('user', '')
    search_guest = request.GET.get('name', '')
    guests = Guest.objects.filter(Q(realname__icontains=search_guest) | Q(phone__contains=search_guest)).order_by('id')
    paginator = Paginator(guests, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {'user': username,
                                                 'guests': contacts})


@login_required
def sign_index(request, eid):
    """
    签到页面-根据event
    :param request:
    :param eid:
    :return:
    """
    event = get_object_or_404(Event, id=eid)
    guest_num = len(Guest.objects.filter(event_id=eid))
    signed_num = len(Guest.objects.filter(event_id=eid, sign='1'))
    return render(request, 'sign_index.html', {'event': event,
                                               'all_guest': guest_num,
                                               'all_signed': signed_num,
                                               })


@login_required
def sign_index_action(request, eid):
    """
    签到动作
    :param request:
    :param eid:
    """
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    guest_num = len(Guest.objects.filter(event_id=eid))
    signed_num = len(Guest.objects.filter(event_id=eid, sign='1'))
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'all_guest': guest_num,
                                                   'all_signed': signed_num,
                                                   'hint': 'Phone Error.'})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'all_guest': guest_num,
                                                   'all_signed': signed_num,
                                                   'hint': 'event id or phone error.'})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event,
                                                   'all_guest': guest_num,
                                                   'all_signed': signed_num,
                                                   'hint': 'user had signed.'})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event,
                                                   'all_guest': guest_num,
                                                   'all_signed': signed_num,
                                                   'hint': 'sign in success.',
                                                   'guest': result})

@login_required
def logout(request):
    auth.logout(request)  # 退出登录
    response = HttpResponseRedirect('/index/')
    return response