import os
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import FastAPI, UploadFile, File as FastAPIFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

from .database import Base, engine, get_db
from . import models, schemas
from .ai_mock import analyze_file_metadata


Base.metadata.create_all(bind=engine)


STORAGE_DIR = Path("./storage")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Document Storage Service",
    description="Мини-сервис для хранения документов с версияцией и AI-анализом",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/files/upload", response_model=schemas.FileOut)
async def upload_file(
    file: UploadFile = FastAPIFile(...), db: Session = Depends(get_db)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    original_name = file.filename


    max_version = (
        db.query(func.max(models.File.version))
        .filter(models.File.original_name == original_name)
        .scalar()
    )
    new_version = (max_version or 0) + 1


    content = await file.read()
    size = len(content)

    safe_name = original_name.replace("/", "_").replace("\\", "_")
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    storage_filename = f"v{new_version}_{timestamp}_{safe_name}"
    storage_path = STORAGE_DIR / storage_filename

    with open(storage_path, "wb") as f:
        f.write(content)

    db_file = models.File(
        original_name=original_name,
        version=new_version,
        path=str(storage_path),
        size=size,
        uploaded_at=datetime.utcnow(),
        uploaded_by=1,
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file



@app.get("/files", response_model=List[schemas.FileOut])
def list_files(db: Session = Depends(get_db)):
    files = db.query(models.File).order_by(
        models.File.original_name, models.File.version
    ).all()
    return files


# ai-analyze
@app.post("/files/{file_id}/analyze", response_model=schemas.FileAnalysisOut)
def analyze_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(models.File).filter(models.File.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    if not os.path.exists(db_file.path):
        raise HTTPException(status_code=500, detail="File missing on disk")

    meta = {
        "file_name": db_file.original_name,
        "file_size": db_file.size,
        "version": db_file.version,
        "uploaded_at": db_file.uploaded_at.isoformat(),
    }

    comment = analyze_file_metadata(meta)

    existing = (
        db.query(models.FileAnalysis).filter(models.FileAnalysis.file_id == file_id).first()
    )
    if existing:
        existing.comment = comment
        existing.created_at = datetime.utcnow()
        analysis = existing
    else:
        analysis = models.FileAnalysis(
            file_id=file_id,
            comment=comment,
            created_at=datetime.utcnow(),
        )
        db.add(analysis)

    db.commit()
    db.refresh(analysis)

    return analysis


@app.get("/files/{file_id}/analysis", response_model=schemas.FileAnalysisOut)
def get_analysis(file_id: int, db: Session = Depends(get_db)):
    analysis = (
        db.query(models.FileAnalysis)
        .filter(models.FileAnalysis.file_id == file_id)
        .first()
    )
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis
