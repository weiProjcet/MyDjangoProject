from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 排除不需要登录即可访问的路径
        excluded_paths = [reverse('login'), reverse('registry')]

        # 如果是登录/注册等公开页面，跳过登录检查
        if request.path in excluded_paths:

            return self.get_response(request)

        # 检查 session 中是否存在 username
        if 'username' not in request.session:
            return redirect('login')  # 重定向到登录页
        print(request.session['username'])
        return self.get_response(request)
