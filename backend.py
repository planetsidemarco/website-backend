"""Python fastapi backend"""

import os
from pathlib import Path
import uvicorn
import boto3
from botocore.exceptions import ClientError
from fastapi import FastAPI, File, UploadFile, Response, HTTPException
from fastapi.responses import FileResponse
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

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    favicon_path = Path("favicon.ico")
    if not favicon_path.is_file():
        return {"error": "Image not found on the server"}
    return FileResponse(favicon_path)

@app.get("/image/test")
async def get_image():
    image_path = Path("test.png")
    if not image_path.is_file():
        return {"error": "Image not found on the server"}
    return FileResponse(image_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)