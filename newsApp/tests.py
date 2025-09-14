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
        image_tag=item.find_all("img")
        for image_tg in image_tag:
            print(image_tag)
        

        for head in heading_tags:
            heading_text = head.get_text(strip=True)

            # Take the first paragraph as body, if exists
            body_text = body_tags[0].get_text(strip=True) if body_tags else ""

            all_headings.append(heading_text)
            message_map[heading_text] = body_text

    return all_headings, message_map
