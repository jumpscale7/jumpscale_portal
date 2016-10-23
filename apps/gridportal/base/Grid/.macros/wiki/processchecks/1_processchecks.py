import JumpScale.grid.gridhealthchecker
import JumpScale.baselib.redis
import itertools

def main(j, args, params, tags, tasklet):
    doc = args.doc
    out = list()

    data = j.core.grid.healthchecker.fetchMonitoringOnAllNodes()
    errors, oldestdate = j.core.grid.healthchecker.getErrorsAndCheckTime(data)
    out.append('Grid was last checked at: {{ts:%s}}' % oldestdate)
    out.append('||Grid ID||Node ID||Node Name||Node Status||Details||')
    rows = list()

    if len(data) > 0:
        for nid, checks in data.iteritems():
            level = 0
            if nid in errors:
                level = -1
                categories = errors.get(nid, [])
                flatchecks = itertools.chain(*checks.values())
                state = j.core.grid.healthchecker.getNodeDataState(flatchecks)
                text = "(issues in %s)" % ', '.join(categories)
                runningstring = j.core.grid.healthchecker.getWikiStatus(state, text)
            else:
                level = 0
                runningstring = '{color:green}*RUNNING*{color}'
            gid = j.core.grid.healthchecker.getGID(nid)
            link = '[Details|nodestatus?nid=%s&gid=%s]' % (nid, gid) 
            row = {'level': level, 'gid': gid, 'nid': nid}
            row['message'] = '|%s|[%s|grid node?id=%s&gid=%s]|%s|%s|%s|' % (gid, nid, nid, gid, j.core.grid.healthchecker.getName(nid), runningstring, link)
            rows.append(row)

    def sorter(row1, row2):
        for sortkey in ('level', 'gid', 'nid'):
            if row1[sortkey] != row2[sortkey] or sortkey == 'nid':
                return cmp(row1[sortkey], row2[sortkey] )

    out.extend([x['message'] for x in sorted(rows, cmp=sorter)])
    params.result = ('\n'.join(out), doc)
    return params

def match(j, args, params, tags, tasklet):
    return True
