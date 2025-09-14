import requests
import base64
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile


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
        news_passer = item.find_all("div")
        for item in news_passer:
            heading_tags = item.find_all("h2")
            body_tags = item.find_all("p")
            image_tags = item.find_all("img")

            # Loop through all headings and bodies
            for i, (head, body) in enumerate(zip(heading_tags, body_tags)):
                heading_text = head.get_text(strip=True)
                body_text = body.get_text(strip=True)

                # Match image by index if available, else None
                image_url = image_tags[i]['src'] if i < len(image_tags) else None

                all_headings.append(heading_text)
                message_map[heading_text] = {"body": body_text, "image": image_url}

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
    
    # Loop through all links and extract the heading
    for link in soup.find_all("a", attrs={"aria-label": True}):
        heading_text = link["aria-label"].strip()
        all_headings.append(heading_text)
        message_map[heading_text] = ""  # leave body blank

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

    # Loop through all <a> tags with href
    for link in soup.find_all("a", href=True):
        heading_text = link.get_text(strip=True)
        if not heading_text:
            continue

        # Body from <p> inside <a> (if exists)
        body_tag = link.find("p")
        body_text = body_tag.get_text(strip=True) if body_tag else ""

        # Image from <img> inside <a> (if exists)
        img_tag = link.find("img")
        image_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

        all_headings.append(heading_text)
        message_map[heading_text] = {"body": body_text, "image": image_url}

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

    # Loop through all divs
    for passer in soup.find_all("div"):
        heading_tags = passer.find_all("h3")
        body_tags = passer.find_all("p")
        img_tags = passer.find_all("img")

        # Loop through all headings in this div
        for i, head in enumerate(heading_tags):
            heading_text = head.get_text(strip=True)
            body_text = body_tags[i].get_text(strip=True) if i < len(body_tags) else ""
            image_url = img_tags[i]['src'] if i < len(img_tags) and 'src' in img_tags[i].attrs else None

            all_headings.append(heading_text)
            message_map[heading_text] = {"body": body_text, "image": image_url}

    return all_headings, message_map


# ------------------- France24 -------------------
# def scrape_france24():
#     url = "https://www.france24.com/en/tag/world/"
#     all_headings = []
#     message_map = {}
#
#     try:
#         page = requests.get(url, timeout=15)
#         page.raise_for_status()
#     except Exception as e:
#         print(f"❌ Failed to fetch France24: {e}")
#         return [], {}
#
#     soup = BeautifulSoup(page.text, "html.parser")
#     for link in soup.find_all("a", href=True):
#         
#         article_soup = BeautifulSoup(article_page.text, "html.parser")
#         headings = article_soup.find_all("h1")
#         body_tags = article_soup.find_all("p")
#
#         for head in headings:
#             heading_text = head.get_text(strip=True)
#             body_text = body_tags[0].get_text(strip=True) if body_tags else ""
#             all_headings.append(heading_text)
#             message_map[heading_text] = body_text
#
#     return all_headings, message_map

# ------------------- DW -------------------
# def scrape_dw():
#     url = "https://www.dw.com/en/top-stories/s-9097"
#     all_headings = []
#     message_map = {}
#
#     try:
#         page = requests.get(url, timeout=15)
#         page.raise_for_status()
#     except Exception as e:
#         print(f"❌ Failed to fetch DW: {e}")
#         return [], {}
#
#     soup = BeautifulSoup(page.text, "html.parser")
#
#     # Loop through all <a> tags
#     for link in soup.find_all("a", href=True):
#         heading_text = link.get_text(strip=True)
#         if not heading_text:
#             continue
#
#         # Try to find an image inside the same <a> tag
#         img_tag = link.find("img")
#         image_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None
#
#         # Optionally get first <p> in parent div as body
#         parent_div = link.find_parent("div")
#         body_text = ""
#         if parent_div:
#             p_tag = parent_div.find("p")
#             if p_tag:
#                 body_text = p_tag.get_text(strip=True)
#
#         all_headings.append(heading_text)
#         message_map[heading_text] = {"body": body_text, "image": image_url}
#
#     return all_headings, message_map

# ------------------- AP News -------------------
# def scrape_apnews():
#     url = "https://www.apnews.com/hub/world-news"
#     all_headings = []
#     message_map = {}
#     try:
#         page = requests.get(url, timeout=15)
#         page.raise_for_status()
#     except Exception as e:
#         print(f"❌ Failed to fetch AP News: {e}")
#         return [], {}
#
#     soup = BeautifulSoup(page.text, "html.parser")
#     for link in soup.find_all("a", href=True):
#         href = link['href']
#         if not href.startswith("http"):
#             continue
#         try:
#             article_page = requests.get(href, timeout=15)
#             article_page.raise_for_status()
#         except Exception as e:
#             print(f"❌ Failed to fetch article {href}: {e}")
#             continue
#
#         article_soup = BeautifulSoup(article_page.text, "html.parser")
#         headings = article_soup.find_all(["h1","h2"])
#         body_tags = article_soup.find_all("p")
#
#         for head in headings:
#             heading_text = head.get_text(strip=True)
#             body_text = body_tags[0].get_text(strip=True) if body_tags else ""
#             all_headings.append(heading_text)
#             message_map[heading_text] = body_text
#
#     return all_headings, message_map

# ------------------- Euronews -------------------
# def scrape_euronews():
#     url = "https://www.euronews.com/news"
#     all_headings = []
#     message_map = {}
#     try:
#         page = requests.get(url, timeout=15)
#         page.raise_for_status()
#     except Exception as e:
#         print(f"❌ Failed to fetch Euronews: {e}")
#         return [], {}
#
#     soup = BeautifulSoup(page.text, "html.parser")
#     for link in soup.find_all("a", href=True):
#         href = link['href']
#         if not href.startswith("http"):
#             continue
#         try:
#             article_page = requests.get(href, timeout=15)
#             article_page.raise_for_status()
#         except Exception as e:
#             print(f"❌ Failed to fetch article {href}: {e}")
#             continue
#
#         article_soup = BeautifulSoup(article_page.text, "html.parser")
#         headings = article_soup.find_all(["h1","h2"])
#         body_tags = article_soup.find_all("p")
#
#         for head in headings:
#             heading_text = head.get_text(strip=True)
#             body_text = body_tags[0].get_text(strip=True) if body_tags else ""
#             all_headings.append(heading_text)
#             message_map[heading_text] = body_text
#
#     return all_headings, message_map

# ------------------- CBS News -------------------
# def scrape_cbsnews():
#     url = "https://www.cbsnews.com/world/"
#     all_headings = []
#     message_map = {}
#
#     try:
#         page = requests.get(url, timeout=15)
#         page.raise_for_status()
#     except Exception as e:
#         print(f"❌ Failed to fetch CBS News: {e}")
#         return [], {}
#
#     soup = BeautifulSoup(page.text, "html.parser")
#
#     # Loop through all divs to find h4 and images
#     for div in soup.find_all("div"):
#         heading_tag = div.find("h4")
#         if not heading_tag:
#             continue
#         heading_text = heading_tag.get_text(strip=True)
#         if not heading_text:
#             continue
#
#         # Get first image in the same div
#         img_tag = div.find("img")
#         image_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None
#
#         all_headings.append(heading_text)
#         message_map[heading_text] = {"image": image_url}
#
#     return all_headings, message_map

# ------------------- NBC News -------------------
# def scrape_nbcnews():
#     url = "https://www.nbcnews.com/news/world"
#     all_headings = []
#     message_map = {}
#
#     try:
#         page = requests.get(url, timeout=15)
#         page.raise_for_status()
#     except Exception as e:
#         print(f"❌ Failed to fetch NBC News: {e}")
#         return [], {}
#
#     soup = BeautifulSoup(page.text, "html.parser")
#
#     # Loop through all divs to find a and img
#     for div in soup.find_all("div"):
#         a_tag = div.find("a", href=True)
#         if not a_tag:
#             continue
#         heading_text = a_tag.get_text(strip=True)
#         if not heading_text:
#             continue
#
#         # Get first image in the same div
#         img_tag = div.find("img")
#         image_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None
#
#         all_headings.append(heading_text)
#         message_map[heading_text] = {"image": image_url}
#
#     return all_headings, message_map

# ------------------- Fox News -------------------
# def scrape_foxnews():
#     url = "https://www.foxnews.com/world"
#     all_headings = []
#     message_map = {}
#     try:
#         page = requests.get(url, timeout=15)
#         page.raise_for_status()
#     except Exception as e:
#         print(f"❌ Failed to fetch Fox News: {e}")
#         return [], {}
#
#     soup = BeautifulSoup(page.text, "html.parser")
#     for link in soup.find_all("a", href=True):
#         href = link['href']
#         if not href.startswith("http"):
#             continue
#         try:
#             article_page = requests.get(href, timeout=15)
#             article_page.raise_for_status()
#         except Exception as e:
#             print(f"❌ Failed to fetch article {href}: {e}")
#             continue
#
#         article_soup = BeautifulSoup(article_page.text, "html.parser")
#         headings = article_soup.find_all(["h1","h2"])
#         body_tags = article_soup.find_all("p")
#
#         for head in headings:
#             heading_text = head.get_text(strip=True)
#             body_text = body_tags[0].get_text(strip=True) if body_tags else ""
#             all_headings.append(heading_text)
#             message_map[heading_text] = body_text
#
#     return all_headings, message_map
