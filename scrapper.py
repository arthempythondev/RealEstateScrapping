from bs4 import BeautifulSoup


async def fetch(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


async def get_details(session, url):
    retries = 3
    for _ in range(retries):
        html_detail = await fetch(session, url)
        if html_detail:
            detail_soup = BeautifulSoup(html_detail, 'html.parser')
            details = detail_soup.find_all('div', class_='keyDetails-row')
            options = [detail.find('div', class_='keyDetails-value').get_text(strip=True) for detail in details]
            return options
    return None


async def get_properties(session, postcode):
    url = f"https://www.redfin.com/zipcode/{postcode}"
    html = await fetch(session, url)
    soup = BeautifulSoup(html, 'html.parser')

    data = []
    pages = soup.find('div', class_='PageNumbers flex align-center').find_all('span', class_='ButtonLabel')[-1].get_text(strip=True)
    for page in range(1, int(pages) + 1):
        url = f"https://www.redfin.com/zipcode/{postcode}/page-{page}"
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        properties = soup.find_all('div', class_='HomeCardContainer flex justify-center')
        for prop in properties:
            try:
                address = prop.find('div', class_='bp-Homecard__Address flex align-center color-text-primary font-body-xsmall-compact').get_text(strip=True)
                price = prop.find('span', class_='bp-Homecard__Price--value').get_text(strip=True)
                beds = prop.find('div', class_='bp-Homecard__Stats flex flex-grow align-center color-text-primary font-body-small').find_all('span')[0].get_text(strip=True)
                baths = prop.find('div', class_='bp-Homecard__Stats flex flex-grow align-center color-text-primary font-body-small').find_all('span')[1].get_text(strip=True)
                sqft = prop.find('div', class_='bp-Homecard__Stats flex flex-grow align-center color-text-primary font-body-small').find_all('span')[2].get_text(strip=True)
                property_url = "https://www.redfin.com" + prop.find('a')['href']
                details = await get_details(session, property_url)
                data.append({
                    'Address': address,
                    'Price': price,
                    'Beds': beds,
                    'Baths': baths,
                    'Sqft': sqft,
                    'Property URL': property_url,
                    'Details': details,
                })
            except AttributeError as e:
                print(f"Error extracting property data: {e}")
                continue

    return data
