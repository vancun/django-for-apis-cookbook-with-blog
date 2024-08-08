import pytest
from django_fsm import (
    TransitionNotAllowed,
    get_available_FIELD_transitions,
    get_available_user_FIELD_transitions,
    has_transition_perm,
)
from posts.models import Post, PostState

pytestmark = [pytest.mark.django_db]


class TestPostState:
    # DRAFT

    def test_should_have_draft_state_after_created(self, user):
        post = Post(author=user)
        assert post.state == PostState.DRAFT

    def test_should_permit_to_draft_from_archive_by_author(self, post, user):
        assert has_transition_perm(post.draft, user)

    def test_should_not_permit_to_draft_from_archive_by_not_author(self, post, user2):
        assert not has_transition_perm(post.draft, user2)

    def test_should_transition_to_draft_from_archived_after_draft(self, post):
        post.state = PostState.ARCHIVED
        post.save()
        post.draft()
        assert post.state == PostState.DRAFT

    # PUBLISHED

    def test_should_not_permit_publish_by_non_author(self, post, user2):
        assert not has_transition_perm(post.publish, user2)

    def test_should_not_allow_publish_from_archived_after_draft(self, post):
        post.state = PostState.ARCHIVED
        post.save()
        with pytest.raises(TransitionNotAllowed):
            post.publish()

    def test_should_allow_to_publish_by_author(self, post, user):
        assert has_transition_perm(post.publish, user)

    def test_should_transition_to_published_from_draft_after_publish(self, post):
        post.publish()
        assert post.state == PostState.PUBLISHED

    # ARCHIVED

    def test_should_not_permit_archive_by_non_author(self, post, user2):
        assert not has_transition_perm(post.archive, user2)

    def test_should_permit_archive_by_author(self, post, user):
        assert has_transition_perm(post.archive, user)

    def test_should_transition_to_archived_from_draft_after_archive(self, post):
        post.archive()
        assert post.state == PostState.ARCHIVED

    def test_should_transition_to_archived_from_published_after_archive(self, post):
        post.state = PostState.PUBLISHED
        post.archive()
        assert post.state == PostState.ARCHIVED

    # PARAMETRIZED

    @pytest.mark.parametrize(
        "state,expect_states,user_fixture",
        (
            (PostState.DRAFT, ["draft", "publish", "archive"], None),
            (PostState.DRAFT, ["draft", "publish", "archive"], "user"),
            (PostState.DRAFT, [], "user2"),
            (PostState.PUBLISHED, ["draft", "archive"], None),
            (PostState.PUBLISHED, ["draft", "archive"], "user"),
            (PostState.PUBLISHED, [], "user2"),
            (PostState.ARCHIVED, ["draft"], None),
            (PostState.ARCHIVED, ["draft"], "user"),
            (PostState.ARCHIVED, [], "user2"),
        ),
    )
    def test_should_return_available_state_transitions(
        self, post, request, state, expect_states, user_fixture
    ):
        post.state = state
        state_field = Post._meta.get_field("state")
        if user_fixture:
            user = request.getfixturevalue(user_fixture)
            available_state_names = [
                t.name for t in get_available_user_FIELD_transitions(post, user, state_field)
            ]
        else:
            available_state_names = [
                t.name for t in get_available_FIELD_transitions(post, state_field)
            ]
        assert sorted(available_state_names) == sorted(expect_states)
