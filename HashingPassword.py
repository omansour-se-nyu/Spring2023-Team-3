import bcrypt
  
password = input("Enter password: ")

# converting password to array of bytes
bytes = password.encode('utf-8')

#gen salt
salt = bcrypt.gensalt()
  
# Hashing the password
result = bcrypt.hashpw(bytes, salt)

'''
    # Taking user entered password 
    userPassword =  'password000'
  
    # encoding user password
    userBytes = userPassword.encode('utf-8')
  
    # checking password in db against user
    result = bcrypt.checkpw(userBytes, hash)  
'''
  
print(result)


