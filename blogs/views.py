from rest_framework import generics, permissions
from .models import Blog
from .serializers import BlogSerializer

# Create your views here.


# viewing the Blog
class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.AllowAny]

# viewing the Blog Detail
class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.AllowAny]

# Create the Blog View
class BlogCreateView(generics.CreateAPIView):
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'doctor':
            raise PermissionError("Only doctors can create blogs.")
        serializer.save(author=self.request.user)

# Update the Blog 
class BlogUpdateView(generics.UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionError("You can only update your own blogs.")
        serializer.save()

# Delete the Blog
class BlogDeleteView(generics.DestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionError("You can only delete your own blogs.")
        instance.delete()
