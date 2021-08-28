from fastapi import FastAPI, File, UploadFile
from client import infer_image_densenet

app = FastAPI()

@app.get("/")
async def root():
    
    return {"message": "Hello World"}



@app.post("/infer")
def upload_file(file: UploadFile = File(...)): 
    print(file)
    return infer_image_densenet(file.file)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=5000, reload=True)

