from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from image_to_obj import handle_prompt_to_obj, run_tripoSR_inference

app = FastAPI()

# Enable CORS (modify in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate-obj")
def generate_obj_from_prompt(data: PromptRequest):
    try:
        obj_path = handle_prompt_to_obj(data.prompt)
        return FileResponse(
            path=obj_path,
            media_type='application/octet-stream',
            filename=f"{data.prompt.replace(' ', '-')}.obj"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-image")
def generate_obj_from_image(file: UploadFile = File(...)):
    try:
        image_path = "TripoSR/examples/generated.png"

        # Save the uploaded image
        with open(image_path, "wb") as f:
            f.write(file.file.read())

        # Run TripoSR
        obj_path = run_tripoSR_inference(image_path)

        return FileResponse(
            path=obj_path,
            media_type='application/octet-stream',
            filename="uploaded-image.obj"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
