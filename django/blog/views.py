from django.http import HttpResponse
from django.shortcuts import render


def post_list(request):
    # 1. 브라우저에서 요청
    # 2. 요청이 runserver로 실행중인 서버에 도착
    # 3. runserver는 요청을 django code로 전달
    # 4. django code 중 config.urls모듈이 해당 요청을 받음
    # 5. config.urls모듈은 ''(admin/를 제외한 모든 요청)을 blog.urls모듈로 전달
    # 6. blog.urls모듈은 받은 요청의 url과 일치하는 패턴이 있는지 검사
    # 7. 있다면 일치하는 패턴과 연결된 함수(view)를 실행
    #  7-1. settings모둘의 TEMPLATES속성 내의 DIR목록에서 blog/post_list.html파일의 내용을 가져옴
    #  7-2. 가져온 내용을 적절히 처리(렌더링, render()함수)하여 리턴
    # 8. 함수의 실행 결과(리턴값)를 브라우저로 다시 전달

    # HTTP프로토콜로 텍스트 데이터 응답을 반환
    # return HttpRespose('

    #'blog/post_list.html'템플릿 파일을 이용해 http프로토콜로 응답'
    return render(request, 'blog/post_list.html')


def post_detail(request):
    """
    localhost:8000/detail/ 로 온 요청을
    'blog/post_detail.html'을 reder한 결과를 리턴

    urls, views, template을 모두 작성해야 함

    :param request:
    :return:
    """
    return render(request, 'blog/post_detail.html')