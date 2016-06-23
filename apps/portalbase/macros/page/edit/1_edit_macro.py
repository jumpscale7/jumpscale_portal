
def main(j, args, params, tags, tasklet):

    import urlparse
    import urllib
    import re

    page = args.page
    page_match = re.search(r"page\s*:\s*([^:}]*)", args.macrostr)
    querystr = args.requestContext.env['QUERY_STRING']
    querytuples = urlparse.parse_qsl(querystr)
    args_dict = args.tags.getValues(app="", actor="", path="", bucket="", page="", space="", edit=False)
    spacename = ""
    for name, value in querytuples[:]:
        if name in ['space', 'page']:
            if not args_dict.get(name):
                args_dict[name] = value
        if name in ('edit_page', 'edit_space'):
            if name == 'edit_space':
                spacename = value
            querytuples.remove((name, value))

    querystr = urllib.urlencode(querytuples)

    page.addBootstrap()
    page_name = ''

    if page_match:
        page_name = page_match.group(1)

    if page_name == "" and args_dict["path"] == "":
        page.addMessage("ERROR: path needs to be defined")
        params.result = page
        return params

    if args_dict["app"] != "" and args_dict["actor"] != "":
        # look for path for bucket
        aloader = j.core.portal.active.actorsloader.getActorLoaderFromId("%s__%s" % (args_dict["app"].lower(), args_dict["actor"].lower()))
        path = j.system.fs.joinPaths(aloader.model.path, args_dict["path"])
    elif spacename != "":
        # look for path for bucket
        space = j.core.portal.active.getSpace(spacename)
        if page_name != "":
            space = j.core.portal.active.getSpace(spacename)
            doc = space.docprocessor.docGet(page_name.lower())
            path = doc.path
            args_dict["edit"] = True
        else:
            path = j.system.fs.joinPaths(space.model.path, args_dict["path"])
    elif args_dict["bucket"] != "":
        # look for path for bucket
        bucket = j.core.portal.active.getBucket(args_dict["bucket"])
        path = j.system.fs.joinPaths(bucket.model.path, args_dict["path"])
    else:
        page.addMessage("ERROR: could not find the requeted file")
        params.result = page
        return params
    if not j.system.fs.exists(path):
        page.addMessage('Supplied path "%s" does not exist.' % args_dict['path'])
        params.result = page
        return params
    content = j.system.fs.fileGetContents(path)

    page.addMessage('<div class="span12">')
    page.addCodeBlock(content, path=path, exitpage=False, edit=args_dict["edit"], spacename=spacename, pagename=page_name, querystr=querystr)
    page.addMessage('</div>')
    page.addMessage('<div class="span8" style="display: none !important"><iframe space="$space" doc="$doc" id="preview$id" src="/render" width="100%" height="600px"></iframe></div>'.replace('$id', str(page._codeblockid))
                    .replace('$space', spacename).replace('$doc', page_name))

    # This macro should be added _only once_ to a page
    page.addJS('/jslib/underscore/underscore.js')
    page.addJS(jsContent='''
    $(function() {
        var render = _.debounce(function() {
            var content = editor1.getValue();
            console.log('Changed');
            var space = $('#preview1').attr('space');
            var doc = $('#preview1').attr('doc');
            $('#preview1').attr('src', '/render?render_space=' + space + '&render_doc=' + doc + '&content=' + encodeURIComponent(content));
        }, 300);
        render();
        //editor1.on('change', render);

        var createPageLink = $('.dropdown-menu').find('li').first().find('a').attr('href');
        $('.dropdown-menu').find('li').first().find('a').attr('href', createPageLink + '&spaceBeforeEditPage=%s');
    });''' % spacename)


    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
