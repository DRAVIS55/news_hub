import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ====================== Helper Function ====================== #
def get_best_heading_body_image(article_url):
    """
    Fetch the best heading, body, and image from an article:
    - Picks heading with the longest text in any div
    - Picks first <p> inside the same div for body
    - Picks first <img> inside the div for image
    """
    try:
        page = requests.get(article_url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch article {article_url}: {e}")
        return None, None, None

    soup = BeautifulSoup(page.text, "html.parser")
    best_heading = ""
    best_body = ""
    best_img = None

    for div in soup.find_all("div"):
        headings = div.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        body_tag = div.find("p")
        img_tag = div.find("img")

        # Pick the longest heading text in this div
        heading_text = max((h.get_text(strip=True) for h in headings), key=len, default="")
        body_text = body_tag.get_text(strip=True) if body_tag else ""

        img_url = None
        if img_tag:
            src = img_tag.get("src") or img_tag.get("data-src")
            if src:
                img_url = urljoin(article_url, src)

        # Choose this div if it has a better heading and body
        if len(heading_text) > len(best_heading) and body_text:
            best_heading = heading_text
            best_body = body_text
            best_img = img_url

    return best_heading, best_body, best_img

# ====================== Generic Local Scraper ====================== #
def scrape_local_site_with_images(base_url):
    """
    Scrape a local news site and return:
    - all_headings: list of headings
    - message_map: dict mapping heading -> {"body": ..., "image": ...}
    """
    all_headings = []
    message_map = {}

    try:
        page = requests.get(base_url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch {base_url}: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    links = soup.find_all("a", href=True)

    for link in links:
        href = link['href']
        if not href.startswith("http"):
            continue

        heading, body, image = get_best_heading_body_image(href)
        if heading and heading not in message_map:
            all_headings.append(heading)
            message_map[heading] = {"body": body, "image": image}

    return all_headings, message_map

# ====================== Individual Local Sites ====================== #
def scrape_nation():
    return scrape_local_site_with_images("https://nation.africa/kenya")

def scrape_star():
    return scrape_local_site_with_images("https://www.the-star.co.ke/")

def scrape_standard():
    return scrape_local_site_with_images("https://www.standardmedia.co.ke/")

def scrape_capitalfm():
    return scrape_local_site_with_images("https://www.capitalfm.co.ke/news/")

def scrape_kbc():
    return scrape_local_site_with_images("https://www.kbc.co.ke/category/news/")

def scrape_pd():
    return scrape_local_site_with_images("https://www.pd.co.ke/news/")

def scrape_businessdaily():
    return scrape_local_site_with_images("https://www.businessdailyafrica.com/bd/corporate/companies")

def scrape_eastafrican():
    return scrape_local_site_with_images("https://www.theeastafrican.co.ke/tea/news")

def scrape_citizen():
    return scrape_local_site_with_images("https://www.thecitizen.co.tz/tanzania/news")

def scrape_ippmedia():
    return scrape_local_site_with_images("https://www.ippmedia.com/en/news")

def scrape_ghanaweb():
    return scrape_local_site_with_images("https://www.ghanaweb.com/GhanaHomePage/NewsArchive")

def scrape_vanguard():
    return scrape_local_site_with_images("https://www.vanguardngr.com/category/news/")

def scrape_premiumtimes():
    return scrape_local_site_with_images("https://www.premiumtimesng.com/news")

def scrape_thisday():
    return scrape_local_site_with_images("https://www.thisdaylive.com/index.php/2024/06/19")
