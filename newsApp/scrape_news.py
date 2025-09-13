import os
import requests
import base64
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from .models import News
"--------------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----"
# -------------------- AI Image Generation --------------------
def AI_image_generation(news_obj):
    """
    Generates an AI image for a news article using Hugging Face API
    and saves it to the News object if it doesn't already have a file.
    """
    
    HF_API_URL = "https://api-inference.huggingface.co/models/gsdf/Counterfeit-V2.5"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    heading_text = news_obj.heading
    body_text = news_obj.description or ""

    try:
        prompt = f"Realistic high-quality news photo for article: {heading_text}. {body_text[:200]}"
        response = requests.post(
            HF_API_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "generated_image" in data[0]:
                image_base64 = data[0]["generated_image"]
            elif isinstance(data, dict) and "image" in data:
                image_base64 = data["image"]
            else:
                print(f"⚠️ No image returned for: {heading_text}")
                return

            image_bytes = base64.b64decode(image_base64)
            filename = f"{heading_text[:50].replace(' ', '_')}.png"
            news_obj.file.save(filename, ContentFile(image_bytes), save=True)
        else:
            print(f"❌ Hugging Face API failed for {heading_text}: {response.text}")

    except Exception as e:
        print(f"💥 AI image generation failed for {heading_text}: {e}")


# -------------------- Individual Scrapers --------------------
#======================world News=========================#
# ------------------- BBC -------------------
def scrape_bbc():
    url = "https://www.bbc.com/news"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch BBC: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    news_passed = soup.find_all("body")  # BBC structure: headings inside h2, summaries inside p

    for item in news_passed:
        heading_tags = item.find_all("h2")
        body_tags = item.find_all("p")  # returns a list

        for head in heading_tags:
            heading_text = head.get_text(strip=True)

            # Take the first paragraph as body, if exists
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""

            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map



# ------------------- The Guardian -------------------
def scrape_guardian():
    url = "https://www.theguardian.com/world"
    all_headings = []
    message_map = {}

    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch The Guardian: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all("h1")
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- New York Times -------------------
def scrape_nytimes():
    url = "https://www.nytimes.com/section/world"
    all_headings = []
    message_map = {}

    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch NY Times: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all("h1")
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- Washington Post -------------------
def scrape_washingtonpost():
    url = "https://www.washingtonpost.com/world/"
    all_headings = []
    message_map = {}

    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch Washington Post: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all("h1")
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- France24 -------------------
def scrape_france24():
    url = "https://www.france24.com/en/tag/world/"
    all_headings = []
    message_map = {}

    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch France24: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all("h1")
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map
import requests
from bs4 import BeautifulSoup

# ------------------- DW -------------------
def scrape_dw():
    url = "https://www.dw.com/en/top-stories/s-9097"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch DW: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1","h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- AP News -------------------
def scrape_apnews():
    url = "https://www.apnews.com/hub/world-news"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch AP News: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1","h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- Euronews -------------------
def scrape_euronews():
    url = "https://www.euronews.com/news"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch Euronews: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1","h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- CBS News -------------------
def scrape_cbsnews():
    url = "https://www.cbsnews.com/world/"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch CBS News: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1","h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- NBC News -------------------
def scrape_nbcnews():
    url = "https://www.nbcnews.com/news/world"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch NBC News: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1","h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- Fox News -------------------
def scrape_foxnews():
    url = "https://www.foxnews.com/world"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch Fox News: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1","h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- USA Today -------------------
def scrape_usatoday():
    url = "https://www.usatoday.com/news/world/"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch USA Today: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1","h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- Wall Street Journal -------------------
def scrape_wsj():
    url = "https://www.wsj.com/news/world"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch WSJ: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1","h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- Bloomberg -------------------
def scrape_bloomberg():
    url = "https://www.bloomberg.com/world"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch Bloomberg: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1","h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- Al Jazeera -------------------
def scrape_aljazeera():
    url = "https://www.aljazeera.com/africa/"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch Al Jazeera: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1","h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- BBC Pidgin -------------------
def scrape_bbc_pidgin():
    url = "https://www.bbc.com/pidgin/tori"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch BBC Pidgin: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1","h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map

#======================Local News=========================#

# ------------------- The East African -------------------
def scrape_eastafrican():
    url = "https://www.theeastafrican.co.ke/tea/news"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch The East African: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1", "h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- The Citizen (Tanzania) -------------------
def scrape_citizen():
    url = "https://www.thecitizen.co.tz/tanzania/news"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch The Citizen: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1", "h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- IPP Media (Tanzania) -------------------
def scrape_ippmedia():
    url = "https://www.ippmedia.com/en/news"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch IPP Media: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1", "h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- GhanaWeb -------------------
def scrape_ghanaweb():
    url = "https://www.ghanaweb.com/GhanaHomePage/NewsArchive"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch GhanaWeb: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1", "h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- Vanguard (Nigeria) -------------------
def scrape_vanguard():
    url = "https://www.vanguardngr.com/category/news/"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch Vanguard: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1", "h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- Premium Times (Nigeria) -------------------
def scrape_premiumtimes():
    url = "https://www.premiumtimesng.com/news"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch Premium Times: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1", "h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- This Day (Nigeria) -------------------
def scrape_thisday():
    url = "https://www.thisdaylive.com/index.php/2024/06/19"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch This Day: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue
        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all(["h1", "h2"])
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map
# ------------------- Capital FM (Kenya) -------------------
def scrape_capitalfm():
    url = "https://www.capitalfm.co.ke/news/"
    all_headings = []
    message_map = {}

    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch Capital FM: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue

        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all("h1")
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- KBC -------------------
def scrape_kbc():
    url = "https://www.kbc.co.ke/category/news/"
    all_headings = []
    message_map = {}

    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch KBC: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue

        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all("h1")
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- People Daily -------------------
def scrape_pd():
    url = "https://www.pd.co.ke/news/"
    all_headings = []
    message_map = {}

    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch People Daily: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue

        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all("h1")
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


# ------------------- Business Daily Africa -------------------
def scrape_businessdaily():
    url = "https://www.businessdailyafrica.com/bd/corporate/companies"
    all_headings = []
    message_map = {}

    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch Business Daily: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link['href']
        if not href.startswith("http"):
            continue

        try:
            article_page = requests.get(href, timeout=15)
            article_page.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch article {href}: {e}")
            continue

        article_soup = BeautifulSoup(article_page.text, "html.parser")
        headings = article_soup.find_all("h1")
        body_tags = article_soup.find_all("p")

        for head in headings:
            heading_text = head.get_text(strip=True)
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""
            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map


def scrape_nation():
    url = "https://nation.africa/kenya"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch Nation: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    new_passed = soup.find_all("body") 
    for item in new_passed:
        news_passed = item.find_all("div")  # headings inside h2, summaries inside p
        for item in news_passed:
            heading_tags = item.find_all("h3")  # Nation uses h3 for headlines
            body_tags = item.find_all("p")  # returns a list of paragraphs

            for head in heading_tags:
                heading_text = head.get_text(strip=True)

                # Take the first paragraph as body if exists
                body_text = body_tags[0].get_text(strip=True) if body_tags else ""

                all_headings.append(heading_text)
                message_map[heading_text] = body_text

    return all_headings, message_map

def scrape_star():
    url = "https://www.the-star.co.ke/"
    all_headings = []
    message_map = {}
    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch Nation: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    new_passed = soup.find_all("body") 
    for item in new_passed:
        news_passed = item.find_all("div")  # headings inside h2, summaries inside p
        for item in news_passed:
            heading_tags = item.find_all("h6")  # Nation uses h3 for headlines
            body_tags = item.find_all("p")  # returns a list of paragraphs

            for head in heading_tags:
                heading_text = head.get_text(strip=True)

                # Take the first paragraph as body if exists
                body_text = body_tags[0].get_text(strip=True) if body_tags else ""

                all_headings.append(heading_text)
                message_map[heading_text] = body_text

    return all_headings, message_map

def scrape_standard():
    url = "https://www.standardmedia.co.ke/"
    all_headings = []
    message_map = {}

    try:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch Standard Media: {e}")
        return [], {}

    soup = BeautifulSoup(page.text, "html.parser")
    new_passed = soup.find_all("body") 

    for item in new_passed:
        news_links = item.find_all("a", href=True)  # only links with href
        for link in news_links:
            href = link['href']
            
            # Skip non-http links
            if not href.startswith("http"):
                continue

            try:
                page_req = requests.get(href, timeout=15)
                page_req.raise_for_status()
            except Exception as e:
                print(f"❌ Failed to fetch article {href}: {e}")
                continue

            soup_article = BeautifulSoup(page_req.text, "html.parser")
            headings = soup_article.find_all("h1")  # headings inside h1
            body_tags = soup_article.find_all("p")  # all paragraphs

            for head in headings:
                heading_text = head.get_text(strip=True)
                body_text = body_tags[0].get_text(strip=True) if body_tags else ""
                all_headings.append(heading_text)
                message_map[heading_text] = body_text

    return all_headings, message_map



# -------------------- Main Scrape Method --------------------
def scrape_method(generate_images=False):
    """
    Main scraping function that calls individual site scrapers,
    updates the database, and optionally generates AI images.
    """
    # Clear old news
    News.objects.all().delete()

    all_headings = []
    message_map = {}

    # List of scraper functions with their news_type
    scraper_functions = [
    # World news scrapers
    (scrape_bbc, "world"),
    (scrape_nation, "local"),
    (scrape_star, "local"),
    #untested
    (scrape_guardian, "world"),
    (scrape_nytimes, "world"),
    (scrape_washingtonpost, "world"),
    (scrape_france24, "world"),
    (scrape_bbc_pidgin, "world"),
    (scrape_dw, "world"),
    (scrape_apnews, "world"),
    (scrape_euronews, "world"),
    (scrape_cbsnews, "world"),
    (scrape_nbcnews, "world"),
    (scrape_foxnews, "world"),
    (scrape_usatoday, "world"),
    (scrape_wsj, "world"),
    (scrape_bloomberg, "world"),
    (scrape_aljazeera, "world"),

    # Local news scrapers

    (scrape_standard, "local"),
    (scrape_capitalfm, "local"),
    (scrape_kbc, "local"),
    (scrape_pd, "local"),
    (scrape_businessdaily, "local"),
    (scrape_eastafrican, "local"),
    (scrape_citizen, "local"),
    (scrape_ippmedia, "local"),
    (scrape_ghanaweb, "local"),
    (scrape_vanguard, "local"),
    (scrape_premiumtimes, "local"),
    (scrape_thisday, "local"),
]


    for scraper, news_type in scraper_functions:
        headings, bodies = scraper()  # each scraper returns (all_headings, message_map)

        for heading_text in headings:
            body_text = bodies.get(heading_text, "")

            # --- Database logic ---
            news_obj, created = News.objects.get_or_create(
                heading=heading_text,
                defaults={
                    "description": body_text,
                    "author": "news_hub_author",
                    "news_type": news_type,
                }
            )

            # Update if changed
            if body_text and (news_obj.description != body_text or news_obj.news_type != news_type):
                news_obj.description = body_text
                news_obj.news_type = news_type
                news_obj.save()

            # AI image generation
            if generate_images and not news_obj.file:
                AI_image_generation(news_obj)

            # Keep track for return
            if heading_text not in message_map:
                all_headings.append(heading_text)
                message_map[heading_text] = body_text
            else:
                if not message_map[heading_text] and body_text:
                    message_map[heading_text] = body_text

    return all_headings, message_map
