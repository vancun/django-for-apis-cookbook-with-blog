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


@pytest.fixture(name="post_data")
def given_post_data(user):
    data = {
        "title": "post-1",
        "body": "body-1",
        "author": user.id,
    }
    return data


@pytest.fixture(name="post_url")
def given_post_url(post):
    url = f"/api/posts/{post.id}/"
    return url


@pytest.fixture(name="missing_post_url")
def given_missing_post_url():
    url = "/api/posts/1001/"
    return url


@pytest.fixture(name="post_with_tag")
def given_post_with_tag(post, tag):
    post.tags.set([tag])
    return post


@pytest.fixture(name="comments_url")
def given_comments_url():
    return "/api/comments/"


@pytest.fixture(name="comment")
def given_comment(post, user):
    c = Comment.objects.create(
        post=post,
        author=user,
    )
    return c


@pytest.fixture(name="comment_url")
def given_comment_url(comments_url, comment):
    url = f"{comments_url}{comment.id}/"
    return url


@pytest.fixture(name="missing_comment_url")
def given_missing_comment_url(comments_url):
    url = f"{comments_url}/1001/"
    return url


@pytest.fixture(name="comment_data")
def given_comment_data(post, user):
    data = {
        "body": "Comment-1",
        "post": post.id,
        "author": user.id,
    }
    return data


@pytest.fixture(name="tags_url")
def given_tags_url():
    return "/api/tags/"


@pytest.fixture(name="tag")
def given_tag(post, user):
    t = Tag.objects.create(
        name="Tag",
    )
    return t


@pytest.fixture(name="tag_data")
def given_tag_data():
    data = {
        "name": "Tag-1",
    }
    return data


@pytest.fixture(name="tag_url")
def given_tag_url(tag, tags_url):
    url = f"{tags_url}{tag.id}/"
    return url


@pytest.fixture(name="missing_tag_url")
def given_missing_tag_url(tags_url):
    url = f"{tags_url}1001/"
    return url
