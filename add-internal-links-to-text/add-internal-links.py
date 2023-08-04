import streamlit as st

def add_internal_links(text, urls_anchors):
    linked_text = text

    for url, anchor in urls_anchors:
        # Find the anchor text and replace it with the Markdown link
        anchor_regex = rf'\b{anchor}\b'
        linked_text = linked_text.replace(anchor, f'[{anchor}]({url})')

    return linked_text

def main():
    st.title("Internal Link Generator")

    input_text = """
    This is a sample text with multiple anchors: anchor1, anchor2, and anchor3.

    This is a sample text with multiple anchors: anchor1, anchor2, and anchor3.

    This is a sample text with multiple anchors: anchor1, anchor12, and anchor3.
    """

    input_urls_anchors = [
        ["https://example.com1", "anchor1"],
        ["https://example.com2", "anchor2"],
        ["https://example.com3", "anchor3"],
        ["https://example.com31", "anchor12"]
    ]

    result = add_internal_links(input_text, input_urls_anchors)

    st.subheader("Input Text:")
    st.text_area("Input Text", value=input_text, height=200)

    st.subheader("Links:")
    for url, anchor in input_urls_anchors:
        st.markdown(f"Link: [{anchor}]({url})")

    st.subheader("Result:")
    st.text_area("Result", value=result, height=200)

if __name__ == "__main__":
    main()