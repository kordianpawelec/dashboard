from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse
from shared.schemas import Files, User
from pathlib import Path
from shared.crud_operations import crud_operations
from passlib.context import CryptContext
import os

password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

class APILogic:
    def __init__(self):
        self.file_storage = Path('shared/data')
    
    async def upload_file(self, user_id: int, file: UploadFile, session: Session):
        user_folder = self.file_storage / Path(f'user_{user_id}')
        os.makedirs(user_folder, exist_ok=True)
        
        user_folder = user_folder / f'user_{user_id}'
        user_folder.mkdir(parents=True, exist_ok=True)
        
        file_path = user_folder / file.filename
        file_path.write_bytes(await file.read())

        file_size = file_path.stat().st_size
        
        crud_operations.create_file(
            session=session,
            user_id=user_id,
            original_name=file.filename,
            stored_filename=str(file_path),
            file_size=file_size,
            file_type=file.content_type or "Unknown"
        )
        
        return {'status': 'success', 'filename': file.filename}
    
    def list_files(self, user_id: int, session: Session):
        files = crud_operations.get_files_by_user(session=session, user_id=user_id)
        return [
            {
                'file_id': f.file_id,
                'name': f.original_name,
                'size': f.file_size,
                'type': f.file_type
            }
            for f in files
        ]
    
    def download_file(self, user_id: int, file_id: int, session: Session):
        file_record = crud_operations.get_file_by_id(
            session=session,
            file_id=file_id,
            user_id=user_id
        )
        
        if not file_record:
            raise HTTPException(status_code=404, detail='File not found')
        
        return FileResponse(
            path=file_record.stored_filename,
            filename=file_record.original_name
        )
    
    def register_user(self, username: str, email: str, password: str, session: Session):
        existing_user = crud_operations.get_user_by_username(session, username)
        if existing_user:
            raise HTTPException(status_code=400, detail='user already exists')
        
        existing_email = crud_operations.get_user_by_email(session, email)
        if existing_email:
            raise HTTPException(status_code=400, detail='email already in use')
        
        hashed_password = password_hasher.hash(password[:72])
        new_user = crud_operations.create_user(
            session=session,
            username=username,
            email=email,
            hashed_password=hashed_password
        )

        return {
            'status': 'success',
            'user_id': new_user.id,
            'username': username,
            'email': email
        }
    
    def login_user(self, username: str, password:str, session: Session):
        user = crud_operations.get_user_by_username(session, username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not password_hasher.verify(password[:72], user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return {
            'status': 'success',
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }