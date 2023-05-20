import pprint
from serpapi import GoogleSearch


# Get articles from gloogle scholars
def get_articles(query: str, limit: int, key:str):
    print("Getting Articles...")
    # Serpa API params
    params = {
        "api_key": key,
        "engine": "google_scholar",
        "q": query,
        "hl": "en",
        "num": limit
    }

    # Run the API
    search = GoogleSearch(params)
    results = search.get_dict()

    result_list = []
    authors_names_list = []

    organic_results = results["organic_results"]

    # Filter the data and only keep the needed documents
    for result in organic_results:
        title = result.get("title", [])
        link = result.get("link", [])
        summary = result.get("publication_info", []).get("summary", [])
        authors = result.get("publication_info", []).get("authors", [])

        if authors != []:
            for authors_info in authors:
                authors_name = authors_info.get('name', [])
                authors_names_list.append(authors_name)

        result_list.append({
            'authorsNamesList': authors_names_list,
            'link': link,
            'summary': summary,
            'title': title,
        })

    pprint.pprint(result_list)
    return result_list
