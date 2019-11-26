import xmlrpc.client
import sys
naming_proxy = xmlrpc.client.ServerProxy("http://localhost:5000/", allow_none = True)
import proxy
#
# naming_proxy = proxy.TupleSpaceAdapter("http://localhost:5000/")

v = str("alice_ts")
name = naming_proxy.getURI(v)


blog = proxy.TupleSpaceAdapter(name)

alice_tuples = ["alice_ts","gtcn","This graph theory stuff is not easy"]

def operations_for_Alice():
    print(blog._out(alice_tuples))

if __name__ == '__main__':
    operations_for_Alice()
