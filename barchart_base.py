
import common
import model

NoValue = 1.7E+308  # chartdirector constant for skipping entries
class Barchart_base:

    def __init__(self, **kwargs ):

        self.d = kwargs.get('d', None)
        f = kwargs.get('f', None)
        if self.d is None:
            import db
            self.d = db.connect()
        if f is not None:
            self.f = f
        else:
            self.f = self.d.cursor()

        self.score_type = kwargs.get('score_type', '3')
        self.questionnaire_id = kwargs.get('questionnaire_id', 2)

        self.score = model.Scores(dbConnection=self.d)

        period = kwargs.get('period',None)
        if period and all(period):
            self.latest_period = period
        else:
            self.latest_period = self.score.latest_period()

        self.theme = kwargs.get('theme', None)
        if not self.theme:
            import brand_theme
            #get default brand theme
            bt = brand_theme.BrandTheme(None, None)
            self.theme =bt.theme


    def theme_val(self, name):
        valstr = self.theme[name]
        if valstr[0] == '#':
            return int('0x%s'%(valstr[1:]),0)

        #FIXME: throw or try harder to convert!
        return valstr


    def set_bar_colours(self, limit=11):
        '''set barchart colours based on the month number. 3,6,9 and 12 get one colour
        while the others are another'''

        year, month = self.latest_period
        bar_colours = []

        # 1 month scores to show an extra month
        if self.score_type == '1':
            limit += 1

        for x in range(0, limit):
            if month in (3,6,9,12):
                bar_colours.append(self.theme_val('bc_bar_colour_q'))
            else:
                bar_colours.append(self.theme_val('bc_bar_colour'))
            month -= 1
            if month < 1:
                year -= 1
                month = 12

        bar_colours.reverse()
        return bar_colours


    #--------------
    def set_bar_labels(self, limit=11, qurt_required = 1):
        '''return barchart labels'''
        bar_labels = []

        # 1 month scores to show an extra month
        if self.score_type == '1':
            limit += 1

        # if we have lots of column labels we need to split the months into 
        # two line to prevent the texts overlapping
        if limit > 7:
            split = True
        else:
            split = False

        year, month = self.latest_period

        for x in range(0, limit):
            # 2011 results are starting as Jan only for 3mth, so we're only going to show
            # Jan as the split label
            single_month = bool(year == 2011 and month == 1)

            # 2011 Jan-Feb label fudge
            if (year == 2011 and month==2):
                offset_months = 2
            else:
                offset_months = 3

            if self.score_type == '1':
                label = common.short_month_names[month-1]
            else:
                label = common.period_text(month, split, single_month=single_month, 
                                            offset_months=offset_months)
            if month in (3,6,9,12) and qurt_required:
                label += '\n(Q%s %s)' % (int(month/3), str(year)[2:])
            bar_labels.append(label)

            month -= 1
            if month < 1:
                year -= 1
                month += 12

        bar_labels.reverse()

        return bar_labels


    #--------------
    def rtv_venue_scores(self, result_id, answer_value, venue_id,  *args, **kwargs):
        '''pull in the score for the specified result_id'''

        worst = kwargs.get('worst', False)
        country_id = kwargs.get('country_id', None)
        region_id = kwargs.get('region_id', None)
        super_region_id = kwargs.get('super_region_id', None)
        brand_id = kwargs.get('brand_id', None)
        limit = kwargs.get('limit', 11)
        id_type = kwargs.get('id_type', 0)
        rounding_dp = kwargs.get('rounding_dp', 1)
        id = venue_id

        # 1 month scores to show an extra month
        if self.score_type == '1':
            limit += 1

        data = []
        responses = []
        year, month = self.latest_period

        # prep extra results access for special case
        if id is None:
            vs = model.VenueScores(dbConnection=self.d, f=self.f )


        if year is None:
            common.dm('Scores are being updated, please try again in a few minutes')

        base = 0
        # retrieve the data working backwards for the required number of periods
        for x in range(0, limit):
            allow_override = common.result_override(year, month)

            if venue_id is None:
                vs.allow_override = allow_override
                if worst:
                    id = vs.worst_venue_in_brand(questionnaire_id=self.questionnaire_id, year=year,
                      month=month, score_type=score_type, result_id=result_id, 
                      answer_value=answer_value, brand_id=brand_id)
                else:
                    id = vs.best_venue_in_brand(questionnaire_id=self.questionnaire_id, year=year,
                      month=month, score_type=score_type, result_id=result_id,
                      answer_value=answer_value, brand_id=brand_id)


            venue_score = model.VenueScores(dbConnection=self.d, f=self.f, 
                    questionnaire_id=self.questionnaire_id, year=year,
                    month=month, score_type=self.score_type, id_type=id_type, id=id, result_id=result_id,
                    answer_value=answer_value, allow_override=allow_override)

            if venue_score.score is not None:
                score = round(venue_score.score, rounding_dp)
                base = venue_score.base
                occ = venue_score.occurences

                data.append(score)
            else:
                data.append(NoValue)

            if base == 0 or base is None:
                responses.append(NoValue)
            else:
                responses.append(base)

            month -= 1
            if month < 1:
                year -= 1
                month = 12

        # reverse the data so it's in the right order for the charts
        data.reverse()
        responses.reverse()

        return data, responses

    def rtv_aggregate_scores(self, **kwargs):

        scores = kwargs.get('scores', None)
        limit = kwargs.get('limit', 11)
        id_type = kwargs.get('id_type', 0)
        id = kwargs.get('id', None)
        questionnaire_id = kwargs.get('questionnaire_id', None)
        score_type = kwargs.get('score_type', None)
        result_id = kwargs.get('result_id', None)
        answer_value = kwargs.get('answer_value', None)
        worst = kwargs.get('worst', False)
        best = kwargs.get('best', False)
        brand_id = kwargs.get('brand_id', None)
        rounding_dp = kwargs.get('rounding_dp', 1)
        start_year = kwargs.get('start_year', None)
        start_month = kwargs.get('start_month', None)

        # save score keyfields if we have been given a scoring obj. We need to do
        # this because the score obj itself will handle qst/result_id overrides
        # required for the pan-questionnaire/year trending
        if scores is not None:
            sav_questionnaire_id = scores.questionnaire_id
            sav_score_type = scores.score_type
            sav_id_type = scores.id_type
            sav_id = scores.id
            sav_result_id = scores.result_id
            sav_answer_value = scores.answer_value

            sav_brand_id =None
            sav_demense_id =None
            if hasattr(scores,"brand_id"): sav_brand_id = scores.brand_id
            if hasattr(scores,"demense_id"): sav_demense_id = scores.demense_id

        # 1 month scores to show an extra month
        if self.score_type == '1':
            limit += 1

        data = []
        responses = []

        if start_year and start_month:
            year = start_year
            month = start_month
        else:
            year, month = self.latest_period


        if year is None:
            return 'Scores are being updated, please try again in a few minutes'

        # retrieve the data working backwards for the required number of periods
        for x in range(0, limit):


            # restore keyfields
            if scores is not None:
                scores.questionnaire_id = sav_questionnaire_id
                scores.score_type = sav_score_type
                scores.id_type = sav_id_type
                scores.id = sav_id
                scores.result_id = sav_result_id
                scores.answer_value = sav_answer_value
                if sav_brand_id : scores.brand_id = sav_brand_id
                if sav_demense_id : scores.demense_id = sav_demense_id

            scores.year = year
            scores.month = month
            scores.allow_override = common.result_override(year, month)

            if worst:
                scores.id = scores.worst_level_score(questionnaire_id=questionnaire_id, 
                                   year=year, month=month,
                                   score_type=score_type, id_type=id_type, result_id=result_id, 
                                   answer_value=answer_value, brand_id=brand_id)
            elif best:
                scores.id = scores.best_level_score(questionnaire_id=questionnaire_id, 
                                   year=year, month=month,
                                   score_type=score_type, id_type=id_type, result_id=result_id, 
                                   answer_value=answer_value, brand_id=brand_id)


            scores.load()
            if scores.score is not None:
                score = round(scores.score, rounding_dp)
                base = scores.base
                occ = scores.occurences

                data.append(score)
            else:
                base = 0
                data.append(NoValue)


            if base == 0 or base is None:
                responses.append(NoValue)
            else:
                responses.append(base)

            month -= 1
            if month < 1:
                year -= 1
                month = 12

        # reverse the data so it's in the right order for the charts
        data.reverse()
        responses.reverse()
        return data, responses

