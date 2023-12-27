# board > views.py
from django.urls import is_valid_path
from board.serializers import PostSerializer, PostCreateSerializer, PostDetailSerializer, CommentSerializer
from .permissions import CustomReadOnly, IsOwnerOrReadOnly
from .models import Post, Comment

from rest_framework import viewsets
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404, get_list_or_404

# Post의 목록 보여주기
class PostViewSet(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at') # 생성일자기준으로 내림차순
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly] # 비인증 요청에 대해서는 읽기만 허용
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'published_at']
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

# Post 조회, 수정, 삭제
class PostDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all().order_by('-created_at') # 생성일자기준으로 내림차순
    serializer_class = PostDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly] # 비인증 요청에 대해서는 읽기만 허용
    lookup_field = 'post_id'
    # partial_update = True  # 부분 업데이트 허용 설정
        
# (댓글) Comment 목록 보여주기
class CommentViewSet(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'post_id'
    
    def get_queryset(self):
        post_pk = self.kwargs.get("post_id")
        return Comment.objects.filter(reply__post_id=post_pk).order_by('-created_at')

    def perform_create(self, serializer):
        post_pk = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_pk)
        serializer.save(user=self.request.user, reply=post)
        
# (댓글) Comment 조회, 수정, 삭제     
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'
    queryset = Comment.objects.all()