from fastapi import FastAPI,status,HTTPException,File,UploadFile
import os
from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from repository import JWTRepo, JWTBearer
from SKlearn.  outlierdetection.outlierdetectionmodels.GMMModel import GMM
from fastapi.responses import FileResponse
from typing import Union



router = APIRouter()



@router.post("/GMM-upload-file/", dependencies=[Depends(JWTBearer())])
async def create_GMM_upload_file(scoreThreshold : float = 0 ,uploaded_file: UploadFile = File(...),noOfRows : int=0,noOfColumns : int=0,
                 fileName : str = "",n_Init: int = 0,n_Components: int =0,max_Iter: int = 100 ):
    file_location = f"SKlearn/outlierdetection/outlierdetectionapi/uploadedFiles/{uploaded_file.filename}"
    print("scoreThreshold:::",scoreThreshold)
    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(uploaded_file.file.read())
            print("file_location is: ",file_location)
            file_object.close()
            filedestination  =  os.path.join(os.path.dirname(__file__), f"uploadedFiles\{uploaded_file.filename}")
            print('filedestination', filedestination)
            GMMobj = GMM(filedestination, noOfRows, noOfColumns)
            gmm,n_components,n_features_in_,max_iter,weights_,means_,th= GMMobj.createModel(scoreThreshold,nInit=n_Init,nComponents=n_Components,maxIter=max_Iter ,OutputFileName =fileName)

            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, 'savedmodel/'+fileName+'.pkl')
            GMMobj.saveModel(gmm, filename)
            return { "GMM": "model created", "n_components":n_components,
                     "n_features_in_":n_features_in_,
                     "max_iter":max_iter,
                     "scoreThreshold":th}

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)}
        )