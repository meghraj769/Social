from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
	path('', PostList.as_view(), name='post_list'),
	path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
	path('post/<int:pk>/like', LikePost.as_view(), name='like'),
	path('post/<int:pk>/unlike', UnLikePost.as_view(), name='unlike'),
	path('post/edit/<int:pk>/', PostEditView.as_view(), name='post_edit'),
	path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
	path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),
	path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
	path('profile/<int:pk>/follow', AddFollower.as_view(), name='follow'),
	path('profile/<int:pk>/unfollow', RemoveFollower.as_view(), name='unfollow'),
	path('profile/<int:pk>/edit', ProfileEditView.as_view(), name='profile_edit'),
	path('search', UserSearch.as_view(), name='search'),
	

]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)