import requests
from bs4 import BeautifulSoup
import json
import csv
import streamlit as st
import pandas as pd
import io

def scrape_sidebar_urls(urls):
    sidebar_urls = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for successful response

            soup = BeautifulSoup(response.content, 'html.parser')
            script_tag = soup.find('script', id='__NEXT_DATA__')

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
                st.warning(f"No script tag with id '__NEXT_DATA__' found in {url}")
        except requests.exceptions.RequestException as e:
            st.warning(f"Failed to fetch {url}. Error: {e}")

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
                st.table(pd.DataFrame(sidebar_urls))
                # Export to CSV and provide download link
                csv_file = pd.DataFrame(sidebar_urls).to_csv(index=False)
                st.download_button(label="Download CSV", data=io.StringIO(csv_file), file_name='enyoMZ_sidebar_urls-all-pages.csv', mime='text/csv')
                st.success("Data exported to CSV successfully.")
            else:
                st.warning('No data found. Make sure the URLs are correct and the sidebar exists.')
        else:
            st.warning('Please enter at least one URL.')

if __name__ == '__main__':
    main()
