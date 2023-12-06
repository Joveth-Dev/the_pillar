from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('authors', views.AuthorViewSet)
# router.register('readers', views.ReaderViewSet)
router.register('issues', views.IssueViewSet, basename='issues')
router.register('articles', views.ArticleViewSet, basename='articles')
router.register('updates', views.UpdateViewSet)
router.register('banners', views.BannerViewSet)

urlpatterns = router.urls
