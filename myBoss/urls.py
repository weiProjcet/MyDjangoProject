from django.urls import path, re_path

from myProjects import settings
from . import views
from .views import LoginView, RegistryView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registry/', RegistryView.as_view(), name='registry'),

    path('index/', views.index, name='index'),
    path('logOut/', views.logOut, name='logOut'),
    path('download_jobs/', views.download_jobs, name='download_jobs'),
    path('selfInfo/', views.selfInfo, name='selfInfo'),

    path('tableData/', views.tableData, name='tableData'),

    path('historyTableData/', views.historyTableData, name='historyTableData'),
    path('addHistory/<int:jobId>/', views.addHistory, name='addHistory'),
    path('removeHistory/<int:hisId>/', views.removeHistory, name='removeHistory'),

    path('companyTags/', views.companyTags, name='companyTags'),
    path('download_companyTags', views.download_companyTags, name='download_companyTags'),
]
