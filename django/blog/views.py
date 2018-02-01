
from django.shortcuts import render, redirect

from .models import Post


def post_list(request):
    # 1. 브라우저에서 요청
    # 2. 요청이 runserver로 실행중인 서버에 도착
    # 3. runserver는 요청을 Django code로 전달
    # 4. Django code중 config.urls모듈이 해당 요청을 받음
    # 5. config.urls모듈은 ''(admin/를 제외한 모든 요청)을 blog.urls모듈로 전달
    # 6. blog.urls모듈은 받은 요청의 URL과 일치하는 패턴이 있는지 검사
    # 7. 있다면 일치하는 패턴과 연결된 함수(view)를 실행
    #   7-1. settings모듈의 TEMPLATES속성 내의 DIRS목록에서
    #        blog/post_list.html파일의 내용을 가져옴
    #   7-2. 가져온 내용을 적절히 처리(렌더링, render()함수)하여 리턴
    # 8. 함수의 실행 결과(리턴값)를 브라우저로 다시 전달

    # HTTP프로토콜로 텍스트 데이터 응답을 반환
    # return HttpResponse('<html><body><h1>Post list</h1><p>Post목록을 보여줄 예정입니다</p></body></html>')

    # 구글검색: django model order recently created in view
    # order_by
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
    # 위 return코드와 같음
    # return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    context = {
        'post': Post.objects.get(pk=pk),
    }
    return render(
        request,
        'blog/post_detail.html',
        context
    )


def post_edit(request, pk):
    """
    1. pk에 해당하는 Post인스턴스를
        context라는 dict에 'post'키에 할당
        위에서 생성한 dict는 render의 context에 전달
        사용하는 템플릿은 'blog/post_add.html'을 재사용
            HTML새로 만들지 말고 있던 html을 그냥 할당
    2. url은 /<pk>/edit/ <- 에 매칭되도록 urls.py작성
    3. 이 위치로 올 수 있는 a요소를 post_detail.html에 작성 (form아님)

    - request.method가 POST일 때는 request.POST에 있는 데이터를 이용해서
      pk에 해당하는 Post인스턴스의 값을 수정, 이후 post-detail로 redirect
        값을 수정하는 코드
            post = Post.objects.get(pk=pk)
            post.title = <새 문자열>
            post.content = <새 문자열>
            post.save()  <- DB에 업데이트 됨

    - request.method가 GET일 때는 현재 아래에 있는 로직을 실행

    :param request:
    :param pk:
    :return:
    """
    # 현재 URL (pk가 3일경우 /3/edit/)에 전달된 pk에 해당하는 Post인스턴스를 post변수에 할당
    post = Post.objects.get(pk=pk)
    context = {
        'post': post,
    }
    # 만약 POST메서드 요청일 경우
    if request.method == 'POST':
        # post의 제목/내용을 전송받은 값으로 수정 후
        title = request.POST['title']
        content = request.POST['content']
        # title과 content가 모두 있을 경우
        if title and content:
            post.title = title
            post.content = content
            # DB에 저장
            post.save()
            # 이후 상세화면으로 이동
            return redirect('post-detail', pk=post.pk)
        # title이나 content중 하나라도 빈 값일 경우, context['form_error']를 채운 뒤
        # 아래의 GET메서드 요청과 같은 로직을 실행
        context['form_error'] = '제목과 내용을 입력해주세요'
    # GET메서드 요청일 경우
    # 수정할 수 있는 페이지를 보여줌
    return render(request, 'blog/post_add_edit.html', context)


def post_add(request):
    # localhost:8000/add로 접근시
    # 이 뷰가 실행되어서 Post add page라는 문구를 보여주도록 urls작성
    # HttpResponse가 아니라 blog/post_add.html을 출력
    # post_add.html은 base.html을 확장, title(h2)부분에 'Post add'라고 출력
    context = {}
    if request.method == 'POST':
        # 요청의 method가 POST일 때
        # HttpResponse로 POST요청에 담겨온
        # title과 content를 합친 문자열 데이터를 보여줌
        title = request.POST['title']
        content = request.POST['content']

        # 만약 title이나 content가 비어있으면
        # 다시 글 작성화면으로 이동
        # 이동시키지말고, 아래까지 내려가서 오류메세지를 출력
        # 힌트1: 아래의 else문을 없애야합니다
        # 힌트2: if request.method판단부분보다 위에 context객체를 만듭니다
        # 힌트3: context로 전달된 form_error값(단순이름)을 템플릿에서 출력합니다
        #   ex) context = {'form_error': '빈 값은 안돼요'} <- 이런식으로..
        if title and content:
            # ORM을 사용해서 title과 content에 해당하는 Post생성
            post = Post.objects.create(
                author=request.user,
                title=title,
                content=content,
            )
            # post-detail이라는 URL name을 가진 뷰로
            # 리디렉션 요청을 보냄
            # 이 때, post-detail URL name으로 특정 URL을 만드려면
            # pk값이 필요하므로 키워드 인수로 해당 값을 넘겨준다
            return redirect('post-detail', pk=post.pk)
        context['form_error'] = '제목과 내용을 입력해주세요'
    # 요청의 method가 GET일 때
    return render(request, 'blog/post_add_edit.html', context)


def post_delete(request, pk):
    """
    post_detail의 구조를 참조해서
    pk에 해당하는 post를 삭제하는 view를 구현하고 url과 연결
    pk가 3이면 url은 "/3/delete/"
    이 view는 POST메서드에 대해서만 처리한다 (request.method == 'POST')
    (HTML 템플릿을 사용하지 않음)

    삭제코드
        post = Post.objects.get(pk=pk)
        post.delete()

    삭제 후에는 post-list로 redirect (post_add()를 참조)

    1. post_delete() view함수의 동작을 구현
    2. post_delete view와 연결될 urls를 blog/urls.py에 구현
    3. post_delete로 연결될 URL을 post_detail.html의 form에 작성
        csrf_token사용!
        action의 위치가 요청을 보낼 URL임
    """
    if request.method == 'POST':
        # pk에 해당하는 Post를 삭제
        post = Post.objects.get(pk=pk)
        # 삭제 요청한 user와 post의 author가 같을때만 해당 post를 삭제
        if request.user == post.author:
            post.delete()
            # 이후 post-list라는 URL name을 갖는 view로 redirect
            return redirect('post-list')
        # 요청한 유저가 다르면 다시 글 상세화면으로 돌아옴
        return redirect('post-detail', pk=post.pk)