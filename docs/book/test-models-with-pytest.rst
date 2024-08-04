Test Models with Pytest
=============================

In this guide we are going to:

1. Setup our project for testing with ``pytest``.
2. Create tests for the ``CustomUser`` model.
3. Create tests for the ``Post`` model.
4. Create tests for the ``Comment`` model.
5. Create tests for the ``Tag`` model.
6. Execute the test suite.

Pre-requisites
++++++++++++++++++++

Requires the :doc:`create-blogapi-django-models` guide to be completed.

Guide code:
+++++++++++++++++

- `test-models-with-pytest <https://github.com/vancun/django-for-apis-cookbook-with-blog/tree/recipe/test-models-with-pytest>`_ branch in the GitHub `repository <https://github.com/vancun/django-for-apis-cookbook-with-blog>`_.


Setup for Testing with Pytest
++++++++++++++++++++++++++++++

Create folder for tests :file:`/src/tests/` and add an empty :file:`/src/tests/__init__.py` file to it:

.. code-block:: bash

    mkdir src/tests
    touch src/tests/__init__.py

Create file :file:`/src/tests/pytest.ini` to configure ``pytest``:

.. code-block:: ini

    [pytest]
    DJANGO_SETTINGS_MODULE = blogapi.settings

    testpaths = 
        src/tests

    pythonpath = 
        src

    addopts = -v

    markers =
        model: mark test as model-related

Configure VSCode for ``pytest``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Open the command palete (Ctrl-Shift-P)
2. Select ``Python: Configure Tests`` command.
3. Select ``pytest`` as testing framework.
4. Select ``src`` as folder to search for tests.



Test the ``CustomUser`` Model
++++++++++++++++++++++++++++++++

Let's create Python pacakge for ``accounts`` app tests:

.. code-block:: bash

    mkdir src/tests/accounts
    touch src/tests/accounts/__init__.py

And now let's create a test class to test the ``CustomUser`` model with first test.

.. code-block:: python

    # /src/tests/accounts/test_models.py
    from accounts.models import CustomUser

    class TestCustomUser:
        def test_should_be_returned_by_get_user_model(self):
            user_model = get_user_model()
            assert user_model is CustomUser

Execute the tests
~~~~~~~~~~~~~~~~~~~~~

Execute the tests from the command line:

.. code-block:: bash

    pytest

.. code-block:: text

    ================================== test session starts ===================================
    platform linux -- Python 3.10.13, pytest-8.3.2, pluggy-1.5.0
    django: version: 5.0.7, settings: blogapi.settings (from ini)
    rootdir: /workspaces/django-for-apis-cookbook-with-blog
    configfile: pytest.ini
    testpaths: src/tests
    plugins: anyio-4.4.0, cov-5.0.0, django-4.8.0
    collected 1 item                                                                         

    src/tests/accounts/test_models.py::TestCustomUser::test_should_be_recognized_as_user_model_by_django_auth PASSED [100%]

    =================================== 1 passed in 0.04s ====================================

Exclude model tests
~~~~~~~~~~~~~~~~~~~~~

In :file:`pytest.ini` we defined ``model`` mark which allows us to selectively include or exclude model tests.

.. code-block:: bash

    pytest -m "not model"

.. code-block:: text

    =============================================== test session starts ================================================
    platform linux -- Python 3.10.13, pytest-8.3.2, pluggy-1.5.0
    django: version: 5.0.7, settings: blogapi.settings (from ini)
    rootdir: /workspaces/django-for-apis-cookbook-with-blog
    configfile: pytest.ini
    testpaths: src/tests
    plugins: anyio-4.4.0, cov-5.0.0, django-4.8.0
    collected 1 item / 1 deselected / 0 selected                                                                       

    ============================================== 1 deselected in 0.06s ===============================================

More ``CustomUser`` tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We are going to create tests that user can be created and deleted.

First let's create a ``user`` fixture which could be used in all project tests:

.. code-block:: python

    # src/conftest.py
    import pytest

    from accounts.models import CustomUser

    @pytest.fixture(name="user")
    def given_user():
        u = CustomUser.objects.create()
        return u

And add create delete tests to :file:`src/tests/accounts/test_models.py`:

.. code-block:: python

    # ............
    class TestCustomUser:
        # ............

        @pytest.mark.django_db
        def test_should_create_user_instance(self):
            # WHEN New user model instance is created
            u = CustomUser.objects.create()
            # THEN the object is a CustomUser instance
            assert isinstance(u, CustomUser)
            # AND is persisted in the database
            u.refresh_from_db()

        @pytest.mark.django_db
        def test_should_delete_user_instance(self, user: CustomUser):
            # WHEN User is deleted
            user.delete()
            # THEN the user instance is no longer found in the database
            with pytest.raises(CustomUser.DoesNotExist):
                user.refresh_from_db()

Running the tests:

.. code-block:: text

    ================================================ test session starts ================================================
    platform linux -- Python 3.10.13, pytest-8.3.2, pluggy-1.5.0 -- /home/codespace/.python/current/bin/python
    cachedir: .pytest_cache
    django: version: 5.0.7, settings: blogapi.settings (from ini)
    rootdir: /workspaces/django-for-apis-cookbook-with-blog
    configfile: pytest.ini
    testpaths: src/tests
    plugins: anyio-4.4.0, cov-5.0.0, django-4.8.0
    collected 3 items                                                                                                   

    src/tests/accounts/test_models.py::TestCustomUser::test_should_create_user_instance PASSED                    [ 33%]
    src/tests/accounts/test_models.py::TestCustomUser::test_should_delete_user_instance PASSED                    [ 66%]
    src/tests/accounts/test_models.py::TestCustomUser::test_should_be_recognized_as_user_model_by_django_auth PASSED [100%]

    ================================================= 3 passed in 0.23s =================================================


Test the ``Post`` Model
++++++++++++++++++++++++

Create test package for ``posts`` app:

.. code-block:: bash

    mkdir src/tests/posts
    touch src/tests/posts/__init__.py

And add a :file:`src/tests/posts/test_models.py` file to it:

.. code-block:: python

    import pytest

    from posts.models import Post

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

For above test we also created a ``post`` fixture in :file:`src/tests/conftest.py`:

.. code-block:: python

    # src/tests/conftest.py
    import pytest

    from accounts.models import CustomUser
    from posts.models import Post

    # .......................

    @pytest.fixture(name="post")
    def given_post(user):
        p = Post.objects.create(
            author=user,
        )
        return p


Test the ``Comment`` Model
+++++++++++++++++++++++++++

Add the tests for the ``Comment`` model to :file:`src/tests/posts/test_models.py`:

.. code-block:: python

    # src/tests/posts/test_models.py
    import pytest

    from posts.models import Comment, Post

    pytestmark = pytest.mark.model

    # .........................

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
            # THEN the post instance is no longer found in the database
            with pytest.raises(Comment.DoesNotExist):
                comment.refresh_from_db()

        @pytest.mark.django_db
        def test_should_delete_comment_when_post_is_deleted(self, post: Post, comment: Comment):
            # WHEN post is deleted
            post.delete()
            # THEN the comment is also deleted
            with pytest.raises(Comment.DoesNotExist):
                comment.refresh_from_db()

Also add a ``comment`` fixture to :file:`src/tests/conftest.py`:

.. code-block:: python

    import pytest

    from accounts.models import CustomUser
    from posts.models import Comment, Post

    # .....................

    @pytest.fixture(name="comment")
    def given_comment(post, user):
        c = Comment.objects.create(
            post=post,
            author=user,
        )
        return c


Test the ``Tag`` Model
++++++++++++++++++++++++++++++

Add the tests for the ``Tag`` model to :file:`src/tests/posts/test_models.py`:

.. code-block:: python

    # src/tests/posts/test_models.py
    import pytest

    from posts.models import Comment, Post, PostTag, Tag

    pytestmark = pytest.mark.model

    # ........................

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


Add also fixtures to :file:`src/tests/conftest.py`:

.. code-block:: python

    # src/tests/conftest.py
    import pytest

    from accounts.models import CustomUser
    from posts.models import Comment, Post, Tag

    # ...................................

    @pytest.fixture(name="post_with_tag")
    def given_post_with_tag(post, tag):
        post.tags.set([tag])
        return post

    @pytest.fixture(name="tag")
    def given_tag(post, user):
        t = Tag.objects.create(
            name="Tag",
        )
        return t

Execute the test suite
++++++++++++++++++++++++++++++++++

Running ``pytest`` from the command line passes all tests:

.. code-block:: text

    ================================================ test session starts ================================================
    platform linux -- Python 3.10.13, pytest-8.3.2, pluggy-1.5.0 -- /home/codespace/.python/current/bin/python
    cachedir: .pytest_cache
    django: version: 5.0.7, settings: blogapi.settings (from ini)
    rootdir: /workspaces/django-for-apis-cookbook-with-blog
    configfile: pytest.ini
    testpaths: src/tests
    plugins: anyio-4.4.0, cov-5.0.0, django-4.8.0
    collected 12 items                                                                                                  

    src/tests/accounts/test_models.py::TestCustomUser::test_should_create_user_instance PASSED                    [  8%]
    src/tests/accounts/test_models.py::TestCustomUser::test_should_delete_user_instance PASSED                    [ 16%]
    src/tests/posts/test_models.py::TestPost::test_should_create_post_instance PASSED                             [ 25%]
    src/tests/posts/test_models.py::TestPost::test_should_delete_post_instance PASSED                             [ 33%]
    src/tests/posts/test_models.py::TestComment::test_should_create_comment_instance PASSED                       [ 41%]
    src/tests/posts/test_models.py::TestComment::test_should_delete_comment_instance PASSED                       [ 50%]
    src/tests/posts/test_models.py::TestComment::test_should_delete_comment_when_post_is_deleted PASSED           [ 58%]
    src/tests/posts/test_models.py::TestTag::test_should_create_tag_instance PASSED                               [ 66%]
    src/tests/posts/test_models.py::TestTag::test_should_delete_tag_instance PASSED                               [ 75%]
    src/tests/posts/test_models.py::TestTag::test_should_remove_tag_from_post_when_tag_is_deleted PASSED          [ 83%]
    src/tests/posts/test_models.py::TestTag::test_should_not_delete_tag_when_post_is_deleted PASSED               [ 91%]
    src/tests/accounts/test_models.py::TestCustomUser::test_should_be_recognized_as_user_model_by_django_auth PASSED [100%]

    ================================================ 12 passed in 0.38s =================================================

