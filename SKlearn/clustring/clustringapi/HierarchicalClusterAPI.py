from fastapi import FastAPI,status,HTTPException,File,UploadFile
from SKlearn.clustring.clustringmodel.HierarchicalCluster import HierarchicalCluster
import os
import sys
from repository import JWTRepo, JWTBearer, UsersRepo
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from jose import jwt
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

@router.post("/HClusterUpload-file/", dependencies=[Depends(JWTBearer())])
async def create_upload_file(request: Request,uploaded_file: UploadFile = File(...),noOfRows : int=0, noOfColumns : int=0
                             , clustringImageName : str = "",number_of_HCluster : int = 2,affinity: str ='euclidean' , linkage: str = 'ward' ):
    token = request.headers.get('Authorization').replace("Bearer ", "")
    print(token)
    payload = jwt.decode(token, key='lemoncode21', options={"verify_signature": False})
    print(payload["userName"])
    file_location = f"SKlearn/clustring/clustringapi/uploadedFiles/{uploaded_file.filename}"
    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(uploaded_file.file.read())
            print("file_location is: ",file_location)
            file_object.close()
            filedestination  =  os.path.join(os.path.dirname(__file__), f"uploadedFiles\{uploaded_file.filename}")
            print('filedestination', filedestination)
            HierarchicalClusterobj = HierarchicalCluster(filedestination, noOfRows, noOfColumns)
            print("HierarchicalCluster:",number_of_HCluster)
            Hierarchicalcluster, y_Hierarchicalcluster,numberOfK = \
                HierarchicalClusterobj.createmodel( k=number_of_HCluster,affinity=affinity,linkage=linkage,OutputFileName =clustringImageName)
            dirname = os.path.dirname(__file__)
            HierarchicalClusterobj.plotKMeans(Hierarchicalcluster, y_Hierarchicalcluster,clustringImageName)
            filename = os.path.join(dirname, 'savedmodel/'+clustringImageName+'.pkl')
            HierarchicalClusterobj.saveModel(Hierarchicalcluster, filename)
            print("numberOfK", numberOfK)
            return { "numberOfK": str(numberOfK),"HierarchicalCluster": "model created", "n_clusters": Hierarchicalcluster.n_clusters}

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)}
        )
