from rest_framework.routers import DefaultRouter
from Auth.views import Signup
router=DefaultRouter()
router.register(prefix='signup',viewset=Signup ,basename='signup_auth')

urlpatterns=router.urls
