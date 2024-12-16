import streamlit as st
import pickle
import pandas as pd
import requests
import os

# Absolute paths for the pickle files
movies_pkl_path = r"C:\Users\yashj\OneDrive\Desktop\ML_ProjectProjects\Movie_Recommender_system\movies.pkl"
movie_dict_pkl_path = r"C:\Users\yashj\OneDrive\Desktop\ML_ProjectProjects\Movie_Recommender_system\movie_dict.pkl"
similarity_pkl_path = r"C:\Users\yashj\OneDrive\Desktop\ML_ProjectProjects\Movie_Recommender_system\similarity.pkl"

# Function to load a pickle file from a given path
def load_pickle_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    else:
        st.error(f"File not found: {file_path}")
        return None

# Fetch poster and movie page URL function
def fetch_poster_and_url(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=258625ab22d9951475f952e6e8028139&language=en-US')
    data = response.json()
    poster_url = "http://image.tmdb.org/t/p/w500/" + data['poster_path']
    movie_page_url = f"https://www.themoviedb.org/movie/{movie_id}"
    return poster_url, movie_page_url

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_urls = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        movie_title = movies.iloc[i[0]].title
        poster_url, movie_page_url = fetch_poster_and_url(movie_id)
        recommended_movies.append(movie_title)
        recommended_movies_posters.append(poster_url)
        recommended_movies_urls.append(movie_page_url)
    return recommended_movies, recommended_movies_posters, recommended_movies_urls

# Load movie data and similarity matrix using the provided paths
movies_dict = load_pickle_file(movie_dict_pkl_path)  # Load movie_dict.pkl
if movies_dict:
    movies = pd.DataFrame(movies_dict)
else:
    movies = pd.DataFrame()

similarity = load_pickle_file(similarity_pkl_path)  # Load similarity.pkl

# Streamlit UI
st.title("Movie Recommender System")

# Movie Search Section
selected_movie_name = st.selectbox(
    "Write the name of the movie you want to recommend:",
    movies['title'].values if not movies.empty else []
)

if st.button("Recommend") and not movies.empty and similarity is not None:
    names, posters, urls = recommend(selected_movie_name)

    cols = st.columns(5)  # Create 5 columns for displaying recommendations
    for i, col in enumerate(cols):
        with col:
            # Make the poster clickable using HTML and markdown
            movie_html = f"""
            <a href="{urls[i]}" target="_blank">
                <img src="{posters[i]}" alt="{names[i]}" style="width:100%;border-radius:10px;"/>
            </a>
            <div style="text-align:center; font-weight:bold; font-style:italic; margin-top:5px;">
                {names[i]}
            </div>
            """
            st.markdown(movie_html, unsafe_allow_html=True)
