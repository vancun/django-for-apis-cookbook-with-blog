import pytest

from posts.models import Comment, Post, PostTag, Tag

pytestmark = pytest.mark.model


class TestPost:
    @pytest.mark.django_db
    def test_should_create_post_instance(self, user):
        # WHEN New post model instance is created
        p = Post.objects.create(author=user)
        # THEN the object is a Post instance
        assert isinstance(p, Post)
        # AND is persisted in the database
        p.refresh_from_db()

    @pytest.mark.django_db
    def test_should_delete_post_instance(self, post: Post):
        # WHEN Post is deleted
        post.delete()
        # THEN the post instance is no longer found in the database
        with pytest.raises(Post.DoesNotExist):
            post.refresh_from_db()


class TestComment:
    @pytest.mark.django_db
    def test_should_create_comment_instance(self, post, user):
        # WHEN New comment model instance is created
        c = Comment.objects.create(post=post, author=user)
        # THEN the object is a Comment instance
        assert isinstance(c, Comment)
        # AND is persisted in the database
        c.refresh_from_db()
        # AND comment is attached to post
        assert c in post.comments.all()

    @pytest.mark.django_db
    def test_should_delete_comment_instance(self, comment: Comment):
        # WHEN Post is deleted
        comment.delete()
        # THEN the comment instance is no longer found in the database
        with pytest.raises(Comment.DoesNotExist):
            comment.refresh_from_db()

    @pytest.mark.django_db
    def test_should_delete_comment_when_post_is_deleted(
        self, post: Post, comment: Comment
    ):
        # WHEN post is deleted
        post.delete()
        # THEN the comment is also deleted
        with pytest.raises(Comment.DoesNotExist):
            comment.refresh_from_db()


class TestTag:
    @pytest.mark.django_db
    def test_should_create_tag_instance(self):
        # WHEN New tag model instance is created
        t = Tag.objects.create(name="tag")
        # THEN the object is a Comment instance
        assert isinstance(t, Tag)
        # AND is persisted in the database
        t.refresh_from_db()

    @pytest.mark.django_db
    def test_should_delete_tag_instance(self, tag: Tag):
        # WHEN Tag is deleted
        tag.delete()
        # THEN the tag instance is no longer found in the database
        with pytest.raises(Tag.DoesNotExist):
            tag.refresh_from_db()

    @pytest.mark.django_db
    def test_should_remove_tag_from_post_when_tag_is_deleted(
        self, post_with_tag: Post, tag: Tag
    ):
        # WHEN tag is deleted
        tag.delete()
        # THEN tag is no longer assigned to post
        assert 0 == len(post_with_tag.tags.all())

    @pytest.mark.django_db
    def test_should_not_delete_tag_when_post_is_deleted(self, post: Post, tag: Tag):
        # WHEN post is deleted
        post.delete()
        # THEN the tag is still in the database
        tag.refresh_from_db()
        # AND post link to tag is deleted
        assert not PostTag.objects.filter(tag=tag).all()
