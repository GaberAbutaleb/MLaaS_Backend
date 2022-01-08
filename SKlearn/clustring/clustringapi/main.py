from fastapi import FastAPI,status,HTTPException,File,UploadFile
from SKlearn.clustring.clustringmodel.KmeansClustring import Kmeans
import os
import sys
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

router = APIRouter()
# origins = ["*"]
#
# router.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# @router.post('/createkmeansmodel',status_code=status.HTTP_201_CREATED)
async def create_KmeansModel( filePath :str, noOfRows : int=0,noOfColumns : int=0, method: str = "elbow"):
    Kmeansobj = Kmeans(filePath,noOfRows,noOfColumns)
    kmeans, y_kmeans = Kmeansobj.createmodel(method=method)
    dirname = os.path.dirname(__file__)
    Kmeansobj.plotKMeans(kmeans,y_kmeans)
    # Kmeansobj.kmeansEvaluation(kmeans)
    filename = os.path.join(dirname, 'savedmodel/kmeansmodel')
    Kmeansobj.saveModel(kmeans, filename)
    return {"kmeans": "model created","n_iter":kmeans.n_iter_,"kmeans.inertia":kmeans.inertia_}

@router.post("/upload-file/")
async def create_upload_file(uploaded_file: UploadFile = File(...),noOfRows : int=0,noOfColumns : int=0,
                             method: str = "elbow", clustringImageName : str = ""):
    print("start")
    file_location = f"SKlearn/clustring/clustringapi/uploadedFiles/{uploaded_file.filename}"
    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(uploaded_file.file.read())
            print("file_location is: ",file_location)
            file_object.close()
            filedestination  =  os.path.join(os.path.dirname(__file__), f"uploadedFiles\{uploaded_file.filename}")
            print('filedestination', filedestination)
            Kmeansobj = Kmeans(filedestination, noOfRows, noOfColumns)
            kmeans, y_kmeans,numberOfK = Kmeansobj.createmodel(method=method)
            dirname = os.path.dirname(__file__)
            Kmeansobj.plotKMeans(kmeans, y_kmeans,clustringImageName)
            # Kmeansobj.kmeansEvaluation(kmeans)
            filename = os.path.join(dirname, 'savedmodel/'+clustringImageName+'.pkl')
            Kmeansobj.saveModel(kmeans, filename)
            print("numberOfK", numberOfK)
            return { "numberOfK": str(numberOfK),"kmeans": "model created", "n_iter": kmeans.n_iter_, "inertia": kmeans.inertia_}
        #return {"info": f"file '{uploaded_file.filename}' uploaded successfully"}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)}
        )

# @router.get("/")
@router.post('/kmclustring/image', response_class=FileResponse, responses={200: {'content': {'image/png': {}}}})
async def getClusterImage(imageName):
    ROOT_DIR =Path(__file__).parent.parent
    root = str(ROOT_DIR )+ f"\images\{imageName}.png"
    print("ROOT :", root)
    return FileResponse(root, media_type='image/png')

@router.get('/kmclustring/model', response_class=FileResponse)
async def getClusterModel(modelName):
    projectPath = "D:\\PHDLAP\\MLaaS\\SKlearn\\clustring\\clustringapi\\savedmodel\\"
    # ROOT_DIR =Path(__file__).parent.parent
    # root = str(ROOT_DIR )+ path
    print("ROOT :", projectPath )
    return FileResponse(projectPath +modelName , media_type='application/octet-stream',filename=modelName)