from rest_framework.generics import RetrieveAPIView, ListAPIView

from .models import BlogPost
from .serializers import BlogPostSerializer


# Create your views here.
class DetailBlogPostAPIView(RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


class BlogPostListAPIView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
