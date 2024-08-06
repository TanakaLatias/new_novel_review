from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # top
    path('', TopAndIndexView.as_view(), name='top'),
    # users
    path('user_detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user_detail_posts/<int:pk>/', UserDetailPostsView.as_view(), name='user_detail_posts'),
    path('user_detail_likes/<int:pk>/', UserDetailLikesView.as_view(), name='user_detail_likes'),
    path('user_detail_reads/<int:pk>/', UserDetailReadsView.as_view(), name='user_detail_reads'),
    path('user_update/', UserUpdateView.as_view(), name='user_update'),
    # works
    path('work_index/', WorkIndexView.as_view(), name='work_index'),
    path('work_index_posted/', WorkIndexPostedView.as_view(), name='work_index_posted'),
    path('work_index_read/', WorkIndexReadView.as_view(), name='work_index_read'),
    path('work_index_scened/', WorkIndexScenedView.as_view(), name='work_index_scened'),
    path('work_search/', WorkSearchView.as_view(), name='work_search'),
    path('work_detail/<int:pk>/', WorkDetailView.as_view(), name='work_detail'),
    path('work_detail_scene/<int:pk>/', WorkDetailSceneView.as_view(), name='work_detail_scene'),
    path('work_create/', WorkCreateView.as_view(), name='work_create'),
    path('work_update/<int:pk>/', WorkUpdateView.as_view(), name='work_update'),
    # scene
    path('scene_create/<int:pk>/', SceneCreateView.as_view(), name='scene_create'),
    path('scene_delete/<int:pk>/', SceneDeleteView.as_view(), name='scene_delete'),
    # posts
    path('post_index/', PostIndexView.as_view(), name='post_index'),
    path('post_search/', PostSearchView.as_view(), name='post_search'),
    path('post_detail/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post_create/<int:pk>/', PostCreateView.as_view(), name='post_create'),
    path('post_update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post_delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    # likes
    path('like_create/<int:pk>/', LikeCreateView.as_view(), name='like_create'),
    path('like_delete/<int:pk>/', LikeDeleteView.as_view(), name='like_delete'),
    # reads
    path('read_create/<int:pk>/', ReadCreateView.as_view(), name='read_create'),
    path('read_delete/<int:pk>/', ReadDeleteView.as_view(), name='read_delete'),
    # polls
    path('poll_create/<int:pk>/', PollCreateView.as_view(), name='poll_create'),
    path('poll_delete/<int:pk>/', PollDeleteView.as_view(), name='poll_delete'),
    # errors
    path('error/',ErrorView.as_view(), name='error'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)