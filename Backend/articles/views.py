
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Authentication Decorators
from rest_framework.decorators import authentication_classes

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer
from .models import Article, Comment
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication




# @permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        # articles = Article.objects.all()
        print("게시글 전체 리스트 GET 요청")
        articles = get_list_or_404(Article)
        print(articles)
        serializer = ArticleListSerializer(articles, many=True)
        print(serializer)
        return Response(serializer.data)

    elif request.method == 'POST':
        print("게시글 작성 POST 요청")
        token_auth = TokenAuthentication()
        print('>>>>>>>')
        print(token_auth.authenticate(request))
        # print(token_auth.authenticate(request.auth))
        
        user, _ = token_auth.authenticate(request)

        print('작성자는', user)

        serializer = ArticleSerializer(data=request.data)
        print('게시글 정보', request.data)
        # print('좋아요한 사람', user.what.all())
        # print(serializer)
        # print(serializer.data)
        like_user = user.what.all()
        print("@@@@@@@@@@@@")
        print(like_user)
        if serializer.is_valid(raise_exception=True):
            print('유효하므로 저장합니다.')
            # serializer.save()
            serializer.save(user=user, like_user=like_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'PUT'])
def article_detail(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        print(serializer.data)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['GET'])
def comment_list(request):
    if request.method == 'GET':
        # comments = Comment.objects.all()
        comments = get_list_or_404(Comment)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, comment_pk):
    # comment = Comment.objects.get(pk=comment_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        tmp = comment
        comment.delete()
        return Response({"detail" : f'{tmp.content}를 지웠습니다'},status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    
# 댓글 생성
@api_view(['POST'])
def comment_create(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    print('댓글 POST 요청')
    article = get_object_or_404(Article, pk=article_pk)
    token_auth = TokenAuthentication()
    user, _ = token_auth.authenticate(request)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(article=article, user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def like(request, pk):
    print('좋아요 POST 요청')
    article = Article.objects.get(pk=pk)
    token_auth = TokenAuthentication()
    user, _ = token_auth.authenticate(request)
    print(article.like_user)
    if article.like_user.filter(pk=user.pk).exists():
        print('좋아요중이므로 취소를 실시합니다')
        article.like_user.remove(user)
        return Response(
            {'detail': (f'Successfully add Like_user. {user}를 {article.user}의 팔로우 목록에 추가합니다.')},
                status=status.HTTP_200_OK,
        )
    else:
        print('좋아요중이지 않으므로 추가를 실시합니다')
        article.like_user.add(user)
        return Response(
            {'detail': (f'Successfully remove Like_user. {user}를 {article.user}의 팔로우 목록에서 제거합니다.')},
                status=status.HTTP_200_OK,
        )
