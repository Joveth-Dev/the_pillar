from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from .validators import validate_image_size


class Reader(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )
    birthdate = models.DateField(
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    country = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.user.get_full_name()


class Author(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )
    pen_name = models.CharField(max_length=85)
    date_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user.get_full_name()

    def delete(self, *args, **kwargs):
        # set is_active to False instead of deleting
        self.is_active = False
        super(Author, self).save(*args, **kwargs)


class Position(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.title

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user.setter
    # def _history_user(self, value):
    #     self.changed_by = value

    class Meta:
        ordering = ['id']


class AuthorPosition(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)
    date_assigned = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.position.title

    class Meta:
        verbose_name = 'Author Position'
        verbose_name_plural = 'Author Positions'


class Issue(models.Model):
    LITERARY_FOLIO = 'LF'
    TABLOID = 'T'
    SPORTS_MAGAZINE = 'SM'
    NEWSLETTER = 'N'

    CATEGORY_CHOICES = [
        (LITERARY_FOLIO, 'Literary Folio'),
        (TABLOID, 'Tabloid'),
        (SPORTS_MAGAZINE, 'Sports Magazine'),
        (NEWSLETTER, 'Newsletter')
    ]
    uploaded_by = models.ForeignKey(Author, on_delete=models.CASCADE)
    volume_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)])
    issue_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)])
    description = models.TextField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_published = models.DateField()
    end_date = models.DateField()
    is_posted = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'Volume : {self.volume_number} | Issue : {self.issue_number}'


class IssueFile(models.Model):
    issue = models.OneToOneField(
        Issue,
        on_delete=models.CASCADE,
        primary_key=True)
    file = models.FileField(
        upload_to='publication/files',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    image_for_thumbnail = models.ImageField(
        upload_to='publication/files/thumbnails',
        validators=[validate_image_size])

    def __str__(self) -> str:
        file_name = f'File name: {self.file.name.replace("publication/files/", "")}'
        return file_name


class Contributor(models.Model):
    name_or_pen_name = models.CharField(max_length=255)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name_or_pen_name


class Article(models.Model):
    NEWS = 'N'
    NEWS_FEATURE = 'NF'
    FEATURE = 'F'
    OPINION = 'O'
    CULTURE = 'C'
    EDITORIAL = 'E'
    COLUMN = 'CL'
    LITERARY = 'L'
    SPORTS = 'S'

    CATEGORY_CHOICES = [
        (NEWS, 'News'),
        (NEWS_FEATURE, 'News Feature'),
        (FEATURE, 'Feature'),
        (OPINION, 'Opinion'),
        (CULTURE, 'Culture'),
        (EDITORIAL, 'Editorial'),
        (LITERARY, 'Literary'),
        (COLUMN, 'Column'),
        (SPORTS, 'Sports'),
    ]
    uploaded_by = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='article_uploader')
    authors = models.ManyToManyField(Author)
    contributors = models.ManyToManyField(Contributor)
    title_or_headline = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        blank=True,
        null=True,
    )
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_published = models.DateField()
    end_date = models.DateField()
    is_posted = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=True)
    is_highlight = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title_or_headline

    # def validate_highlight(self):
    #     if self.is_highlight:
    #         # check if there's already an existing highlight for this category
    #         existing_highlight = Article.objects.filter(
    #             category=self.category,
    #             is_highlight=True,
    #         ).exclude(id=self.id).first()
    #         if existing_highlight:
    #             raise ValidationError(
    #                 'Only one article per category can be highlighted'
    #             )

    def save(self, *args, **kwargs):
        # self.validate_highlight()
        # set the previous highlight to False if this article is now the highlight
        if self.is_highlight:
            Article.objects.filter(
                category=self.category,
                is_highlight=True,
            ).exclude(id=self.id).update(is_highlight=False)
        super().save(*args, **kwargs)


class ArticleImage(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='article_images')
    image = models.ImageField(
        upload_to='publication/images',
        validators=[validate_image_size])
    image_caption = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        image_name = f'File name: {self.image.name.replace("publication/images/", "")}'
        return image_name


class Update(models.Model):
    member = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    description = models.TextField()
    image = models.ImageField(
        upload_to='publication/update/images',
        null=True,
        blank=True,
    )
    image_caption = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    is_posted = models.BooleanField(default=False)
    date_posted = models.DateField(
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self) -> str:
        if self.title is None:
            description = self.description[:50]
            return description.rstrip() + '...'
        return self.title


class Banner(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    member = models.ForeignKey(Author, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='publication/banners',
        validators=[validate_image_size])
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.article.title_or_headline
