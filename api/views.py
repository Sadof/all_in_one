from .serializers import *
from rest_framework import generics
from tests.models import Test


class TestListView(generics.ListAPIView):
    queryset = Test.objects.filter(status=True)
    serializer_class = TestSerializer



class TestDetailView(generics.RetrieveAPIView):
    queryset = Test.objects.filter(status=True)
    serializer_class = TestSerializer


class TestEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        return Test.objects.filter(status=False,author=self.request.user)