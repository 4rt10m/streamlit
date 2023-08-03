import requests
from bs4 import BeautifulSoup
import json
import csv
import streamlit as st

def scrape_sidebar_urls(urls):
    sidebar_urls = []

    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            # Get the script tag from HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            script_tag = soup.find('script', id='__NEXT_DATA__')

            # Get data from the script
            if script_tag:
                script_content = script_tag.string
                script_json = json.loads(script_content)
                page_props = script_json.get('props', {}).get('pageProps', {}).get('page', {})
                sidebar = page_props.get('sidebar', {})
                if sidebar is not None:
                    sidebar_items = page_props.get('sidebar', {}).get('items', [{}])
                    sidebar_type = page_props.get('sidebar', {}).get('name', '')

                if sidebar and sidebar_items:
                    for item in sidebar_items:
                        sidebarSectionName = item.get('name', '')
                        heading = item.get('heading', '')
                        items = item.get('items', [])
                        for sidebaraurl in items:
                            urlPathWithAncestry = sidebaraurl.get('urlPathWithAncestry', '')
                            if urlPathWithAncestry:
                                sidebar_urls.append({
                                    'URL': url,
                                    'Heading': heading,
                                    'SidebarURL': urlPathWithAncestry,
                                    'Sidebar Type': sidebar_type
                                })
                else:
                    st.warning('No sidebar found for ' + url)
            else:
                st.warning(f"No script tag with id '__NEXT_DATA__' found in {url}")
        else:
            st.warning(f"Failed to fetch {url}. Status code: {response.status_code}")

    return sidebar_urls

def main():
    st.title('Sidebar URL Scraper')
    st.write('Enter URLs to scrape sidebar data:')

    # User input for URLs
    input_urls = st.text_area('Enter URLs (one per line)', '')

    if st.button('Scrape URLs'):
        urls = [url.strip() for url in input_urls.split('\n') if url.strip()]
        if urls:
            sidebar_urls = scrape_sidebar_urls(urls)
            if sidebar_urls:
                # Display the scraped data in a table
                st.table(sidebar_urls)
                # Export to CSV
                output_file = 'enyoMZ_sidebar_urls-all-pages.csv'
                with open(output_file, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['URL', 'Heading', 'SidebarURL', 'Sidebar Type'])
                    for row in sidebar_urls:
                        writer.writerow([row['URL'], row['Heading'], row['SidebarURL'], row['Sidebar Type']])
                st.success(f"Data exported to {output_file} successfully.")
            else:
                st.warning('No data found. Make sure the URLs are correct and the sidebar exists.')
        else:
            st.warning('Please enter at least one URL.')

if __name__ == '__main__':
    main()