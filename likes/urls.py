from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('likes', views.LikeViewSet)
router.register('comments', views.CommentViewSet)
router.register('replies', views.ReplyViewSet)

urlpatterns = router.urls
