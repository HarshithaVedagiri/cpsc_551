# Distributed System Blog application 

The goal of this project is to design and develop a scalable distributed system blog application (replication of twitter) using tuplespace and heterogeneous .


## Distributed Nodes 
There are 2 nodes in the network, one act as client (written in python) and one act as server, which is a tuple space in the network (written in Ruby).

- In version 1.0 of this project, we implemented the adapter pattern in RUBY, which is internally connected to the RInda tuple space.

- This architecture can also be implemented in python tuplespace, While our concerns are:
  - The PyLinda package is not not the same as the pylinda package available on PyPI.
  - PyLinda was written for Python 2.
  - The available code for PyLinda is missing some source files.
  - The original author of the code seems to have disappeared from the Internet.

- Fortunately Ruby, another common scripting language, includes a module named Rinda which implements the Linda distributed computing paradigm.

## How to run the project:
 Install the dependencies by the following command 
 
 ```
 $ gem install --user-install xmlrpc
 
 ```
 Start the Rinda TupleSpace 
 
 ```
 ruby tuplespace.rb
 
 ```

 Start the adapter.rb file 
 
 ```
 ruby adapter.rb
 
 ```

 if you're running the blog application in a single file, then run 
 
 ```
 python blog.py
 
 ```
 if you're running the arithmetic operations
 
 ```
 1. python arithmetic_client.py
 2. python arithmetic_server.py
 ```
 
# The Project Team
## Team Members
- Shekhar Palit
- Aditya Dingre
- Saket Gonte
## Project Technologies
- Programming Language - Python, Ruby 
- Storage_Server - RInda TupleSpace
- RPC modules - XMLRPC(Ruby server, Python Client)
