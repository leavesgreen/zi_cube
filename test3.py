# -*- coding: utf-8 -*-
import socket ,hashlib
 
def handle_request ( client):  
  buf = client . recv( 1024 ) 
  print buf 
  client .send ( "HTTP/1.1 200 OK\r\n\r\n" ) 
  client .send ( "Hello, World" ) 
 
def main ():  
   sock = socket . socket( socket .AF_INET , socket .SOCK_STREAM ) 
   sock .bind (( 'localhost' ,8080 )) 
   sock .listen ( 5)  
  
   while True : 
     connection , address = sock .accept ()  
     handle_request ( connection ) 
     connection . close()  
  

def main2():
    s1 = "useid"
    UPDATE ZZ_PROTECT_WORDS set WordId =  CONCAT(MD5(WordId),LENGTH(WordId));
    
    print hashlib.md5(s1).hexdigest()+str(len(s1)) == "7f7e9fcc2cdd3eef17abf778c8da2d2712"


if __name__ == '__main__' : 
   main2 ()  
