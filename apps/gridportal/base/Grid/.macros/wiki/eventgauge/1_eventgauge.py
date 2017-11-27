import datetime
import time

def main(j, args, params, tags, tasklet):
    doc = args.doc
    id = args.getTag('id')
    width = args.getTag('width')
    height = args.getTag('height')
    result = "{{jgauge width:%(width)s id:%(id)s height:%(height)s val:%(last24h)s start:0 end:%(total)s}}"
    cl = j.clients.osis.getByInstance('main')
    now = datetime.datetime.now()
    aweekago = j.base.time.getEpochAgo('-7d')
    ecl = j.clients.osis.getCategory(cl, 'system', 'eco')
    query = {'epoch': {'eq':'gte', 'value': aweekago, 'name': 'lasttime'}}
    total, firsteco = ecl.simpleSearch(query, size=1, withtotal=True)

    last24h = j.base.time.getEpochAgo('-1d')
    query = {'epoch': {'eq':'gte', 'value': last24h, 'name': 'lasttime'}}
    current, _ = ecl.simpleSearch(query, size=1, withtotal=True)
    average = total

    if firsteco:
        date = datetime.datetime.fromtimestamp(firsteco[0]['epoch'])
        delta = now - date
        if delta.days != 0:
            average = int(total / delta.days) * 2

    if average < current:
        average = current

    result = result % {'height': height,
                       'width': width,
                       'id': id,
                       'last24h': current,
                       'total': average}
    params.result = (result, doc)
    return params

def match(j, args, params, tags, tasklet):
    return True
