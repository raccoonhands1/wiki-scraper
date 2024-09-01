import requests
from bs4 import BeautifulSoup

# Main Wikipedia page URL that contains the list of URLs
main_url = 'https://en.wikipedia.org/wiki/List_of_research_universities_in_the_United_States'

class articleData:
    url: str
    students: int

numArticles = 0

def extract_urls_from_main_page(url):
    try:
        # Send a GET request to the main URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all the URLs within the list (assumed to be in <a> tags)
        links = soup.find_all('a', href=True)
        
        # Filter and return full Wikipedia URLs
        urls = ['https://en.wikipedia.org' + link['href'] for link in links if link['href'].startswith('/wiki/')]

        return urls

    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return []

def scrape_students_section(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the "Students" section by looking for a header with that title
        students_header = soup.find(['h2', 'h3', 'h4'], string=lambda text: text and 'student' in text.lower())

        if not students_header:
            print(f"'Students' section not found in {url}")
            return None

        # Get the next sibling elements until the next header of the same level or higher
        students_content = []
        for sibling in students_header.find_next_siblings():
            if sibling.name and sibling.name.startswith('h'):
                break
            students_content.append(sibling.get_text(strip=True))

        # Combine the content into a single string
        return '\n'.join(students_content).strip()

    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None

# Extract URLs from the main Wikipedia page
embedded_urls = extract_urls_from_main_page(main_url)

# Scrape the "Students" section from each extracted URL
for url in embedded_urls:
    students_section = scrape_students_section(url)
    if students_section:
        print(f"Students section from {url}:\n{students_section}\n")
        numArticles+=1

print("{numArticles} found containing student data" )