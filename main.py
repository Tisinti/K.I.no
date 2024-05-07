#from app.web import app
#from app.training import iterate_models
from app.preprocessor import export_whole_meta


if __name__ == "__main__":
    #app.run(debug=True)
    #print(iterate_models())
    export_whole_meta()