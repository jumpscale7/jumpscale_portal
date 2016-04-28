import re
import urllib
import cgi

def main(j, args, params, tags, tasklet):
    page = args.page
    doc = args.doc
    page.addCSS('/jslib/old/breadcrumbs/breadcrumbs.css')

    data = "<ul class='breadcrumb'>%s</ul>"
    breadcrumbs = []
    space = j.core.portal.active.getSpace(doc.getSpaceName())
    if 'breadcrumbdata' in args.requestContext.params:
        for breadcrumb in args.requestContext.params['breadcrumbdata'][::-1]:
            for name, link in breadcrumb.iteritems():
                breadcrumbs.insert(0, (link, name, {}))
    else:
        breadcrumbs.append((doc.original_name, cgi.escape(doc.title), {}))
        while doc.parent:
            doc = space.docprocessor.name2doc.get(doc.parent)
            if not doc:
                break
            args = {}
            for arg in doc.requiredargs:
                if arg in doc.appliedparams:
                    args[arg] = doc.appliedparams[arg]
            breadcrumbs.insert(0, (doc.original_name, cgi.escape(doc.title), args))

    innerdata = ""
    breadcrumbs.insert(0, ('/%s' % space.model.id, space.model.name, {}))
    for link, title, args in breadcrumbs[:-1]:
        if args:
            link = "%s?%s" % (link, urllib.urlencode(args))
        innerdata += "<li><a href='%s'>%s</a><span style='opacity: 0.5; margin-right: 8px; margin-left: 2px;' class='icon-chevron-right'></span></li>" % (link, title)
    innerdata += "<li class='active'>%s</li>" % breadcrumbs[-1][1]

    page.addMessage(data % innerdata)
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
