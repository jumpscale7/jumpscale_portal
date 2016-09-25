from JumpScale import j
import re
import json

class GridDataTables:

    def __init__(self, page, online=False):
        self.page = page
        self._tableids = set()
        self.liblocation = "/jslib"

        self.page.addJS("%s/old/datatables/datatables.min.js" % self.liblocation, header=False)
        self.page.addCSS("%s/old/datatables/datatables.min.css" % self.liblocation)
        self.page.addBootstrap()
        self.page.addTimeStamp()

    def makeTime(self, row, field):
        if row[field] == 0:
            return ''
        return '<div class="jstimestamp" data-ts="%s"></div>' % row[field]

    def makeTimeOnly(self, row, field):
        if row[field] == 0:
            return ''
        return '<div class="jstimestamp" data-ts="%s" data-timeonly="true"></div>' % row[field]

    def addTableForModel(self, namespace, category, fieldids, fieldnames=None, fieldvalues=None, filters=None, nativequery=None, selectable=False):
        """
        @param namespace: namespace of the model
        @param cateogry: cateogry of the model
        @param fieldids: list of str pointing to the fields of the dataset
        @param fieldnames: list of str showed in the table header if ommited fieldids will be used
        @param fieldvalues: list of items resprenting the value of the data can be a callback
        """
        key = j.apps.system.contentmanager.extensions.datatables.storInCache(fieldids=fieldids, fieldname=fieldnames, fieldvalues=fieldvalues, filters=filters, nativequery=nativequery)
        url = "/restmachine/system/contentmanager/modelobjectlist?namespace=%s&category=%s&key=%s" % (namespace, category, key)
        if not fieldnames:
            fieldnames = fieldids
        tableid = 'table_%s_%s' % (namespace, category)
        return self.addTableFromURL(url, fieldnames, tableid, selectable)

    def addTableFromData(self, data, fieldnames):
        import random
        tableid = 'table%s' % random.randint(0, 1000)

        C = """
$(document).ready(function() {
    $('#$tableid').dataTable( {
        "sDom": "<'row'<'col-md-6'l><'col-md-6'f>r>t<'row'<'col-md-6'i><'col-md-6'p>>",
        "bServerSide": false,
        "bDestroy": true,
        "sPaginationType": "bootstrap",
        "render" : {
            "_": "plain",
            "filter": "filter",
            "display": "display"
        },
        "data": %s
    } );
    $.extend( $.fn.dataTableExt.oStdClasses, {
        "sWrapper": "dataTables_wrapper form-inline"
    } );
} );""" % json.dumps(data)
        C = C.replace("$tableid", tableid)
        self.page.addJS(jsContent=C, header=False)

#<table cellpadding="0" cellspacing="0" border="0" class="display" id="example">
# <table class="table table-striped table-bordered" id="example" border="0" cellpadding="0" cellspacing="0" width="100%">

        C = """
<div id="dynamic">
<table class="table table-striped table-bordered" id="$tableid" border="0" cellpadding="0" cellspacing="0" width="100%">
    <thead>
        <tr>
$fields
        </tr>
    </thead>
    <tbody>
    <tbody>
    </tbody>
</table>
</div>"""

        fieldstext = ""
        for name in fieldnames:
            classname = re.sub('[^\w]', '', name)
            fieldstext += "<th class='datatables-row-%s'>%s</th>\n" % (classname,name)
        C = C.replace("$fields", fieldstext)
        C = C.replace("$tableid", tableid)

        self.page.addMessage(C, isElement=True, newline=True)
        return tableid

    def addTableFromURL(self, url, fieldnames, tableid=None, selectable=False):
        import random
        tableid = tableid or 'table'
        basename = tableid
        counter = 1
        while tableid in self._tableids:
            tableid = "%s_%" % counter
            counter += 1

        C = """
$(document).ready(function() {
    $('#$tableid').dataTable( {
        "sDom": "<'row'<'col-md-6'l><'col-md-6'f>r>t<'row'<'col-md-6'i><'col-md-6'p>>",
        "bServerSide": true,
        "bDestroy": true,
        "select": $selectable,
        "columnDefs": [{"targets": [0], "visible": false}],
        "sAjaxSource": "$url"
    } );
    $.extend( $.fn.dataTableExt.oStdClasses, {
        "sWrapper": "dataTables_wrapper form-inline"
    } );
} );"""
        C = C.replace("$url", url)
        C = C.replace("$tableid", tableid)
        C = C.replace("$selectable", json.dumps(selectable))
        self.page.addJS(jsContent=C, header=False)

#<table cellpadding="0" cellspacing="0" border="0" class="display" id="example">
# <table class="table table-striped table-bordered" id="example" border="0" cellpadding="0" cellspacing="0" width="100%">

        C = """
<div id="dynamic">
<table class="table table-striped table-bordered" id="$tableid" border="0" cellpadding="0" cellspacing="0" width="100%">
    <thead>
        <tr>
$fields
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan="5" class="dataTables_empty">Loading data from server</td>
        </tr>
    </tbody>
</table>
</div>"""

        fieldstext = ""
        fieldnames.insert(0, "id")
        for name in fieldnames:
            classname = re.sub('[^\w]', '', name)
            fieldstext += "<th class='datatables-row-%s'>%s</th>\n" % (classname,name)
        C = C.replace("$fields", fieldstext)
        C = C.replace("$tableid", tableid)

        self.page.addMessage(C, isElement=True, newline=True)
        return tableid

    def addSearchOptions(self, tableid=".dataTable"):
        self.page.addJS(jsContent='''
          $(function() {
              $('%s').each(function() {
                  var table = $(this);
                  var numOfColumns = table.find('th').length;
                  var tfoot = $('<tfoot />');
                  for (var i = 0; i < numOfColumns; i++) {
                      var td = $('<td />');
                      td.append(
                          $('<input />', {type: 'text', 'class': 'datatables_filter'}).keyup(function() {
                              table.dataTable().fnFilter(this.value, tfoot.find('input').index(this));
                          })
                      );
                      tfoot.append(td);
                  }
                  if (table.find('tfoot').length == 0)
                    table.append(tfoot);
              });
            });''' % tableid
        , header=False)

    def addSorting(self, tableid=".dataTable", columnindx=1, order='asc'):
        self.page.addJS(jsContent='''
            $(document).ready( function() {
              $('%s').dataTable().fnSort( [ [ %s, '%s' ] ] );
            } );''' % (tableid, columnindx, order)
        , header=False)

    def prepare4DataTables(self, autosort=True, displaylength=None):
        data = {"sDom": "<'row'<'col-md-6'l><'col-md-6'f>r>t<'row'<'col-md-6'i><'col-md-6'p>>",
                "bDestroy": True,
                "oLanguage": {
                        "sLengthMenu": "_MENU_ records per page"
                }
        }
        if not autosort:
            data['aaSorting'] = []
        if displaylength:
            data['iDisplayLength'] = displaylength
        C = """
         $(document).ready(function() {
         $('.JSdataTable').dataTable(%s);
} );
""" % json.dumps(data)
        self.page.addJS(jsContent=C, header=False)
        self.page.functionsAdded["datatables"] = True
        return self.page
