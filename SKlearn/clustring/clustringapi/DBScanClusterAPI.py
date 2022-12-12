from fastapi import FastAPI,status,HTTPException,File,UploadFile
import os
from SKlearn.clustring.clustringmodel.DBScanClustring import DBScan
from typing import List
import sys
from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from pathlib import Path
from repository import JWTRepo, JWTBearer
from fastapi.middleware.cors import CORSMiddleware
from schema import PredictClustringModel

router = APIRouter()

@router.post("/DBScan-upload-file/", dependencies=[Depends(JWTBearer())])
async def create_upload_file(uploaded_file: UploadFile = File(...),noOfRows : int=0,noOfColumns : int=0,
                 clustringImageName : str = "",espvalue : int = 0, minSamples : int = 10):
    print("start")
    file_location = f"SKlearn/clustring/clustringapi/uploadedFiles/{uploaded_file.filename}"
    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(uploaded_file.file.read())
            print("file_location is: ",file_location)
            file_object.close()
            filedestination  =  os.path.join(os.path.dirname(__file__), f"uploadedFiles\{uploaded_file.filename}")
            print('filedestination', filedestination)
            DBScansobj = DBScan(filedestination, noOfRows, noOfColumns)
            print("espvalue:",espvalue)
            DBSCan, y_DBScan,numberOfK ,epsvalue,silhouette_score,calinski_harabasz_score,davies_bouldin_score= DBScansobj.createmodel( k=espvalue,minSamples = minSamples,OutputFileName =clustringImageName)

            dirname = os.path.dirname(__file__)
            DBScansobj.plotDBScan(DBSCan, y_DBScan,clustringImageName)
            # Kmeansobj.kmeansEvaluation(kmeans)
            filename = os.path.join(dirname, 'savedmodel/'+clustringImageName+'.pkl')
            DBScansobj.saveModel(DBSCan, filename)
            print("numberOfK", numberOfK)
            return { "numberOfK": str(numberOfK),"DBScan": "model created", "n_noise":list(DBSCan.labels_).count(-1),
                     "epsvalue":epsvalue,"silhouette_score":silhouette_score,
                     "calinski_harabasz_score":calinski_harabasz_score,
                     "davies_bouldin_score":davies_bouldin_score}

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)}
        )
