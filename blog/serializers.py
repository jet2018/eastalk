from rest_framework import serializers

from blog.models import Blog, Category
from modules import DisplayNameWritableField


# done with getting blogs!
# TODO: Adding them now
class BlogSerializer(serializers.ModelSerializer):
    """ 
        Blog serializers
    """
    sub_category = serializers.StringRelatedField(many=True)
    category = serializers.StringRelatedField(many=True)
    total_upvotes = serializers.ReadOnlyField()
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
            'posted_on'
        ]

    def get_poster_image(self, obj):
        return obj.author.dp.url if obj.author.dp else "/static/img/img_avatar.png"

    def get_full_name(self, obj):
        return obj.author.user.username + " " + obj.author.user.first_name + " " + obj.author.user.last_name


class CategorySerializer(serializers.ModelSerializer):
    sub_category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = '__all__'
