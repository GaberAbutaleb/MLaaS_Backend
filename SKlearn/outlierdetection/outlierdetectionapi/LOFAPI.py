from fastapi import FastAPI,status,HTTPException,File,UploadFile
import os
from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from repository import JWTRepo, JWTBearer
from SKlearn.  outlierdetection.outlierdetectionmodels.LocalOutlierFactor import  LOF
from fastapi.responses import FileResponse


router = APIRouter()


@router.post("/LOF-upload-file/", dependencies=[Depends(JWTBearer())])
async def create_LOF_upload_file(uploaded_file: UploadFile = File(...),noOfRows : int=0,noOfColumns : int=0,
                 fileName : str = "",no_of_neighbors : int = 0):
    print("start")
    file_location = f"SKlearn/outlierdetection/outlierdetectionapi/uploadedFiles/{uploaded_file.filename}"
    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(uploaded_file.file.read())
            print("file_location is: ",file_location)
            file_object.close()
            filedestination  =  os.path.join(os.path.dirname(__file__), f"uploadedFiles\{uploaded_file.filename}")
            print('filedestination', filedestination)
            LOFobj = LOF(filedestination, noOfRows, noOfColumns)
            print("no_of_neighbors:",no_of_neighbors)
            lof_outlier,labels,leaf_size,n_features_in_,n_neighbors,n_samples_fit_= LOFobj.createModel(no_neighbors = no_of_neighbors,OutputFileName =fileName)

            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, 'savedmodel/'+fileName+'.pkl')
            LOFobj.saveModel(LOFobj, filename)
            return { "LOF": "model created", "n_noise":list(labels).count(1),
                     "leaf_size":leaf_size,"n_features_in_":n_features_in_,
                     "n_neighbors":n_neighbors,
                     "n_samples_fit_":n_samples_fit_}

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)}
        )
@router.get('/outlierdetection/model', response_class=FileResponse, dependencies=[Depends(JWTBearer())])
async def getoutlierdetectionModel(modelName):
    projectPath = "D:\\PHDLAP\\MLaaS\\SKlearn\\outlierdetection\\outlierdetectionapi\\savedmodel\\"
    print("ROOT :", projectPath )
    return FileResponse(projectPath +modelName , media_type='application/octet-stream',filename=modelName)

@router.get('/outlierdetection/outputdata', response_class=FileResponse, dependencies=[Depends(JWTBearer())])
async def getoutlierdetectionOutputFile(outputFileName):
    projectPath = "D:\\PHDLAP\\MLaaS\\SKlearn\\outlierdetection\\outputFiels\\"
    print("ROOT :", projectPath )
    return FileResponse(projectPath +outputFileName , media_type='application/octet-stream',filename=outputFileName)
