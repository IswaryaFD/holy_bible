from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
from uuid import uuid4

router = APIRouter()
BASE_DIR = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(BASE_DIR, '..', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post('/upload-image')
async def upload_image(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    fn = f"{uuid4().hex}{ext}"
    save_path = os.path.join(UPLOAD_DIR, fn)
    with open(save_path, 'wb') as f:
        content = await file.read()
        f.write(content)
    return {'filename': fn}

@router.post('/bible-verse')
async def post_bible_verse(text: str = Form(...), file: UploadFile | None = File(None)):
    file_name = None
    if file:
        ext = os.path.splitext(file.filename)[1]
        file_name = f"{uuid4().hex}{ext}"
        with open(os.path.join(UPLOAD_DIR, file_name), 'wb') as f:
            f.write(await file.read())
    return {'id': uuid4().hex, 'text': text, 'file': file_name}

@router.post('/qa')
async def post_qa(question: str = Form(...), answer: str = Form(...)):
    return {'id': uuid4().hex, 'question': question, 'answer': answer}

@router.get('/health')
async def health():
    return JSONResponse({'status':'ok'})
