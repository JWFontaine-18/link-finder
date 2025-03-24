from django.shortcuts import render
from django import forms
import requests

class LinkSearchForm(forms.Form):
    url = forms.URLField(label='Enter the URL to search for', max_length=200)

def search_view(request):
    results = None
    if request.method == 'POST':
        form = LinkSearchForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            params = {
                "engine": "google",
                "q": f'"{url}"',
                "api_key": "37d30b93d7c3cd8e5ce5f7ef201505671d27b4e6d2f165fa86ae6291e8328642"
            }

            response = requests.get("https://serpapi.com/search", params=params)

            if response.status_code == 200:
                serp_data = response.json()
                results = []
                for result in serp_data.get("organic_results", []):
                    results.append({
                        "title": result.get("title"),
                        "link": result.get("link")
                    })
            else:
                results = [{"title": "Error retrieving data from SerpAPI.", "link": "#"}]
    else:
        form = LinkSearchForm()
    return render(request, 'searchapp/search.html', {'form': form, 'results': results})