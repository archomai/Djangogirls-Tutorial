from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post


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
    # return HttpResponse('<html></html>

    posts = Post.objects.all()
    # render()함수에 전달할 dict객체 생성
    context = {
        'posts': posts,
    }
    return render(
        request=request,
        template_name='blog/post_list.html',
        context=context,
    )

    #'blog/post_list.html'템플릿 파일을 이용해 http프로토콜로 응답'
    # return render(request, 'blog/post_list.html')


def post_detail(request, pk):
    context = {
       'post': Post.objects.get(pk=pk)
    }
    return render(
        request=request,
        template_name='blog/post_detail.html',
        context=context,
    )


def post_add(request):
    # localhost:8000/add 로 접근시
    # 이뷰가 실행 되어서 Post and page 라는 문구를 보여주도록 urls 작성
    # httpResponse가 아니라 blog/post_add.html을 출력
    # post_add.html은 base.html을 확장, title(h2)부분에 'Post add'라고 출력
    if request.method == 'POST':

        # 요청의 method가 POST일때
        # HttpResponse로 POST요청을 담겨온
        # title과 content를 합친 문자열 데이터를 보여줌
        title = request.POST['title']
        content = request.POST['content']
        # ORM을 사용해서 title과 content에 해당하는 POST생성
        post = Post.objects.create(
            author=request.user,
            title=title,
            content=content,
        )
        # post-detail이라는 URL name을 가진 뷰로
        # 리디렉션 요청을 보냄
        # 이 때 post-detail URL name으로 특정 URL을 만드려면
        # pk 값이 필요함으로 키워드 인수로 해당 값을 넘겨준다
        return redirect('post-detail', pk=post.pk)

        # return HttpResponse(f'{post.pk} {post.title} {post.content}')
    else:
        # 요청의 method가 GET일때
        return render(request, 'blog/post_add.html')


def post_delete(request, pk):
    """
    post_detail의 구조를 참조해서
    pk에 해당하는 post를 삭제하는 view를 구현하고 url과 연결
    pk가 3이면 url은 "/3/delete/"
    이 view는 POST매서드에 대해서만 처리한다 (request.metho = "POST")

    삭제코드
        post = Post.objects.get(pk=pk)
        post.delete()

    삭제 후에는 post-list로 redirect (post_add()를 참조)

    1. post_delete() view함수의 동작을 구현
    2. post_delete view와 연결될 urls를 blog/urls.py에 구현
    3. post_delete로 연결된 URL을 post_detail.html의 form에 작석
        csrf_token사용
        action의 위치가 요청을 보낼 URL임
    :param request:
    :return:
    """
    # pk에 해당하는 post를 삭제
    post = Post.objects.get(pk=pk)
    post.delete()

    # 이후 post-list 라는 URL name 을 갖는 view로 redirect
    return redirect('post-list')