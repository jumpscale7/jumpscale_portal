import JumpScale.grid.gridhealthchecker
import JumpScale.baselib.redis
import ujson
import datetime
import time

def main(j, args, params, tags, tasklet):
    doc = args.doc
    
    out = list()
    rediscl = j.clients.redis.getByInstance('system', gevent=True)

    data = rediscl.hget('healthcheck:monitoring', 'results')
    errors = rediscl.hget('healthcheck:monitoring', 'errors')
    data = ujson.loads(data) if data else dict()
    errors = ujson.loads(errors) if errors else dict()


    if rediscl.hexists('healthcheck:monitoring', 'lastcheck'):
        lastchecked = j.basetype.float.fromString(rediscl.hget('healthcheck:monitoring', 'lastcheck'))
        lastchecked = '{{span: class=jstimestamp|data-ts=%s}}{{span}}' % lastchecked
    else:
        lastchecked = 'N/A'
    out.append('Grid was last checked at: %s.' % lastchecked)

    if errors:
        nodeids = errors.keys()
        nodenames = [j.core.grid.healthchecker.getName(nodeid) for nodeid in nodeids]
        out.append('{{html: <div><p class="alert alert-danger padding-vertical-none width-50"> Something on node(s) %s is not running.</p></div>}}' % ', '.join(nodenames))
    else:
        out.append('{{html: <div><p class="alert alert-success padding-vertical-none width-50">Everything seems to be OK.</p></div>}}')
    out.append('For more details, check [status overview.|/grid/Status Overview]')

    out = '\n'.join(out)

    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
