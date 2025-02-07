from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Blog
from .serializers import BlogSerializer

# Create your views here.


# viewing the Blog
class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.AllowAny]

# ......................View a Single Blog
# (URL: /blogs/<id>/) .............  (Method: GET) ............(Description: View details of a specific blog.)


# viewing the Blog Detail
class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.AllowAny]
# .............................View All Blogs
# (URL: /blogs/) 
# .................... (Method: GET) .................(Description: Retrieve all the list blogs.)
# (Response):
# [
#   {
#     "id": 1,
#     "author": "Dr. John Doe",
#     "title": "The Importance of Regular Check-Ups",
#     "content": "Regular check-ups can help detect diseases early and save lives.",
#     "created_at": "2025-01-27"
#   }
# ]




# Create the Blog View
class BlogCreateView(generics.CreateAPIView):
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'doctor':
            raise PermissionDenied("Only doctors can create blogs.")
        serializer.save(author=self.request.user)
# .....................Create a Blog

# (URL: /blogs/)
# ......................(Method: POST)..................(Role Required: Doctor)
# (Request):
# {
#   "title": "The Importance of Regular Check-Ups",
#   "content": "Regular check-ups can help detect diseases early and save lives."
# }

# (Response):
# {
#   "id": 1,
#   "author": "Dr. John Doe",
#   "title": "The Importance of Regular Check-Ups",
#   "content": "Regular check-ups can help detect diseases early and save lives.",
#   "created_at": "2025-01-27"
# }




# Update the Blog 
class BlogUpdateView(generics.UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionError("You can only update your own blogs.")
        serializer.save()
# ........................................Edit a Blog
# (URL: /blogs/<id>/)   
# ................(Method: PATCH) ...........(Role Required: Doctor (Author Only))
# (Request):
# {
#   "content": "Updated content about regular check-ups."
# }




# Delete the Blog
class BlogDeleteView(generics.DestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionError("You can only delete your own blogs.")
        instance.delete()
# ...................................(Delete a Blog)
# (URL: /blogs/<id>/) .......... (Method: DELETE) ............(Role Required: Doctor (Author Only))
#                               (Description: Delete a specific blog.)
