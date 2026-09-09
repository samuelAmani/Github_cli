import pytest
import responses
from github_cli.api_client import GitHubClient
from github_cli.exceptions import (UserNotFoundError, RateLimitExceededError, AuthenticationError, APIConnectionError)


@responses.activate
def test_get_user_profile_success():
    client = GitHubClient()

    responses.add(
        method=responses.GET,
        url="https://api.github.com/users/octocat",
        json={"login": "octocat", "name": "The Octocat"},
        status=200
    )
    user = client.get_user_profile("octocat")
    assert user["login"] == "octocat"

@responses.activate
def test_get_user_profile_not_found():
    client = GitHubClient()

    responses.add(
        method=responses.GET,
        url="https://api.github.com/users/inconnu",
        #json={"login": "octocat", "name": "The Ocotcat"},
        status=404,
    )
    with pytest.raises(UserNotFoundError):
        client.get_user_profile("inconnu")

@responses.activate
def test_rate_limit_exceed():
    client = GitHubClient()

    responses.add(
        method=responses.GET,
        url="https://api.github.com/users/inconnu",
        headers={"X-Ratelimit-Reset": "1672531199"},
        status=403,
    )
    with pytest.raises(RateLimitExceededError):
        client.get_user_profile("inconnu")

@responses.activate
def test_authentification_error():
    client = GitHubClient()
    responses.add(
        method=responses.GET,
        url="https://api.github.com/users/inconnu",
        status=401,
    )
    with pytest.raises(AuthenticationError):
        client.get_user_profile("inconnu")