from fastapi import FastAPI, Depends, Header,HTTPException

app = FastAPI()

#Auth Example
def verify_token(token: str = Header(None)):
    if token != "My_Secret_Token":
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    return{
        "user":"Authorized User"
    }

@app.get("/secure_data")
def secure_data(user = Depends(verify_token)):
    return {
        "message":"Secure data Accessed",
        "user":user
    }




#  Depends basic
# def common_logic():
#     return {
#         "message":"Common Logic executed"
#     }



#Reusable Code
# @app.get("/home")
# def home(data = Depends(common_logic)):
#     return data

# def get_current_user():
#    return{
#     "user":"Sherry"
#    }

# @app.get("/profile")
# def profile(user = Depends(get_current_user)):
#     return user

# @app.get("/dashboard")
# def dashboard(user = Depends(get_current_user)):
#     return user