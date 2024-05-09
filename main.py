#from app.web import app
#from app.training import iterate_models
from app.preprocessor import export_whole_meta
from app.preprocessor import execute_export
from app.analysis import createAllPlotsPipe


if __name__ == "__main__":
    #app.run(debug=True)
    #print(iterate_models())
    #execute_export()
    #export_whole_meta()
    createAllPlotsPipe()