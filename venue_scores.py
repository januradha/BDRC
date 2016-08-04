#!/usr/bin/python

# Generate venue scores!

import decimal as dec, sys
import db, calc_types, responses, question_reference, calc_control
import event_results
import venue
import model
from itertools import chain
import currency

try:
    from consolidation_control import *
except ImportError:
    rerun = False
    rerun_year = None
    rerun_month = None
    vs_questionnaires = tuple()
    rerun_venues = None

def convert_all_to_cur(this_cur,cur,period):
    total = 0
    for rated_currency,amt in cur.items():
        if rated_currency == this_cur.currency_code:
            #Don't convert if the currencies match, although
            # we fetch Identity conversions - we don't have historic
            # data form before we enable this feature this means, 
            # the conversion will fail - even though it could work.
            cvt_amt = amt
        else:
            cvt_amt = this_cur.convert(amt,rated_currency,period=period)
        if cvt_amt is None:
            import sys
            msg = "Cannot convert  %s -> %s\n"%(rated_currency,this_cur.currency_code)
            #sys.stderr.write(msg)
            raise ValueError(msg)
        else:
            total += cvt_amt

    return total

class Score:
    def __init__(self, dbConnection):

        if dbConnection:
            self.d = dbConnection
        else:
            import db
            self.d = db.connect()

        self.f = self.d.cursor()


        self.ct = calc_types.Calc_types()
        self.calc_ctl = calc_control.Calc_control(self.d,)
        self.q_ref = question_reference.Question_reference(self.d, None)
    
        self.r = responses.Responses(self.d, None, None, None, None, None, None)

        # setting this will force the responses table to be updated for the
        # current criteria
        self.run_responses = True

        self.periods = []

        # run time parameters
        self.adhoc = 'N'
        self.questionnaires = vs_questionnaires
        self.rerun = rerun
        self.rerun_start_year = rerun_year
        self.rerun_start_month = rerun_month
        self.rerun_last_period = rerun_last  # last period to include


        self.responses_done = False

    #--------------
    def calc_percentage(self, occ, base):
        '''return a percentage for the specified occurences and base'''

        # we force rounding to 5 d.p. rather than let the DB generate rounding warnings
        if base:
            score = dec.Decimal(dec.Decimal(occ) / dec.Decimal(base) * dec.Decimal('100'))
        else:
            score = 0
        

        return round(score, 5)

    #--------------
    def currency_mean(self, result_id, calc_type_id, answer_no, alt_base_answer_no):

        base = 0
        cur = { }

        for year, month in self.periods:
            # get all responses for this answer ready for performing the calcs
            self.r.year = year
            self.r.month = month
            self.r.answer_no = answer_no
            self.r.init() 
            resps = self.r.full_set
       
            if resps:


                #Create the total amount quoted summed within 
                #currency it was created in
                for answer_value in resps.keys():
                    occurences = resps[answer_value]
                    amt, cur_code = list(chain(answer_value.split(" "),[None]*3))[:2]

                    #If currency not specified treat as Uk ponds.
                    if cur_code is None:
                        cur_code = "GBP"

                    if cur_code == "None":
                        cur_code = "GBP"

                    if cur_code in cur:
                        cur[cur_code] += float(amt) * occurences
                    else:
                        cur[cur_code] = float(amt) * occurences

                    base += occurences

        ##Go through ALL the currencies we know about and create 
        # total values of all the quotes covnerted into that currency.
        cr = currency.Currency(self.d,None)
        for this_cur in cr.all_objs():
            try:
                total = convert_all_to_cur(this_cur,cur,(year,month))
            except ValueError: 
                #No conversion for this currency so don't store partial values.
                continue

            if base:
                score = dec.Decimal(dec.Decimal(str(total)) / dec.Decimal(base))
                self.results_set.append( ( result_id, this_cur.currency_code, score , total ,base ))



    #--------------
    def value_mean(self, result_id, calc_type_id, answer_no, alt_base_answer_no):
        '''Generate a mean of the values of the responses'''

        occ = 0
        base = 0


        for year, month in self.periods:
            # get all responses for this answer ready for performing the calcs
            self.r.year = year
            self.r.month = month
            self.r.answer_no = answer_no
            self.r.init() 
            resps = self.r.full_set
        
            if resps:

                for answer_value in resps.keys():
                    occurences = resps[answer_value]
		    #Use base 14, so we allow a->10 etc, 14 so we as we don't really 
		    #have any values above A.	
                    occ += occurences * int(answer_value,14)
                    base += occurences
                 
        if base:
            x = dec.Decimal(dec.Decimal(occ) / dec.Decimal(base))
            score = round(x, 5)

            self.results_set.append((result_id, '!', score, occ, base))



    def split_stack(self, result_id, calc_type, answer_no, dft_answer_value, ):
        ''' calc type using dict not list in occ set to create multiple answer values.
            
            So we have different scores to be using for a stacked chart.
        
            This is the same splits as used for net_promoter , but to be used for stacking.
        
        '''
        occ = 0
        base = 0.0

        # prep values we're going to be concerned about
        calc_type, occs_dct, base_set, txt = self.ct.calcs.get(calc_type)

        parts = dict(( (k,0,) for k in occs_dct.keys() ))

        for year, month in self.periods:
            # get all responses for this answer ready for performing the calcs
            self.r.year = year
            self.r.month = month
            self.r.answer_no = answer_no
            self.r.init() 
            resps = self.r.full_set

            if resps:
                for answer_value in resps.keys():
                    occurences = resps[answer_value]

                    for result_av, range in occs_dct.items():
                        if answer_value in range:
                            base += occurences
                            parts[result_av] += occurences

        if base > 0:
            for key,occ in parts.items():
                score = round((occ/base*100.0), 5)
                self.results_set.append((result_id, key , score , occ, base))




    #--------------
    def percentage(self, result_id, calc_type_id, answer_no, alt_base_answer_no):
        '''Generate a percentage for each response'''

        occ = 0
        base = 0
        occ_counts = {}

        # prep values we're going to be concerned about
        calc_type, occ_set, base_set, txt = self.ct.calcs.get(calc_type_id)

        for response in occ_set:
            occ_counts[response] = 0

        for year, month in self.periods:
            # get all responses for this answer ready for performing the calcs
            self.r.year = year
            self.r.month = month
            self.r.answer_no = answer_no
            self.r.init() 
            resps = self.r.full_set

            if resps:

                # count base
                for answer_value in resps.keys():
                    occurences = resps[answer_value]
                    if base_set:
                        if answer_value in base_set:
                            base += occurences
                    else:
                        base += occurences
                  
                # store each response count
                    if answer_value in occ_set:
                        occ_counts[answer_value] += occurences


        # if we have an alternate base to use, replace whatever base we've just created
        if alt_base_answer_no:
            base = 0
            for year, month in self.periods:
                self.r.year = year
                self.r.month = month
                self.r.answer_no = alt_base_answer_no
                self.r.init() 
                resps = self.r.full_set
                
                if resps:
                    for answer_value in resps.keys():
                        if base_set:
                            if answer_value in base_set:
                                base += resps[answer_value]
                        else:  
                            base += resps[answer_value]

        if base:
            for answer_value in occ_counts.keys():
                occ = occ_counts[answer_value]
                # now we have the total occurences and base we can generate the score,
                score = self.calc_percentage(occ, base)


                self.results_set.append((result_id, answer_value, score, occ, base))

    #--------------
    def combi_mean(self, result_id, calc_type_id, answer_no, dft_answer_value):
        '''combination mean where a set of responses are combined to give a single response'''

        occ = 0
        base = 0

        for year, month in self.periods:
            # get all responses for this answer ready for performing the calcs
            self.r.year = year
            self.r.month = month
            self.r.answer_no = answer_no
            self.r.init()    #:we need to modify the schema. 
            resps = self.r.full_set
            # prep values we're going to be concerned about
            calc_type, occ_set, base_set, txt = self.ct.calcs.get(calc_type_id)
        
            if resps:
                for answer_value in resps.keys():
                    occurences = resps[answer_value]
                    if answer_value in occ_set:
                        occ += occurences
                    if answer_value in base_set:
                        base += occurences

        if base:
            score = self.calc_percentage(occ, base)

            self.results_set.append((result_id, dft_answer_value, score, occ, base))



    #--------------
    def process_question(self, venue_id, year, month, result_id, calc_type_id, answer_no, alt_base_answer_no):


        calc_type, occ_set, base_set, txt = self.ct.calcs.get(calc_type_id)
        if calc_type == 'PC':
            self.combi_mean(result_id, calc_type_id, answer_no, '!')
            
        # percentage
        elif calc_type == 'P':
            self.percentage(result_id, calc_type_id, answer_no, alt_base_answer_no)
            
        # values mean, e.g. mean of no. of seconds
        elif calc_type == 'VM':
            self.value_mean(result_id, calc_type_id, answer_no, alt_base_answer_no)

        elif calc_type == 'CUR':
            self.currency_mean(result_id, calc_type_id, answer_no, alt_base_answer_no)
            
        elif calc_type == 'SS':
            self.split_stack(result_id, calc_type_id, answer_no, alt_base_answer_no)
            

    #--------------
    def overall_scores(self, venue_id, questionnaire_id):
        # non-standard calcs for making results from scores created with feedback reports

        er = event_results.Event_results(self.d, None)
        tot_occ = {}
        tot_score = {}
        for yr, mn in self.periods:
            rows = er.get_core_set(self.adhoc, venue_id, yr, mn, questionnaire_id)
            
            for event_result_id, score, occ in rows:
                if tot_score.has_key(event_result_id):
                    tot_score[event_result_id] += float(score)
                    tot_occ[event_result_id] += occ
                else:
                    tot_score[event_result_id] = float(score)
                    tot_occ[event_result_id] = occ


        for event_result_id in tot_occ.keys():
            score = tot_score[event_result_id]
            occ = tot_occ[event_result_id]

            if questionnaire_id == 3:
                result_id = event_result_id + 300
            elif questionnaire_id == 4:
                result_id = event_result_id + 400
            elif questionnaire_id == 5:
                result_id = event_result_id + 500
            elif questionnaire_id == 6:
                result_id = event_result_id + 600
            elif questionnaire_id == 7:
                result_id = event_result_id + 7000
            elif questionnaire_id == 8:
                result_id = event_result_id + 8000
            elif questionnaire_id == 9:
                result_id = event_result_id + 9000
            elif questionnaire_id == 10:
                result_id = event_result_id + 10000
            elif questionnaire_id == 11:
                result_id = event_result_id + 11000
            elif questionnaire_id == 12:
                result_id = event_result_id + 12000
            elif questionnaire_id == 13:
                result_id = event_result_id + 13000
            else:
                result_id = event_result_id

            #Skip a value if it is going to be (or has been) overridden.
            if result_id in  event_results.override_ids.values(): continue

            # now override the result_id if we have a special case
            result_id = event_results.override_ids.get(result_id, result_id)

            if occ > 0:
                self.results_set.append((result_id, '!',  round(score / occ, 5), score, occ))
            else:
                self.results_set.append((result_id, '!',  0, 0, 0))


    def main_calcs(self, venue_id, year, month, questionnaire_id):

        # loop for each question for the specifed questionnaire
        # and only process those that have entries in calc_control    
        self.q_ref.questionnaire_id = questionnaire_id
        self.q_ref.get_all()

        for question_id in self.q_ref.full_set.keys():
            result_id, calc_type_id, alt_base_answer_no = self.calc_ctl.full_set.get(question_id, (None, None, None))
            if result_id:
                answer_no = self.q_ref.full_set.get(question_id)
                self.process_question(venue_id, year, month, result_id, calc_type_id, answer_no, alt_base_answer_no)


    #--------------
    def process_venue(self, venue_id, year, month, questionnaire_id, score_type):
  
        # set up responses sets, updating if required
        self.r.adhoc = self.adhoc
        self.r.venue_id = venue_id
        self.r.year = year
        self.r.month = month
        self.r.quest = questionnaire_id

        if self.run_responses and self.responses_done is False:
            success = self.r.update_set()
            self.responses_done = True


        # initialise results set because we're going to generate the full set
        self.results_set = []


        # generate main calcs
        self.main_calcs(venue_id, year, month, questionnaire_id)

        
        # now generate the overall and section scores, which are means
        # of the venues events for the period
        self.overall_scores(venue_id, questionnaire_id)

       
        # store the results
        res = model.VenueScores(dbConnection=self.d, f=self.f,
            questionnaire_id=questionnaire_id, year=year, month=month,
            score_type=score_type, id_type=0, id=venue_id, set_mode=True)
        success = res.update_set(self.results_set)
        if success is False:
            print 'failed', venue_id

    #--------------
    def store_period_months(self, year, month, period_limit):

        yr = year
        mn = month
        self.periods = [(yr, mn)]
        while period_limit > 1:
            mn -= 1
            if mn < 1:
                yr -= 1
                mn = 12
            self.periods.append((yr, mn))
            period_limit -= 1

    #--------------
    def set_work_periods(self, score_type, year, month):
        '''set the periods required for the specified score_type'''

        self.periods = []

        # 3 month cumulative
        if score_type == '3':
            self.store_period_months(year, month, 3)

        # single month
        elif score_type == '1':
            self.store_period_months(year, month, 1)

        # year to date
        elif score_type == 'Y':
            self.store_period_months(year, month, month)

        # 12 month cumulative
        elif score_type == 'C':
            self.store_period_months(year, month, 12)


    #--------------
    def do_all_venues(self, year, month, score_type):
        """Process all active venues"""

        self.set_work_periods(score_type, year, month)

        v = venue.Venue(score.d, None, f=self.f)
        for ven in v.get_all_active():
            if not rerun or rerun_venues == None or ven.venue_id in rerun_venues:
                print "\tprocessing venue %s"%(ven.venue_id)
                self.responses_done = False
                for questionnaire_id in self.questionnaires:
                    venue_id = ven.venue_id
                    score.process_venue(venue_id, year, month, questionnaire_id, score_type)

    def do_core(self,year,month):

        self.run_responses = True
        score_type = '1'
        self.do_all_venues(year, month, score_type)
        # don't generate responses data again - the routine only does the
        # current month anyway.
        self.run_responses = False

        #
        # 2015, we've changes result_id etc so we 
        # need to go back to using group_v_scores for these
        #

        #score_type = '3'
        #self.do_all_venues(year, month, score_type)

        #score_type = 'Y'
        #self.do_all_venues(year, month, score_type)

        #score_type = 'C'
        #self.do_all_venues(year, month, score_type)


    def main(self, ):


        sc = model.Scores(dbConnection=self.d, f=self.f )


        if self.rerun:
        
            year = self.rerun_start_year
            month = self.rerun_start_month
            period = '%s-%02d' % (year, month)
            print "regenerating venue scores for:",
        
            while period <= self.rerun_last_period:
                print " %s-%02d" % (year, month),
                sys.stdout.flush()

                self.do_core(year, month)

                # get ready for next period
                year, month = sc.next_period(year=year, month=month)
                period = '%s-%02d' % (year, month)


            print  # kill last comma
        else:

            year, month = sc.next_period()
            print "generating venue scores for: %s-%02d" % (year, month)
            self.do_core(year, month)
 

if __name__ == '__main__':
    score = Score(None)
    score.main()

