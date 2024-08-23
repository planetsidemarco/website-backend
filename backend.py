"""Python fastapi backend"""

import os
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import boto3


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
s3 = boto3.client('s3',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
)

@app.get("/api/data")
async def get_data():
    # Fetch data from your database
    return {"text": "Dynamic content", "imageUrl": "https://planetsidemarco-bucket.s3.amazonaws.com/test.png"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    # Upload file to S3
    s3.upload_fileobj(file.file, "planetsidemarco-bucket", file.filename)
    return {"filename": file.filename}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)