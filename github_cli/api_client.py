import os
from urllib import response 
from dotenv import load_dotenv
import requests
from github_cli.exceptions import APIConnectionError, AuthenticationError, GitHubCLIError, RateLimitExceededError, UserNotFoundError, UserNotFoundError
import responses

class GitHubClient:
    def __init__(self, token: str| None = None):
        self.base_url = "https://api.github.com"
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.headers = {"Accept": "application/vnd.github.v3+json", "X-GitHub-Api-Version": "2022-11-28"}

        if self.token:
            self.headers["Authorization"] = "bearer " + self.token

    #methode privée pour effectuer les requetes GET, gerer les erreurs et  et retourner les données JSON
    def _get(self, endpoint:str, params: dict | None = None):
        try:
            url = f"{self.base_url}/{endpoint}"
            request = requests.get(url,headers = self.headers, params=params, timeout=10)
        
        except requests.exceptions.ConnectionError:
            raise APIConnectionError()
        except requests.exceptions.Timeout:
            raise APIConnectionError()
        
        if request.status_code == 404:
            raise UserNotFoundError("User not found")

        if request.status_code == 401:
            raise AuthenticationError()

        if request.status_code in (403, 429):
            reset_time = request.headers.get("X-RateLimit-Reset")
            raise RateLimitExceededError(reset_time)

        if request.status_code >= 500:
            raise GitHubCLIError("Server error. Please try again later.")

        if 200 <= request.status_code < 300:
            return request.json()

        
        




    #methodes publiques pour interagir avec l'API GitHub
    def get_user_profile(self, username:str):
        return self._get(f"users/{username}")

    def get_user_repos(self, username:str, per_page:int = 30, page:int = 1):
        params = {"per_page": per_page, "page": page, "sort": "updated", "direction": "desc"} 
        return self._get(f"users/{username}/repos", params=params)

    def get_starred_repos(self, username:str, per_page:int = 30, page:int = 1):
        params = {"per_page": per_page, "page": page, "sort": "updated", "direction": "desc"}
        return self._get(f"users/{username}/starred", params=params)

    def get_user_activity(self, username:str, per_page:int = 30, page:int = 1):
        params = {"per_page": per_page, "page": page}
        return self._get(f"users/{username}/events/public", params=params)






#verification de la validité du nom d'utilisateur GitHub
def validate_username(username: str) -> bool:
    import re
    pattern = r'^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$'
    return bool(re.match(pattern, username))





if __name__ == "__main__":
    from github_cli.exceptions import (GitHubCLIError, UserNotFoundError, RateLimitExceededError, AuthenticationError, APIConnectionError) 

    client = GitHubClient()

   # 1. Test Cas Nominal (Succès)
    print("--- 1. Test Succès (200) ---")
    try:
        user = client.get_user_profile("octocat")
        print("OK : Profil récupéré pour", user.get("login"))
    except Exception as e:
        print("Échec inattendu :", e)

    # 2. Test Utilisateur Inexistant (404)
    print("\n--- 2. Test 404 (User Inexistant) ---")
    try:
        # Pseudo très improbable pour garantir le 404
        client.get_user_profile("ce-compte-n-existe-absolument-pas-998877")
        print("Erreur : la méthode aurait dû lever UserNotFoundError !")
    except UserNotFoundError as e:
        print("OK : Exception interceptée correctement ->", type(e).__name__, e)

    # 3. Test Token Invalide (401)
    print("\n--- 3. Test 401 (Token Invalide) ---")
    bad_client = GitHubClient(token="ghp_faux_token_invalide")
    try:
        bad_client.get_user_profile("octocat")
        print("Erreur : la méthode aurait dû lever AuthenticationError !")
    except AuthenticationError as e:
        print("OK : Exception interceptée correctement ->", type(e).__name__)

    # 4. Test Coupure Réseau / Mauvaise URL (ConnectionError)
    print("\n--- 4. Test Erreur Réseau ---")
    offline_client = GitHubClient()
    offline_client.base_url = "https://api.github-adresse-invalide-test.com"
    try:
        offline_client.get_user_profile("octocat")
        print("Erreur : la méthode aurait dû lever APIConnectionError !")
    except APIConnectionError as e:
        print("OK : Exception interceptée correctement ->", type(e).__name__)