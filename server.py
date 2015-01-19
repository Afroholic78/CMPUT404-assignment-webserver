# coding: utf-8
import SocketServer
import os.path


# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Mickael Zerihoun, Glenn Meyer
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        #Check for a GET request, if it is received break it down into the path and the HTTP
        if self.data.split(" ")[0] == "GET":
            path = self.data.split(" ")[1]
            path = "www" + path
            http = self.data.split(" ")[2]
            http = http.splitlines()[0]
            self.get(path, http)

    def get(self,path,http):
        #If an http/1.1 is received, proceed with the rest of the program, otherwise drop it
        if http == "HTTP/1.1":
            req_path = os.path.abspath(path)
            flag = req_path.find(os.getcwd())
            if flag > -1:
                try:
                    #If / is given, redirect to index.html
                    if path[-1] == "/":
                        path = path + "index.html"
                    #Fetch the extension
                    extension = path.split(".")[-1]
                    f = open(path, 'r')
                    #Construct the content before sending it back, at this point it must be a 200 OK
                    content = "HTTP/1.1 200 OK" + "\r\n" + "Content-Type: text/" + extension + "\r\n\r\n" + f.read()
                    self.request.sendall(content)
                except IOError:
                    #Construct the 404 content since if it reaches this point then we haven't found the file
                    self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n" + "404 Error :( No page here buddy")
            else:
                #Unsecure access attempted, send back 404 error
                self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n" + "404 Error :( No page here buddy")
        else:
            self.request.sendall("HTTP/1.1 501 Not Implemented\r\n\r\n" + "501 Not implemented")



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
