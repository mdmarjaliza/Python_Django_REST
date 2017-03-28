from rest_framework import serializers

from post.models import Post


class UserPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post


class UserPostsListsSerializer(UserPostsSerializer):
    class Meta(UserPostsSerializer.Meta):
        fields = ("titulo", "url", "intro", "fec_publicacion")
