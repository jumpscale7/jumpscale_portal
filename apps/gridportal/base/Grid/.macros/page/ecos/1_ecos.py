def main(j, args, params, tags, tasklet):
    page = args.page
    modifier = j.html.getPageModifierGridDataTables(page)

    filters = dict()
    for tag, val in args.tags.tags.iteritems():
        val = args.getTag(tag)
        if tag == 'from' and val:
            filters['from_'] = {'name': 'lasttime', 'value': j.base.time.getEpochAgo(val), 'eq': 'gte'}
        elif tag == 'to' and val:
            filters['to'] = {'name': 'lasttime', 'value': j.base.time.getEpochAgo(val), 'eq': 'lte'}
        elif val:
            if j.basetype.integer.checkString(val):
                val = j.basetype.integer.fromString(val)
            filters[tag] = val

    def makeTime(row, field):
        time = modifier.makeTime(row, field)
        return '[%s|/grid/error condition?id=%s]' % (time, row['guid'])

    nidstr = '[%(nid)s|grid node?id=%(nid)s&gid=%(gid)s]'

    fields = [{'name': 'Last Occurrence',
               'id': 'lasttime',
               'value': makeTime,
               'type': 'date'},
              {'name': 'Error Message',
               'id': 'errormessage',
               'value': 'errormessage'},
              {'name': 'App name',
               'id': 'appname',
               'value': 'appname'},
              {'name': 'Occurrences',
               'id': 'occurrences',
               'type': 'int',
               'value': 'occurrences'},
              {'name': 'Node ID',
               'id': 'nid',
               'type': 'int',
               'value': nidstr},
              {'name': 'Grid ID',
               'id': 'gid',
               'value': 'gid',
               'type': 'int'},
              ]

    tableid = modifier.addTableFromModel('system', 'eco', fields, filters)
    modifier.addSearchOptions('#%s' % tableid)
    modifier.addSorting('#%s' % tableid, 1, 'desc')

    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True
