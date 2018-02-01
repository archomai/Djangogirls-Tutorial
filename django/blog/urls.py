from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.post_list, name='post-list'),
    # 숫자가 1개 이상 반복되는 경우를 정규표현식으로 구현하되
    # 해당 반복구간을 그룹으로 묶고, 그룹 이름을 'pk'로 지정
    # re.compile(r'(?P<pk>\d+)'
    # re_path(r'(?P<pk>\d+)/$', views.post_detail),
    # 3/
    path('<int:pk>/', views.post_detail, name='post-detail'),

    # 3/delete
    path('<int:pk>/delete/', views.post_delete, name='post-delete'),

    # localhost:8000/add 에 접근할수 있는 path 구현
    path('add/', views.post_add, name='post-add'),

    path('<int:pk>/edit/', views.post_edit, name='post-edit')

]
