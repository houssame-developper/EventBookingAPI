from uuid import UUID

from fastapi import HTTPException, status

from repositories.user_repo import UserRepo
from schemas.user_schema import UserCreate, UserUpdate

class UserService:

    async def create_user(self,user_data:UserCreate,user_repo:UserRepo):
        try:

            exists_user = await user_repo.get_by_email(user_data.email)

            if exists_user is not None:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail=f"This email {user_data.email} is already exists")

            user = await user_repo.create(user_data)
            return user

        except HTTPException as e:
            raise e

        except Exception as e:

            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))    
        

    async def update_user(self,user_id:UUID,user_data:UserUpdate,user_repo:UserRepo):
        try:

            exists_user = await user_repo.get_by_id(user_id)

            if exists_user is None:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail=f"This id {str(user_id)} is not exists")
           
            exists_user = await user_repo.update(exists_user, user_data)

            return exists_user

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))    

    async def delete_user(self,user_id:UUID,user_repo:UserRepo):
        try:

            exists_user = await user_repo.get_by_id(user_id)


            if exists_user is None:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail=f"This id {str(user_id)} is not exists")

            
            await user_repo.delete(exists_user)
            return {"message":"user deleted successfully"}

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))    


    async def get_user(self,user_id:UUID,user_repo:UserRepo):
        try:

            exists_user = await user_repo.get_by_id(user_id)

            if exists_user is None:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail=f"This id {str(user_id)} is not exists")

            return exists_user

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

    async def get_list_user(
        self,
        user_repo: UserRepo,
        current_page: int = 1,
        page_size: int = 20,
    ):
        try:
            calculated_offset = (current_page - 1) * page_size
            return await user_repo.get_all_pagination(calculated_offset, page_size)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))