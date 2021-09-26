from django.conf import settings
from django.core.exceptions import ValidationError
from authors.models import Author
from rest_framework import serializers

from blog.models import Blog, BlogComment, Category, SubCategory, Subscribers
from modules import DisplayNameWritableField


class CategorySerializer(serializers.RelatedField):

    def to_representation(self, value):
        return {"category_name": value.category_name, "icon": value.icon}

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset

    def to_internal_value(self, data):
        new_data = data.split(",")
        for cat in new_data:
            try:
                Category.objects.get(category_name=cat)
            except Category.DoesNotExist:
                raise serializers.ValidationError(
                    'Category %s does not exist' % cat)
            return Category(category_name=cat)

    class Meta:
        model = Category


class SubCategorySerializer(serializers.RelatedField):

    def to_representation(self, value):
        return {"sub_category_name": value.sub_category_name, "icon": value.icon}

    def get_queryset(self):
        queryset = SubCategory.objects.all()
        return queryset

    def to_internal_value(self, data):
        new_data = data.split(",")
        for cat in new_data:
            try:
                SubCategory.objects.get(sub_category_name=cat)
            except SubCategory.DoesNotExist:
                raise serializers.ValidationError(
                    'Sub category %s does not exist' % cat)
            return SubCategory(sub_category_name=cat)

    class Meta:
        model = SubCategory


class BlogSerializer(serializers.ModelSerializer):
    """
        Blog serializers
    """
    category = CategorySerializer(many=True)
    sub_category = SubCategorySerializer(many=True)
    total_upvotes = serializers.ReadOnlyField()
    # categories = serializers.TextField()
    # sub_categories = serializers.TextField()
    total_downvotes = serializers.ReadOnlyField()
    total_comments = serializers.ReadOnlyField()
    poster_image = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    blog_color = DisplayNameWritableField()

    class Meta:
        model = Blog  # the model we working on
        fields = '__all__'  # including all fields at ago
        # these fields will be read, but a user can't add anything on them.
        read_only_fields = [
            'slug',
            'poster_image',
            'full_name',
            'blog_color',
            'posted_on'
        ]

    def get_poster_image(self, obj):
        if settings.DEBUG:
            url = "http://localhost:8000/static/img/img_avatar.png"
        else:
            url = settings.CUSTOM_STATIC_URL+"img/img_avatar.png"

        return obj.author.dp.url if obj.author.dp else url

    def get_full_name(self, obj):
        return obj.author.user.username + " " + obj.author.user.first_name + " " + obj.author.user.last_name


class CategorySerializer(serializers.ModelSerializer):
    sub_category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogComment
        fields = "__all__"


class SubScriber(serializers.ModelSerializer):
    class Meta:
        model = Subscribers
        field = "__all__"

    def save(self):
        pass
        #
