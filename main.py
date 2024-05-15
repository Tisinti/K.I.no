#from app.web import app
from app.training import iterate_models
#from app.analysis import createPlotYear
#from app.preprocessor import export_whole_meta

if __name__ == "__main__":
    #app.run(debug=True)
    iterate_models()
    #createPlotYear("data/raw/winter_2324.csv")
    #export_whole_meta()
