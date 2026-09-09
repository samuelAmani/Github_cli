from rich.table import Table
import typer
from typer import Argument, Option
from rich.console import Console
from rich.panel import Panel
from github_cli.api_client import GitHubClient, validate_username
from github_cli.logger import setup_logger
from github_cli.exceptions import (GitHubCLIError, UserNotFoundError, RateLimitExceededError, APIConnectionError)

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    help="CLI Github pour explorer profils, dépôts et activités des utilisateurs GitHub."
                  )
console = Console()


@app.command()
def profile(
            username: str = typer.Argument(..., help="Le nom d'utilisateur GitHub"), 
            verbose: bool = typer.Option(False, "--verbose", "-v", help="Activer les logs détaillés.")
            ):
    """
    Affiche le profil d'un utilisateur GitHub.
    """
    setup_logger(verbose=verbose)
    client = GitHubClient()
    try:
        user = client.get_user_profile(username)
        console.print(f"[bold green]Profil de l'utilisateur {username} :[/bold green]")
    except UserNotFoundError as u:
        console.print(f"[bold red]Erreur : [/bold red] L'utilsateur {u.username} n'existe pas.")
        raise typer.Exit(code=1)
    except RateLimitExceededError as r:
        console.print(f"[bold red]Erreur : [/bold red] {r.message}")
        raise typer.Exit(code=1)
    except APIConnectionError as a:
        console.print(f"[bold red]Erreur : [/bold red] {a.message}")
        raise typer.Exit(code=1)

    console.print(Panel(f"[bold blue]Pseudo :[/bold blue] {user.get('login')}\n"
                             f"[bold blue]Nom :[/bold blue] {user.get('name')}\n"
                             f"[bold blue]Bio :[/bold blue] {user.get('bio')}\n"
                             f"[bold blue]Localisation :[/bold blue] {user.get('location')}\n"
                             f"[bold blue]Nombre de dépôts publics :[/bold blue] {user.get('public_repos')}\n"))



@app.command()
def repos(
    username: str = typer.Argument(..., help="Le nom d'utilisateur GitHub"),
    limit: int = typer.Option(10, "--limit", "-l", help="Nombre de dépôts à afficher"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Activer les logs détaillés.")
):
    setup_logger(verbose=verbose)
    client = GitHubClient()

    try:
        repos_data = client.get_user_repos(username, per_page=limit)
    except UserNotFoundError as u:
        console.print(f"[bold red]Erreur : [/bold red] L'utilisateur {u.username} n'existe pas.")
        raise typer.Exit(code=1)

    table = Table(title=f"📁 Dépôts publics de {username}")
    table.add_column("Nom", style="cyan", no_wrap=True)
    table.add_column("Language", style="green")
    table.add_column("Etoiles ⭐", justify="right", style="yellow")

    for repo in repos_data:
        table.add_row(repo["name"], str(repo["language"]or "N/A"), str(repo["stargazers_count"]))
    console.print(table)

@app.command()
def starred(
    username: str = typer.Argument(..., help="Le nom d'utilisateur GitHub"),
    limit: int = typer.Option(10, "--limit", "-l", help="Nombre de dépôts à afficher"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Activer les logs détaillés.")
):
    setup_logger(verbose=verbose)
    client = GitHubClient()

    try:
        starred_data = client.get_starred_repos(username, per_page=limit)
    except UserNotFoundError as u:
        console.print(f"[bold red]Erreur : [/bold red] L'utilisateur {u.username} n'existe pas.")
        raise typer.Exit(code=1)

    table = Table(title=f"⭐ Dépôts suivis (étoilés) par {username}")
    table.add_column("Nom", style="cyan", no_wrap=True)
    table.add_column("Language", style="green")
    table.add_column("Etoiles ⭐", justify="right", style="yellow")

    for repo in starred_data:
        table.add_row(repo["name"], str(repo["language"]or "N/A"), str(repo["stargazers_count"]))
    console.print(table)

@app.command()
def activity(
    username: str = typer.Argument(..., help="Le nom d'utilisateur GitHub"),
    limit: int = typer.Option(10, "--limit", "-l", help="Nombre de dépôts à afficher"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Activer les logs détaillés.")
):
    setup_logger(verbose=verbose)
    client = GitHubClient()

    try:
        activity_data = client.get_user_activity(username, per_page=limit)

    except UserNotFoundError as u:
        console.print(f"[bold red]Erreur : [/bold red] L'utilisateur {u.username} n'existe pas.")
        raise typer.Exit(code=1)
    
    if not activity_data:
        console.print(f"[yellow]Aucune activité publique récente pour {username}.[/yellow]")
        return

    table = Table(title=f"⚡ Activité publique récente de {username}")
    table.add_column("Type d'événement", style="cyan", no_wrap=True)
    table.add_column("Dépot concerné", style="green")
    table.add_column("Date",style="yellow")

    for event in activity_data:
        event_type = event.get("type", "Inconnu")

        repo_name = event.get("repo", {}).get("name", "N/A")

        created_at = event.get("created_at", "")[:10]

        table.add_row(event_type, repo_name, created_at)

    console.print(table)

        



if __name__ == "__main__":
    app()   