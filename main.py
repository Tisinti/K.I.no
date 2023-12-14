from app.web import app
from app.training import iterate_models

if __name__ == "__main__":
    app.run(debug=True)
    #print(iterate_models())