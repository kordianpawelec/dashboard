from sqlalchemy.orm import Session
from shared.schemas import Files, User
from typing import Optional, List


class CRUDOperations:
    @staticmethod
    def create_file(
        session: Session,
        user_id: int,
        original_name: str,
        stored_filename: str,
        file_size: int,
        file_type: str
    ) -> Files:
        
        file_record = Files(
            user_id=user_id,
            original_name=original_name,
            stored_filename=stored_filename,  
            file_size=file_size,
            file_type=file_type
        )
        session.add(file_record)
        session.commit()
        session.refresh(file_record)
        return file_record

    @staticmethod
    def get_files_by_user(session: Session, user_id: int) -> List[Files]:
        return session.query(Files).filter(Files.user_id == user_id).all()
    
    @staticmethod
    def get_file_by_id(session: Session, file_id: int, user_id: int) -> Optional[Files]:
        return session.query(Files).filter(
            Files.file_id == file_id,
            Files.user_id == user_id
        ).first()
    
    @staticmethod
    def delete_file(session: Session, file_id: int, user_id: int) -> bool:
        file_record = CRUDOperations.get_file_by_id(session, file_id, user_id)
        if file_record:
            session.delete(file_record)
            session.commit()
            return True
        return False
    
    @staticmethod
    def create_user(session: Session, username: str, email: str, hashed_password: str) -> User:
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_active=True
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
    @staticmethod
    def get_user_by_username(session: Session, username: str) -> Optional[User]:
        return session.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        return session.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
        return session.query(User).filter(User.id == user_id).first()

crud_operations: CRUDOperations = CRUDOperations()