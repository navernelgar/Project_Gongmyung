import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import sys
import os
import re

def fetch_and_convert(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements (scripts, styles, navs, footers)
        for script in soup(["script", "style", "nav", "footer", "iframe", "noscript"]):
            script.decompose()

        # Get Title
        title = soup.title.string if soup.title else "Untitled"
        title = clean_filename(title)

        # Convert to Markdown
        # heading_style="ATX" makes headers like # Header instead of underlined
        markdown_content = md(str(soup), heading_style="ATX")
        
        # Clean up excessive newlines
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        
        # Add Metadata
        final_content = f"""---
url: {url}
date: {os.path.dirname(__file__)}
type: scraped
---

# {title}

{markdown_content}
"""
        return title, final_content

    except Exception as e:
        return None, str(e)

def clean_filename(filename):
    # Remove invalid characters for Windows filenames
    return re.sub(r'[\\/*?:"<>|]', "", filename).strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <url>")
        sys.exit(1)
        
    url = sys.argv[1]
    print(f"Fetching {url}...")
    title, content = fetch_and_convert(url)
    
    if title:
        print(f"Successfully converted: {title}")
        # For testing, just print the first 500 chars
        print(content[:500])
    else:
        print(f"Error: {content}")
