#!/usr/bin/python

import sys
import optparse
import Cobalt
import Cobalt.Util
from Cobalt.Proxy import ComponentProxy


if __name__ == '__main__':

    try:
        system = Cobalt.Proxy.ComponentProxy("system", defer=False)
    except:
        print >> sys.stderr, "failed to connect to system component"
        sys.exit(1)

    status = system.get_node_status()
    queue_data = system.get_queue_assignments()

    header = [['Host', 'Queue', 'State']]
    #build output list
    output = []
    for t in status:
        host_name = t[0]
        status = t[1]
        queues = []
        for q in queue_data:
            if host_name in queue_data[q]:
                queues.append(q) 
        output.append([host_name, ":".join(queues), status])
        
    Cobalt.Util.printTabular(header + output)
