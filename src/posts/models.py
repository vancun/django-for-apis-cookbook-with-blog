from django.conf import settings
from django.db import models
from django_fsm import FSMField, transition


def truncate_with_elipsis(s: str, max_length: int, elipsis: str = "...") -> str:
    if not isinstance(s, str):
        s = str(s)
    truncated = (s[:max_length] + "..") if len(s) > max_length else s
    return truncated


class PostState(models.TextChoices):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    tags = models.ManyToManyField("Tag", related_name="posts", through="PostTag")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = FSMField(default=PostState.DRAFT, choices=PostState.choices)

    def can_publish(self, user):
        return self.author == user

    def can_archive(self, user):
        return self.author == user

    def can_draft(self, user):
        return self.author == user

    @transition(
        field=state,
        source=PostState.DRAFT,
        target=PostState.PUBLISHED,
        permission=can_publish,
    )
    def publish(self):
        pass

    @transition(
        field=state, source="*", target=PostState.ARCHIVED, permission=can_archive
    )
    def archive(self):
        pass

    @transition(field=state, source="*", target=PostState.DRAFT, permission=can_draft)
    def draft(self):
        pass

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        label = truncate_with_elipsis(self.body, 50)
        return f"{self.author.username}: {label}"


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post", "tag")
