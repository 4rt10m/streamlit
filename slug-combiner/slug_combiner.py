import streamlit as st
from itertools import permutations

st.title("Slug Combinations Generator")

# Input fields for Slug 1 and Slug 2
slug1 = st.text_input("Slug 1", "")
slug2 = st.text_input("Slug 2", "")

# Function to generate combinations
def generate_combinations(slug1, slug2):
    slugs = [slug1, slug2]
    combinations = ['/'.join(perm) for perm in permutations(slugs)]
    return combinations

# Generate combinations and display
if st.button("Generate Combinations"):
    if slug1 and slug2:
        combinations = generate_combinations(slug1, slug2)
        st.write("Combinations:")
        for combo in combinations:
            st.write(combo)
    else:
        st.warning("Please enter both Slug 1 and Slug 2")

st.write("Note: The order of slugs doesn't matter, so x/y and y/x are equivalent.")
