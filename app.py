import streamlit as st
import pickle
import requests

st.set_page_config(page_title='Movies Recommender', page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

def local_css(file_name):
  with open(file_name) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

def fetch_poster(movie_id):
  response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=741df89ec07d3926f71889482ba5e706'.format(movie_id))
  data = response.json()
  return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
  movie_index = movies_list[movies_list['title'] == movie].index[0]
  distances = similarity[movie_index]
  movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
  recommended_movies = []
  recommended_movies_posters = []
  for i in movies:
    movie_id = movies_list.iloc[i[0]].movie_id
    recommended_movies.append(movies_list.iloc[i[0]].title)
    recommended_movies_posters.append(fetch_poster(movie_id))
  return recommended_movies, recommended_movies_posters

movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
  'Search the movies based on your test',
  movies_list['title'].values
)


if st.button('Recommend'):
  names, posters = recommend(selected_movie_name)
  col1, col2, col3, col4, col5 = st.columns(5)
  with col1:
    st.text(names[0])
    st.image(posters[0])
  with col2:
    st.text(names[1])
    st.image(posters[1])
  with col3:
    st.text(names[2])
    st.image(posters[2])
  with col4:
    st.text(names[3])
    st.image(posters[3])
  with col5:
    st.text(names[4])
    st.image(posters[4])