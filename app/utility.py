import bcrypt
def hashing_password(password:str)->str:
    TXT_To_Byte=password.encode('utf-8')
    return bcrypt.hashpw(TXT_To_Byte,bcrypt.gensalt()).decode('utf-8')
def verify_hashed_password(plainpassword:str,hashedpassword:str)->bool:
    return bcrypt.checkpw(plainpassword.encode('utf-8'),hashedpassword.encode('utf-8'))