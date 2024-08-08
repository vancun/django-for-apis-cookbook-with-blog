import pytest

from django.test import Client
from rest_framework import status

from posts.models import Comment, Post, Tag

pytestmark = [pytest.mark.django_db]

CONTENT_TYPE = "application/json"


class TestPostUrls:
    def test_should_list_posts(self, client: Client, post):
        response = client.get("/api/posts/")
        # THEN request is successfull
        assert response.status_code == status.HTTP_200_OK, response.content
        # AND response contains all expected posts
        (actual_post_data,) = response.data
        # AND acutal posts match expected
        assert post.id == actual_post_data["id"]

    def test_should_create_posts(self, client: Client, post_data):
        response = client.post("/api/posts/", data=post_data, content_type=CONTENT_TYPE)
        # THEN request is successfull
        assert response.status_code == status.HTTP_201_CREATED, response.content
        actual_post = Post.objects.all().first()
        assert actual_post.title == post_data["title"]
        assert actual_post.body == post_data["body"]
        assert actual_post.author.id == post_data["author"]

    def test_should_retrieve_existing_post(self, client, post_url, post):
        response = client.get(post_url)
        # THEN
        assert response.status_code == status.HTTP_200_OK, response.content
        actual_post_data = response.data
        assert post.id == actual_post_data["id"]
        assert post.title == actual_post_data["title"]
        assert post.body == actual_post_data["body"]
        assert post.author.id == actual_post_data["author"]

    def test_should_fail_to_retrieve_non_existing_post(self, client, missing_post_url):
        response = client.get(missing_post_url)
        # THEN
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content

    def test_should_update_existing_post(
        self, client: Client, post, post_url, post_data
    ):
        updated_title = "Updated Post"
        post_data["title"] = updated_title
        # WHEN
        response = client.put(post_url, data=post_data, content_type=CONTENT_TYPE)
        # THEN request is successfull
        assert response.status_code == status.HTTP_200_OK, response.content
        post.refresh_from_db()
        assert post.title == updated_title

    def test_should_fail_to_update_non_existing_post(self, client, missing_post_url):
        response = client.put(missing_post_url, content_type=CONTENT_TYPE)
        # THEN
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content

    def test_should_delete_existing_post(self, client: Client, post, post_url):
        # WHEN
        client.delete(post_url)
        # THEN
        with pytest.raises(Post.DoesNotExist):
            post.refresh_from_db()

    def test_should_fail_to_delete_non_existing_post(self, client, missing_post_url):
        response = client.delete(missing_post_url)
        # THEN
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content



class TestCommentUrls:
    def test_should_list_comments(self, client: Client, comments_url, comment):
        response = client.get(comments_url)
        # THEN request is successfull
        assert response.status_code == status.HTTP_200_OK, response.content
        # AND response contains all expected comments
        (actual_data,) = response.data
        # AND acutal posts match expected
        assert comment.id == actual_data["id"]

    def test_should_create_comment(self, client: Client, comments_url, comment_data):
        response = client.post(comments_url, data=comment_data, content_type=CONTENT_TYPE)
        # THEN request is successfull
        assert response.status_code == status.HTTP_201_CREATED, response.content
        actual_obj: Comment = Comment.objects.all().first()
        assert actual_obj.body == comment_data["body"]
        assert actual_obj.post.id == comment_data["post"]
        assert actual_obj.author.id == comment_data["author"]

    def test_should_retrieve_existing_comment(self, client, comment_url, comment):
        response = client.get(comment_url)
        # THEN
        assert response.status_code == status.HTTP_200_OK, response.content
        actual_data = response.data
        assert comment.id == actual_data["id"]
        assert comment.body == actual_data["body"]
        assert comment.post.id == actual_data["post"]
        assert comment.author.id == actual_data["author"]

    def test_should_fail_to_retrieve_non_existing_comment(self, client, missing_comment_url):
        response = client.get(missing_comment_url)
        # THEN
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content

    def test_should_update_existing_comment(
        self, client: Client, comment, comment_url, comment_data
    ):
        updated_body = "Updated Comment"
        comment_data["body"] = updated_body
        # WHEN
        response = client.put(comment_url, data=comment_data, content_type=CONTENT_TYPE)
        # THEN request is successfull
        assert response.status_code == status.HTTP_200_OK, response.content
        comment.refresh_from_db()
        assert comment.body == updated_body

    def test_should_fail_to_update_non_existing_comment(self, client, missing_comment_url):
        response = client.put(missing_comment_url, content_type=CONTENT_TYPE)
        # THEN
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content

    def test_should_delete_existing_comment(self, client: Client, comment, comment_url):
        # WHEN
        client.delete(comment_url)
        # THEN
        with pytest.raises(Comment.DoesNotExist):
            comment.refresh_from_db()

    def test_should_fail_to_delete_non_existing_post(self, client, missing_comment_url):
        response = client.delete(missing_comment_url)
        # THEN
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content




class TestTagUrls:
    def test_should_list_tags(self, client: Client, tags_url, tag):
        response = client.get(tags_url)
        # THEN request is successfull
        assert response.status_code == status.HTTP_200_OK, response.content
        # AND response contains all expected tags
        (actual_data,) = response.data
        # AND acutal tags match expected
        assert tag.id == actual_data["id"]

    def test_should_create_tag(self, client: Client, tags_url, tag_data):
        response = client.post(tags_url, data=tag_data, content_type=CONTENT_TYPE)
        # THEN request is successfull
        assert response.status_code == status.HTTP_201_CREATED, response.content
        actual_obj: Comment = Tag.objects.all().first()
        assert actual_obj.name == tag_data["name"]

    def test_should_retrieve_existing_tag(self, client, tag_url, tag):
        response = client.get(tag_url)
        # THEN
        assert response.status_code == status.HTTP_200_OK, response.content
        actual_data = response.data
        assert tag.id == actual_data["id"]
        assert tag.name == actual_data["name"]

    def test_should_fail_to_retrieve_non_existing_tag(self, client, missing_tag_url):
        response = client.get(missing_tag_url)
        # THEN
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content

    def test_should_update_existing_tag(
        self, client: Client, tag, tag_url, tag_data
    ):
        updated_name = "Updated Tag"
        tag_data["name"] = updated_name
        # WHEN
        response = client.put(tag_url, data=tag_data, content_type=CONTENT_TYPE)
        # THEN request is successfull
        assert response.status_code == status.HTTP_200_OK, response.content
        tag.refresh_from_db()
        assert tag.name == updated_name

    def test_should_fail_to_update_non_existing_tag(self, client, missing_tag_url):
        response = client.put(missing_tag_url, content_type=CONTENT_TYPE)
        # THEN
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content

    def test_should_delete_existing_tag(self, client: Client, tag, tag_url):
        # WHEN
        client.delete(tag_url)
        # THEN
        with pytest.raises(Tag.DoesNotExist):
            tag.refresh_from_db()

    def test_should_fail_to_delete_non_existing_post(self, client, missing_tag_url):
        response = client.delete(missing_tag_url)
        # THEN
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content


