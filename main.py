from app.utils import SearchMovie
from app.utils import genre_helper

if __name__ == "__main__":
    genre = genre_helper.id_to_genre(35)
    search = "Apocalypse Now"
    result = SearchMovie(search)
    print(result)
    


