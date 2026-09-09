from typer.testing import CliRunner
from unittest.mock import patch
from github_cli.cli import app
from github_cli.exceptions import UserNotFoundError

runner = CliRunner()

#on verifie l'aide --help
def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "profile" in result.stdout
    assert "repos" in result.stdout

#on simule un renvoi de donnee de GithubClient.get_user_profile
@patch("github_cli.cli.GitHubClient.get_user_profile")
def test_profile_command_success(mock_get_profile):
    mock_get_profile.return_value = {
        "login": "octocat",
        "name": "The Octocat",
        "bio": "Mascote Github",
        "location": "San Fransico",
        "public_repos": 8
    }
    result= runner.invoke(app, ["profile", "octocat"])

    assert result.exit_code == 0
    assert "octocat"in result.stdout
    assert "The Octocat" in result.stdout


#on s'assure que la cli affiche bien le message d'erreur en cas de UserNotFoundError
@patch("github_cli.cli.GitHubClient.get_user_profile")
def test_profile_command_user_not_found(mock_get_profile):
    mock_get_profile.side_effect = UserNotFoundError("inconnu")

    result = runner.invoke(app, ["profile", "inconnu"])

    assert result.exit_code == 1
    assert "n'existe pas" in result.stdout

    