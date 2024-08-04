import pytest

from accounts.models import CustomUser
from posts.models import Comment, Post, Tag

@pytest.fixture(name="user")
def given_user():
    u = CustomUser.objects.create()
    return u

@pytest.fixture(name="post")
def given_post(user):
    p = Post.objects.create(
        author=user,
    )
    return p

@pytest.fixture(name="post_with_tag")
def given_post_with_tag(post, tag):
    post.tags.set([tag])
    return post

@pytest.fixture(name="comment")
def given_comment(post, user):
    c = Comment.objects.create(
        post=post,
        author=user,
    )
    return c

@pytest.fixture(name="tag")
def given_tag(post, user):
    t = Tag.objects.create(
        name="Tag",
    )
    return t
