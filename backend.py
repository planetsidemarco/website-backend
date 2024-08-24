"""Python fastapi backend"""

import os
from pathlib import Path
import uvicorn
import boto3
from botocore.exceptions import ClientError
from fastapi import FastAPI, File, UploadFile, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# S3 client setup
env_path = Path("./awsaccess.env")
load_dotenv(dotenv_path=env_path)
s3 = boto3.client('s3',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name=os.environ['AWS_REGION']
)

@app.post("/s3/upload")
async def upload_file(file: UploadFile = File(...)):
    # Upload file to S3
    s3.upload_fileobj(file.file, os.environ['AWS_BUCKET_NAME'], file.filename)
    return {"filename": file.filename}

@app.get("/image/{image_name}")
async def get_image(image_name: str):
    try:
        response = s3.get_object(Bucket=os.environ['AWS_BUCKET_NAME'], Key=image_name)
        return Response(content=response['Body'].read(), media_type="image/png")
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise HTTPException(status_code=404, detail="Image not found")
        else:
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)