from fastapi import FastAPI,status,HTTPException,File,UploadFile,Depends,Form

from SKlearn.DataPreprocessing.DataExplorationReport import PDF,PDFCreation
from SKlearn.DataPreprocessing.PreprocessingRequest import PreProcesingRequest
from SKlearn.DataPreprocessing.DataCleaningPrep import DataCleaning
from SKlearn.DataPreprocessing.DataOutlierPrep import OutlierPrep
from SKlearn.DataPreprocessing.DataScalingPrep import  DataScaling
from SKlearn.DataPreprocessing.DimensionalityReductionPrep import  DimensionalityReductionPrep
from SKlearn.DataPreprocessing.ImbalancePrep import  DataBalance
from SKlearn.DataPreprocessing.CategoricalDataPrep import CategoricalData
import os
import sys
from typing import ClassVar, List
from repository import JWTRepo, JWTBearer, UsersRepo
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from jose import jwt
from fastapi.responses import FileResponse
from pathlib import Path
import pandas as pd


router = APIRouter()

# @router.post("/MLaaS/dataexploration", dependencies=[Depends(JWTBearer())])
# @router.post("/MLaaS/dataexploration")
async def dataExploration(request: Request,uploaded_file: UploadFile = File(...)):
    # token = request.headers.get('Authorization').replace("Bearer ", "")
    # print(token)
    # payload = jwt.decode(token, key='lemoncode21', options={"verify_signature": False})
    # print(payload["userName"])
    file_location = f"SKlearn/DataPreprocessing/uploadedFiles/{uploaded_file.filename}"
    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(uploaded_file.file.read())
            print("file_location is: ",file_location)
            file_object.close()
            filedestination  =  os.path.join(os.path.dirname(__file__), f"uploadedFiles\{uploaded_file.filename}")
            print('filedestination', filedestination)
            df = pd.read_csv(filedestination)
            dataCleaningobj =DataCleaning()
            nullColumnSummary = dataCleaningobj.data_explorationNullCounts(df)

            # print("before return")
            print(type(nullColumnSummary.to_json()))
            return nullColumnSummary.to_json()

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)}
        )

@router.post('/MLaaS/dataexplorationheatmap', response_class=FileResponse, responses={200: {'content': {'image/png': {}}}})
async def getheatmapImage(imageName):
    ROOT_DIR =Path(__file__).parent
    root = str(ROOT_DIR )+ f"\images\{imageName}.png"
    print("ROOT :", root)
    return FileResponse(root, media_type='image/png')

@router.post('/MLaaS/dataexplorationreport', response_class=FileResponse)
async def getdataexplorationreport(uploaded_file: UploadFile = File(...)):
    filedestination = os.path.join(os.path.dirname(__file__), f"uploadedFiles\{uploaded_file.filename}")
    try:
        with open(filedestination, "wb+") as file_object:
            file_object.write(uploaded_file.file.read())
            print("file_location is: ",filedestination)
            file_object.close()
            filedestination  =  os.path.join(os.path.dirname(__file__), f"uploadedFiles\{uploaded_file.filename}")
            print("filedestination", filedestination)
            pdfCreation = PDFCreation(filedestination)
            filename = pdfCreation.startUp()
            print(filename, " is Created")
            return FileResponse(filename, media_type='application/octet-stream', filename="Data Exploration Report.pdf")
            # filedestination = os.path.join(os.path.dirname(__file__), f"uploadedFiles\{uploaded_file.filename}")

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)}
        )
@router.post('/MLaaS/dataPreprocessing', response_class=FileResponse)
async def dataPreprocessing(handleDataCleaning: bool=True,dO_HandlingOutliers : bool=True,dCD_HandelCategoricalData:bool =True,dS_HandelScaling:bool=True,
    dI_HandelImbalance:bool=True,
    dR_HandelDimRed:bool=True,
    dC_HandlingMethod : str="median",
    dC_columnList : str="",
    dC_Threshold : int=6,
    dR_n_components :int=6,
    dC_regTarColumn="",
    dO_detectionMethod ="iqrMethod" ,
    dO_HandlingMethod="median",
    dS_columnsList:str ="",
    categoryEncoderMethod = "OneHotEncoding",
    dS_scaleMethod="StandardScaler",
    dI_className="",
    dI_technique = "RCMND",
    dR_handelingMethod="PCA",
    uploaded_file: UploadFile = File(...)) :
    print("DataPreProcessing")
    if(dC_columnList):
        dC_columnList=dC_columnList.split(",")
    else:
        dC_columnList=[]
    if (dS_columnsList):
        dS_columnsList = dS_columnsList.split(",")
    else:
        dS_columnsList = []
    print(dC_columnList)
    filedestination = os.path.join(os.path.dirname(__file__), f"uploadedFiles\{uploaded_file.filename}")
    df = pd.DataFrame()
    try:
        with open(filedestination, "wb+") as file_object:
            file_object.write(uploaded_file.file.read())
            print("file_location is: ",filedestination)
            file_object.close()
            filedestination  =  os.path.join(os.path.dirname(__file__), f"uploadedFiles\{uploaded_file.filename}")
            print("filedestination", filedestination)
            df = pd.read_csv(filedestination)
            if (handleDataCleaning):
                dataCleaningObj = DataCleaning()
                print(df.shape)
                df = dataCleaningObj.HandlingMissingValuesMethod(df,HandlingMethod=dC_HandlingMethod,columnList=dC_columnList,threshold=dC_Threshold,regressionTargetColumn=dC_regTarColumn)
            if(dO_HandlingOutliers):
                print("handleAllOutliers")
                outlierPrepObj =OutlierPrep(df)
                df= outlierPrepObj.handleAllOutliers(df,HandlingMethod=dO_HandlingMethod,detectionMethod =dO_detectionMethod)
                print("HandlingOutliers")
            if(dCD_HandelCategoricalData):
                print("dCD_HandelCategoricalData")
                categoricalDataObj=CategoricalData()
                df=categoricalDataObj.HandelCategoricalData(df,category_encoder_method=categoryEncoderMethod)
            if (dI_HandelImbalance):
                print("dI_HandelImbalance")
                dataBalanceObj = DataBalance(dataFrame=df, target=dI_className)
                df = dataBalanceObj.balance(technique=dI_technique)
            if(dR_HandelDimRed):
                print("dR_HandelDimRed")
                DimRedPrep = DimensionalityReductionPrep(df, dR_n_components, dR_handelingMethod)
                df = DimRedPrep.handelingDimRed()
            if(dS_HandelScaling):
                print("HandelScaling")
                dataScalingObj = DataScaling()
                df=dataScalingObj.HandlingScale(df=df, columnsList=dS_columnsList, scaleMethod=dS_scaleMethod)

        dirname = os.path.dirname(__file__)
        finalOutputFilePath = f'{dirname}/downloadedFiles/'
        df.to_csv(f"{finalOutputFilePath}"+"/"+f"{uploaded_file.filename}.csv", index=False)
        return FileResponse(finalOutputFilePath+f"{uploaded_file.filename}.csv", media_type='application/octet-stream', filename=f"{uploaded_file.filename}")
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)}
        )
