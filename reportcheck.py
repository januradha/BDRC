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


##Questionniare Ids 14
##Meetinds
M_TELEPHONE=140 #85
M_OVERALL =144 #84
M_OVERALL_INC_QUICKCHECK =170
M_QUICKCHECK =174
M_ELECTRONIC=143 # 83
M_EMAIL = 141 # 86
M_RFP =  142 # 87

G_TELEPHONE = 145 #88
E_TELEPHONE = 156 #89
B_TELEPHONE = 155 #90
def fmt(val, decimal_places=1):
    ''' format number to one decimal place'''
    if val is None:
        return '-'
#    elif val == 0:
#        return '-'
    elif val == 100:
        return '100'
    else :
        return round(val,decimal_places)

class ReportCheck(common.ScreenBase):
    def setup(self,**kwargs):
        self.name = 'reportcheck.py'
        self.first_time = 'first' in self.parts




    def edit_form(self,errors): 
        return ''

    def validate(self,):
#        self.year = cctrls.numeric(self,"year")
        self.month = cctrls.numeric(self,"month",min=1,max=self.maxmonth,default=self.maxmonth)
        self.brand = brand_control(self,"brand_id", default=brand.Brand(self.d,225))
        self.demense = demense_control(self,"demense",default=demense.Demense(self.d,1))
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
        if errors or self.first_time:
            body = self.edit_form(errors)
        else:
            body= self._show_output()

        page_title = u'Report Checker'
#        if self.ven.venue_id is not None:
#            page_title += u'<br>%s' % self.ven.venue_name

        body = self._show_selection() + body
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
        x.append(u'<INPUT type="submit" value="GO">')
        submitbutton = u'<a href="!CGIPATH!gen_pptx_report.py" id="hrefdata" style="text-decoration:none;"><input type="button" onclick="generatepptx(this.form,%s);" value="Generate PPTX"></a>' % (self.year)
        x.append(submitbutton)
        x.append(u'</form>\n')
        script = '''
        function generatepptx(frmobj,year){
            var month = frmobj["month"].value;
            var brand_id = frmobj["brand_id"].value;
            var demense = frmobj["demense"].value;
            var division = frmobj["division"].value;
            var parameters = '?year=' + year + '&month=' + month + '&brand_id=' + brand_id + '&demense_id=' + demense + '&division_id=' + division;
            hrefvalue = document.getElementById("hrefdata").getAttribute("href");
            hrefvalue = hrefvalue.split("?")[0];
            document.getElementById("hrefdata").href = hrefvalue + parameters;
        };

        '''
        x.append('<script>')
        x.append(script)
        x.append('</script>')

        return ''.join(x)

    def validate_division(self,):
        value = self.get_form_value("division",factory=int,default=0)
        return value

    def get_division_controls(self,):
        div_data = self.all_divisions    # get full list

        if self.division_id == 0 :
            dflt = u' selected="selected"'
        else:
            dflt = ''

        x = [u'<SELECT name="division" class="text-input" id="division">',
            u'<OPTION value="0"%s>-- All --</OPTION>\n'%(dflt)]
#        c = 0
#        for did in colt:
        for did,absdid,name,obj in div_data:
            if did == self.division_id :
                dflt = u' selected="selected"'
            else:
                dflt = ''
            x.append(u'<OPTION value="{0}"{1}>{2}</OPTION>\n'.format(did,dflt,name))
#            c += 1
        x.append('</SELECT>')
        return x


    #---------------
    def _show_output(self,):
        x = []
        x.append(u"<div class='block'>Top Hotels Worldwide</div>")
        x.append(self._top_hotels(header=str(common.short_month_names[self.month.value-1])+' '+str(self.year),questionnaire_id=M_OVERALL,score_type='1',year=self.year,month=self.month.value,result_id=19000, id_type=0,brand_id=self.brand.value.brand_id,answer_value='!'))
        x.append(self._top_hotels(header='YTD '+str(self.year),questionnaire_id=M_OVERALL,score_type='Y',year=self.year,month=self.month.value,result_id=19000, id_type=0,brand_id=self.brand.value.brand_id,answer_value='!'))
        x.append(u'<div style="clear:both;"></div>')
        x.append(self.rep_summary())
        x.append(self.ce_summary())
        x.append(self.ce_focus())
        x.append(self.ce_trends())
        x.append(self.improvement())
        x.append(self.comparison())
        x.append(self.competitor_league())
        x.append(self.league())

        return ''.join(x)


    def ce_summary(self,):
        scores = self.brand_score_obj #model.Own_Brand_Demense_scores
        did = self.demense.value.demense_id
        name=''
        if self.division_id != 0:
            junk,did,name,scores = self.division_arr[0]
            name = ' for '+name

        x = []
        x.append(u"<div class='block'>C&amp;E: Summary of Performance%s</div>"%(name))
        x.append(u"<div id='cesummary'>")
        data = []
        types = ['1','Y']
        for type in types:
            data.append(scores(dbConnection=self.d, f=self.f,
                    questionnaire_id=M_OVERALL_INC_QUICKCHECK,
                    year=self.year,
                    id=did,
                    month=self.month.value,
                    score_type=type, id_type=0, brand_id=self.brand.value.brand_id,
                    result_id=19000, answer_value='!', allow_override=True).score)

        if data[0] is None:
            data[0] = 0

        scorel = scores(dbConnection=self.d, f=self.f,      # last month's score
                    questionnaire_id=M_OVERALL_INC_QUICKCHECK,
                    year=self.lastyear,
                    id=did,
                    month=self.lastmonth,
                    score_type='1', id_type=0, brand_id=self.brand.value.brand_id,
                    result_id=19000, answer_value='!', allow_override=True).score
        if scorel is None:
            scorel = 0

        x.append(u'<div style="float:left">')
        x.append(u"""<table border="1"><caption>Overall {0}</caption>
                    <tr><td>Score</td><td>Change since {1}</td><td>YTD</td></tr>
                    <tr><td id='cesummarysc'>{2}</td><td id='cesummarych'>{3}</td><td id='cesummaryytd'>{4}</td></tr>
                    </table>""".format(self.demense,
                month_names[self.month.value-1],
                fmt(data[0]), fmt(data[0]-scorel), fmt(data[1])))
#                    </table>""".format(demense.Demense(self.d, self.demense.value.demense_id),
        x.append(u'</div>')

        data = []
        types = ['1','Y']
        for type in types:
            data.append(scores(dbConnection=self.d, f=self.f,
                    questionnaire_id=M_OVERALL,
                    year=self.year,
                    id=did,
                    month=self.month.value,
                    score_type=type, id_type=0, brand_id=self.brand.value.brand_id,
                    result_id=19000, answer_value='!', allow_override=True).score)

        if data[0] is None:
            data[0] = 0

        scorel = scores(dbConnection=self.d, f=self.f,      # last month's score
                    questionnaire_id=M_OVERALL,
                    year=self.lastyear,
                    id=did,
                    month=self.lastmonth,
                    score_type='1', id_type=0, brand_id=self.brand.value.brand_id,
                    result_id=19000, answer_value='!', allow_override=True).score
        if scorel is None:
            scorel = 0

        x.append(u'<div style="float:left">')
        x.append(u"""<table border="1"><caption>Excl. Quick Check score for {0}</caption>
                    <tr><td>Score</td><td>Change since {1}</td><td>YTD</td></tr>
                    <tr><td id='cesummaryxsc'>{2}</td><td id='cesummaryxch'>{3}</td><td id='cesummaryxytd'>{4}</td></tr>
                    </table>""".format(self.demense,
                month_names[self.month.value-1],
                fmt(data[0]), fmt(data[0]-scorel), fmt(data[1])))
#                    </table>""".format(demense.Demense(self.d, self.demense.value.demense_id),
        x.append(u'</div>')
        
        qids = [(M_TELEPHONE,u'Telephone','tel'),(M_QUICKCHECK,u'Quick Check','quickcheck'),(M_EMAIL,u'Email','email'),(M_RFP,u'Web/RFP','rfp')]
        x.append(u'<div style="float:left">')
        x.append(u'<table border="1"><caption> Channel breakdown</caption>')
        x.append(u'<tr>')
        for qid in qids:
            x.append(u'<td>{0}</td>'.format(qid[1]))
        x.append(u'</tr><tr>')
        for qid in qids:
            val = scores(dbConnection=self.d, f=self.f,
                    questionnaire_id=qid[0],
                    year=self.year,
                    id=did,
                    month=self.month.value,
                    score_type='1', id_type=0, brand_id=self.brand.value.brand_id,
                    result_id=19000, answer_value='!', allow_override=True).score

            x.append(u'<td id="cesummary{0}">{1}</td>'.format(qid[2],fmt(val)))
        x.append(u'</tr></table></div>')


        rids = [(19025,u'Selling skills','sellskill'),
                (19026,u'Customer Ease','custease'),
                (19021,u'Connection','connection'),
                (19022,u'Service Delivery','delivery'),
                (19023,u'Manner &amp; Approach','manner'),
                (19024,u'Follow up','follow')]
        x.append(u'<div style="float:left">')
        x.append(u'<table border="1"><caption>Telephone: Sectional breakdown</caption>')
        x.append(u'<tr>')
        for rid in rids:
            x.append(u'<td>{0}</td>'.format(rid[1]))
        x.append(u'</tr><tr>')

        for rid in rids:
            val = scores(dbConnection=self.d, f=self.f,
                questionnaire_id=M_TELEPHONE,
                year=self.year,
                id=did,
                month=self.month.value,
                score_type='1', id_type=0, brand_id=self.brand.value.brand_id,
                result_id=rid[0], answer_value='!', allow_override=True).score
            x.append(u'<td id="cesummary{0}">{1}</td>'.format(rid[2],fmt(val)))
        x.append(u'</tr></table></div>')

        x.append(u'<div style="clear:both;"></div>')
        x.append(u"</div>")
        return ''.join(x)

    def ce_trends(self,):
        import barchart_base

        info = [(M_OVERALL_INC_QUICKCHECK,19000,u"Overall Performance *","overall"),
                (M_TELEPHONE,19025,u"Selling Skills","sellskill"),
                (M_TELEPHONE,19026,u"Customer Ease","custease"),
                (M_TELEPHONE,19000,u"Telephone *","tel"),
                (M_ELECTRONIC,19000,u"Electronic","elec")]

        bb = barchart_base.Barchart_base(d=self.d,f=self.f)
        labels = bb.set_bar_labels()

        did = self.demense.value.demense_id
        name=''
        score_o = self.brand_score_obj
        if self.division_id != 0:
            junk,did,name,score_o = self.division_arr[0]
            name = ' for '+name

        x = [u"<div class='block'>C&amp;E: Recent Headline Performance Trends%s</div>"%(name)]
        x.append(u'<div id="trends">')

        for inf in info:
            x.append(u'<div id="trend{0}" style="float:left">'.format(inf[3]))

            scores = score_o(dbConnection=self.d, f=self.f, questionnaire_id=inf[0],
                score_type='3', id_type=0, brand_id=self.brand.value.brand_id, id= did,
                result_id=inf[1], answer_value='!',
                set_mode=True,allow_override=True )
            natscores = self.demense_score_obj(dbConnection=self.d, f=self.f, questionnaire_id=inf[0],
                score_type='3', id_type=0, brand_id=self.brand.value.brand_id, id= self.demense.value.demense_id,
                result_id=inf[1], answer_value='!',
                set_mode=True,allow_override=True )
            brand_data, responses_data = bb.rtv_aggregate_scores(scores=scores, rounding_dp=1)
            nat_data, responses_data = bb.rtv_aggregate_scores(scores=natscores, rounding_dp=1)
            x.append(u'<table border="1"><caption>{0}</caption>'.format(inf[2]))
            x.append(u'<tr><th></th>')
            for lab in labels:
                x.append(u'<th>{0}</th>'.format(lab.replace('\n',u'<br/>')))
            x.append(u'</tr>')

            rows = [(u'Value','v',brand_data),
                    (u'Avg','a',nat_data)]
            for row in rows:
                x.append(u'<tr><td>{0}</td>'.format(row[0]))
                count = 0
                for d in row[2]:
                    if d == barchart_base.NoValue:
                        d = None
                    x.append(u'<td id="trend{3}{1}-{2}">{0}</td>'.format(fmt(d),inf[3],count,row[1]))
                    count += 1
                x.append(u'</tr>')

            x.append(u'</table></div>')

        x.append(u'</div>')
        x.append(u'<div style="clear:both;"></div>')
        return ''.join(x)


    # create a dict of venue_id:rankings for the given demense grouping
    def _ytd_ranking(self,demense_group_id):
        vs = model.VenueScores(dbConnection=self.d, f=self.f,set_mode=True,
            questionnaire_id=M_OVERALL_INC_QUICKCHECK,
            result_id=19000,score_type='Y',
            id_type=0,brand_id=self.brand.value.brand_id,answer_value='!'
            )

        #
        # We recompute ranking here absed on the top-N scores (eg sorted scores)
        # and searching. The *may* be different from what is in VenueClusterRanks,
        # but if so we've got a problem anyway!
        #
        topg = vs.top_N_venue_in_brand(year=self.year, month=self.month.value, score_type='Y', limit=None 
                ,demense_id=demense_group_id,brand_id=self.brand.value.brand_id)
        rank = 1
        rankg = {}
        last = -1
        count = 0
        lastc = u''
        lastv = -1
        for ven in topg:
            count += 1
            if ven[2]==last:    # same score
                rankg[ven[0]] = lastc
                rankg[lastv] = lastc
            else:
                rankg[ven[0]] = u'{0}'.format(count)
                lastc = u'={0}'.format(count)
                lastv = ven[0]
                last = ven[2]
        return rankg

    def competitor_league(self,):
        x = []
        x.append(u'<div class="block">Brand League Table (Tele enq only not inc Quick Check)</div>')
        x.append(u'<div id="competitor_league">')
        brand_scores = self.brand_score_obj #model.Own_Brand_Demense_scores
        did = self.demense.value.demense_id
        data = []
        types = ['1','Y']

        allbrands = brand.Brand(self.d,None).get_all()
        f = self.d.cursor()     # obtain a new cursor
        rankw = self._ytd_ranking(1) # worldwide rankings

        x.append(u'<table border="1">')
        x.append(u'''<tr><th rowspan="2">{0} {1}</th>
                         <th colspan="2">Tele Overall Score</th>
                         <th>YTD Rank</th>
                         <th>Score: Last 3 Months</th>
                    </tr>
                    <tr>
                         <th>Last Month</th>
                         <th>&nbsp;YTD&nbsp;</th>
                         <th>Worldwide</th>
                         <th>Overall Tele</th>
                    </tr>'''.
                    format(month_names[self.month.value-1],self.year))
        scores = model.VenueScores(dbConnection=self.d, f=self.f, 
                id_type=0,
                answer_value='!',
                set_mode=True,allow_override=True )
        count = 0
        branddata = {}
        for brand_id, brand_name, logo_id, independent, exclude_from_main_study in allbrands:
            branddata[str(brand_id) + '_' + brand_name] = brand_scores(dbConnection=self.d, f=self.f,
                    questionnaire_id=M_TELEPHONE,
                    year=self.year,
                    id=did,
                    month=self.month.value,
                    score_type='Y',
                    id_type=0, 
                    brand_id=brand_id,
                    result_id=19000,
                    answer_value='!',
                    allow_override=True).score
        branddata = sorted(branddata.items(), key=lambda x: x[1],reverse=True)

        for item in branddata:
            b_value = item[0].split('_')
            brand_id = int(b_value[0])
            brand_name = b_value[1]
            score = item[1]
            x.append(u'<tr>')
            x.append(u'<td id="leaguename{1}">{0}</td>'.format(brand_name,brand_id))   # name
            x.append(u'<td id="leaguelastmonth{1}">{0}</td>'.format( 
                    fmt(brand_scores(dbConnection=self.d, f=self.f,
                    questionnaire_id=M_TELEPHONE,
                    year=self.year,
                    id=did,
                    month=self.lastmonth,
                    score_type='1',
                    id_type=0, 
                    brand_id=brand_id,
                    result_id=19000,
                    answer_value='!',
                    allow_override=True).score),
                    count))       # last month
            x.append(u'<td id="leagueytd{1}">{0}</td>'.format( 
                    fmt(score),
                    count))       # last month   # ytd
            x.append(u'<td id="leaguewrank{1}">{0}</td>'.format( 
                    fmt(model.VenueScores(
                    dbConnection=self.d, f=self.f,
                    questionnaire_id=M_TELEPHONE,
                    year=self.year,
                    id=did,
                    month=self.month.value,
                    score_type='Y',
                    id_type=0,
                    brand_id=brand_id,
                    result_id=19000, 
                    answer_value='!',
                    allow_override=True
                    ).score),
                    count)) # 3 month tel
            x.append(u'<td id="league3tel{1}">{0}</td>'.format(
                    fmt(brand_scores(dbConnection=self.d, f=self.f,
                    questionnaire_id=M_TELEPHONE,
                    year=self.year,
                    id=did,
                    month=self.month.value,
                    score_type='C',
                    id_type=0, 
                    brand_id=brand_id,
                    result_id=19000,
                    answer_value='!',
                    allow_override=True).score),
                    count)) # 3 month tel
            x.append(u'</tr>')
            count += 1
        x.append(u'</table>')
        x.append(u'</div>')
        return ''.join(x)

    def league(self,):
        from operator import itemgetter
        name=''
        if self.division_id != 0:
            junk,junk,name,junk = self.division_arr[0]
            name = ' for '+name
        x = []
        x.append(u'<div class="block">{0} Hotel League{1}</div>'.format(self.demense,name))
        x.append(u'<div id="league">')
        vs = model.VenueScores(dbConnection=self.d, f=self.f,set_mode=True,
            questionnaire_id=M_OVERALL_INC_QUICKCHECK,
            result_id=19000, 
            id_type=0,brand_id=self.brand.value.brand_id,answer_value='!'
            )
        tp = vs.top_N_venue_in_brand(year=self.lastyear, month=self.lastmonth, score_type='1', limit=None ,
            demense_id=self.demense.value.demense_id,brand_id=self.brand.value.brand_id,
            omit_secret = True, omit_private = True, omit_normal = False
        )
        top = sorted(tp,key=lambda item: (-item[3],item[1].lower()),reverse=False)
        f = self.d.cursor()     # obtain a new cursor
        regions = [(2,u'EMEA'),(4,u'Asia-Pacific'),(1208,u'EMEA'),(1220,u'APAC')]   # old & new regions for hilton
        sql = "select max(s) from bdrcshared.demense_closure where s in(%s) and d="%(','.join([str(r[0]) for r in regions])) + "%s"
        f.execute(sql,self.demense.value.demense_id)
        group = None
        groupn = u'Unknown'
        for row in f.fetchall():
            group = row[0]
            for reg in regions:
                if group == reg[0]:
                    groupn = reg[1]
        if group:
            rankg = self._ytd_ranking(group) # EMEA/APAC rankings
        rankw = self._ytd_ranking(1) # worldwide rankings

        x.append(u'<table border="1">')
        x.append(u'''<tr><th rowspan="2">{0} {1}</th><th colspan="2">Overall Score Including Quick Check</th><th colspan="2">YTD Rank</th><th colspan="3">Score: Last 3 Months</th></tr>
                    <tr><th>Last Month</th><th>&nbsp;YTD&nbsp;</th><th>In {2}</th><th>Worldwide</th><th>Tel*</th><th>Electronic</th><th>Quick Check</th></tr>'''.
                    format(month_names[self.month.value-1],self.year, groupn))
        scores = model.VenueScores(dbConnection=self.d, f=self.f, 
                id_type=0,
                answer_value='!',
                set_mode=True,allow_override=True )
        count = 0
        for item in top:
            if self._exclude_venue_by_division(item[0]):
                continue
            x.append(u'<tr>')
            x.append(u'<td id="leaguename{1}">{0}</td>'.format(item[1],item[0]))   # name
            x.append(u'<td id="leaguelastmonth{1}">{0}</td>'.format( 
                    fmt(item[3]),count))       # last month
            x.append(u'<td id="leagueytd{1}">{0}</td>'.format(fmt(model.VenueScores(
                    dbConnection=self.d, f=self.f,
                    questionnaire_id=M_OVERALL_INC_QUICKCHECK,
                    year=self.year,
                    id=item[0],
                    month=self.month.value,
                    score_type='Y', id_type=0,
                    result_id=19000, 
                    answer_value='!',
                    allow_override=True
                    ).score),count))   # ytd

            if group and item[0] in rankg:
                grank = rankg[item[0]]
            else:
                grank = u'-'
            x.append(u'<td id="leaguegrank{1}">{0}</td>'.format( grank, count)) # EMEA/APAC ranking

            if item[0] in rankw:
                wrank = rankw[item[0]]
            else:
                wrank = u'-'
            x.append(u'<td id="leaguewrank{1}">{0}</td>'.format( wrank,count)) # World ranking
            x.append(u'<td id="league3tel{1}">{0}</td>'.format(
                    fmt(model.VenueScores(
                    dbConnection=self.d, f=self.f,
                    questionnaire_id=M_TELEPHONE,
                    year=self.year,
                    id=item[0],
                    month=self.month.value,
                    score_type='3', id_type=0,
                    result_id=19000, 
                    answer_value='!',
                    allow_override=True
                    ).score),
                    count)) # 3 month tel
            x.append(u'<td id="league3elec{1}">{0}</td>'.format(
                    fmt(model.VenueScores(
                    dbConnection=self.d, f=self.f,
                    questionnaire_id=M_ELECTRONIC,
                    year=self.year,
                    id=item[0],
                    month=self.month.value,
                    score_type='3', id_type=0,
                    result_id=19000, 
                    answer_value='!',
                    allow_override=True
                    ).score),
                    count)) # 3 month electronic
            x.append(u'<td id="league3quickcheck{1}">{0}</td>'.format(
                    fmt(model.VenueScores(
                    dbConnection=self.d, f=self.f,
                    questionnaire_id=M_QUICKCHECK,
                    year=self.year,
                    id=item[0],
                    month=self.month.value,
                    score_type='3', id_type=0,
                    result_id=19000, 
                    answer_value='!',
                    allow_override=True
                    ).score),
                    count)) # 3 month electronic
            x.append(u'</tr>')
            count += 1
        x.append(u'</table>')
        x.append(u'</div>')
        return ''.join(x)


    def ce_focus(self,):
        name=''
        if self.division_id != 0:
            junk,junk,name,junk = self.division_arr[0]
            name = ' for '+name
        x = []
        x.append(u'<div class="block">C&amp;E: Focus Hotels, {0} {1}{2}</div>'.format(month_names[self.month.value-1],self.year,name))
        x.append(u'<div id="cefocus">')
        vs = model.VenueScores(dbConnection=self.d, f=self.f,set_mode=True,
            questionnaire_id=M_OVERALL_INC_QUICKCHECK,
            result_id=19000, 
            id_type=0,brand_id=self.brand.value.brand_id,answer_value='!'
            )
        top = vs.top_N_venue_in_brand(year=self.year, month=self.month.value, score_type='1', limit=None 
        ,demense_id=self.demense.value.demense_id,brand_id=self.brand.value.brand_id
        )

        spilt50 = []
        split80 = []
        addn = [M_TELEPHONE, M_ELECTRONIC, M_QUICKCHECK] # we get Overall score from top_N_venue_in brand; tag on Tel & Elec scores
        for ven in top:
            if self._exclude_venue_by_division(ven[0]):
                continue
            if ven[2] > 80: # ignore anyone with >80% score
                continue
            val = []
            for n in addn:
                val.append(model.VenueScores(
                    dbConnection=self.d, f=self.f,
                    questionnaire_id=n,
                    year=self.year,
                    id=ven[0],
                    month=self.month.value,
                    score_type='1', id_type=0,
                    result_id=19000, 
                    answer_value='!',
                    allow_override=True
                    ).score)
            if ven[2] >= 50: # split out the >50%
                spilt50.append((ven[0],ven[1],ven[2],val[0],val[1],val[2]))
            else: # split out the 50%-80%
                split80.append((ven[0],ven[1],ven[2],val[0],val[1],val[2]))

        x.append(self._focus_output(u'Between 50&#37; and 80&#37;',spilt50,50))
        x.append(self._focus_output(u'Less than 50&#37;',split80,80))

        x.append(u'</div>')
        x.append(u'<div style="clear:both;"></div>')
        return ''.join(x)

    def _focus_output(self,title,data,split):
        x = []
        x.append(u'<div style="float:left"><table border="1" id="cefocus{0}">'.format(split))
        x.append(u'<tr><th>{0}</th><th>C&amp;E<br/>Overall *</th><th>C&amp;E Tel</th><th>C&amp;E Elec</th><th>C&amp;E<br/>Quick Check</th></tr>'.format(title))
        for row in data:
            x.append(u'''
<tr>
<td id="cefocusid{0}">{1}</td>
<td id="cefocuso{0}">{2}</td>
<td id="cefocuse{0}">{3}</td>
<td id="cefocust{0}">{4}</td>
<td id="cefocust{0}">{5}</td>
</tr>'''.format(row[0],row[1],fmt(row[2]),fmt(row[3]),fmt(row[4]),fmt(row[5])))
        x.append(u'</table></div>')
        return ''.join(x)

    # calculate data block for comparison and improvement
    def _comp_data(self,scores,year,month,did):
        data = [(M_TELEPHONE,15604,u'Make package seem attractive',u'p',u'Selling Skills',12),
                (M_TELEPHONE,15166,u'Provide Unique venue decision',u'q',None,0),
                (M_TELEPHONE,15605,u'Mentioned seasonal offers/loyalty programme',u'r',None,0),
                (M_TELEPHONE,15608,u'Suggested relevant upgrades',u's',None,0),
                (M_TELEPHONE,15170,u'Proposed provisional booking',u't',None,0),
                (M_TELEPHONE,15401,u'Asked if could help with future business requirements',u'u',None,0),
                (M_TELEPHONE,15754,u'Product Knowledge',u'v',None,0),
                (M_TELEPHONE,15756,u'Interest in enquiry',u'w',None,0),
                (M_TELEPHONE,15758,u'Handling of your special request',u'x',None,0),
                (M_TELEPHONE,15250,u'Follow up calls within 3 days',u'y',None,0),
                (M_TELEPHONE,15753,u'Friendliness',u'y',None,0),
                (M_TELEPHONE,15757,u'Closing of cal',u'y',None,0), 
                (M_TELEPHONE,15191,u'Number of calls to complete enquiry',u'a',u'Customer Ease',8),
                (M_TELEPHONE,15751,u'Helpfulness',u'f',None,0),
                (M_TELEPHONE,15752,u'Clarity of explanation',u'g',None,0),
                (M_TELEPHONE,15755,u'Caller gave enough time',u'h',None,0),
                (M_TELEPHONE,15200,u'Speed of delivery:Email',u'h',None,0),
                (M_TELEPHONE,15390,u'Information received in appropriate format',u'j',None,0),
                (M_TELEPHONE,15122,u'Correct sign off',u'i',None,0),
                (M_TELEPHONE,15247,u'Reference to special request',u'k',None,0)]

        out = []
        for inf in data:
            if not inf[1]: # hack to deal with where we don't yet know the question number
                out.append((inf[2],inf[3],inf[4],inf[5],u'-',u'-'))
                continue
            row = []
            for stype in ('1','Y'):
                s = scores(dbConnection=self.d, f=self.f, questionnaire_id=inf[0],year=year, month=month,
                    score_type=stype, id_type=0, brand_id=self.brand.value.brand_id, id= did,
                    result_id=inf[1], answer_value='1',
                    allow_override=True )
                row.append(
                    s.score)
            out.append((inf[2],inf[3],inf[4],inf[5],row[0],row[1]))
        return out

    def improvement(self,): 
        scores = self.brand_score_obj #model.Own_Brand_Demense_scores
        did = self.demense.value.demense_id
        name = ''
        if self.division_id != 0:
            junk,did,name,scores = self.division_arr[0]
            name = ' for '+name
        data1 = self._comp_data(scores,self.year, self.month.value,did)
        data2 = self._comp_data(scores,self.lastyear, self.lastmonth,did)
        return self._outp_impr(
                u'Improvement, {0} {1} to {2} {3}{4}'.format(month_names[self.lastmonth-1], self.lastyear,month_names[self.month.value-1],self.year,name),
                u'{0} {1} vs {2} {3}'.format(month_names[self.lastmonth-1], self.lastyear,month_names[self.month.value-1],self.year),
                u'Change in<br/>Single Month<br>Scores',
                u'Change in<br/>YTD<br/>Scores',
                u'improvement',
                data1,data2)

    def comparison(self,):
        scores1 = self.brand_score_obj # model.Own_Brand_Demense_scores
        scores2 = self.demense_score_obj # model.Demense_scores
        did = self.demense.value.demense_id
        name=''
        if self.division_id != 0:
            junk,did,name,scores1 = self.division_arr[0]
            name = ' for '+name
        data1 = self._comp_data(scores1,self.year, self.month.value,did)
        data2 = self._comp_data(scores2,self.year, self.month.value,did)
        return self._outp_impr(
                u'Competitive Comparison, {0} {1}{2}'.format(month_names[self.month.value-1],self.year,name),
                u'{0} vs {1} Average'.format(self.brand,self.demense),
                u'Single Month<br>Scores',
                u'YTD<br/>Scores',
                u'comparison',
                data1,data2)


    def _outp_impr(self,caption,tcaption,h1,h2,did,data1,data2):
        data = []
        for i in range(0,len(data1)):
            row = list(data1[i])
            row.extend((u'-',u'-'))
            if row[4] != u'-': # hack to deal with where we don't yet know the question number
                for x in (4,5):
                    row[x+2] = u'{0}-{1}'.format(data1[i][x] , data2[i][x]) # keep the calc in a hidden cell
                    if data1[i][x] is None or data2[i][x] is None:
                        if data1[i][x] is None:
                            if data2[i][x] is None:
                                row[x] = u'??'   # show when we have no numbers to calc
                            else:
                                row[x] = u'?-'   # show when we have no numbers to calc
                        else:
                            row[x] = u'-?'   # show when we have no numbers to calc
                    else:
                        row[x] =  u'{0}'.format(fmt(data1[i][x] - data2[i][x]))  # calculated cell
            data.append(row)

        x = []
        x.append(u'<div class="block">{0}</div>'.format(caption))
        x.append(u'<div id="{0}">'.format(did))
        x.append(u'<table border="1"><caption>{0}</caption><tr><th></th><th></th><th>{1}</th><th>{2}</th></tr>'.format(tcaption,h1,h2))
        for row in data:
            x.append(u'<tr>')
            if row[3]:
                x.append(u'<td rowspan="{0}">{1}</td>'.format(row[3],row[2]))
            x.append(u'<td>{0}</td><td id="{3}1{4}">{1}</td><td id="{3}y{4}">{2}</td>'.format(row[0],row[4],row[5],did,row[1]))
            x.append(u'<td id="{2}c1{3}" style="display:none">{0}</td><td id="{2}cy{3}" style="display:none">{1}</td>'.format(row[6],row[7],did,row[1]))
            x.append(u'</tr>')
        x.append(u'</table></div>')
        return ''.join(x)

    #--------------
    def titlebar(self,):
        x = [u'Report Checker',]
        return ' &nbsp;->&nbsp;&nbsp; '.join(x)

    def _top_hotels(self,**kwargs):
        vs = model.VenueScores(dbConnection=self.d, f=self.f,set_mode=True,**kwargs)

        top = vs.top_N_venue_in_brand(**kwargs)

        header = kwargs.get('header','no header')
        stype = kwargs.get('score_type',None)
        x = [u'<div class="block" id="top{0}" style="float:left">'.format(stype)]
        x.append(u"<table border='1'>")
        x.append(u'<tr><th>{0}</th><th>score</th></tr>'.format(header))
        count = 1
        for row in top:
            val = fmt(row[2])
#            if val == 100:  # force "100.0" -> "100"
#                val = int(val)
            x.append(u'''<tr id="top{0}row{1}">
                    <td id="top{0}name{1}">{2}</td>
                    <td id="top{0}val{1}">{3}</td>
                    <td id="top{0}vid{1}" style="display:none">{4}</td>
                    <td id="top{0}xsort{1}" style="display:none">{5}</td>
                    </tr>\n'''.format(stype,count,row[1],val,row[0],row[3]))
            count += 1

        x.append(u"</table>")
        x.append(u"</div>")
        return ''.join(x)

    def _exclude_venue_by_division(self,venue_id):
        ''' filter venues according to division selected'''
        import venue

        if self.division_id==0: # no division selected
            return False
        did,adid,name,obj = self.division_arr[0]
        v = venue.Venue(self.d,venue_id)
        if did<0:   # divisions
            if self.demense_list is None:
                self.demense_list = demense.Demense(self.d,division.Division(self.d,adid).demense_id).get_child_ids(recurse=True)

        else:       # demenses
            if self.demense_list is None:
                self.demense_list=demense.Demense(self.d,adid).get_child_ids(recurse=True)
        return v.demense_id not in self.demense_list

    def _get_divisions(self,selected=0):
        EXCLUDE_DIVISIONS = [16,18] # exclude "Hilton Worldwide - Europe Top 22" & "Hilton Worldwide - MEA Top 10"
        divs = [-19,-21,-22,-10,-26,-24,1200,1196,-34,-30,-32,-28,1210,1224,1226,1230,1232] # -ve are divisions, +ve are demenses
        div_data = []
        B = self.brand_score_obj
        D = self.division_score_obj
        for did in divs:
            if (not selected == 0) and (not did == selected):
                continue
            if did in EXCLUDE_DIVISIONS:
                continue

            if did < 0:
                name = division.Division(self.d,-did).division_name
                obj = D
            else:
                name = demense.Demense(self.d,did).demense_name
                obj = B
            div_data.append((did,abs(did),name,obj,))
        return div_data

    def rep_summary(self,**kwargs):
        scores = self.brand_score_obj #model.Own_Brand_Demense_scores
        scoret = self.division_score_obj #model.Division_scores
        rows = [M_OVERALL_INC_QUICKCHECK,M_OVERALL,M_QUICKCHECK,M_TELEPHONE,M_EMAIL,M_RFP,E_TELEPHONE,G_TELEPHONE,B_TELEPHONE]
        adjrows = [common.ovr_result_id(x,0,self.year)[0] for x in rows]    # adjust rows for previous years

        div_data = self.all_divisions    # get all divisions

        data = []
        data.append(self._get_summary_data( rows, div_data, self.year,self.month.value, '1', 0, self.brand.value.brand_id, 19000, '!'))
        data.append(self._get_summary_data( rows, div_data, self.year,self.month.value, 'Y', 0, self.brand.value.brand_id, 19000, '!'))

        x = [u"<div class='block'>International: {0} {1} Summary</div>".format(month_names[self.month.value-1],self.year)]
        x.extend(self._output_summary_data(self.year, self.month.value, "summary", adjrows, div_data, self.brand.value.brand_id, ['1','Y'], data))

        delta = []
        delta.append(self._calc_changes(data[0],self._get_summary_data( rows, div_data, self.lastyear,self.lastmonth, '1', 0, self.brand.value.brand_id, 19000, '!')))
        delta.append(self._calc_changes(data[1],self._get_summary_data( rows, div_data, self.lastyear,self.lastmonth, 'Y', 0, self.brand.value.brand_id, 19000, '!')))

        x.append(u"<div class='block'>International: Changes since last month</div>".format(month_names[self.month.value-1],self.year))
        x.extend(self._output_summary_data( self.year, self.month.value, "changes", adjrows, div_data, self.brand.value.brand_id, ['1','Y'], delta))

        return u''.join(x)

    # return an x by y array of differences between 2 x by y arrays (r =array1-array2)
    def _calc_changes(self, array1, array2):
        ret = [[0 for x in range(len(array1[0]))] for x in range(len(array1)) ]
        for row in range(len(array1)):
            for col in range(len(array1[0])):
                ret[row][col] = array1[row][col] - array2[row][col]
        return ret
        

        
#    def _output_summary_data(self, dbConnection, year, month, tag_id, rows, cols, brand_id, types, values, bnames):
    def _output_summary_data(self, year, month, tag_id, rows, col_data, brand_id, types, values):
        x = [u'<div class="block" id="{0}">'.format(tag_id)]
        x.append(u"<table border='1'>")
        x.append(u'<tr><th>{0} {1}</th>'.format(month_names[month-1],year))
        c = 0
        for col in col_data:
            x.append(u'<th>{0}</th>'.format(col[2]))
        x.append(u'</tr>')
        for block in range(len(types)):
            for row in range(len(rows)):
                x.append(u'<tr><td id="{0}{1}q{2}">{3}</td>'.format( tag_id, types[block],
                    rows[row],
                    questionnaire.Questionnaires(self,quest=rows[row],brand_id=brand_id).user_desc))
                for col in range(len(col_data)):
                    x.append(u'<td id="{0}{1}q{2}d{3}">{4}</td>'.format(tag_id, types[block], rows[row],col_data[col][0], fmt(values[block][row][col])))
                x.append(u'</tr>')
            if(block == 0):
                x.append(u'<tr><td>YTD {1}</td><td colspan="{0}"></td></tr>'.format(len(col_data),year))
        x.append(u"</table>")
        x.append(u"</div>")
        return x



    def _get_summary_data(self, questionnaire_rows, id_cols, year, month, score_type, id_type, brand_id, result_id, answer_value):
        scores = self.brand_score_obj #model.Own_Brand_Demense_scores
        scoret = self.division_score_obj #model.Division_scores
        dbConnection = self.d
        cursor = self.f
        ret = [[0 for x in range(len(id_cols))] for x in range(len(questionnaire_rows)) ]
        rcount = 0
        for row in questionnaire_rows:
            ccount = 0
            for col,abs_col,name,score_obj in id_cols:
                args = {    'dbConnection':self.d,
                            'f':self.f,
                            'questionnaire_id':row,
                            'year':year,
                            'id': abs_col,  # -col for brand,col for 
                            'month':month,
                            'score_type':score_type,
                            'id_type':id_type,
                            'brand_id':brand_id,
                            'result_id':result_id,
                            'answer_value':answer_value,
                            'allow_override':True
                }
                score = score_obj(**args).score
                if score != None:
                    ret[rcount][ccount] = score
                else:
                    ret[rcount][ccount] = 0
                ccount += 1
            rcount += 1
        return ret

def main():
    page = ReportCheck()
    page.write_form()





def _brand_factory(newid):
    if isinstance(newid,brand.Brand):
        _set_db(newid.d)
        return newid

    d = _get_db()
    return brand.Brand(d,newid)

class brand_control(object):
    def __init__(self,form,name,default = None):
        self.name = name

        self.value = form.get_form_value(name,default=default,factory=_brand_factory)

        self.text = str(self.value.brand_id)

    def __unicode__(self,):
        return self.value.brand_name or u""

    def get_controls(self,**kwargs):
        return self.value.dropdown(name= self.name,current_brand_id=self.value.brand_id,**kwargs)


class demense_control(demense.demense_area_control):
    """Dropdown list of nations"""
    @classmethod
    def keyfn(cls):
        return ( a[0] for a in demense.Demense(cls._get_db(),None).get_all() )
    pre_order = [ (None,False), (11,True) ]

if __name__ == '__main__':
    cgitb.enable()
    main()
#    try:
#        main()
#    except Exception, e:
#        import traceback,sys
#        sys.stderr.write('\n'.join(traceback.format_tb(sys.exc_info()[2])))
#        common.dm(str(e.__class__).split(".")[-1]+":"+str(e))
