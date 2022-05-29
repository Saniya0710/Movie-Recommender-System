
# Movie Recommender System

Based on the past user behavior, MoRe recommends the movies to users based on their similarity. It suggests movies to users with a recommendation rate that is greater than the preference rate of movie for the same user
## Using cosine similarity
Cosine Similarity
Cosine similarity is a metric used to measure how similar two items are. Mathematically it calculates the cosine of the angle between two vectors projected in a multidimensional space. Cosine similarity is advantageous when two similar documents are far apart by Euclidean distance(size of documents) chances are they may be oriented closed together. The smaller the angle, higher the cosine similarity.
![image](https://user-images.githubusercontent.com/92110239/170874251-da93fc88-8ad9-4f91-99d0-24612b447e18.png)

1 - cosine-similarity = cosine-distance
## Installation/Environment Setup

1. Clone this repository in your local system.
..Open terminal in a new folder and enter the command given below.

```bash
git clone https://github.com/Saniya0710/Movie-Recommender-System.git
```
2. Make sure that Python is installed and updated in your machine.
3. Install dependencies.
..Open terminal in the cloned folder and enter the command given below.
```bash
pip3 install -r requirements.txt

```
4. Run the project.
..write the following command in terminal to run the website locally
```bash
streamlit run app1.py
```


    

## 🔗 Links
https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv
