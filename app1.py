import streamlit as st
import pandas as pd
import sqlite3
import pickle
import requests
import hashlib
from PIL import Image


movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity_matrix.pkl', 'rb'))


def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False


conn = sqlite3.connect('data.db')
c = conn.cursor()


# function to  create username and password

def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')


# function to add userdata

def add_userdata(username, password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
	conn.commit()


def login_user(username, password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
	data = c.fetchall()
	return data


with open('style.css') as f:
	st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# function to fetch_movie-poster

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=ff87a08588cf890748016a3047c27781".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


#function to fetch the data of a required movie

def fetch_data(movie_id):

    url = "https://api.themoviedb.org/3/movie/{}?api_key=ff87a08588cf890748016a3047c27781".format(movie_id)
    data = requests.get(url)
    data = data.json()
    return data

#function to get the recommended movies

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_release = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_release.append(fetch_data(movie_id))

    return recommended_movie_names, recommended_movie_posters, recommended_movie_release


# showing particular details of movie such as releaseData, vote_avg

def show_details(data):
	rel_date = data['release_date']
	vote_avg = data['vote_average']
	cap = "Released:{} \n ({}/10) ".format(rel_date, vote_avg)
	return cap

def main():
	st.title("Movie Recommendation System")
	menu = ["Home", "Login", "SignUp"]
	choice = st.sidebar.selectbox("Menu", menu)

	if choice == "Home":
		st.subheader("Unlimited Movies!")
		st.image(Image.open("images/home.jpg"), caption='SignUp to enjoy watching your favourite movies')
	elif choice == "Login":
		st.subheader("Login Section")
		st.image(Image.open("images/login.jpg"))

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password", type='password')
		if st.sidebar.checkbox("Login"):
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username, check_hashes(password, hashed_pswd))
			if result:

				st.success("Welcome {}!".format(username))
				movie_list = movies['title'].values
				selected_movie = st.selectbox(
					"Type or select a movie from the dropdown",
					movie_list
				)
				#collecting recommendations
				if st.button('Show Recommendation'):
					recommended_movie_names, recommended_movie_posters, recommended_movie_data = recommend(selected_movie)
					col1, col2, col3, col4, col5 = st.columns(5)

					with col1:
						st.text(recommended_movie_names[0])
						st.image(recommended_movie_posters[0], caption=show_details(recommended_movie_data[0]))
					with col2:
						st.text(recommended_movie_names[1])
						st.image(recommended_movie_posters[1], caption=show_details(recommended_movie_data[1]))

					with col3:
						st.text(recommended_movie_names[2])
						st.image(recommended_movie_posters[2], caption=show_details(recommended_movie_data[0]))
					with col4:
						st.text(recommended_movie_names[3])
						st.image(recommended_movie_posters[3], caption=show_details(recommended_movie_data[0]))
					with col5:
						st.text(recommended_movie_names[4])
						st.image(recommended_movie_posters[4], caption=show_details(recommended_movie_data[0]))

			else:
				st.warning("Incorrect Username/Password")

	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password", type='password')

		if st.button("Signup"):
			create_usertable()
			if len(new_user) > 3:
				add_userdata(new_user, make_hashes(new_password))
				st.success("You have successfully created a valid Account")
				st.info("Go to Login Menu to login")
			else:
				st.warning('username must be atleast 4 characters')


if __name__ == '__main__':
	main()