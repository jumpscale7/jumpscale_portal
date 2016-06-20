import os

def main(j, args, params, tags, tasklet):
    params.result = page = args.page

    spaceBeforeEditPage = args.paramsExtra.get('spaceBeforeEditPage')
    if spaceBeforeEditPage:
        page_space = args.paramsExtra.get('spaceBeforeEditPage')
    else:
        page_space = args.paramsExtra.get('page_space')

    page_name = args.paramsExtra.get('page_name')
    # Creating a new page
    page.addMessage('''<h2>Create a new page in '%s' space</h2>''' % j.html.escape(page_space) )
    if page_name and page_space:
        space = j.core.portal.active.getSpace(page_space)
        if not page_name:
            page.addMessage("ERROR: page name must be specified")
            return

        space = j.core.portal.active.getSpace(page_space)
        j.system.fs.createDir(os.path.join(space.model.path, page_name))
        j.system.fs.writeFile(os.path.join(space.model.path, page_name, page_name + '.wiki'), '')

        # Reload spaces to discover the new page
        # TODO: find an efficient way of doing this
        j.core.portal.active.loadSpaces()

        # Redirect to edit the new page
        page.addMessage("<script>window.open('/system/edit?edit_space={0}&edit_page={1}', '_self', '');</script>".format(page_space, page_name))
    elif page_name==None and page_space!=None:

        page.addMessage('''
            <form class="form-horizontal" method="get" action="/system/create">
                <fieldset>
                <div class="control-group">
                <input type="hidden" name="page_space" value="$$space">
                </div>
                <div class="control-group">
                  <label class="control-label" for="page_name">Name</label>
                  <div class="controls">
                    <input id="page" name="page_name" type="text" placeholder="" class="input-xlarge margin-bottom-large width-40" required="">
                  </div>
                </div>

                <div class="control-group">
                  <div class="controls">
                    <button class="btn btn-primary">Create</button>
                  </div>
                </div>

                </fieldset>
            </form>
            '''.replace("$$space",page_space))
    else:

        spaces = sorted(s for s in j.core.portal.active.getSpaces())
        spaces = ''.join('<option value="{0}">{0}</option>'.format(space) for space in spaces)
        page.addMessage('''
            <form class="form-horizontal" method="get" action="/system/create">
                <fieldset>
                <div class="control-group">
                  <label class="control-label" for="selectbasic">Select space...</label>
                  <div class="controls">
                    <select id="space" name="space" class="input-xlarge">
                      {0}
                    </select>
                  </div>
                </div>

                <div class="control-group">
                  <label class="control-label" for="name">Name</label>
                  <div class="controls">
                    <input id="page" name="page" type="text" placeholder="" class="input-xlarge margin-bottom-large width-40" required="">
                  </div>
                </div>

                <div class="control-group">
                  <div class="controls">
                    <button class="btn btn-primary">Create</button>
                  </div>
                </div>

                </fieldset>
            </form>
            '''.format(spaces))

    return params


def match(j, args, params, tags, tasklet):
    return True
