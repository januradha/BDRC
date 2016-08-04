#!/usr/bin/python
# print "Content-Type: text/html; charset=utf-8\n"
import bdrcshared.demense as demense
import questionnaire
import brand
import model
import cgitb
import common_controls as cctrls
import division

import common
from common import full_month_names as month_names
import reportcheck


class ReportOrder(reportcheck.ReportCheck):
    def setup(self,**kwargs):
        self.name = 'reportorder.py'
        self.first_time = 'first' in self.parts

    def edit_form(self,errors): 
        return ''

    def validate(self,):
#        self.year = cctrls.numeric(self,"year")
        self.month = cctrls.numeric(self,"month",min=1,max=self.maxmonth,default=self.maxmonth)
        self.brand = reportcheck.brand_control(self,"brand_id", default=brand.Brand(self.d,225))
        self.demense = reportcheck.demense_control(self,"demense",default=demense.Demense(self.d,1))
        self.division_id = self.validate_division()

        self.brand_score_obj = model.Own_Brand_Demense_scores
        self.division_score_obj = model.Division_scores
        self.demense_score_obj = model.Demense_scores

        self.division_arr = self._get_divisions(self.division_id)
        self.all_divisions = self._get_divisions()
        self.demense_list = None
        return {}

    #--------------
    def write_form(self,):
        '''Display sanity report'''

        score = model.Scores(d=self.d)
        self.year, self.maxmonth = score.latest_period()
        errors =  self.validate()
        self.lastyear, self.lastmonth = score.previous_period(year=self.year,month=self.month.value)

        page_title = u'Slide Report Order'
#        if self.ven.venue_id is not None:
#            page_title += u'<br>%s' % self.ven.venue_name

        body = self._show_selection()
        if errors or self.first_time:
            body = body + self.edit_form(errors)

        cgi = '%s/%s' % (self.name,self.me.user_id)

        o = common.rtvTemplate('reportcheck.html')
        o = o.replace(u'!BREADCRUMB!', self.titlebar())
        o = o.replace(u'!BODY!', body)
        o = o.replace(u'!TITLE!', page_title)
        o = o.replace(u'$BRAND_ERROR_CLASS', '')

        common.stdOutput(o, me=self.me)

    #--------------
    def _show_selection(self,):
        x = [u'<form method="post" action="!CGIPATH!{0}">'.format(self.name),
            u'{0}: <SELECT name="month" class="text-input">'.format(self.year)]

        for m in range(0,self.maxmonth):
            if m+1 == self.month.value :
                dflt = u' selected="selected"'
            else:
                dflt = ''
            x.append(u'<OPTION value="{0}"{1}>{2}</OPTION>\n'.format(m+1,dflt,month_names[m]))
        x.append(u'</SELECT>')
        
        x.append(u' Brand: ')
        x.append(self.brand.get_controls())
        x.append(u' Demense: ')
        x.append(self.demense.get_controls())
        x.append(u' Division: ')
        x.extend(self.get_division_controls())
        # x.append(u'<INPUT type="submit" value="GO">')
        submitbutton = u'<a href="!CGIPATH!gen_pptx_report.py" id="hrefdata" style="text-decoration:none;"><input type="button" onclick="generatepptx(this.form,%s);" value="Generate PPTX"></a>' % (self.year)
        x.append(submitbutton)
        x.append(u'</br></br>')
        title_description = [ ('International Comparison', 'At a glance view of overall regional scores and international top performers','Slide2.jpg'),
                              ('International Summary', 'Regional and Divisional scores by type of enquiry for the month of report and calendar YTD','Slide3.jpg'),
                              ('International Summary of Changes since last month', 'Regional and Divisional score changes (from previous month) by type of enquiry for the single-month and YTD scores','Slide4.jpg'),
                              ('C&E Summary of Performance', 'An overview of the region/division\'s performance in C&E enquiry handling','Slide5.jpg'),
                              ('C&E Focus Hotels', 'Highlights those hotels whose scores are below the international target performance','Slide6.jpg'),
                              ('C&E Recent Headline Performance Trends', 'A view of score progression for overall performance as well as by-channel breakdowns','Slide7.jpg'),
                              ('Improvement', 'Change in scores, from previous month, on key questions from the assessment','Slide8.jpg'),
                              ('Competitive Comparison', 'Difference in your performance from BDRC\'s average on key questions from the assessment','Slide9.jpg'),
                              ('Competitor League Table', 'A league table of competitors tracked in the region.  (Based on comparable enquiry types and channels only)','Slide10.jpg'),
                              ('Hotel League', 'League table of the region/division\'s individual properties','Slide11.jpg'),
                            ]
        o = common.rtvTemplate('slide_order.html')
        li_item = common.rtvTemplate('slide_list.html')

        li_content = ''
        for loop,(title,description,image) in enumerate(title_description):
            li_content = li_content + \
                         li_item.replace('!SLIDEX!','slide' + str(loop+1)) \
                                .replace('!TITLETEXT!',title) \
                                .replace('!DESCRIPTION!',description) \
                                .replace('!IMAGE!',image)

        o = o.replace('!LIST!',li_content)
        x.append(o)
        x.append(u'</form>\n')
        script = '''
        function generatepptx(frmobj,year){
            var month = frmobj["month"].value;
            var brand_id = frmobj["brand_id"].value;
            var demense = frmobj["demense"].value;
            var division = frmobj["division"].value;
            var selectBox =  document.getElementById('sortable');
            var items =  selectBox.getElementsByTagName('LI');
            var selected_index =  []

            for(i=0; i<items.length; i++) {
                checkboxId = items[i].id.split("_")[0]
                if (frmobj[checkboxId].checked) {
                    selectedvalue  = checkboxId.split("slide")[1]
                    selected_index.push(parseInt(selectedvalue)); 
                }
            }
            var parameters = '?year=' + year + '&month=' + month + '&brand_id=' + brand_id + '&demense_id=' + demense + '&division_id=' + division + '&selected_index=' + selected_index;
            hrefvalue = document.getElementById("hrefdata").getAttribute("href");
            hrefvalue = hrefvalue.split("?")[0];
            document.getElementById("hrefdata").href = hrefvalue + parameters;
        };

        '''
        x.append('<script>')
        x.append(script)
        x.append('</script>')
        script = '''

        <meta charset="utf-8">
        <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
        <script src="//code.jquery.com/jquery-1.10.2.js"></script>
        <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
        <link rel="stylesheet" type="text/css" href="!DOCPATH!css/dg-picture-zoom.css">
        <script type="text/javascript" src="!DOCPATH!js/external/mootools-1.2.4-core-yc.js"></script>
        <script type="text/javascript" src="!DOCPATH!js/external/mootools-more.js"></script>
        <script type="text/javascript" src="!DOCPATH!js/dg-picture-zoom.js"></script>
        <script type="text/javascript" src="!DOCPATH!js/dg-picture-zoom-autoload.js"></script>
        <style>
            #nonsortable {
                list-style-type: none;
                margin: 0;
                padding: 0;
                width: 100%;
            }
            #nonsortable li {
                margin: 0 3px 3px 3px;
                padding: 0.4em;
                padding-left: 1.5em;
                font-size: 1.4em;
                height: 30px;
            }
            #nonsortable li span {
                position: absolute;
                margin-left: -1.3em; 
            }
            #sortable {
                list-style-type: none;
                margin: 0;
                padding: 0;
                width: 100%;
            }
            #sortable li {
                margin: 0 3px 3px 3px;
                padding: 0.4em;
                padding-left: 1.5em;
                font-size: 1.4em;
                height: 40px;
            }
            #sortable li span {
                position: absolute;
                margin-left: -1.3em; 
            }
            .titletext {
                font-size: 16px;
                font-weight: bold;
                left:140px;
            }
            .description {
                left:135px;
                margin-top: 7px;
            }
        </style>
        <script>
            $(function() {
                $( "#sortable" ).sortable();
                $( "#sortable" ).disableSelection();
            });
        </script>

        '''
        x.append(script)
        return ''.join(x)

def main():
    page = ReportOrder()
    page.write_form()

if __name__ == '__main__':
    cgitb.enable()
    main()

