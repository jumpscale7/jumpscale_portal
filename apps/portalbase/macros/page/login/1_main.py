
def main(j, args, params, tags, tasklet):

    page = args.page
    page.addCSS("/jslib/bootstrap/css/bootstrap-3-3-1.min.css")
    page.addCSS("/jslib/old/bootstrap/css/bootstrap-responsive.css")
    page.addCSS("/jslib/flatui/css/flat-ui.css")
    page.addCSS(cssContent='''
      body{
        background-color: #1abc9c !important;
      }
      .login-form:before{
        border-width: 0;
      }
      .login-screen{
        padding: 0;
      }
      h4{
        color: #fff;
        text-align: center;
      }
      .span12{
        margin-top: 14%;
      }
      .login-field{
        height: 40px !important;
      }
    ''')
    head = """
<title>Login</title>
	"""

    body = """
    <form id="loginform" class="form-signin" method="post" action="/$$path$$querystr">
       <div class="col-sm-offset-3 col-md-6 login-screen">
        <div class="login-form">
          <div class="form-group">
            <input type="text" class="form-control login-field" value="" name="user_login_" placeholder="Enter your username" id="login-name">
            <label class="login-field-icon fui-user" for="login-name"></label>
          </div>

          <div class="form-group">
            <input type="password" class="form-control login-field" value="" name="passwd" placeholder="Password" id="login-pass">
            <label class="login-field-icon fui-lock" for="login-pass"></label>
          </div>

          <button class="btn btn-primary btn-lg btn-block" type="submit">Sign in</button>
        </div>
      </div>
    </form>
	"""
    if args.tags.tagExists("jumptopath"):
        jumpto = args.tags.tagGet("jumptopath")
    else:
        jumpto = args.requestContext.path
        if jumpto.find("wiki") == 0:
            jumpto = jumpto[5:].strip("/")

    querystr = args.requestContext.env['QUERY_STRING']

    session = args.requestContext.env['beaker.session']
    session["querystr"] = querystr
    session.save()

    # if jumpto=="$$path":
        # path unknown
        # jumpto=""

    page.addBootstrap()
    page.addHTMLHeader(head)
    page.body += body
    page.body = page.body.replace("$$path", jumpto)
    if querystr:
        querystr = "?%s" % querystr
    page.body = page.body.replace("$$querystr", querystr)

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
