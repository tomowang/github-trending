
import os
import logging
import json
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import click

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s %(filename)s:%(lineno)d - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output to console
    ],
)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
headers = {
    "User-Agent": USER_AGENT,
}

# Initialize FastAPI app
app = FastAPI(
    title="GitHub Trending Crawler API",
    description="API to crawl GitHub trending repositories and return structured data."
)


# Pydantic model for the structured repository data
class TrendingRepository(BaseModel):
    """
    Represents a single trending GitHub repository.
    """
    name: str
    description: Optional[str] = None
    language: Optional[str] = None
    stars: int
    forks: int
    today_stars: Optional[int] = 0  # Optional field for today's stars
    built_by: List[str] = []  # List of contributor usernames


@app.get("/trending", response_model=List[TrendingRepository])
async def get_trending_api():
    """
    Endpoint to get trending repositories from GitHub.
    Returns a list of structured data for each repository.
    """
    try:
        repositories = get_trending_repositories()
        logging.info(f"Fetched {len(repositories)} trending repositories.")
        return repositories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/trending/{language}", response_model=List[TrendingRepository])
async def get_trending_by_language(language: str):
    """
    Endpoint to get trending repositories from GitHub by language.
    Returns a list of structured data for each repository.
    """
    try:
        repositories = get_trending_repositories(language)
        logging.info(f"Fetched {len(repositories)} trending repositories.")
        return repositories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@click.group()
def cli():
    """A command-line interface for fetching GitHub trending repositories."""
    pass # This group doesn't do anything by itself, it just holds subcommands.


@cli.command("trending")
@click.option(
    "--language", default=None,
    help="Optional option to return trending repositories by specific programming language.")
def get_trending_command(language: Optional[str] = None):
    """
    Command-line interface to fetch trending repositories.
    """
    try:
        repositories = get_trending_repositories(language)
        logging.info(f"Fetched {len(repositories)} trending repositories.")
        click.echo(json.dumps([repo.model_dump() for repo in repositories]))
        return 0
    except Exception as e:
        logging.error(f"Error fetching trending repositories: {e}")
        raise click.ClickException(f"Failed to fetch trending repositories: {e}")


def get_trending_repositories(language: Optional[str] = None) -> List[TrendingRepository]:
    """
    Crawls github.com/trending, extracts structured data for repositories,
    and returns it. This data can then be saved to a database like Supabase.
    """
    trending_url = "https://github.com/trending"
    if language:
        trending_url += f"/{language.lower()}"

    try:
        # Fetch the trending page content
        response = requests.get(trending_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch GitHub trending page: {e}")

    repositories_data = []
    # Find all articles representing repositories
    # GitHub's trending page uses <article> tags with specific classes
    repo_articles = soup.find_all("article", class_="Box-row")

    for rank, article in enumerate(repo_articles):
        try:
            # Extract repository name
            title_tag = article.find("h2", class_="h3")
            if title_tag and title_tag.a:
                full_name = title_tag.a.text.strip().replace('\n', '').replace(' ', '')
                # Format: "owner/repo-name"
                repo_name_parts = full_name.split('/')
                if len(repo_name_parts) >= 2:
                    owner = repo_name_parts[0]
                    repo_name = repo_name_parts[1]
                    name = f"{owner.strip()}/{repo_name.strip()}"
                else:
                    name = full_name.strip() # Fallback if format isn't as expected
            else:
                continue # Skip if name is not found

            # Extract description
            description_tag = article.find("p", class_="col-9")
            description = description_tag.text.strip() if description_tag else None

            # Extract language
            language_tag = article.find("span", itemprop="programmingLanguage")
            language = language_tag.text.strip() if language_tag else None

            # Extract stars and forks
            # Look for <a> tags with specific href patterns
            star_link = article.find("a", href=f"/{name}/stargazers")
            fork_link = article.find("a", href=f"/{name}/forks")
            stars = int(star_link.text.strip().replace(',', '')) if star_link else 0
            forks = int(fork_link.text.strip().replace(',', '')) if fork_link else 0

            # Extract "Built by" contributors (optional)
            built_by_avatars = []
            built_by_container = article.find("span", class_="d-inline-block mr-3")
            if built_by_container:
                for img_tag in built_by_container.find_all("img", class_="avatar-user"):
                    alt_text = img_tag.get('alt')
                    if alt_text and alt_text.startswith('@'):
                        built_by_avatars.append(alt_text[1:]) # Remove '@' prefix

            today_stars = 0
            today_stars_tag = article.find("span", class_="d-inline-block float-sm-right")
            if today_stars_tag:
                today_stars_text = today_stars_tag.text.strip().split()[0]  # Get the first part of the text
                if 'k' in today_stars_text:
                    today_stars = int(float(today_stars_text.replace('k', '')) * 1000)
                else:
                    today_stars = int(today_stars_text.replace(',', ''))

            repo_data = TrendingRepository(
                name=name,
                description=description,
                language=language,
                stars=stars,
                forks=forks,
                today_stars=today_stars,
                built_by=built_by_avatars,
            )
            repositories_data.append(repo_data)

        except Exception as e:
            logging.exception(f"Error parsing repository: {e} in article: {article.prettify()}")
            # Continue to next repository even if one fails to parse
            continue
    return repositories_data


if __name__ == "__main__":
    # Run the CLI command if this script is executed directly
    cli()
