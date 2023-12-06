from datetime import datetime
from rest_framework import serializers
from . import models


class AuthorSerializer(serializers.ModelSerializer):
    user_avatar = serializers.SerializerMethodField(read_only=True)
    sex = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    current_position = serializers.SerializerMethodField()

    def get_user_avatar(self, author: models.Author):
        if author.user.avatar.name == '':
            return ''
        return self.context['request'].build_absolute_uri(author.user.avatar.url)

    def get_sex(self, author: models.Author):
        return author.user.sex

    def get_full_name(self, author: models.Author):
        return str(author.user.get_full_name())

    def get_current_position(self, author: models.Author):
        return author.current_position

    class Meta:
        model = models.Author
        fields = ['id', 'user_avatar', 'full_name',
                  'sex', 'pen_name', 'current_position']


# class ReaderSerializer(serializers.ModelSerializer):
#     user_id = serializers.IntegerField(read_only=True)

#     class Meta:
#         model = models.Reader
#         fields = ['id', 'user_id', 'birthdate', 'city', 'country']


class CustomReaderSerializer(serializers.ModelSerializer):
    """ 
    This is a custom serializer for the auth/users endpoint.
    To be able to view the user with additional info in one endpoint.
    """

    class Meta:
        model = models.Reader
        fields = ['id', 'birthdate', 'city', 'country']


class IssueFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IssueFile
        fields = ['issue_id', 'file', 'image_for_thumbnail']


class IssueSerializer(serializers.ModelSerializer):
    issue_file = IssueFileSerializer(source='issuefile')
    uploaded_by = serializers.StringRelatedField()
    date_published = serializers.SerializerMethodField()

    def get_date_published(self, issue: models.Issue):
        return issue.date_published.strftime('%B %d, %Y')

    def create(self, validated_data):
        return super().create(validated_data)

    class Meta:
        model = models.Issue
        fields = ['id', 'volume_number', 'issue_number', 'category', 'issue_file',
                  'description', 'date_published', 'date_updated', 'uploaded_by']


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArticleImage
        fields = ['id', 'image', 'image_caption']


class CustomAuthorSerializer(serializers.ModelSerializer):
    """ 
    This is a custom serializer for the publication/articles endpoint.
    To be able to view the articles with author details in one endpoint.
    """
    user_avatar = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    sex = serializers.SerializerMethodField(read_only=True)

    def get_user_avatar(self, author: models.Author):
        if author.user.avatar.name == '':
            return ''
        return self.context['request'].build_absolute_uri(author.user.avatar.url)

    def get_full_name(self, author: models.Author):
        return author.user.get_full_name()

    def get_sex(self, author: models.Author):
        return author.user.sex

    class Meta:
        model = models.Author
        fields = ['id', 'user_avatar', 'full_name', 'pen_name', 'sex']


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contributor
        fields = ['id', 'name_or_pen_name', 'date_added']


class ArticleSerializer(serializers.ModelSerializer):
    authors = CustomAuthorSerializer(many=True)
    contributors = ContributorSerializer(many=True)
    article_images = ArticleImageSerializer(many=True)
    date_published = serializers.SerializerMethodField()

    def get_date_published(self, article: models.Article):
        return article.date_published.strftime('%B %d, %Y')

    class Meta:
        model = models.Article
        fields = ['id', 'authors', 'contributors', 'category', 'title_or_headline',
                  'article_images', 'body', 'date_published', 'date_updated', 'is_highlight']


class UpdateSerializer(serializers.ModelSerializer):
    member = serializers.StringRelatedField()
    date_posted = serializers.SerializerMethodField()

    def get_date_posted(self, update: models.Update):
        return update.date_posted.strftime('%B %d, %Y')

    class Meta:
        model = models.Update
        fields = ['id', 'title', 'description', 'member',
                  'image', 'image_caption', 'date_created', 'date_posted']


class CustomArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = ['id', 'title_or_headline', 'category']


class BannerSerializer(serializers.ModelSerializer):
    article = CustomArticleSerializer()
    member = serializers.StringRelatedField()

    class Meta:
        model = models.Banner
        fields = ['id', 'article', 'image', 'member', 'date_created']
