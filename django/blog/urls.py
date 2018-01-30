from django.urls import path, re_path
from . import views


urlpatterns = [
    path('list', views.post_list, name='post-list'),
    # path('detail/', views.post_detail),

    # 3/
    # 53/
    # 53/asdf/ <- x
    # re_path(r'(?P<pk>\d+)/$', views.post_detail),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),

    # 숫자가 1개 이상 반복되는 경우를 정규표현식으로 구현하되
    # 해당 반복구간을 그룹으로 묶고, 그룹 이름을 'pk'로 지정
    # re.compile(r'(?P<pk>\d+)')

]
