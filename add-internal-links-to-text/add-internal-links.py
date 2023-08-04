import streamlit as st

def add_internal_links(text, urls_anchors):
    linked_text = text

    for url, anchor in urls_anchors:
        # Find the anchor text and replace it with the HTML link
        anchor_regex = rf'\b{anchor}\b'
        linked_text = linked_text.replace(anchor, f'<a href="{url}">{anchor}</a>')

    return linked_text

def main():
    st.title("Internal Link Generator")

    st.subheader("Add Links:")
    urls_anchors = []
    i = 1
    while True:
        url = st.text_input(f"URL {i}:")
        anchor = st.text_input(f"Anchor Text {i}:")
        if not url or not anchor:
            break
        urls_anchors.append([url, anchor])
        i += 1

    input_text = st.text_area("Input Text", value="", height=200)
    
    if st.button("Generate Output"):
        result = add_internal_links(input_text, urls_anchors)
        st.subheader("Result:")
        st.markdown(result, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
