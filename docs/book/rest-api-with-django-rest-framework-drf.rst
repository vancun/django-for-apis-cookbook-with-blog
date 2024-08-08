REST API with Djangno Rest Rest Framework
============================================

In this guide we will perform following steps:

1. Install Django Rest Framework
2. Create model serializers for the ``posts`` application models
3. Create model viewsets for the ``posts`` application models
4. Explore the APIs using Django Rest Framework browsable API
5. Create tests for the ``posts`` application REST API

Pre-requisites
++++++++++++++++++++

Requires the :doc:`create-blogapi-django-models` guide to be completed (:doc:`test-models-with-pytest` - recommended).

Guide code:
+++++++++++++++++

- `custom-django-user-model <https://github.com/vancun/django-for-apis-cookbook-with-blog/tree/recipe/rest-api>`_ branch in the GitHub `repository <https://github.com/vancun/django-for-apis-cookbook-with-blog>`_.

Install Django Rest Framework
+++++++++++++++++++++++++++++++++

Add ``djangorestframework`` the the project dependencies in :file:`requirements.txt`:

.. code-block:: text

    -r docs/requirements.txt
    django
    djangorestframework
    pytest
    pytest-cov
    pytest-django
    python-dotenv

Install the dependencies:

.. code-block:: bash

    pip install -U -r requirements.txt

Add ``rest_framework`` to ``INSTALLED_APPS`` in :file:`src/blogapi/settings.py`:

.. code-block:: python

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # 3rd Party
        "rest_framework",   # new
        # Local
        "accounts.apps.AccountsConfig",
        "posts.apps.PostsConfig",
    ]

Create Model Serializers
+++++++++++++++++++++++++++++++++

.. code-block:: python

    # src/posts/serializers.py

    from rest_framework import serializers
    from .models import Post, Comment, Tag

    class TagSerializer(serializers.ModelSerializer):
        class Meta:
            model = Tag
            fields = ['id', 'name']

    class PostSerializer(serializers.ModelSerializer):
        tags = TagSerializer(many=True, read_only=True)
        class Meta:
            model = Post
            fields = ['id', 'title', 'body', 'author', 'created_at', 'updated_at', 'tags']

    class CommentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ['id', 'post', 'body', 'author', 'created_at', 'updated_at']

Create Model ViewSets
++++++++++++++++++++++++++++++

.. code-block:: python

    # src/posts/views.py

    from rest_framework import viewsets
    from .models import Post, Comment, Tag
    from .serializers import PostSerializer, CommentSerializer, TagSerializer

    class PostViewSet(viewsets.ModelViewSet):
        queryset = Post.objects.all()
        serializer_class = PostSerializer

    class CommentViewSet(viewsets.ModelViewSet):
        queryset = Comment.objects.all()
        serializer_class = CommentSerializer

    class TagViewSet(viewsets.ModelViewSet):
        queryset = Tag.objects.all()
        serializer_class = TagSerializer

Define URL Routing for the Posts Application
++++++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: python

    # src/posts/urls.py

    from django.urls import path, include
    from rest_framework.routers import DefaultRouter
    from .views import PostViewSet, CommentViewSet, TagViewSet

    router = DefaultRouter()
    router.register(r'posts', PostViewSet)
    router.register(r'comments', CommentViewSet)
    router.register(r'tags', TagViewSet)

    urlpatterns = [
        path('', include(router.urls)),
    ]

Add Posts Application URL Routes to the Project's URL Routes
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: python

    # src/blogapi/urls.py
    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include('posts.urls')),
    ]

Explore the API
++++++++++++++++++++++++++++++

Start a development server:

.. code-block:: bash

    python src/manage.py runserver

And open http://localhost:8000/api/ in a web browser. You can explore the API through Django Rest Framework's browsable API feature.

In future recipe we will implement Swagger interface which is much more common UI.


Create Tests for the ``posts`` application API
+++++++++++++++++++++++++++++++++++++++++++++++++

Here is the source for the full set of tests:

.. code-block:: python

    # /src/tests/posts/test_urls.py
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


Questions
++++++++++++++++++

1. The API tests are missing some test cases. Can you spot which are they and implement them?

Further Reading
+++++++++++++++++++++++

1. `Django Rest Framework <https://www.django-rest-framework.org/>`_
2. `Django for APIs <https://djangoforapis.com/>`_ book
3. `Good Code, Bad Code <https://learning.oreilly.com/library/view/good-code-bad/9781617298936/OEBPS/Text/P3.htm>`_ book - Part 3. Unit Testing
4. `Python Testing with Pytest <https://learning.oreilly.com/library/view/python-testing-with/9781680509427/>`_, Second Edition
5. `From Testing Pyramid to Diamond <https://steven-giesel.com/blogPost/86b6fae7-95a7-44fa-a85a-00ee1b6dd697>`_
6. `Test Shapes <https://testerstories.com/2020/09/test-shapes/>`_
