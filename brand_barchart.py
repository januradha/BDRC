#!/usr/bin/python
# -*- coding: utf-8 -*-



'''
AJAX return page details for brand report overall sections chart and table
'''

import cgi, sys
import db, common, user, gatekeeper
import barchart, brand, barchart_base
import demense
from brand_report_overall import delegate_rates, set_text, overall_set, no_percents, MA_duals, proprietary_results, proprietary_result
import model
from barchart_base import NoValue
import questionnaire
import brand_theme

#--------------
def rtv_unit_scores(result_id, answer_value, brand_id,  limit=11, worst=False):
    '''get the scores for the best (or worst) venue within this brand'''

    id_type = 0

    # 1 month scores to show an extra month
    if score_type == '1':
        limit += 1

    data = []
    responses = []
    
    vs = model.VenueScores(dbConnection=d, f=f )
    cs = model.Cluster_scores(dbConnection=d, f=f )

    year, month = bb.latest_period

    if year is None:
        return 'Scores are being updated, please try again in a few minutes'

    check_clusters = b.has_clusters()
    

  
    # retrieve the data working backwards for the required number of periods
    for x in range(0, limit):
        allow_override = common.result_override(year, month)
        vs.allow_override = allow_override

        # find the worse/best venue in the current period
        if worst:
            id = vs.worst_venue_in_brand(questionnaire_id=questionnaire_id, year=year,
              month=month, score_type=score_type, result_id=result_id, 
              answer_value=answer_value, brand_id=brand_id, demense_id=demense_id)
        else:
            id = vs.best_venue_in_brand(questionnaire_id=questionnaire_id, year=year,
              month=month, score_type=score_type, result_id=result_id, 
              answer_value=answer_value, brand_id=brand_id, demense_id=demense_id)

    
        # get the venue's score
        vs = model.VenueScores(dbConnection=d, f=f, questionnaire_id=questionnaire_id,
                        score_type=score_type, id_type=id_type, id=id,
                        result_id=result_id, answer_value=answer_value,
                        year=year, month=month, allow_override=allow_override)
        row = [vs.score, vs.occurences, vs.base]
        score = vs.score
  
        # if the brand has clusters, look for best/worst and use it if it's better/worse
        # than the existing venue 
        if check_clusters:
            # find the worse/best venue in the current period
            if worst:
                id = cs.worst_in_brand(questionnaire_id=questionnaire_id, year=year,
                        month=month, score_type=score_type, result_id=result_id, 
                        answer_value=answer_value, brand_id=brand_id , demense_id =demense_id )
            else:
                id = cs.best_in_brand(questionnaire_id=questionnaire_id, year=year,
                        month=month, score_type=score_type, result_id=result_id, 
                        answer_value=answer_value, brand_id=brand_id , demense_id =demense_id  )

            cs = model.Cluster_scores(dbConnection=d, f=f, questionnaire_id=questionnaire_id,
                        score_type=score_type, id_type=id_type, id=id,
                        result_id=result_id, answer_value=answer_value,
                        year=year, month=month)


            if worst:
                if vs.score is None:
                    row = [cs.score, cs.occurences, cs.base]
                if cs.score is not None and cs.score < score:
                    row = [cs.score, cs.occurences, cs.base]
            else:
                if vs.score is None:
                    row = [cs.score, cs.occurences, cs.base]
                if cs.score is not None and cs.score > score:
                    row = [cs.score, cs.occurences, cs.base]

        if row and row[0] is not None:

            score, occ, base = row
            score = round(score, rounding_dp)
            
            if score < -100:
                data.append(NoValue)
            else:
                data.append(score)
            responses.append(base)
        else:

            data.append(NoValue)
            responses.append(NoValue)


        month -= 1
        if month < 1:
            year -= 1
            month = 12

    # reverse the data so it's in the right order for the charts
    data.reverse()
    responses.reverse()
    
    return data, responses



#--------------
def do_chart_unit(title_prefix=''):
    
    id_type = 0

    year, month = bb.latest_period

    if year is None:
        return 'Scores are being updated, please try again in a few minutes'


    import barchart
    bc = barchart.Barchart(theme=bt.theme)

    # size chart area
    bc.width = 750
    bc.height = 500
    

    # set currency prefix of we dealing with delegate rates
    if currency_mode:
        bc.label_prefix = ''


    # switch off percentage postfix in bar labels?
    bc.no_percent = bool(result_id in no_percents)
    bc.rounding_dp = rounding_dp

    txt, answer_value = set_text.get(result_id, ('missing text', None))
    if not answer_value:
        answer_value = '!'

    brand_scores = model.Own_Brand_Demense_scores(dbConnection=d, f=f, questionnaire_id=questionnaire_id,
                score_type=score_type, id_type=id_type, brand_id=brand_id, id= dm.demense_id,
                result_id=result_id, answer_value=answer_value,
                set_mode=True, )
    brand_data, responses_data = bb.rtv_aggregate_scores(scores=brand_scores, rounding_dp=rounding_dp)

    # no national scores for proprietary questions
    if not proprietary_result(result_id, questionnaire_id=questionnaire_id):
        national_scores = model.Demense_scores(dbConnection=d, f=f, questionnaire_id=questionnaire_id,
                score_type=score_type, id_type=id_type, id=dm.demense_id,
                result_id=result_id, answer_value=answer_value,
                set_mode=True, )
        national_data, nat_responses = bb.rtv_aggregate_scores(scores=national_scores, rounding_dp=rounding_dp)

    if result_id in overall_set or currency_mode:
        best_data, best_responses = rtv_unit_scores(result_id, answer_value, brand_id, )
        weakest_data, weakest_responses = rtv_unit_scores(result_id, answer_value, brand_id, worst=True)

    bc.bar_labels = bb.set_bar_labels()
    bc.bar_colours = bb.set_bar_colours()
    bc.bar_data = brand_data

    if not proprietary_result(result_id, questionnaire_id=questionnaire_id):
        #Barchart isn't happy with Unicode data.
        if dm.demense_id:
            name =  str(dm.demense_name + u' Average')
            bc.line_data.append((national_data, name , 0, True))
    if result_id in overall_set:
        bc.line_data.append((best_data, 'Your Best Unit', 2, False))
        bc.line_data.append((weakest_data, 'Your Weakest Unit', 1, False))
    elif currency_mode:
        bc.line_data.append((best_data, 'Your Highest Rate', 2, False))
        bc.line_data.append((weakest_data, 'Your Lowest Rate', 1, False))


    imagedata = bc.make_barchart()
    
    print "Content-type: image/png\n"
    try: print imagedata
    except: pass



#--------------


score_type = '3'

if __name__ == '__main__':

    form = cgi.FieldStorage()

    parts = common.path_info_parts()

    try: questionnaire_id = int(parts[0])
    except: 
        try: questionnaire_id = int(form['questionnaire_id'].value.strip())
        except: questionnaire_id = questionnaire.default_qst

    if common.is_one_month(parts):
        score_type = '1'

    try: brand_id = int(form['b'].value.strip())
    except: brand_id = None

    try: result_id = int(form['r'].value.strip())
    except: result_id = None

    try: demense_id = int(form['d'].value.strip())
    except: demense_id = None

    try: yr = int(form['yr'].value.strip())
    except: yr = None

    try: mn = int(form['mn'].value.strip())
    except: mn = None

    d = db.connect()
    f = d.cursor()
    ses = user.UserSession(d, f)
    ses.validate_login()
    me = user.Users(d, ses.user_id, f=f)
  
    # ensure user has access to this screen before continuing
    gatekeeper.access_control(me)
    

    currency_mode = bool(result_id in delegate_rates)

    if currency_mode:
        rounding_dp = 2
    else:
        rounding_dp = 1

    b = brand.Brand(d, brand_id, f=f)

    bt =brand_theme.BrandTheme(d, me.guess_brand())

    dm = demense.Demense(d,demense_id)
    ud = model.User_demenses(d,me.user_id)

    # user must be associated with event via brand. If not, send 
    # them back to the report list, which'll present a list of 
    # brands available to them
    if demense_id in ud.demense_ids and b.check_brand(b.brand_id, me.user_id, me.groups):
        bb = barchart_base.Barchart_base(d=d, f=f, score_type=score_type, 
                questionnaire_id=questionnaire_id, theme=bt.theme, period=(yr,mn))

        do_chart_unit()
    else:
        o = 'Security Violation'
        common.stdOutput(o)


    d.close()
