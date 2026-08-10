import pytest

from models.user import User


def test_create_user(user_repo):
    user = User(
        name="Alice",
        email="alice@example.com",
        password_hash="hashed_password",
    )
    created_user = user_repo.create(user)
    assert created_user.id is not None
    assert created_user.name == "Alice"
    assert created_user.email == "alice@example.com"
    assert created_user.password_hash == "hashed_password"
    saved_user = user_repo.find_by_id(created_user.id)
    assert saved_user is not None
    assert saved_user.id == created_user.id
    assert saved_user.name == "Alice"
    assert saved_user.email == "alice@example.com"
    assert saved_user.password_hash == "hashed_password"
    assert created_user.created_at is not None


def test_find_user_by_id(user_repo, sample_user: User):
    found_user = user_repo.find_by_id(sample_user.id)
    assert found_user is not None
    assert found_user.id == sample_user.id
    assert found_user.name == sample_user.name
    assert found_user.email == sample_user.email
    assert found_user.password_hash == sample_user.password_hash
    assert found_user.created_at == sample_user.created_at


def test_find_user_by_id_returns_none_for_invalid_user(user_repo):
    user = user_repo.find_by_id(99999)
    assert user is None


def test_find_user_by_email(user_repo, sample_user):
    found_user = user_repo.find_by_email(sample_user.email)
    assert found_user.email is not None
    assert found_user.email == sample_user.email
    assert found_user.name == sample_user.name
    assert found_user.password_hash == sample_user.password_hash
    assert found_user.id == sample_user.id
    assert found_user.created_at == sample_user.created_at


def test_find_user_by_email_returns_none_for_invalid_user(user_repo):
    user = user_repo.find_by_email("abc@abc.com")
    assert user is None


def test_find_all(user_repo):
    user1 = User(
        name="Alice",
        email="alice@example.com",
        password_hash="password1",
    )

    user2 = User(
        name="Bob",
        email="bob@example.com",
        password_hash="password2",
    )

    user_repo.create(user1)
    user_repo.create(user2)

    users = user_repo.find_all()
    assert len(users) == 2
    emails = {user.email for user in users}
    assert emails == {
        "alice@example.com",
        "bob@example.com",
    }


def test_exists_by_email(user_repo, sample_user):
    found_user = user_repo.exists_by_email(sample_user.email)
    assert found_user is True


def test_exists_by_email_returns_none_if_invalid_email(user_repo):
    user = user_repo.exists_by_email("abc@abc.com")
    assert user is False


def test_update_name(user_repo, sample_user):
    sample_user.name = "Alice Smith"
    updated_user = user_repo.update_name(sample_user.id, sample_user.name)
    assert updated_user.name == "Alice Smith"
    saved_user = user_repo.find_by_id(sample_user.id)
    assert saved_user is not None
    assert saved_user.name == "Alice Smith"


def test_update_name_returns_none_if_invalid_user(user_repo):
    user = User(
        id=99999,
        name="Alice",
        email="alice@example.com",
        password_hash="password",
    )
    updated_user = user_repo.update_name(user.id, user.name)
    assert updated_user is None


def test_delete(user_repo, sample_user):
    user = user_repo.find_by_id(sample_user.id)
    assert user_repo.delete(user.id) is True


def test_delete_returns_false_for_invalid_user(user_repo):
    user = User(
        id=99999,
        name="Alice",
        email="alice@example.com",
        password_hash="password",
    )
    assert user_repo.delete(user.id) is False
