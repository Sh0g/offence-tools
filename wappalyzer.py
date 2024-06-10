import warnings
from urllib.parse import urlparse
from subprocess import call
import requests
import validators
from Wappalyzer import Wappalyzer, WebPage

requests.packages.urllib3.disable_warnings()
warnings.filterwarnings("ignore")


def detect_tech(url: str) -> (dict, bool):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/110.0.0.0 Safari/537.36'
    }
    category = dict()
    resp = requests.get(url=url, headers=headers, timeout=5, allow_redirects=True, verify=False)
    if 200 <= resp.status_code <= 299:
        wappalyzer = Wappalyzer.latest()
        webpage = WebPage.new_from_response(resp)
        techs = wappalyzer.analyze_with_versions_and_categories(webpage)
        if techs:
            for tech in techs:
                if techs[tech].get('categories')[0]:
                    if not techs[tech].get('categories')[0] in category:
                        category[techs[tech].get('categories')[0]] = dict()
                    try:
                        category[techs[tech].get('categories')[0]].update({tech: techs[tech].get('versions')[0]})
                    except IndexError:
                        category[techs[tech].get('categories')[0]].update({tech: ""})
            return category if category else False
        return False
    return False


def main():
    url = input("Enter the target URL: ")
    url = f"http://{url}"
    if validators.url(url):
        if category := detect_tech(url):
            ln = len(f"Technology are using on the site: {urlparse(url).hostname}")
            print(f"\nTechnology are using on the site: {urlparse(url).hostname}\n{'-' * ln}")
            for cat in category:
                print(f'{cat}:')
                for item in category[cat]:
                    print(f'   - {item} {category[cat][item]}'.strip())
                print("")
        else:
            print("Couldn't find technology from this site")


if __name__ == "__main__":
    main()
    call(["python", "run.py"])