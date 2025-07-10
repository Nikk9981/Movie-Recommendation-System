import pickle
import streamlit as st
import requests

# ---- CONFIG ----
TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"


# ---- POSTER FETCH FUNCTION ----
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        poster_path = data.get('poster_path')
        if poster_path:
            return {
                'poster_url': f"https://image.tmdb.org/t/p/w500/{poster_path}",
                'tmdb_url': f"https://www.themoviedb.org/movie/{movie_id}"
            }
        else:
            return None
    except:
        return None

# ---- RECOMMEND FUNCTION ----
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended = []
    for i in distances[1:15]:  # Take more in case of missing posters
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster_data = fetch_poster(movie_id)
        
        if poster_data:
            recommended.append((title, poster_data['poster_url'], poster_data['tmdb_url']))
        
        if len(recommended) == 5:
            break
    return recommended

# ---- LOAD MODEL ----
movies = pickle.load(open(r'C:\Users\DELL\OneDrive\Desktop\Python\ML Projects\Movie Recommandation\movie_list.pkl', 'rb'))
similarity = pickle.load(open(r'C:\Users\DELL\OneDrive\Desktop\Python\ML Projects\Movie Recommandation\similarity.pkl', 'rb'))

# ---- STREAMLIT UI ----
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")
st.write("Find your next favorite movie — start by picking one from the list!")

selected_movie = st.selectbox("🎥 Choose a movie", movies['title'].values)

if st.button("Show Recommendation"):
    recommendations = recommend(selected_movie)
    
    if recommendations:
        cols = st.columns(5)
        for idx, (title, poster_url, tmdb_url) in enumerate(recommendations):
            with cols[idx]:
                st.markdown(f"**{title}**")
                # st.image(poster_url, use_column_width=True)
                st.image(poster_url, use_container_width=True)

                st.markdown(f"[🔗 View on TMDB]({tmdb_url})", unsafe_allow_html=True)
    else:
        st.warning("No recommendations found with available posters.")
