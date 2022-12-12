from fastapi import FastAPI,status,HTTPException,File,UploadFile
import os
from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from repository import JWTRepo, JWTBearer
from SKlearn.  outlierdetection.outlierdetectionmodels.KNNModel import  KNN
from fastapi.responses import FileResponse
from pathlib import Path



router = APIRouter()


@router.post("/KNN-upload-file/", dependencies=[Depends(JWTBearer())])
async def create_KNN_upload_file(distancesThreshold : float = 0,uploaded_file: UploadFile = File(...),noOfRows : int=0,noOfColumns : int=0,
                 fileName : str = "",no_of_neighbors : int = 5):
    file_location = f"SKlearn/outlierdetection/outlierdetectionapi/uploadedFiles/{uploaded_file.filename}"
    print("knn")
    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(uploaded_file.file.read())
            print("file_location is: ",file_location)
            file_object.close()
            filedestination  =  os.path.join(os.path.dirname(__file__), f"uploadedFiles\{uploaded_file.filename}")
            print('filedestination', filedestination)
            KNNobj = KNN(filedestination, noOfRows, noOfColumns)
            print("no_of_neighbors:",no_of_neighbors)
            nbrsModel,labels,n_neighbors,n_features_in_,n_samples_fit_,th= KNNobj.createModel(distancesThreshold,no_neighbors = no_of_neighbors,OutputFileName =fileName)

            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, 'savedmodel/'+fileName+'.pkl')
            KNNobj.saveModel(KNNobj, filename)
            return { "KNN": "model created", "n_features_in_":n_features_in_,
                     "n_neighbors":n_neighbors,
                     "n_samples_fit_":n_samples_fit_, "distancesThreshold":th}

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)}
        )
# @router.get('/KNNoutlierdetection/model', response_class=FileResponse, dependencies=[Depends(JWTBearer())])
# async def getoutlierdetectionKNN(modelName):
#     projectPath = "D:\\PHDLAP\\MLaaS\\SKlearn\\outlierdetection\\outlierdetectionapi\\savedmodel\\"
#     print("ROOT :", projectPath )
#     return FileResponse(projectPath +modelName , media_type='application/octet-stream',filename=modelName)
#
# @router.get('/KNNoutlierdetection/outputdata', response_class=FileResponse, dependencies=[Depends(JWTBearer())])
# async def getoutlierdetectionKNNOutputFile(outputFileName):
#     projectPath = "D:\\PHDLAP\\MLaaS\\SKlearn\\outlierdetection\\outputFiels\\"
#     print("ROOT :", projectPath )
#     return FileResponse(projectPath +outputFileName , media_type='application/octet-stream',filename=outputFileName)

@router.post('/outlierclustring/image', response_class=FileResponse, responses={200: {'content': {'image/png': {}}}}, dependencies=[Depends(JWTBearer())])
async def getClusterImage(imageName):
    ROOT_DIR =Path(__file__).parent.parent
    root = "SKlearn\clustring"+ f"\images\{imageName}.png"
    print("ROOT :", root)
    return FileResponse(root, media_type='image/png')