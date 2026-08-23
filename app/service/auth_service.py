from config.auth_utils import TokenData, generate_token, verify_password, verify_token
from config.settings import TIME_EXPIRE_REFRESH_TOKEN
from repositories.user_repo import UserRepo
from schemas.user_schema import Login, UserRead,Register
from fastapi import HTTPException, Response,status
from fastapi.concurrency import run_in_threadpool
class AuthService:
    
    async def login(self,login_data:Login,user_repo:UserRepo,response:Response):
        try:
            exists_user = await user_repo.get_by_email(login_data.email)
            if exists_user is None:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail=f"This email {login_data.email} is not exists")
            
            if exists_user.deleted_at is not None:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"This email {login_data.email} is deleted")

            check_password = await run_in_threadpool(verify_password,login_data.password,exists_user.password_hash)
            if not check_password:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"This password is not correct")

            access_token = generate_token(TokenData(user_id=exists_user.id,role=exists_user.role))    
            refresh_token = generate_token(TokenData(user_id=exists_user.id,role=exists_user.role),refresh_token=True)   
            import json 
            response.set_cookie("refresh_token",
                                 refresh_token,
                                 max_age=TIME_EXPIRE_REFRESH_TOKEN,
                                 httponly=True, 
                                 secure=True, 
                                 samesite="lax") 


            return {"user":UserRead.model_validate(exists_user,from_attributes=True),"access_token":access_token}                     

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

    async def register(self,register_data:Register,user_repo:UserRepo,response:Response):
        try:
            exists_user = await user_repo.get_by_email(register_data.email)
            if exists_user is not None:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail=f"This email {register_data.email} is exists")

            user = await user_repo.create(register_data)
            if not user:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail=f"empty")


            access_token = generate_token(TokenData(user_id=user.id,role=user.role))    
            refresh_token = generate_token(TokenData(user_id=user.id,role=user.role),refresh_token=True)   
            import json 
            response.set_cookie("refresh_token",
                                 refresh_token,
                                 max_age=TIME_EXPIRE_REFRESH_TOKEN,
                                 httponly=True, 
                                 secure=True, 
                                 samesite="lax") 


            return {"user":UserRead.model_validate(user,from_attributes=True),"access_token":access_token}                     

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

    def refresh_access_token(self, refresh_token: str):
        try:
            payload = verify_token(refresh_token)
            access_token = generate_token(payload)
            return {"access_token": access_token}
            
        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))                       

    def logout(self,response:Response):
        try:
            response.delete_cookie("refresh_token")
            return {"message":"Logout successfully"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
                               