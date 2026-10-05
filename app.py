import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests
from sklearn.metrics.pairwise import cosine_similarity

url = "https://huggingface.co/datasets/sanjivani777/book.pkl/resolve/main/books.pkl"

response = requests.get(url)

with open("books.pkl", "wb") as f:
    f.write(response.content)

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Book Recommendation System",
    page_icon="📚",
    layout="wide"
)

# ----------------------------
# Custom CSS Styling
# ----------------------------
st.markdown("""
<style>
.main { background-color: #f9fafb; }
h1 { text-align: center; }
.book-title { font-size: 16px; font-weight: 600; }
.book-author { font-size: 14px; color: gray; }
.rating { font-size: 14px; color: #f59e0b; }
.footer { text-align: center; font-size: 14px; margin-top: 50px; color: gray; }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Age Group Function
# ----------------------------
def get_age_group(age):
    if age < 18:
        return "Teen"
    elif age < 30:
        return "Young Adult"
    elif age < 50:
        return "Adult"
    else:
        return "Senior"

# ----------------------------
# Load Data
# ----------------------------
popular_books = pickle.load(open("popular_books.pkl", "rb"))
pivot_table = pickle.load(open("pivot_table.pkl", "rb"))
books = pickle.load(open("books.pkl","rb"))

books.columns = books.columns.str.strip()

books['Age_Group'] = books['Age'].apply(
    lambda x: get_age_group(x) if pd.notnull(x) else "Unknown"
)

popularity_df = books.groupby(
    ['Book-Title', 'Book-Author', 'Image-URL-M', 'Country', 'Age_Group']
)['Book-Rating'].agg(['count', 'mean']).reset_index()

popularity_df.rename(columns={
    'count': 'rating_count',
    'mean': 'avg_rating'
}, inplace=True)

# ----------------------------
# Demographic Recommendation Function
# ----------------------------
def recommend_demographic(age, country):

    age_group = get_age_group(age)

    filtered_books = popularity_df[
        (popularity_df['Country'] == country) &
        (popularity_df['Age_Group'] == age_group)
    ]

    filtered_books = filtered_books[
        filtered_books['rating_count'] > 30
    ]

    filtered_books = filtered_books.sort_values(
        by=['avg_rating', 'rating_count'],
        ascending=False
    )

    return filtered_books.head(8)

# ----------------------------
# Sidebar Navigation
# ----------------------------
st.sidebar.title("📖 Book Recommender Navigation")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Go to",
    ["🏆 Popular Books", "🔍 Explore Similar Reads", "🎯 Personalized Picks"]
)

st.sidebar.markdown("---")

# ----------------------------
# App Title
# ----------------------------
st.title("📚 Book Recommendation System")
st.markdown("### Discover Books You’ll Love")

# ----------------------------
# Popular Books Section
# ----------------------------
if menu == "🏆 Popular Books":

    st.subheader("Top Rated Popular Books")

    cols = st.columns(4)

    for i in range(12):
        with cols[i % 4]:
            st.image(popular_books.iloc[i]['Image-URL-M'], use_container_width=True)
            st.markdown(f"**{popular_books.iloc[i]['Book-Title']}**")
            st.caption(f"by {popular_books.iloc[i]['Book-Author']}")
            st.markdown(
                f"⭐ {round(popular_books.iloc[i]['avg_rating'],2)} "
                f"({popular_books.iloc[i]['rating_count']} ratings)"
            )

# ----------------------------
# Similar Book Recommendation
# ----------------------------
elif menu == "🔍 Explore Similar Reads":

    st.subheader("🔍 Find Similar Books")

    search_term = st.text_input("Type a book name")

    if search_term:
        matching_books = [
            book for book in pivot_table.index
            if search_term.lower() in book.lower()
        ]

        if matching_books:

            selected_book = st.selectbox(
                "Select from matching books",
                matching_books
            )

            if st.button("Recommend"):

                with st.spinner("Finding similar books..."):

                    book_index = pivot_table.index.get_loc(selected_book)
                    book_vector = pivot_table.iloc[book_index].values.reshape(1, -1)
                    similarity_scores = cosine_similarity(book_vector, pivot_table)[0]

                    similar_indices = similarity_scores.argsort()[::-1][1:9]

                    st.subheader("📚 Recommended Books")

                    cols = st.columns(4)

                    for idx, i in enumerate(similar_indices):

                        book_title = pivot_table.index[i]
                        similarity_score = round(similarity_scores[i] * 100, 2)

                        book_info = books[books['Book-Title'] == book_title]

                        if not book_info.empty:
                            book_info = book_info.iloc[0]

                            with cols[idx % 4]:
                                st.image(book_info['Image-URL-M'], use_container_width=True)
                                st.markdown(f"**{book_info['Book-Title']}**")
                                st.caption(f"by {book_info['Book-Author']}")
                                st.progress(int(similarity_score))
                                st.caption(f"Similarity: {similarity_score}%")

# ----------------------------
# Personalized Recommendation
# ----------------------------
elif menu == "🎯 Personalized Picks":

    st.subheader("🎯 Personalized Recommendation")

    age_input = st.number_input(
        "Enter your age",
        min_value=5,
        max_value=100,
        value=25
    )

    country_input = st.selectbox(
        "Select your country",
        sorted(books['Country'].dropna().unique())
    )

    if st.button("Get Personalized Recommendations"):

        results = recommend_demographic(age_input, country_input)

        if not results.empty:

            cols = st.columns(4)

            for idx, row in results.iterrows():
                with cols[idx % 4]:
                    st.image(row['Image-URL-M'], use_container_width=True)
                    st.markdown(f"**{row['Book-Title']}**")
                    st.caption(f"by {row['Book-Author']}")
                    st.markdown(
                        f"⭐ {round(row['avg_rating'],2)} "
                        f"({row['rating_count']} ratings)"
                    )
        else:
            st.warning("No books found for this demographic.")