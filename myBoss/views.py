import hashlib

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, HttpResponse, redirect
from django.views import View

from myBoss.models import User
from myBoss.utils import getSelfInfo, getTableData, getHistoryData
from myBoss.utils.error import errorResponse
import myBoss.utils.getHomeData as getHomeData
import myBoss.utils.getPublicData as getPublicData
from myBoss.utils.forms import LoginForm, RegistryForm, selfInfoForm


# Create your views here.
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            md5 = hashlib.md5()
            md5.update(password.encode())
            pwd_hashed = md5.hexdigest()
            try:
                user = User.objects.get(username=username, password=pwd_hashed)
                request.session['username'] = username
                # auth_login(request, user)
                return redirect('index')
            except User.DoesNotExist:
                form.add_error(None, '用户名或密码错误')
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})


class RegistryView(View):
    def get(self, request):
        form = RegistryForm()
        return render(request, 'registry.html', {'form': form})

    def post(self, request):
        form = RegistryForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            checkPwd = form.cleaned_data['check_password']
            if User.objects.filter(username=username).exists():
                form.add_error('username', '该用户名已被注册')
                return render(request, 'registry.html', {'form': form})
            if password != checkPwd:
                form.add_error(None, '两次密码不同！')
                return render(request, 'registry.html', {'form': form})
            md5 = hashlib.md5()
            md5.update(password.encode())
            pwd = md5.hexdigest()
            User.objects.create(username=username, password=pwd)
            return redirect('login')
        else:
            return render(request, 'registry.html', {'form': form})


def logOut(request):
    request.session.clear()
    return redirect('login')


def index(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)  # 用户信息
    year, month, day = getHomeData.getNowTime()  # 当前时间
    jobsLen, educationsTop, salaryTop, salaryMonthTop, addressTop, praticeMax = getHomeData.getTagData()
    tableData = getHomeData.getTableData()
    paginator = Paginator(tableData, 10)  # 每页显示10条
    page = request.GET.get('page')  # 获取当前页码
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {
        'userInfo': userInfo,
        'year': year,
        'month': month,
        'day': day,
        'jobsLen': jobsLen,
        'educationsTop': educationsTop,
        'salaryTop': salaryTop,
        'salaryMonthTop': salaryMonthTop,
        'praticeMax': praticeMax,
        'addressTop': addressTop,
        'tableData': current_page
    })


def selfInfo(request):
    uname = request.session.get('username')
    user = User.objects.get(username=uname)  # 用户信息
    if request.method == 'POST':
        form = selfInfoForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return render(request, 'selfInfo.html', {'form': form, 'userInfo': user})
    form = selfInfoForm(instance=user)
    return render(request, 'selfInfo.html', {'form': form, 'userInfo': user})


def tableData(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    tableData = getTableData.getTableData()
    paginator = Paginator(tableData, 10)
    cur_page = 1
    if request.GET.get('page'):
        cur_page = int(request.GET.get('page'))
    c_page = paginator.page(cur_page)
    page_range = []
    visibleNumber = 10
    min = int(cur_page - visibleNumber / 10)
    if min < 1:
        min = 1
    max = min + visibleNumber
    if max > paginator.page_range[-1]:
        max = paginator.page_range[-1]
    for i in range(min, max):
        page_range.append(i)
    return render(request, 'tableData.html', {
        'userInfo': userInfo,
        'c_page': c_page,
        'page_range': page_range,
        'paginator': paginator
    })


def historyTableData(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    historyData = getHistoryData.getHistoryData(userInfo)
    return render(request, 'historyTableData.html', {
        'userInfo': userInfo,
        'historyData': historyData
    })


def addHistory(request, jobId):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    getHistoryData.addHistory(userInfo, jobId)
    return redirect('historyTableData')


def removeHistory(request, hisId):
    getHistoryData.removeHistory(hisId)
    return redirect('historyTableData')
