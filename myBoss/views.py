import hashlib

from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from django.shortcuts import render, redirect
from django.views import View

from myBoss.models import User
from myBoss.utils import getSelfInfo, getTableData, getHistoryData
import myBoss.utils.getHomeData as getHomeData
from myBoss.utils.forms import LoginForm, RegistryForm, selfInfoForm
import logging

logger = logging.getLogger(__name__)


# Create your views here.
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        logger.info("用户尝试登录")
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

                logger.info(f"用户{username}登录成功")
                return redirect('index')
            except User.DoesNotExist:
                logger.warning(f"用户名或密码错误：{username}")
                form.add_error(None, '用户名或密码错误')
                return render(request, 'login.html', {'form': form})
        else:
            logger.debug("登录表单验证失败")
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
    uname = request.session.get('username')
    logger.info(f"用户{uname}登出")
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
    # 获取当前页码
    cur_page = int(request.GET.get('page', 1))
    page_size = 10
    # 缓存键：根据用户或数据源生成唯一 key
    prefix = 'jobs'
    cache_key_all = f'{prefix}:cache_key_all'
    cache_key_page = f'{prefix}:page_{cur_page}_size_{page_size}'
    # 获取全部数据（缓存）
    AllData = cache.get(cache_key_all)
    if not AllData:
        AllData = getTableData.GetAllData()
        cache.set(cache_key_all, AllData, timeout=60 * 5)  # 缓存5分钟

    # 构造 Paginator，传入全部数据来切片（只传当前页数据有问题，无法正确判断总页数、当前是否越界）
    paginator = Paginator(AllData, page_size)
    try:
        c_page = paginator.page(cur_page)
        print(f"Current page number: {c_page.number}")
    except EmptyPage as e:
        print(f"EmptyPage error: {e}")
        c_page = paginator.page(1)

    # 对当前页数据进行处理后的 object_list 缓存
    processed_objects = cache.get(cache_key_page)
    if not processed_objects:
        processed_objects = getTableData.getTableData(c_page.object_list)
        cache.set(cache_key_page, processed_objects, timeout=60 * 5)

    c_page.object_list = processed_objects

    # 页面导航栏显示的页码范围
    visibleNumber = 10
    start = max(1, cur_page - visibleNumber // 2)
    end = min(paginator.num_pages, start + visibleNumber)
    page_range = range(start, end + 1)

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
