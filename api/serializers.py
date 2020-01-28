from rest_framework import serializers
from tests.models import Test, Page, Question




class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id','text',)




class PageSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = ('order', 'title', 'text','image','right_answer','question')


class TestSerializer(serializers.ModelSerializer):
    page = PageSerializer(many=True, read_only=True);

    class Meta:
        model = Test
        fields = ('id','author','slug','title','description', 'status','completed','len','page')
