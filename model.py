# -*- coding: utf-8 -*-

import local
import common
import bdrcshared.model 

FactoryBase = bdrcshared.model.FactoryBase

class Base(bdrcshared.model.Base):
    @property
    def db(self,):
        import db
        return db

class Scores(Base):

    def setup(self, *args, **kwargs ):
        
        self.questionnaire_id = kwargs.get('questionnaire_id', None)
        self.year = kwargs.get('year', None)
        self.month = kwargs.get('month', None)
        self.score_type = kwargs.get('score_type', None)
        self.id_type = kwargs.get('id_type', None)
        self.id = kwargs.get('id', None)
        self.result_id = kwargs.get('result_id', None)
        self.answer_value = kwargs.get('answer_value', None)

        # When specified, retriving of scores will look for overriding qst/result_ids
        self.allow_override = kwargs.get('allow_override', False)

        self.score = None
        self.occurences = None
        self.base = None

        # when set_mode is set, we don't attempt load data or reset attributes
        self.set_mode = kwargs.get('set_mode', None)

        # set table name, because we're using this for multiple score tables
        self.table = None
        self.set_table(**kwargs)


        if not self.set_mode:
            # if all key criteria has been specified, set up the data otherwise
            # reset attributes to None
            if self.all_keys(**kwargs):
                self.load()
            else:
                self.reset()

    def set_table(self,**kwargs):
        pass


    def latest_period(self, ):
        '''determine the lastest period of results. We assume top level nationals are
        done, so we look for the latest for that. Returns year and month'''

        s = """SELECT year, month FROM division_scores
                ORDER BY year DESC, month DESC LIMIT 1"""
        self.f.execute(s)
        row = self.f.fetchone()

        if row:
            return row
        else:
            return None, None


    def next_period(self, *args, **kwargs ):
        '''return the next period based on clocking on the last period'''

        year = kwargs.get('year', None)
        month = kwargs.get('month', None)

        # if both date elements were not supplied, use the last period we generated results for
        if year is None or month is None:
            year, month = self.latest_period()

        if year and month:
            month += 1
            if month > 12:
                year += 1
                month = 1
            
        return year, month


    def previous_period(self, *args, **kwargs ):
        '''return the previous period based on clocking back the specified criteria'''

        year = kwargs.get('year', None)
        month = kwargs.get('month', None)

        # if both date elements were not supplied, use the last period we generated results for
        if year is None or month is None:
            year, month = self.latest_period()

        if year and month:
            month -= 1
            if month < 1:
                year -= 1
                month = 12
            
        return year, month




    def __repr__(self, ):
        return u'Score (%s): questionnaire_id=%s, year=%s, month=%s, score_type=%s, id_type=%s, id=%s, result_id=%s, answer_value=%s, score=%s, occurences=%s, base=%s' % (self.table, self.questionnaire_id, self.year, self.month, self.score_type, self.id_type, self.id, self.result_id, self.answer_value, self.score, self.occurences, self.base)

    def all_keys(self, *args, **kwargs):
        'return True if all keys have been specified'

        return bool(
            self.questionnaire_id is not None and
            self.year is not None and
            self.month is not None and
            self.score_type is not None and
            self.id_type is not None and
            self.id is not None and
            self.result_id is not None and
            self.answer_value is not None
            )
        


    def reset(self, ):

        self.questionnaire_id = None
        self.year = None
        self.month = None
        self.score_type = None
        self.id = None
        self.id_type = None
        self.result_id = None
        self.answer_value = None
        self.score = None
        self.occurences = None
        self.base = None


    def get(self, ):

        questionnaire_id, result_id, answer_value = self.trending_overrides(
            self.questionnaire_id, self.result_id, self.year)

        s = '''SELECT questionnaire_id, year, month, score_type, id_type,
                        id, result_id, answer_value, score, occurences, base
                    FROM %s ''' % self.table
        s += '''WHERE questionnaire_id = %s
                    AND year = %s
                    AND month = %s
                    AND score_type = %s
                    AND id_type = %s
                    AND id = %s
                    AND result_id = %s
                    AND answer_value = %s'''

        self.f.execute(s, (questionnaire_id, self.year, self.month, self.score_type,
                            self.id_type, self.id, result_id, answer_value))
        return self.f.fetchone()

    def load(self, *args, **kwargs ):

        row = self.get()

        if row:
            self.questionnaire_id = row[0]
            self.year = row[1]
            self.month = row[2]
            self.score_type = row[3]
            self.id_type = row[4]
            self.id = row[5]
            self.result_id = row[6]
            self.answer_value = row[7]
            self.score = row[8]
            self.occurences = row[9]
            self.base = row[10]
        else:
            self.reset()


    def delete_set(self, ):
        '''delete the data for the current class attributes'''

        success = None

        s = "DELETE FROM %s " % self.table
        s += '''WHERE questionnaire_id = %s
                    AND year = %s
                    AND month = %s
                    AND score_type = %s
                    AND id_type = %s
                    AND id = %s'''


        try:
            self.f.execute(s, (self.questionnaire_id, self.year, self.month, self.score_type,
                                self.id_type, self.id))
        except:
            success = False
        else:
            success = True

        return success


    def add(self, result_id, answer_value, score, occurences, base):
        '''add the specified score'''


        s = "INSERT INTO %s " % self.table
        s += """(questionnaire_id, year, month, score_type, id_type, id, result_id, answer_value, score, occurences, base)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        try:
            self.f.execute(s, (self.questionnaire_id, self.year, self.month, self.score_type,
                                self.id_type, self.id, result_id, answer_value,
                                score, occurences, base))
        except Exception, e:
            success = False
            print e
        else:
            success = True

        return success




    def update_set(self, list, delete=True):
        '''replace the existing set of results with those specifed in the list'''
        

        # first we remove the existing set
        if delete:
            success = self.delete_set()
        else:
            success = True

        
        # and if no errors, we add all those in the list
        if success:
            for result_id, answer_value, score, occurences, base in list:
                success = self.add(result_id, answer_value, score, occurences, base)
                if not success:
                    break


        if success:
            self.d.commit()
        else:
            self.d.rollback()

        return success

    def aggregate_result(self, id, result_id, ):
        '''NOTE: scoring methods do not do joins and check the standard business rules, instead
        we set venue_ids to be a list of venue IDs relevant to the brand and country combo being 
        processed as it proved to be substantially faster'''
        
        id_type = 0   # venues

        s = """SELECT answer_value, SUM(occurences), SUM(base)
                        FROM venue_scores
                    WHERE questionnaire_id=%s
                        AND year=%s
                        AND month=%s
                        AND score_type=%s
                        AND id_type=%s
                        AND result_id=%s
                        """
        
        if self.venue_ids:
            s += ' AND id IN (%s)' % self.venue_ids

        s += " GROUP BY answer_value"

        self.f.execute(s, (self.questionnaire_id, self.year, self.month, self.score_type, id_type, result_id, ))
        return self.f.fetchall()


    def group_score(self, id, result_id, ):
        '''NOTE: scoring methods do not do joins and check the standard business rules, instead
        we set venue_ids to be a list of venue IDs relevant to the brand and country combo being 
        processed as it proved to be substantially faster'''
        
        id_type = 0   # venues


        s = """SELECT SUM(occurences), sum(base)
                    FROM venue_scores
                    WHERE questionnaire_id=%s
                        AND year=%s
                        AND month=%s
                        AND score_type=%s
                        AND id_type=%s
                        AND result_id=%s"""

        # add subsetting for brands if id_type has been set to brand_id, which has
        # to be above zero
        if self.venue_ids:
            s += ' AND id IN (%s)' % self.venue_ids


        
        self.f.execute(s, (self.questionnaire_id, self.year, self.month, self.score_type, id_type, result_id, ))
        return self.f.fetchall()

    
    def trending_overrides(self, questionnaire_id, result_id, year):
        '''return questionnaire_id, result_id and answer_value for the obj's current
        keys if we're into trending and need to replace the current ones with specific
        ones for earlier years'''

        # look for overrides before retriving the scrore
        if self.allow_override:
            questionnaire_id, result_id = common.ovr_result_id(questionnaire_id, result_id, year)
            from brand_report_overall import set_text
            x = set_text.get(result_id, None)
            if x:
                answer_value = x[1]
            else: 
                answer_value = self.answer_value
            return questionnaire_id, result_id, answer_value
        else:
            return self.questionnaire_id, self.result_id, self.answer_value


    def best_level_score(self, *args, **kwargs):
        
        questionnaire_id = kwargs.get('questionnaire_id', None)
        year = kwargs.get('year', None)
        month = kwargs.get('month', None)
        score_type = kwargs.get('score_type', None)
        id_type = kwargs.get('id_type', 0)
        id = kwargs.get('id', None)
        result_id = kwargs.get('result_id', None)
        answer_value = kwargs.get('answer_value', None)
        order = kwargs.get('order', 'DESC')

        questionnaire_id, result_id, answer_value = self.trending_overrides(questionnaire_id, result_id, year)

        x = ["""SELECT id
            FROM %s """ % self.table]

        x.append(""" WHERE questionnaire_id=%s
                AND year=%s
                AND month=%s 
                AND score_type=%s 
                AND id_type=%s 
                AND result_id=%s
                AND answer_value=%s
            ORDER BY score """)

        x.append(' %s' % order)

        x.append(' LIMIT 1')

        s = ''.join(x)
        
        self.f.execute(s, (questionnaire_id, year, month, score_type, id_type, result_id, answer_value))
        row = self.f.fetchone()
        if row: 
            return row[0]
        else:
            return None


    def worst_level_score(self, *args, **kwargs):

        return self.best_level_score(order='ASC', **kwargs)



class VenueScores(Scores):
    def set_table(self,**kwargs):
        self.table = 'venue_scores'

    def top_N_venue_in_brand(self, *args, **kwargs):
        '''Get the best score for the specified region for the current period.
            NOTE: cluster venues are excluded by default (use omit_cluster=True)!'''
        questionnaire_id = kwargs.get('questionnaire_id', None)
        result_id = kwargs.get('result_id', None)
        year = kwargs.get('year', None)
        month = kwargs.get('month', None)
        score_type = kwargs.get('score_type', None)
        omit_secret = kwargs.get('omit_secret', True)
        omit_private = kwargs.get('omit_private', False)
        omit_normal = kwargs.get('omit_normal', False)
        omit_cluster = kwargs.get('omit_cluster', False)
        month_order_by = kwargs.get('month_order_by', None)
        ytd_order_by = kwargs.get('ytd_order_by', None)
        

        if score_type in ('1','3'):
            score_type2 = 'Y'
        else:
            score_type2 = '1'

        id_type = kwargs.get('id_type', 0)
        demense_id = kwargs.get('demense_id', None)
        answer_value = kwargs.get('answer_value', None)


        # set brand_id to limit to only this brand
        brand_id = kwargs.get('brand_id', None)

        # set exclude_brand_id to select all but this brand_id
        exclude_brand_id = kwargs.get('exclude_brand_id', None)

        limit = kwargs.get('limit', 10)

        order = kwargs.get('order', 'DESC')

        questionnaire_id, result_id, answer_value = self.trending_overrides(questionnaire_id, result_id, year)

        if month_order_by or ytd_order_by:
            x = ["""SELECT venue_id, venue_name as name,
                    score
                FROM {0} v
                    JOIN venues ON (venue_id=id) 
                    JOIN brands USING (brand_id)
                """.format(self.table)]
        else:
            x = ["""SELECT venue_id, venue_name as name,
                    score,
                    (select score from {0}
                        where questionnaire_id = v.questionnaire_id
                        and year = v.year
                        and month = v.month
                        and score_type = '{1}'
                        and id_type = v.id_type
                        and id = v.id
                        and result_id = v.result_id
                        and answer_value = v.answer_value
                    ) as score2
                FROM {0} v
                    JOIN venues ON (venue_id=id) 
                    JOIN brands USING (brand_id)
                """.format(self.table, score_type2)]

#        if demense_id is not None:
#            x.append(""" JOIN demense_closure dc ON (dc.d = demense_id ) """)

        x.append("""   
            WHERE exclude_from_main_study IS NULL
                AND exclude_from_groupings IS NULL
                AND delete_date IS NULL""")

        if omit_secret:
            if omit_private: # omit S & P
                if omit_normal: # ???? we really shouldn't allow this since it excludes all
                    import sys
                    sys.stderr.write('VenueScores.top_N_in_brand ERROR: omitting secret, private and normal gives no results\n')
                    return []
                else: # this is the default
                    x.append(' AND secret IS NULL')
            else:
                if omit_normal:
                    x.append(" AND secret !='Y'")
                else: # omit S only
                    x.append(" AND (secret IS NULL OR secret !='Y')")
        else:
            if omit_private:
                if omit_normal:
                    x.append(" AND secret !='P'")
                else: # omit P only
                    x.append(" AND (secret IS NULL OR secret !='P')")
            else: # keep S & P
                if omit_normal:
                    x.append(' AND secret IS NOT NULL')
                else: # keep all
                    pass

        qid,rid = common.ovr_result_id(questionnaire_id,result_id,year)

        if month_order_by:
            x.append('''
                        AND questionnaire_id={0}
                        AND year={1}
                        AND month={2} 
                        AND score_type='{3}' 
                        AND id_type={4} 
                        AND result_id={5}
                        AND answer_value='{6}'
                     '''.format(qid, year, month, score_type, id_type,  rid, answer_value  ))
        elif ytd_order_by:
            x.append('''
                    AND questionnaire_id={0}
                    AND year={1}
                    AND month={2} 
                    AND score_type='{3}' 
                    AND id_type={4} 
                    AND result_id={5}
                    AND answer_value='{6}'
                 '''.format(qid, year, month, score_type2, id_type,  rid, answer_value  ))
        else: 
            x.append('''
                    AND questionnaire_id={0}
                    AND year={1}
                    AND month={2} 
                    AND score_type='{3}' 
                    AND id_type={4} 
                    AND result_id={5}
                    AND answer_value='{6}'
                 '''.format(qid, year, month, score_type, id_type,  rid, answer_value  ))

        if not omit_cluster:
            x.append(' AND cluster_id IS NULL')

        if brand_id is not None:
            x.append(' AND brand_id={0}'.format(brand_id))

        if demense_id is not None:
            x.append(" AND exists( select * from bdrcshared.demense_closure where d=demense_id and s = {0} ) ".format(demense_id))

        if month_order_by or ytd_order_by:
            x.append('''
                ORDER BY score {0}, name '''.format(order))
        else:
            x.append('''
                ORDER BY score {0}, score2 {0}, name '''.format(order))

        if limit:
            x.append(' LIMIT {0}'.format(limit))

        s = ''.join(x)

        s=s.format(questionnaire_id, year, month, score_type, id_type,  result_id, answer_value  )

        try:
            self.f.execute(s)
        except Exception,e:
            import sys
            sys.stderr.write("top_sql=%s\n"%s)
            raise e
#        sys.stderr.write('\n')

        ret = []
        for row in self.f.fetchall():
            ret.append((row))
        return ret

    def best_venue_in_brand(self, *args, **kwargs):
        '''Get the best score for the specified region for the current period.
            NOTE: cluster venues are excluded!'''
        r = self.top_N_venue_in_brand(self, *args, limit=1, **kwargs)
        if len(r) > 0:
            return r[0][0]
        else:
            return None

    def worst_venue_in_brand(self, **kwargs):
        '''Get the worst score for the specified region for the current period'''

        return self.best_venue_in_brand(order='', **kwargs)



class Cluster_scores(Scores):
    def set_table(self,**kwargs):
        self.table = 'cluster_scores'


    def best_in_brand(self, *args, **kwargs):
        '''Get the best score for the specified brand for the current period.'''
        
        questionnaire_id = kwargs.get('questionnaire_id', None)
        year = kwargs.get('year', None)
        month = kwargs.get('month', None)
        score_type = kwargs.get('score_type', None)
        id_type = kwargs.get('id_type', 0)
        result_id = kwargs.get('result_id', None)
        answer_value = kwargs.get('answer_value', None)
        demense_id = kwargs.get('demense_id', None)

        # set brand_id to limit to only this brand
        brand_id = kwargs.get('brand_id', None)

        order = kwargs.get('order', 'DESC')

        x = ["""SELECT score, occurences, base, id
            FROM %s
                JOIN venues ON (cluster_id=id) 
                JOIN brands USING (brand_id ) """ %self.table ]


        if demense_id is not None:
            x.append(""" JOIN demense_closure dc ON (dc.d = demense_id ) """)


        x.append("""
            WHERE exclude_from_main_study IS NULL
                AND exclude_from_groupings IS NULL
                AND cluster_id IS NOT NULL
                AND delete_date IS NULL""") 

        if brand_id is not None:
            x.append(' AND brand_id=%s' % brand_id)


        if demense_id is not None:
            x.append(" AND ( dc.s = %s OR demense_id =%s ) "%(demense_id,demense_id))




        x.append('''
                AND questionnaire_id=%s
                AND year=%s
                AND month=%s 
                AND score_type=%s 
                AND id_type=%s 
                AND result_id=%s
                AND answer_value=%s
            ORDER BY score ''')

        if order:
            x.append(' DESC')

        x.append(' LIMIT 1')
        s = ''.join(x)
        
        self.f.execute(s, (questionnaire_id, year, month, score_type, id_type, result_id, answer_value, ))
        row = self.f.fetchone()

        if row:
            return row[3]
        else:
            return None


    def worst_in_brand(self, **kwargs):
        '''Get the worst score for the specified brand for the current period'''

        return self.best_in_brand(order='', **kwargs)



class Crs_scores(Scores):
    def set_table(self,**kwargs):
        self.table = 'crs_scores'

    def aggregate_result(self, id, result_id, ):
        s = """SELECT answer_value, SUM(occurences), SUM(base)
                    FROM venue_scores
                        JOIN venues ON (id=venue_id)
                        JOIN brands USING(brand_id)
                    WHERE exclude_from_main_study IS NULL
                        AND exclude_from_groupings IS NULL
                        AND delete_date IS NULL
                        AND (cluster_id IS NOT NULL OR crs IS NOT NULL)
                        AND questionnaire_id=%s
                        AND year=%s
                        AND month=%s
                        AND score_type=%s
                        AND id_type=%s
                        AND result_id=%s
                    GROUP BY answer_value"""
        self.f.execute(s, (self.questionnaire_id, self.year, self.month, self.score_type, self.id_type, result_id, ))

        return self.f.fetchall()


    def group_score(self, id, result_id, ):
        

        s = """SELECT SUM(occurences), sum(base)
                    FROM venue_scores
                        JOIN venues ON (id=venue_id)
                        JOIN brands USING(brand_id)
                    WHERE exclude_from_main_study IS NULL
                        AND exclude_from_groupings IS NULL
                        AND delete_date IS NULL
                        AND (cluster_id IS NOT NULL OR crs IS NOT NULL)
                        AND questionnaire_id=%s
                        AND year=%s
                        AND month=%s
                        AND score_type=%s
                        AND id_type=%s
                        AND result_id=%s"""

        self.f.execute(s, (self.questionnaire_id, self.year, self.month, self.score_type, self.id_type, result_id, ))

        return self.f.fetchall()



class Brand_scores(Scores):
    def set_table(self,**kwargs):
        self.table = 'brand_scores'


class Indy_scores(Scores):
    def set_table(self,**kwargs):
        self.table = 'brand_scores'

    def aggregate_result(self, id, result_id, ):
        '''NOTE: scoring methods do not do joins and check the standard business rules, instead
        we set venue_ids to be a list of venue IDs relevant to the brand and country combo being 
        processed as it proved to be substantially faster'''
        
        s = """SELECT answer_value, SUM(occurences), SUM(base)
                        FROM venue_scores
                        JOIN venues ON (venue_id=id)
                        LEFT JOIN brands USING (brand_id)
                    WHERE (brand_id IS NULL OR independent IS NOT NULL)
                        AND questionnaire_id=%s
                        AND year=%s
                        AND month=%s
                        AND score_type=%s
                        AND id_type=%s
                        AND result_id=%s
                        """
        
        if self.venue_ids:
            s += ' AND id IN (%s)' % self.venue_ids

        s += " GROUP BY answer_value"

        self.f.execute(s, (self.questionnaire_id, self.year, self.month, self.score_type, self.id_type, result_id, ))
        return self.f.fetchall()



class Country_scores(Scores):
    
    def set_table(self,**kwargs):
        self.table = 'country_scores'



    def aggregate_result(self, id, result_id, ):
        s = """SELECT answer_value, SUM(occurences), SUM(base)
                    FROM venue_scores
                        JOIN venues ON (id=venue_id)
                        JOIN brands USING(brand_id)
                    WHERE exclude_from_main_study IS NULL
                        AND exclude_from_groupings IS NULL
                        AND questionnaire_id=%s
                        AND year=%s
                        AND month=%s
                        AND score_type=%s
                        AND id_type=%s
                        AND result_id=%s
                    GROUP BY answer_value"""
        self.f.execute(s, (self.questionnaire_id, self.year, self.month, self.score_type, self.id_type, result_id, ))

        return self.f.fetchall()


    def group_score(self, id, result_id, ):
        
        id_type = 0   # venues


        s = """SELECT SUM(occurences), sum(base)
                    FROM venue_scores
                        JOIN venues ON (id=venue_id)
                        JOIN brands USING(brand_id)
                    WHERE exclude_from_main_study IS NULL
                        AND exclude_from_groupings IS NULL
                        AND questionnaire_id=%s
                        AND year=%s
                        AND month=%s
                        AND score_type=%s
                        AND id_type=%s
                        AND result_id=%s"""

        self.f.execute(s, (self.questionnaire_id, self.year, self.month, self.score_type, self.id_type, result_id, ))

        return self.f.fetchall()


class Region_scores(Scores):
    
    def set_table(self,**kwargs):
        self.table = 'region_scores'

class Demense_scores(Scores):
    
    def set_table(self,**kwargs):
        self.table = 'demense_scores'


class Brand_Demense_scores(Scores):
    
    def set_table(self,**kwargs):
        self.brand_id = kwargs.get('brand_id', None)
        self.table = 'brand_demense_scores'



    def __repr__(self, ):
        return u'Brand_Demense_Score (%s): questionnaire_id=%s, year=%s, month=%s, score_type=%s, id_type=%s, id=%s, brand_id =%s, result_id=%s, answer_value=%s, score=%s, occurences=%s, base=%s' % (self.table, self.questionnaire_id, self.year, self.month, self.score_type, self.id_type, self.id, self.brand_id, self.result_id, self.answer_value, self.score, self.occurences, self.base)

    def all_keys(self, *args, **kwargs):
        'return True if all keys have been specified'

        return bool(
            self.questionnaire_id is not None and
            self.year is not None and
            self.month is not None and
            self.score_type is not None and
            self.id_type is not None and
            self.id is not None and
            self.brand_id is not None and
            self.result_id is not None and
            self.answer_value is not None and
            self.brand_id is not None
            )
        


    def reset(self, ):

        self.questionnaire_id = None
        self.year = None
        self.month = None
        self.score_type = None
        self.id = None
        self.id_type = None
        self.result_id = None
        self.answer_value = None
        self.score = None
        self.occurences = None
        self.brand_id = None
        self.base = None

    def get(self, ):

        questionnaire_id, result_id, answer_value = self.trending_overrides(
            self.questionnaire_id, self.result_id, self.year)

        s = '''SELECT questionnaire_id, year, month, score_type, id_type,
                        id, brand_id, result_id, answer_value, score, occurences, base
                    FROM %s ''' % self.table
        s += '''WHERE questionnaire_id = %s
                    AND year = %s
                    AND month = %s
                    AND score_type = %s
                    AND id_type = %s
                    AND id = %s
                    AND brand_id = %s
                    AND result_id = %s
                    AND answer_value = %s'''

        self.f.execute(s, (questionnaire_id, self.year, self.month, self.score_type,
                            self.id_type, self.id, self.brand_id, result_id, answer_value))
        return self.f.fetchone()

    def load(self, *args, **kwargs ):

        row = self.get()

        if row:
            self.questionnaire_id = row[0]
            self.year = row[1]
            self.month = row[2]
            self.score_type = row[3]
            self.id_type = row[4]
            self.id = row[5]
            self.brand_id = row[6]
            self.result_id = row[7]
            self.answer_value = row[8]
            self.score = row[9]
            self.occurences = row[10]
            self.base = row[11]
        else:
            self.reset()

    def delete_set(self, ):
        '''delete the data for the current class attributes'''

        success = None

        s = "DELETE FROM %s " % self.table
        s += '''WHERE questionnaire_id = %s
                    AND year = %s
                    AND month = %s
                    AND score_type = %s
                    AND id_type = %s
                    AND id = %s
                    AND brand_id = %s
                    '''


        try:
            self.f.execute(s, (self.questionnaire_id, self.year, self.month, self.score_type,
                                self.id_type, self.id,self.brand_id))
        except:
            success = False
        else:
            success = True

        return success


    def add(self, result_id, answer_value, score, occurences, base):
        '''add the specified score'''


        s = "INSERT INTO %s " % self.table
        s += """(questionnaire_id, year, month, score_type, id_type, id,brand_id, result_id, answer_value, score, occurences, base)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        try:
            self.f.execute(s, (self.questionnaire_id, self.year, self.month, self.score_type,
                                self.id_type, self.id, self.brand_id, result_id, answer_value,
                                score, occurences, base))
        except Exception, e:
            success = False
            print e
        else:
            success = True

        return success


class Own_Brand_Demense_scores( Brand_Demense_scores ):
    
    def set_table(self,**kwargs):
        self.brand_id = kwargs.get('brand_id', None)
        self.table = 'own_brand_demense_scores'

    def __repr__(self, ):
        return u'Brand_Demense_Score (%s): questionnaire_id=%s, year=%s, month=%s, score_type=%s, id_type=%s, id=%s, brand_id =%s, result_id=%s, answer_value=%s, score=%s, occurences=%s, base=%s' % (self.table, self.questionnaire_id, self.year, self.month, self.score_type, self.id_type, self.id, self.brand_id, self.result_id, self.answer_value, self.score, self.occurences, self.base)

#
# Arguably Brand_Demense_scores should derive from this, 
# but when it was frist made id -> demense_id and a new field
# was added for demense_id. 
#
# Ideally id -> brand_id and a new field added for demense_id,
# which is what this class does. WHich makes it more usefull.
#
class Demense_enabled_Scores(Scores):
    '''An ABC for score split by demense.'''

    def setup(self, *args, **kwargs ):
        self.demense_id = kwargs.get('demense_id', None)
        super(Demense_enabled_Scores,self).setup(*args,**kwargs)


    def __repr__(self, ):
        return self.__class__.__name__  + u' (%s): questionnaire_id=%s, year=%s, month=%s, score_type=%s, id_type=%s, id=%s, demense_id =%s, result_id=%s, answer_value=%s, score=%s, occurences=%s, base=%s' % (self.table, self.questionnaire_id, self.year, self.month, self.score_type, self.id_type, self.id, self.demense_id, self.result_id, self.answer_value, self.score, self.occurences, self.base)

    def all_keys(self, *args, **kwargs):
        'return True if all keys have been specified'

        return bool(
            self.questionnaire_id is not None and
            self.year is not None and
            self.month is not None and
            self.score_type is not None and
            self.id_type is not None and
            self.id is not None and
            self.demense_id is not None and
            self.result_id is not None and
            self.answer_value is not None 
            )
        


    def reset(self, ):

        self.questionnaire_id = None
        self.year = None
        self.month = None
        self.score_type = None
        self.id = None
        self.id_type = None
        self.result_id = None
        self.answer_value = None
        self.score = None
        self.occurences = None
        self.demense_id = None
        self.base = None

    def get(self, ):

        questionnaire_id, result_id, answer_value = self.trending_overrides(
            self.questionnaire_id, self.result_id, self.year)

        s = '''SELECT questionnaire_id, year, month, score_type, id_type,
                        id, demense_id, result_id, answer_value, score, occurences, base
                    FROM %s ''' % self.table
        s += '''WHERE questionnaire_id = %s
                    AND year = %s
                    AND month = %s
                    AND score_type = %s
                    AND id_type = %s
                    AND id = %s
                    AND demense_id = %s
                    AND result_id = %s
                    AND answer_value = %s'''

        self.f.execute(s, (questionnaire_id, self.year, self.month, self.score_type,
                            self.id_type, self.id, self.demense_id, result_id, answer_value))
        return self.f.fetchone()

    def load(self, *args, **kwargs ):

        row = self.get()

        if row:
            self.questionnaire_id = row[0]
            self.year = row[1]
            self.month = row[2]
            self.score_type = row[3]
            self.id_type = row[4]
            self.id = row[5]
            self.demense_id = row[6]
            self.result_id = row[7]
            self.answer_value = row[8]
            self.score = row[9]
            self.occurences = row[10]
            self.base = row[11]
        else:
            self.reset()

    def delete_set(self, ):
        '''delete the data for the current class attributes'''

        success = None

        s = "DELETE FROM %s " % self.table
        s += '''WHERE questionnaire_id = %s
                    AND year = %s
                    AND month = %s
                    AND score_type = %s
                    AND id_type = %s
                    AND id = %s
                    AND demense_id = %s
                    '''


        try:
            self.f.execute(s, (self.questionnaire_id, self.year, self.month, self.score_type,
                                self.id_type, self.id,self.demense_id))
        except:
            success = False
        else:
            success = True

        return success


    def add(self, result_id, answer_value, score, occurences, base):
        '''add the specified score'''


        s = "INSERT INTO %s " % self.table
        s += """(questionnaire_id, year, month, score_type, id_type, id,demense_id, result_id, answer_value, score, occurences, base)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        try:
            self.f.execute(s, (self.questionnaire_id, self.year, self.month, self.score_type,
                                self.id_type, self.id, self.demense_id, result_id, answer_value,
                                score, occurences, base))
        except Exception, e:
            success = False
            print e
        else:
            success = True

        return success


class Venue_category_scores(Scores):
    
    def set_table(self,**kwargs):
        self.table = 'venue_category_scores'

class Tradingbrand_Demense_scores(Demense_enabled_Scores):
    def set_table(self,**kwargs):
        self.table = 'tradingbrand_demense_scores'

class SDivision_Demense_scores(Demense_enabled_Scores):
    def set_table(self,**kwargs):
        self.table = 'division_demense_scores'

class Own_SDivision_Demense_scores(Demense_enabled_Scores):
    def set_table(self,**kwargs):
        self.table = 'own_division_demense_scores'


class Venue_category_demense_scores(Demense_enabled_Scores):
    
    def set_table(self,**kwargs):
        self.table = 'venue_category_demense_scores'


class Competitor_scores(Scores):

    def set_table(self,**kwargs):
        self.table = 'competitor_scores'


class Division_scores(Scores):

    def set_table(self,**kwargs):
        self.table = 'division_scores'



class VVUserGroups(Base):
    '''Pull in VV user_groups. We need these for user extracts for BDRC staff'''


    def __repr__(self, ):
        return u"%s: user_id=%s,   groups=%s" % (self.__class__.__name__, self.user_id, self.groups)

    def setup(self, *args, **kwargs):
   
        self.user_id = kwargs.get('user_id', None)
        self.groups = []

        if self.user_id:
            data = self.get(self.user_id)
        else:
            data = None

        if data:
            self.set(data)
        else:
            self.reset()


    def reset(self, ):
        self.groups = []


    def set(self, data):
        for row in data:
            self.groups.append(row[0])


    def get(self, user_id):

        s = """SELECT user_type
                FROM %s.user_groups""" % local.vv_schema
        s += " WHERE user_id=%s"
        self.f.execute(s, (self.user_id))
        rows = self.f.fetchall()
        return rows




class VenueExtras(Base):
    '''Free format client supplied addition info for their venues'''

    # when a venue doesn't have these details, we're to use a special default set
    default_venue_id = 1250

    def __repr__(self, ):
        return "%s: venue_id=%s, extras=%s" % (self.__class__.__name__, self.venue_id, self.extras)

    def setup(self, *args, **kwargs):
        self.venue_id = kwargs.get('venue_id', None)
        self.extras = {}

        if self.venue_id is None:
            self.reset_obj()
        else:
            self.set_obj()

    def reset_obj(self,):
        self.extras = {}

    def set_obj(self, ):
        self.reset_obj()

        s = """SELECT data_type_id, extras_values
                FROM venue_extras
                WHERE venue_id=%s"""
        self.f.execute(s, (self.venue_id))
        for data_type_id, extension_value in self.f.fetchall():
            self.extras[data_type_id] = extension_value


    def enquiry_types(self, ):

        items = {1: 1000, 2: 1001, 3: 1002}
        eqs = {1:2, 2:1, 3:1}
        for k in items.keys():
            eqs[k] = int(self.extras.get(items[k], eqs[k]))
        return eqs


    def delete_set(self, ):
        '''delete the data for the current class attributes'''

        success = None

        s = "DELETE FROM venue_extras WHERE venue_id=%s"

        try:
            self.f.execute(s, (self.venue_id))
        except:
            success = False
        else:
            success = True

        return success


    def update_set(self, ):
        '''replace the existing set of extras with what the obj has now'''
        
        success = False

        s = '''DELETE FROM venue_extras
                WHERE venue_id=%s'''
        self.f.execute(s, (self.venue_id))


        if self.extras:
            for k in self.extras.keys():
                s = '''INSERT INTO venue_extras
                        VALUES(%s, %s, %s)'''
                try:
                    self.f.execute(s, (self.venue_id, k, self.extras[k]))
                except:
                    success = False
                else:
                    success = True

        # else, no extras selected so we says successful
        else:
            success = True


        if success == True:
            self.d.commit()
        elif success == False:
            self.d.rollback()

        return success

    def venue_locked(self, ):
        '''Return True is venue is locked from venue admins'''
        return bool(self.extras.get(0, None) is not None)


class TData_Metaclass(type):
    def __iter__(self,):
        obj = self()
        for o in obj.get_all_obj(): yield o

class TrivialData(FactoryBase):
    '''Some data is so trivial and unchanging we don't need to put it in the database, just 
    a basic dictionary will be suffice. However, we want their objects to act like
    regular db tables rather than faffing around with dicts direct'''

    __metaclass__ = TData_Metaclass

    data = {}

    def __repr__(self, ):
        x = u"%s: id=%s,   description=%s" % (self.__class__.__name__, self.key_id, self.description)
        return x.encode('utf-8')

    def __init__(self, *args, **kwargs):

        self.key_id = kwargs.get('key_id', None)
        self.description = None

        self.setup()

    def setup(self, ):
        if self.key_id is None:
            self.description = None
        else:
            self.description = self.data.get(self.key_id, None)


    def get_all_obj(self, ):

        objs = []
        for key_id in self.data.keys():
            objs.append(self.factory(key_id=key_id))
        return objs

    def __hash__(self,):
        return hash(( self.__class__, self.key_id ,) )

    def __ne__(self,other):
        return not self.__eq__(other)

    def __eq__(self,other):
        """Test equivalence with either the key_id or a similir Trivaldata object"""
        return (self.__class__ == other.__class__ and
                self.key_id == other.key_id ) or (
                other.__class__ == self.key_id.__class__ and
                other == self.key_id )


class NamedTrivialData(TrivialData):
    def setup(self,):
        super(NamedTrivialData,self).setup()
        if self.key_id is not None:
            self.name = self.names[self.key_id]
            self.name_lc = self.names_lc[self.key_id]
    

class EnquiryType(NamedTrivialData):


    ##Negative numbers represent virtual only types.
    OVERALL_INC_SF = -4
    OVERALL = -3
    ANY_TELE = -2
    ELECTRONIC = -1

    TELEPHONE = 1
    RFP = 2
    EMAIL = 3
    SHORT_TELE = 4

    names  = [ None, 'TELEPHONE','RFP','EMAIL', 'SHORT_TELE',
            ## These must be at the end.
             "OVERALL_INC_SF" "OVERALL", "ANY_TELE", "ELECTRONIC"]

    #lower case varinsts are nicer for html classes
    names_lc = [ x and x.lower() for x in names ]

    data = { 
            OVERALL_INC_SF :"Overall inc Quick check",
            OVERALL : "Overall",
            ANY_TELE: 'Any Telephone',
            ELECTRONIC: 'Electronic',
            TELEPHONE: 'Telephone',
            RFP:   'RFP',
            EMAIL: 'e-Mail',
            SHORT_TELE: 'Short form Telephone',
    }

    members_data = {
        ANY_TELE: set( [TELEPHONE, SHORT_TELE]),
        ELECTRONIC: set([ RFP, EMAIL] ),
        OVERALL: set([TELEPHONE, EMAIL, RFP]),
        OVERALL_INC_SF: set([TELEPHONE, EMAIL, RFP, SHORT_TELE]),
    }

    # default questionnaire_ids for each enquiry type
    questionnaires = {TELEPHONE:16 , RFP:18, EMAIL: 17 }

    @classmethod
    def is_virtual(key_id):
        '''report if an enquirytype is virtual or not'''
        return key_id < 0   # -ve is virtual

    @property
    def vmembers(self,):
        if self.key_id >= 0:
            return set([self])
        else:
            return set( self.factory (key_id=x ) for x in self.members_data[self.key_id] )


    #
    # We could probably cache this on the class but I don't expect it
    # to be called very often.
    #
    @property
    def vmember_of(self,):
        if self.key_id < 0:
            return set([self])
        else:
            rv = set()
            ##Walk the membership lists to find which types we are a member of.
            for vtype, members in self.members_data.items():
                if self.key_id in members:
                    rv.add(self.factory(key_id = vtype) )

            return rv


    def quest2type(self, quests):
        '''convert list of questionnaire_ids to list of enquiry_types
        '''
        #
        # This function is deprecated the Questionnaire object
        # should be able to resolve this, via it's etype attribute.
        #

        from questionnaire import group_qsts
        enq_types = []
        for q_id in quests:
            if q_id in group_qsts.get('Telephone', []):
            #if q_id in (2, 7, 8):
                enq_type = self.TELEPHONE
            elif q_id in group_qsts.get('RFP', []):
            #elif q_id in (3, 9,):
                enq_type = self.RFP
            elif q_id in group_qsts.get('Email', []):
            #elif q_id == (4, 10,):
                enq_type = self.EMAIL
            else:
                continue
            enq_types.append(enq_type)
        return enq_types


class MeetingSize:
    '''Questionnaires have different meeting sizes available to them'''

    # define meeting_size_id values
    SMALL = 1
    MID = 2
    LARGE = 3
    TYPICAL = 4

    descriptions = {
        SMALL: 'Small',
        MID: 'Mid-Sized',
        LARGE: 'Large',
        TYPICAL: 'Typical Event Size',
    }


    def meeting_size_set(self, enquiry_type):

        if (enquiry_type == EnquiryType.RFP or
            enquiry_type == EnquiryType.EMAIL):
            return [self.SMALL, self.MID, self.TYPICAL,]
        elif enquiry_type == EnquiryType.TELEPHONE:
            return [self.SMALL, self.MID, self.LARGE, self.TYPICAL, ]
        else:
            return []



class EnquiryTarget(NamedTrivialData):
    # define enquiry targets - Eg things we are enquiring about.

    MEETINGS =0 
    SOCIAL = 1
    CENTRAL = 2
    GROUP = 3
    INDIV = 4
    LONG = 5
    AGENCY = 6
    HOSPITALITY = 7
    AGENCY_ACCOM = 8
    MATCHDAY = 9

    names  = [ 'MEETINGS','SOCIAL','CENTRAL','GROUP','INDIV',
               'LONG','AGENCY','HOSPITALITY' ,'AGENCY_ACCOM',
                'MATCHDAY' ,]

    #lower case varinsts are nicer for html classes
    names_lc = [ x.lower() for x in names ]

    data = { 
            MEETINGS: 'Meetings',
            SOCIAL: 'Social Events',
            CENTRAL: 'Central Desks',
            GROUP: 'Group Reservations',
            INDIV: 'Individual Reservations',
            LONG: 'Long Stay apartments',
            AGENCY: 'Agency',
            AGENCY_ACCOM: 'Agency Accommodation',
            HOSPITALITY: 'Hospitality',
            MATCHDAY: 'Match day',
        }



class EventNature(TrivialData):

    # define event_nature_ids
    data = { 1: 'Senior Management',
             2: 'Departmental Meeting',
             3: 'Sales Meeting',
             4: 'Client Meeting',
             5: 'Graduate Training',
             6: 'Exec Development Workshop',
             7: 'Corporate Learning Day',
             8: 'Team Building Event',
             9: 'Product Launch',
             10:'Conference',
             11:'Policy Group Presentation',
             12:'Annual Middle Managers Meeting',
             13:'value taken from venue extras',
    }


    def is_typical(self, event_nature_id=None):
        '''return True/False according to whether the event nature is TYPICAL'''
        if event_nature_id is None:
            event_nature_id = self.key_id
        return bool(event_nature_id == 13)

    def nature_set(self, meeting_size_id):

        if meeting_size_id == MeetingSize.SMALL:
            return [1, 2, 3, 4,]
        elif meeting_size_id == MeetingSize.MID:
            return [5, 6, 7, 8,]
        elif meeting_size_id == MeetingSize.LARGE:
            return [9, 10, 11, 12,]
        elif meeting_size_id == MeetingSize.TYPICAL:
            return [13, ]
        else:
            return []


class SpecialRequestOLD:

    # define requests:
    # id: enquiry types, description
    requests = {
        1: 'What can you offer in the way of hot snacks?', 
        2: 'What options do you have for an all vegetarian lunch?',
        3: 'Could you please give me an honest assessment of how well your venue deals with disabled delegates',
        4: 'We have a number of Chinese delegates joining the session mid morning. How would you advise we deal with signage and meet and greet?',
        5: 'How would you deal with security? We have had issues in the past especially during breaks.',
        6: 'Can you give me some information about your environmental credentials?',
        7: 'Can you tell me what vodaphone/orange/t-mobile coverage is like in the meeting room?',
        8: 'What can you tell me about your video/remote conferencing capabilities?',
        9: 'Please could you talk me through your cancellation terms and conditions?',
        10:'Can you make any recommendations on the best options for evening entertainment?',
        11:'We are probably going to have a large amount of printing/photocopying throughout the meeting. What facilities do you have on site to deal with this?',
        12:'Can you tell me what quality assurance procedures the venue has in place?',
        13:'A quiet environment is going to be imperative to the success of the event. Can you offer any reassurances about noise levels?',
        14:'Please could you give me some information regarding the possibility of break out facilities.It is not something I want to book at present but there is a chance we may wish to add this to the booking at a later date.',
    }

    RFP = EnquiryType.RFP
    EMAIL = EnquiryType.EMAIL
    TELEPHONE = EnquiryType.TELEPHONE

    request_events = {
        1: [TELEPHONE, RFP, EMAIL, ],
        2: [TELEPHONE, RFP, EMAIL, ],
        3: [TELEPHONE, RFP, EMAIL, ],
        4: [TELEPHONE, RFP, EMAIL, ],
        5: [TELEPHONE, RFP, EMAIL, ],
        6: [TELEPHONE, RFP, EMAIL, ],
        7: [TELEPHONE, RFP, EMAIL, ],
        8: [TELEPHONE, RFP, EMAIL, ],
        9: [TELEPHONE, ],
        10:[TELEPHONE, RFP, EMAIL, ],
        11:[TELEPHONE, RFP, EMAIL, ],
        12:[TELEPHONE, RFP, EMAIL, ],
        13:[TELEPHONE, ],
        14:[TELEPHONE, ],
    }   

    def __repr__(self, ):
        return u"%s: id=%s,   enquiry_types=%s,   description=%s" % (self.__class__.__name__, self.special_request_id, self.enquiry_types, self.description)
    
    def __init__(self, *args, **kwargs):

        self.special_request_id = kwargs.get('special_request_id', None)

        self.description = None
        self.enquiry_types = []

        self.setup()

    def setup(self, ):
        if self.special_request_id is None:
            self.description = None
            self.enquiry_types = []
        else:
            self.description = SpecialRequest.requests.get(self.special_request_id, None)
            self.enquiry_types = SpecialRequest.request_events.get(self.special_request_id, [])

    def electronic_set(self, ):
        '''return ids for specified enquiry type'''
        x = []
        for k in self.request_events.keys():
            if self.RFP in self.request_events[k] or self.EMAIL in self.request_events[k]:
                x.append(k)
        return x


    def tele_set(self, ):
        '''return ids for specified enquiry type'''
        x = []
        for k in self.request_events.keys():
            if self.TELEPHONE in self.request_events[k]:
                x.append(k)
        return x


class SpecialRequest(Base):

    # define requests:
    # id: enquiry types, description
    requests = {}

    RFP = EnquiryType.RFP
    EMAIL = EnquiryType.EMAIL
    TELEPHONE = EnquiryType.TELEPHONE

    request_events = {}   


    def __repr__(self, ):
        return u"%s: id=%s,   enquiry_types=%s,   description=%s" % (self.__class__.__name__, self.special_request_id, self.enquiry_types, self.description)
    
    def setup(self, *args, **kwargs):

        self.table = 'special_requests'
        self.reset_obj()
        self.special_request_id = kwargs.get('special_request_id', None)

        self.load_all()

        if self.special_request_id is not None:
            self.set_obj()



    def reset_obj(self,):
        self.special_request_id = None
        self.description = None
        self.enquiry_types = []



    def get(self, special_request_id):
        s = """SELECT special_request_id, special_request_description
                FROM %s""" % self.table
        s += " WHERE special_request_id=%s"

        self.f.execute(s, (special_request_id,))
        return self.f.fetchone()

    def set_obj(self, ):

        data = self.get(self.special_request_id)
    
        if data:
            self.special_request_id = data[0]
            self.description = data[1]
            self.enquiry_types = self.request_events.get(self.special_request_id, [])
        else:
            self.reset_obj()


    def update(self, ):
       
##        if type(self.description) == unicode:
##            description = self.description.encode('utf-8')
##        else:
##            description = self.description
        description = self.description
        
        if self.get(self.special_request_id):
            s = "UPDATE %s" % self.table
            s += """ SET special_request_description=%s
                    WHERE special_request_id=%s"""
            args = (description, self.special_request_id)
            success, exception_text = self.do_transaction(sql=s, args=args)
        else:
            s = "INSERT INTO %s" % self.table
            s += """ (special_request_description)
                    VALUES(%s)"""
            args = (description,)
            success, exception_text = self.do_transaction(sql=s, args=args)
            if success:
                self.special_request_id = self.last_insert_id()


        # now store the enquiry_types
        s = "DELETE FROM special_request_events WHERE special_request_id=%s"
        self.f.execute(s, self.special_request_id)

        for enq_type in self.enquiry_types:
            s = "INSERT into special_request_events VALUES(%s, %s)"
            try:
                self.f.execute(s, (self.special_request_id, enq_type))
            except:
                success = False
                exception_text = 'special_request_events update failed'
                break
            else:
                success = True
        if success:
            self.d.commit()
        else:
            self.rollback()
        return success, exception_text


    def load_all(self, ):
        '''load all into dict'''
        self.requests = {}
        s = '''SELECT special_request_id, special_request_description
                FROM %s''' % self.table
        self.f.execute(s)
        for special_request_id, description in self.f.fetchall():
            self.requests[special_request_id] = description

        # now load the event types the request is linked to for batch event creation
        self.request_events = {}
        for k in self.requests.keys():
            s = """SELECT special_request_id, special_request_event_id
                    FROM special_request_events
                    WHERE special_request_id=%s"""
            ids = []
            self.f.execute(s, (k,))
            for sr_id, sr_e_id in self.f.fetchall():
                ids.append(sr_e_id)
            self.request_events[k] = ids


    def desc_used(self, description, **kwargs):
        '''return True is the specified description has been used. When using from 
        maintenance, pass in the special_request_id so it can be excluded from the check'''
       
##        if type(description) == unicode:
##            description = description.encode('utf-8')

        exclude_id = kwargs.get('exclude_id', None)
       
        if exclude_id:
            s = """SELECT special_request_id FROM special_requests WHERE special_request_description=%s AND special_request_id <> %s"""
            self.f.execute(s, (description, exclude_id))
        else:
            s = """SELECT special_request_id FROM special_requests WHERE special_request_description=%s"""
            self.f.execute(s, (description,))
        return bool(self.f.fetchone())



    def electronic_set(self, ):
        '''return ids for specified enquiry type'''
        x = []
        for k in self.request_events.keys():
            if self.RFP in self.request_events[k] or self.EMAIL in self.request_events[k]:
                x.append(k)
        return x


    def tele_set(self, ):
        '''return ids for specified enquiry type'''
        x = []
        for k in self.request_events.keys():
            if self.TELEPHONE in self.request_events[k]:
                x.append(k)
        return x


class DisputeNature(TrivialData):
    data = {
        1: u'The Connection Process',
        2: u'Service Delivery - General',
        3: u'Service Delivery - Critical Success Factor',
        4: u'Manner and Approach - General',
        5: u'Manner and Approach - Special Request',
        6: u'Follow Up - Speed of Delivery (including non-receipt of follow up information)',
        7: u'Follow Up - General Content',
        8: u'Telephone Follow Up',
        9: u'Other',
    }



class WorkingTimeZone(TrivialData):
    data = {
        1: u'T1 (Americas/Carribean)',
        2: u'T2 (EMEA)',
        3: u'T3 (India/Sri Lanka)',
        4: u'T4 (HK, CN, JP)',
        5: u'T5 (OZ,NZ,Fiji)',
    }

    def overlaps(self, other):
        try: othercode = int(other)
        except TypeError: othercode = other.key_id

        if self.key_id == 1:
            return othercode in ( 1 ,2 ,)
        if self.key_id == 2:
            return othercode in ( 1 , 2 , 3 , 4)
        if self.key_id == 3:
            return othercode in ( 2, 4,)
        if self.key_id == 4:
            return othercode in ( 2  , 3, 4 ,)
        if self.key_id == 5:
            return othercode in ( 4 , 5)

    def dropdown(self,*args,**kwargs):
        opts = [ (None, "--Please select--" ) ]
        opts += self.data.items()
        return common.make_simple_dropdown(opts,*args,**kwargs)

class DisputeNatureEnqs:
    RFP = EnquiryType.RFP
    EMAIL = EnquiryType.EMAIL
    TELEPHONE = EnquiryType.TELEPHONE
    ALL = -1
    data = {
        1: [TELEPHONE,], 
        2: [TELEPHONE,], 
        3: [TELEPHONE,], 
        4: [TELEPHONE,], 
        5: [TELEPHONE,], 
        6: [TELEPHONE, EMAIL, RFP], 
        7: [TELEPHONE, EMAIL, RFP], 
        8: [TELEPHONE, EMAIL, RFP], 
        9: [ALL], 
    }

    def natures_for_quest(self, questionnaire_id):
        '''return dispute natures for specified questionnaire type'''
        dns = DisputeNature()
        et = EnquiryType()
        enq_type = et.quest2type([questionnaire_id])

        objs = []
        for dn in dns.get_all_obj():
            if [x for x in enq_type if x in self.data.get(dn.key_id, [None])] or self.ALL in self.data.get(dn.key_id,[]):
                objs.append(dn)
        return objs

    def selection_list(self, questionnaire_id, form, natures_prefix, section_exts):
        '''return checkbox selection list'''

        x = [u'<ul>']
        for dn in self.natures_for_quest(questionnaire_id):
            desc = dn.description + section_exts.get(dn.key_id, '')
            label = '%s%d' % (natures_prefix, dn.key_id)
            selected = ['','checked'][int(label in form.keys())]
            x.append(u'''
                    <li><input type="checkbox" name="%(label)s" id="%(label)s" value="y" %(selected)s><label for="%(label)s">%(desc)s</label>
                    ''' % locals())
        x.append(u'</ul>')
        return ''.join(x)

        

class LeadTime(TrivialData):

    data = {  1: '5-6 weeks', 
              2: '6 weeks - 3 months', 
              3: '3-8 months',
              4: '8-12 months',
              5: 'value taken from venue extras',
    }

    def lead_time_set(self, meeting_size_id):

        if meeting_size_id == MeetingSize.SMALL:
            return [1, 2, 3, ]
        elif meeting_size_id == MeetingSize.MID:
            return [1, 2, 3, ]
        elif meeting_size_id == MeetingSize.LARGE:
            return [2, 3, 4, ]
        elif meeting_size_id == MeetingSize.TYPICAL:
            return [5, ]
        else:
            return []


    def is_typical(self, meeting_size_id):
        '''return True/False according to whether the meeting_size_id is TYPICAL'''
        return bool(meeting_size_id == 5)



class Angle(TrivialData):

    data = {  1: 'Please negotiate on rates as far as possible.',
              2: 'Please raise the fact that you have also contacted $VENUE1 or $VENUE2. What are the benefits of your venue over and above this venue?',
    }


    def next_angle(self, current_angle):
        if current_angle == 1:
            return 2
        else:
            return 1


class MysteryShopper(TrivialData):

    data = {  1: 'Shopper 1',
              2: 'Shopper 2',
              3: 'Shopper 3',
              4: 'Shopper 4',
              5: 'Shopper 5',
    }

    def mystery_shopper_set(self, ):

        return self.data.keys()




class EventExtension(Base):

    def __repr__(self, ):
        return u"%s: event_id=%s,   meeting_size_id=%s,  lead_time_id=%s" % (self.__class__.__name__, self.event_id, 
                    self.meeting_size_id, self.lead_time_id)


    def setup(self, *args, **kwargs ):
        
        self.event_id = kwargs.get('event_id', None)
        self.meeting_size_id = kwargs.get('meeting_size_id', None)
        self.lead_time_id = kwargs.get('lead_time_id', None)
        self.nature_of_event_id = kwargs.get('nature_of_event_id', None)
        self.special_request_id = kwargs.get('special_request_id', None)
        self.angle_id = kwargs.get('angle_id', None)
        self.mystery_shopper_id = kwargs.get('mystery_shopper_id', None)
        self.mystery_identity_id = kwargs.get('mystery_identity_id', None)
        self.assignee_id = kwargs.get('assignee_id', None)
        self.enquiry_question_id = kwargs.get('enquiry_question_id', None)

        if self.event_id is not None:
            self.load()
        else:
            self.reset()


    def reset(self, ):
        self.event_id = None
        self.meeting_size_id = None
        self.lead_time_id = None
        self.nature_of_event_id = None
        self.special_request_id = None
        self.angle_id = None
        self.mystery_shopper_id = None
        self.mystery_identity_id = None
        self.assignee_id = None
        self.enquiry_question_id = None

    def get(self, event_id):

        s = '''SELECT event_id, meeting_size_id, lead_time_id, nature_of_event_id, 
                        special_request_id, angle_id, mystery_shopper_id, mystery_identity_id,
                        user_id,enquiry_question_id
                FROM event_extension
                WHERE event_id=%s'''

        self.f.execute(s, (event_id, ))
        return self.f.fetchone()

    def load(self, ):
        row = self.get(self.event_id)

        if row:
            self.event_id = row[0]
            self.meeting_size_id = row[1]
            self.lead_time_id = row[2]
            self.nature_of_event_id = row[3]
            self.special_request_id = row[4]
            self.angle_id = row[5]
            self.mystery_shopper_id = row[6]
            self.mystery_identity_id = row[7]
            self.assignee_id = row[8]
            self.enquiry_question_id = row[9]
        else:
            self.reset()


    def update(self, ):
        if self.get(self.event_id):
            s = """UPDATE event_extension
                    SET meeting_size_id=%s,
                        lead_time_id=%s,
                        nature_of_event_id=%s,
                        special_request_id=%s,
                        angle_id=%s,
                        mystery_shopper_id=%s,
                        mystery_identity_id=%s,
                        user_id=%s,
                        enquiry_question_id=%s
                    WHERE event_id=%s"""
            args = (self.meeting_size_id, self.lead_time_id, self.nature_of_event_id, self.special_request_id,
                    self.angle_id, self.mystery_shopper_id, self.mystery_identity_id, self.assignee_id,
                    self.enquiry_question_id, self.event_id)
            success, exception_text = self.do_transaction(sql=s, args=args)

        else:
            s = """INSERT INTO event_extension
                    (event_id, meeting_size_id, lead_time_id, nature_of_event_id, special_request_id,
                        angle_id, mystery_shopper_id, mystery_identity_id, user_id, enquiry_question_id)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            args = (self.event_id, self.meeting_size_id, self.lead_time_id, self.nature_of_event_id, self.special_request_id,
                    self.angle_id, self.mystery_shopper_id, self.mystery_identity_id, self.assignee_id, self.enquiry_question_id, )
            success, exception_text = self.do_transaction(sql=s, args=args)

        return success, exception_text


class Ranks(Base):

    def setup(self, *args, **kwargs ):
        
        self.questionnaire_id = kwargs.get('questionnaire_id', None)
        self.grouping_level = kwargs.get('grouping_level', None)
        self.score_type = kwargs.get('score_type', None)
        self.ranking_brand = kwargs.get('ranks_for_brand', None)
        self.demense_id = kwargs.get('demense_id', None)
        self.id = kwargs.get('id', None)
        self.id_type = kwargs.get('id_type', None)
        self.year = kwargs.get('year', None)
        self.month = kwargs.get('month', None)
        self.result_id = kwargs.get('result_id', None)
        self.answer_value = kwargs.get('answer_value', None)

        self.rank = None
        self.set_size = None
        self.equals = None

        self.set_mode = kwargs.get('set_mode', None)
        # set table name, because we're using this for multiple score tables
        self.set_table()


        # when set_mode is set, we don't attempt load data or reset attributes
        if not self.set_mode:
            # if all key criteria has been specified, set up the data otherwise
            # reset attributes to None
            if self.all_keys(**kwargs):
                self.load()
            else:
                self.reset()

    def set_table(self,):
        pass


    def __repr__(self, ):
        return u'Rank (%s): questionnaire_id=%s, grouping_level=%s, score_type=%s, id=%s, id_type=%s, year=%s, month=%s, result_id=%s, answer_value=%s, rank=%s, set_size=%s, equals=%s' % (self.table, self.questionnaire_id, self.grouping_level, self.score_type, self.id, self.id_type, self.year, self.month, self.result_id, self.answer_value, self.rank, self.set_size, self.equals)

    def all_keys(self, *args, **kwargs):
        'return True if all keys have been specified'

        return bool(
            self.questionnaire_id is not None and
            self.grouping_level is not None and
            self.score_type is not None and
            self.ranking_brand is not None and
            self.demense_id is not None and
            self.id_type is not None and
            self.id is not None and
            self.year is not None and
            self.month is not None and
            self.result_id is not None and
            self.answer_value is not None
            )
        


    def reset(self, ):
        self.questionnaire_id = None
        self.grouping_level = None
        self.score_type = None
        self.ranking_brand = None
        self.demense_id = None
        self.id = None
        self.id_type = None
        self.year = None
        self.month = None
        self.result_id = None
        self.answer_value = None
        self.rank = None
        self.set_size = None
        self.equals = None


    def get(self, ):

        s = '''SELECT questionnaire_id, ranks_for_brand,demense_id, grouping_level, score_type, id, id_type, 
                        year, month, result_id, answer_value, rank, set_size, equals
                    FROM %s ''' % self.table
        s += '''WHERE questionnaire_id = %s
                    AND ranks_for_brand = %s
                    AND demense_id = %s
                    AND grouping_level = %s
                    AND score_type = %s
                    AND id = %s
                    AND id_type = %s
                    AND year = %s
                    AND month = %s
                    AND result_id = %s
                    AND answer_value = %s'''

        self.f.execute(s, (self.questionnaire_id, self.ranking_brand, self.demense_id , 
                            self.grouping_level, self.score_type,
                            self.id, self.id_type, self.year, self.month, 
                            self.result_id, self.answer_value))
        return self.f.fetchone()

    def load(self, ):

        row = self.get()

        if row:
            self.questionnaire_id = row[0]
            self.ranking_brand = row[1]
            self.demense_id = row[2]
            self.grouping_level = row[3]
            self.score_type = row[4]
            self.id = row[5]
            self.id_type = row[6]
            self.year = row[7]
            self.month = row[8]
            self.result_id = row[9]
            self.answer_value = row[10]
            self.rank = row[11]
            self.set_size = row[12]
            self.equals = row[13]
        else:
            self.reset()


    def fmt_rank(self, *args, **kwargs):
        '''return formatted rank output according to current business rules'''

        table_cell = kwargs.get('table_cell', False)

        rank = [self.rank,'tbc'][int(self.rank is None)]
        if rank != 'tbc':
            rank = common.add_ordinal(rank)
            if self.equals > 1:
                rank += ' ='
        else:
            rank = '<span class="comment">%s</span>' % rank

        if table_cell:
            return '<td class="l">%(rank)s</td>' % locals()
        else:
            return rank


class BrandRanks(Ranks):
    
    def set_table(self,):
        self.table = 'brand_demense_ranks'




class Ranks3(Ranks):

    def setup(self, *args, **kwargs ):
        
        self.cluster_entry = kwargs.get('cluster_entry', None)
        super(Ranks3,self).setup(*args,**kwargs)

    def __repr__(self, ):
        return u'%s (%s): questionnaire_id=%s, grouping_level=%s, score_type=%s, cluster_entry=%s, id=%s, id_type=%s, year=%s, month=%s, result_id=%s, answer_value=%s, rank=%s, set_size=%s, equals=%s' % (self.__class__.__name__, self.table, self.questionnaire_id, self.grouping_level, self.score_type, self.cluster_entry, self.id, self.id_type, self.year, self.month, self.result_id, self.answer_value, self.rank, self.set_size, self.equals)

    def all_keys(self, *args, **kwargs):
        'return True if all keys have been specified'

        return ( super(Ranks3,self).all_keys() and
            self.cluster_entry is not None
            )
        


    def reset(self, ):
        super(Ranks3,self).reset()
        self.cluster_entry = None

    def get(self, ):

        s = '''SELECT questionnaire_id,   ranks_for_brand,demense_id,grouping_level, score_type, cluster_entry,
                        demense_id, id, id_type, 
                        year, month, result_id, answer_value, rank, set_size, equals
                    FROM %s ''' % self.table
        s += '''WHERE questionnaire_id = %s
                    AND ranks_for_brand = %s
                    AND demense_id = %s
                    AND grouping_level = %s
                    AND score_type = %s
                    AND cluster_entry = %s
                    AND id = %s
                    AND id_type = %s
                    AND year = %s
                    AND month = %s
                    AND result_id = %s
                    AND answer_value = %s'''

        self.f.execute(s, (self.questionnaire_id, self.ranking_brand, self.demense_id , 
                            self.grouping_level, self.score_type, self.cluster_entry,
                            self.id, self.id_type, self.year, self.month, 
                            self.result_id, self.answer_value))
        return self.f.fetchone()

    def load(self, ):

        row = self.get()

        if row:
            self.questionnaire_id = row[0]
            self.ranking_brand = row[1]
            self.demense_id = row[2]
            self.grouping_level = row[3]
            self.score_type = row[4]
            self.cluster_entry = row[5]
            self.demense_id = row[6]
            self.id = row[7]
            self.id_type = row[8]
            self.year = row[9]
            self.month = row[10]
            self.result_id = row[11]
            self.answer_value = row[12]
            self.rank = row[13]
            self.set_size = row[14]
            self.equals = row[15]
        else:
            self.reset()


    def fmt_rank(self, *args, **kwargs):
        '''return formatted rank output according to current business rules'''

        table_cell = kwargs.get('table_cell', False)

        rank = [self.rank,'tbc'][int(self.rank is None)]
        if rank != 'tbc':
            rank = common.add_ordinal(rank)
            if self.equals > 1:
                rank += ' ='
        else:
            rank = '<span class="comment">%s</span>' % rank

        if table_cell:
            return '<td class="l">%(rank)s</td>' % locals()
        else:
            return rank


class VenueClusterRanks(Ranks3):
    
    def set_table(self,):
        self.table = 'venue_and_cluster_demense_ranks'



class RankBucket(Base):
    '''simple obj to handle ranking work file'''

    def setup(self, ):
        pass

    def empty(self, ):
        '''delete all of the work data'''

        success = None

        s = "DELETE FROM rank_bucket"

        try:
            self.f.execute(s, )
        except Exception, e:
            success = False
        else:
            success = True

        if success == True:
            self.d.commit()
        elif success == False:
            self.d.rollback()

        return success


    def load_bucket_national(self, questionnaire_id, year, month, score_type, id_type,
                        result_id, answer_value, cluster_entry, minimum_base, brand, demenses ) :


        #Stringfy for SQL
        demenses = ",".join(map(str,demenses))

        if cluster_entry == 'N':
            s = """INSERT INTO rank_bucket
                SELECT id, score, '%(cluster_entry)s'
                FROM venue_scores JOIN venues ON (id=venue_id)
                LEFT JOIN brands USING (brand_id)
                WHERE cluster_id IS NULL  
                   and ( brand_id != %(brand)s OR secret IS NULL )
                    AND stealth_mode IS NULL
                    AND demense_id in ( %(demenses)s )""" % locals()
        else:
            s = """INSERT INTO rank_bucket
                SELECT id, score, '%(cluster_entry)s'
                FROM cluster_scores JOIN clusters ON (id=cluster_id)
                WHERE 1=1 """ % locals()


        s += """ AND questionnaire_id=%s
                    AND year=%s
                    AND month=%s
                    AND score_type=%s
                    AND id_type=%s
                    AND result_id=%s
                    AND answer_value=%s
                    AND base >=%s"""

        self.f.execute(s, (questionnaire_id, year, month, score_type, id_type, 
                            result_id, answer_value, minimum_base))
        self.d.commit()


    def load_bucket_brand(self, questionnaire_id, year, month, score_type, id_type,
                        result_id, answer_value, cluster_entry, minimum_base, brand_id):


        if cluster_entry == 'N':
            s = """INSERT INTO rank_bucket
                    SELECT id, score, '%(cluster_entry)s'
                        FROM venue_scores JOIN venues ON (id=venue_id)
                        WHERE cluster_id IS NULL
                         AND  secret IS NULL
                    """ % locals()
        else:
            s = """INSERT INTO rank_bucket
                SELECT DISTINCT id, score, '%(cluster_entry)s'
                FROM cluster_scores JOIN clusters ON (id=cluster_id)
                    JOIN venues USING (cluster_id)
                    WHERE cluster_id IS NOT NULL""" % locals()


        s += """ AND questionnaire_id=%s
                    AND year=%s
                    AND month=%s
                    AND score_type=%s
                    AND id_type=%s
                    AND result_id=%s
                    AND answer_value=%s
                    AND brand_id=%s
                    AND delete_date IS NULL
                    AND base >=%s"""

        self.f.execute(s, (questionnaire_id, year, month, score_type, id_type,
                            result_id, answer_value, brand_id, minimum_base))
        rows = self.f.fetchall()
        self.d.commit()


    def load_bucket_competitor(self, questionnaire_id, year, month, score_type, id_type,
                        result_id, answer_value, cluster_entry, minimum_base, ids, brand):

#         and ( brand_id != %(brand)s OR secret IS NULL )

        if cluster_entry == 'N':
            s = """INSERT INTO rank_bucket
                    SELECT id, score, '%(cluster_entry)s'
                        FROM venue_scores JOIN venues ON (id=venue_id)
                        LEFT JOIN brands USING (brand_id)
                        WHERE cluster_id IS NULL
                         and ( brand_id != %(brand)s OR secret IS NULL )
                            AND stealth_mode IS NULL""" % locals()
        else:
            s = """INSERT INTO rank_bucket
                SELECT DISTINCT id, score, '%(cluster_entry)s'
                FROM cluster_scores JOIN clusters ON (id=cluster_id)
                    JOIN venues USING (cluster_id)
                    LEFT JOIN brands USING (brand_id)
                    WHERE cluster_id IS NOT NULL
                        AND stealth_mode IS NULL""" % locals()


        s += """ AND questionnaire_id=%s
                    AND year=%s
                    AND month=%s
                    AND score_type=%s
                    AND id_type=%s
                    AND result_id=%s
                    AND answer_value=%s"""
        s += '      AND id IN (%s)' % ids
        s += """    AND delete_date IS NULL
                    AND base >=%s"""

        self.f.execute(s, (questionnaire_id, year, month, score_type, id_type,
                            result_id, answer_value, minimum_base))
        rows = self.f.fetchall()
        self.d.commit()



    def sort_bucket(self, ordering):

        s = """SELECT id, score, cluster_entry
                FROM rank_bucket
                ORDER BY score %(ordering)s""" % locals()
        self.f.execute(s)
        return self.f.fetchall()

#-------------------------------------------------------------------------------
class PropertyAccess(Base):

    def setup(self, *args, **kwargs):


        self.me = kwargs.get('me', None)

        self.grant_access = False
        self.brand_id = kwargs.get('brand_id', None)
        self.select_venue = None
        self.venue_level_user = False
        self.user_vens = []

    def check_property(self, select_venue, **kwargs):
        import user_types as ut
        import brand
        import venue

        self.select_venue = select_venue
        self.grant_access = ut.bdrc_admin(self.me.groups)
    
        # if no access, check brand level
        if not self.grant_access:
            import user_brands
            ub = user_brands.User_brand(self.d, user_id=self.me.user_id)
    
            # if the user is linked to a brand, force the brand
            if ub.brand_id is not None:
                self.brand_id = ub.brand_id
                self.grant_access = True
    
    
    
        # if no access, check venue level
        self.venue_level_user = False
        if not self.grant_access:
            import user_venues
            uv = user_venues.User_venues(dbConnection=self.d, f=self.f, user_id=self.me.user_id)
            self.user_vens = uv.get_all_obj(self.me.user_id)
            if self.user_vens:
                ven = venue.Venue(self.d, self.user_vens[0].venue_id)
                self.brand_id = ven.brand_id   # force brand to be from linked venue
                self.venue_level_user = True
                # override property with single venue if they're coming in with brand option
                if select_venue in ('ALL','Own','Competitors'):
                    self.select_venue = ven.venue_id
    

        # we have brand and some form or selected property, ensure user has access
        # to them
        if self.venue_level_user:
            if not ven.check_venue(self.select_venue, self.me.user_id, groups=self.me.groups,**kwargs):
                common.dm('Venue access security violation')
    
        else:
            b = brand.Brand(self.me.d, self.brand_id)
            if not b.check_brand(b.brand_id, self.me.user_id, self.me.groups):
                common.dm('Brand access security violation')
     
        # if we get here, access is fine 
        self.grant_access = True


    def property_dropdown(self, pre_select, *args, **kwargs):
        '''return property selection dropdown'''

        inc_all_venues = kwargs.get('inc_all_venues', False)

        # match_ are used to add addition texts to the dropdown selection
        # if the venue_id is in the match_set list. I.e. "NEW" for showing
        # new feedback reports against each venue
        label = kwargs.get('label', 'Venue')
        match_label = kwargs.get('match_label', '?')
        match_set = kwargs.get('match_set', {})
        inc_competitor_venues = kwargs.get('inc_competitor_venues', False)

        import venue
        vens = []
        comptvens = []
        opts = []
        if self.venue_level_user:
            for user_ven in self.user_vens:
                # only include active venues
                v2 = venue.Venue(self.me.d, user_ven.venue_id, f=self.f)
                if v2.delete_date is None:
                    vens.append(v2)
        else:
            ven = venue.Venue(self.me.d, None, f=self.f)

            for v in ven.iter_user_venues_for_brand(self.brand_id,self.me.user_id):
                vens.append(venue.Venue(self.me.d, v[0], f=self.f))

            ven_ids = [ v.venue_id for v in vens ]
            for v in  ven.get_user_venues(self.me.user_id):
                if v[0] not in ven_ids:
                    vens.append(venue.Venue(self.me.d, v[0], f=self.f))


        # include venues for PDF Competitors
        if inc_competitor_venues:
            import competitor_venues
            cv=competitor_venues.PDF_Competitor_venues(self.me.d, None)

            ven_ids = [ v.venue_id for v in vens ]

            if len(ven_ids) > 0:
                for v in cv.get_all_comp_venues(ven_ids):
                    comptvens.append(venue.Venue(self.me.d, v[0], f=self.f))


        def add_vens(vens):
            for v in common.sorted_by_attr(vens, 'venue_name'):
                venue_name = v.venue_name
                if v.venue_id in match_set:
                    venue_name += match_set[v.venue_id]
                opts.append((v.venue_id, venue_name))


        if inc_all_venues and not self.venue_level_user:
            opts.append(('ALL', 'All'))

        if inc_competitor_venues and len(comptvens) > 0 :
            opts.append(('Own', 'All Own Brand'))
            opts.append(('Competitors', 'All Brand Competitors'))
            opts.append(('Own', '------------------------ Own Brand ------------------------'))
            add_vens(vens)
            opts.append(('Competitors', '---------------------- Brand Competitors ----------------------'))
            add_vens(comptvens)
        else:
            add_vens(vens)

        return common.make_simple_dropdown(opts, pre_select, 'v', label, **kwargs)
    

class Dispute(Base):
    '''Status: Open, Review, Failed, Success'''
    OPEN_STATUS = 'O'
    CLOSED_STATUS = 'C'
    PENDING_STATUS = 'P'

    status_texts = {
        OPEN_STATUS: u'Open',
        CLOSED_STATUS: u'Closed',
        PENDING_STATUS: u'Pending',

    }

    successful_texts = {
        'Y': u'Successful',
        'N': u'Unsuccessful',
    }

    def __repr__(self, ):
        return u"%s: query_id=%s, event_id=%s, status=%s, successful_claim=%s" % (self.__class__.__name__, 
            self.query_id, self.event_id, self.status, self.successful_claim)


    def setup(self, *args, **kwargs):

        query_id = kwargs.get('query_id', None)
        event_id = kwargs.get('event_id', None)

        self.table = 'disputes'

        self.query_id = None
        self.event_id = None
        self.status = None
        self.successful_claim = None

        if query_id is not None:
            data = self.get(query_id)
        elif event_id is not None:
            data = self.get_by_event(event_id)
        else:
            data = None

        if data:
            self.setdata(data)
        else:
            self.reset()

    def status_text(self, status):
        '''return status text'''
        return self.status_texts.get(status, 'unknown %s' % status)

    def successful_text(self, successful_claim):
        '''return status text'''
        return self.successful_texts.get(successful_claim, '')

    def open_status(self, ):
        return ( self.status in (self.OPEN_STATUS , self.PENDING_STATUS ) )

    def reset(self, ):
        self.query_id = None
        self.event_id = None
        self.status = None
        self.successful_claim = None


    def setdata(self, data):
        self.query_id = data[0]
        self.event_id = data[1]
        self.status = data[2]
        self.successful_claim = data[3]


    def get(self, query_id, ):
        if query_id is None:
            return None
        s = """SELECT query_id, event_id, status, successful_claim
                FROM disputes
                WHERE query_id=%s """ 
        self.f.execute(s, (query_id, ))
        row = self.f.fetchone()
        return row


    def get_by_event(self, event_id, ):
        if event_id is None:
            return None
        s = """SELECT query_id, event_id, status, successful_claim
                FROM disputes
                WHERE event_id=%s """ 
        self.f.execute(s, (event_id, ))
        row = self.f.fetchone()
        return row

#--------------
    def update(self, ):
        
        success = None
        update = self.get(self.query_id)

        if update:
            s = """UPDATE disputes
                SET event_id=%s, status=%s, successful_claim=%s
                WHERE query_id=%s""" 
            success, err = self.do_transaction(sql=s, args=[self.event_id, 
                           self.status, self.successful_claim, self.query_id, ], group_commit=True)

        else:
            s = """INSERT INTO disputes (query_id, event_id, status, successful_claim) 
                    VALUES(%s, %s, %s, %s)""" 
            success, err = self.do_transaction(sql=s, args=[self.query_id, self.event_id, 
                        self.status, self.successful_claim ], group_commit=True)
        return success

    
    def all_for_venues(self, venue_ids, select_status='ALL', *args, **kwargs):

        all_brands = kwargs.get('all_brands', False)
        qsts = kwargs.get('qsts', None )

        # don't look for disputes unless we have a venue list
        # or bdrc level all brands option
        if venue_ids == [] and not all_brands:
            return []

        s = '''SELECT query_id  FROM disputes d JOIN events USING (event_id) WHERE 1 = 1 '''
        if venue_ids and not all_brands:
            s += '''AND  venue_id IN (%s) ''' % ','.join([str(x) for x in venue_ids])

        # add in status selection if needed
        if select_status != 'ALL':
            s += 'AND  d.status=%s'

        if qsts is not None:
            s += ' AND quest in ( %s ) '%','.join([str(x) for x in qsts])

        s += ' ORDER BY year DESC, month DESC'


        if select_status != 'ALL':
            self.f.execute(s, (select_status, ))
        else:
            self.f.execute(s)

        objs = []
        for query_id, in self.f.fetchall():
            objs.append(Dispute(dbConnection=self.d, f=self.f, query_id=query_id))
        return objs


    def get_within_periods(self, venue_id, start_year, start_month):

        period = start_year * 100 + start_month

        s = '''SELECT query_id
                FROM disputes JOIN events USING (event_id)
                WHERE venue_id=%s
                    AND year*100+month > %s'''
        self.f.execute(s, (venue_id, period))
        objs = []
        for query_id, in self.f.fetchall():
            objs.append(Dispute(dbConnection=self.d, f=self.f, query_id=query_id))
        return objs


class Query(Base):
    dispute = 1
    def setup(self, *args, **kwargs):

        query_id = kwargs.get('query_id', None)
        load_notes = kwargs.get('load_notes', False)

        self.table = 'queries'

        self.query_id = None
        self.create_date = None
        self.created_by_user_id = None
        self.closed_date = None
        self.closed_by_user_id = None
        self.query_type = None

        if query_id is not None:
            data = self.get(query_id)
        else:
            data = None

        if data:
            self.setdata(data)
        else:
            self.reset()


        # set up associated query_notes if required
        self.query_notes = []
        if load_notes:
            self.query_notes = self.get_notes()

    def __repr__(self, ):
        return u'Query: query_id=%s, create_date=%s, created_by_user_id=%s, closed_date=%s, closed_by_user_id=%s, query_type=%s' % (self.query_id, self.create_date, self.created_by_user_id, self.closed_date, self.closed_by_user_id, self.query_type)



    def reset(self, ):
        self.query_id = None
        self.create_date = None
        self.created_by_user_id = None
        self.closed_date = None
        self.closed_by_user_id = None
        self.query_type = None


    def setdata(self, data):
        self.query_id = data[0]
        self.create_date = data[1]
        self.created_by_user_id = data[2]
        self.closed_date = data[3]
        self.closed_by_user_id = data[4]
        self.query_type = data[5]


    def get(self, query_id):

        if query_id is None:
            return None

        s = """SELECT query_id, create_date, created_by_user_id, closed_date, closed_by_user_id, query_type
                FROM queries
                WHERE query_id=%s"""

        self.f.execute(s, (query_id))
        row = self.f.fetchone()

        return row


#--------------
    def update(self, ):
        
        success = None
        update = self.get(self.query_id)


        if update:

            s = """UPDATE queries
                SET create_date=%s, created_by_user_id=%s, closed_date=%s, closed_by_user_id=%s, query_type=%s
                WHERE query_id=%s""" 
            success, err = self.do_transaction(sql=s, args=[self.create_date, self.created_by_user_id, 
                                            self.closed_date, self.closed_by_user_id, self.query_type,
                                            self.query_id], group_commit=True)

        else:
            s = """INSERT INTO queries
                        (create_date, created_by_user_id, query_type)
                        VALUES(NOW(), %s, %s)
                """ 
            success, err = self.do_transaction(sql=s, args=[self.created_by_user_id, self.query_type], group_commit=True)

        if success and not update:
            self.setup(query_id=self.last_insert_id())

        return success


    def get_queries_by_mode(self, *args, **kwargs ):
        '''return list of query objects for the specified user'''

        mode = kwargs.get('mode', 'open')

        objs = []
        s = """SELECT query_id
                FROM queries"""
        
        if mode == 'open':
            s += ' WHERE closed_date IS NULL'
        else:
            s += ' WHERE closed_date IS NOT NULL'

        s += " ORDER BY query_id"

        
        self.f.execute(s, )
        for query_id, in self.f.fetchall():
            objs.append(Query(dbConnection=self.d, query_id=query_id, load_notes=True))

        return objs


    def get_user_queries(self, *args, **kwargs ):
        '''return list of query objects for the specified user'''

        user_id = kwargs.get('user_id', None)
        query_type = kwargs.get('query_type', None)

        objs = []
        s = """SELECT query_id
                FROM queries
                WHERE created_by_user_id=%s
                    AND query_type=%s
                ORDER BY create_date DESC"""

        
        self.f.execute(s, [user_id, query_type])
        for query_id, in self.f.fetchall():
            objs.append(Query(dbConnection=self.d, query_id=query_id, load_notes=True))
        return objs

    def get_notes(self, ):

        objs = []
        s = """SELECT query_note_id
                FROM query_notes
                WHERE query_id=%s
                ORDER BY query_note_id"""

        self.f.execute(s, self.query_id)
        for query_note_id, in self.f.fetchall():
            objs.append(QueryNotes(dbConnection=self.d, f=self.f, query_id=query_note_id))
        return objs



class QueryNotes(Base):
    def setup(self, *args, **kwargs):

        query_id = kwargs.get('query_id', None)

        self.table = 'query_notes'

        self.query_note_id = None
        self.query_id = None
        self.create_date = None
        self.created_by_user_id = None
        self.note_body = None

        if query_id is not None:
            data = self.get(query_id)
        else:
            data = None

        if data:
            self.setdata(data)
        else:
            self.reset()

    def __repr__(self, ):
        return u'Query: query_note_id=%s, query_id=%s, create_date=%s, created_by_user_id=%s, note_body=%s' % (self.query_note_id, self.query_id, self.create_date, self.created_by_user_id, self.note_body)



    def reset(self, ):
        self.query_note_id = None
        self.query_id = None
        self.create_date = None
        self.created_by_user_id = None
        self.note_body = None


    def setdata(self, data):
        self.query_note_id = data[0]
        self.query_id = data[1]
        self.create_date = data[2]
        self.created_by_user_id = data[3]
        self.note_body = data[4]


    def get(self, query_id):

        if query_id is None:
            return None

        s = """SELECT query_note_id, query_id, create_date, created_by_user_id, note_body
                FROM query_notes
                WHERE query_note_id=%s"""

        self.f.execute(s, [query_id, ])
        row = self.f.fetchone()

        return row


#--------------
    def update(self, ):
        
        success = None
        update = self.get(self.query_note_id)


        if update:

            s = """UPDATE query_notes
                SET query_id=%s, create_date=%s, created_by_user_id=%s, note_body=%s
                WHERE query_note_id=%s""" 
            success, err = self.do_transaction(sql=s, args=[self.query_id, self.create_date, 
                            self.created_by_user_id, self.note_body, self.query_note_id, ], 
                            group_commit=True)

        else:
            s = """INSERT INTO query_notes
                        (query_id, create_date, created_by_user_id, note_body)
                        VALUES(%s, NOW(), %s, %s)
                """ 
            success, err = self.do_transaction(sql=s, args=[self.query_id, 
                            self.created_by_user_id, self.note_body, ], group_commit=True)

        # set the query_id to one assigned by the db
        if success and not update:
            self.setup(query_id=self.last_insert_id())

        return success



class EventDisputeNatures(Base):
    def setup(self, *args, **kwargs):

        self.event_id = kwargs.get('event_id', None)
        self.dispute_natures = []


        if self.event_id is not None:
            data = self.get_all(self.event_id)
        else:
            data = None

        if data:
            self.setdata(data)
        else:
            self.reset()


    def __repr__(self, ):
        return "%s: event_id=%s, dispute_natures=%s" % (self.__class__.__name__, self.event_id, self.dispute_natures,)

    def reset(self, ):
        self.event_id = None
        self.dispute_natures = []


    def setdata(self, data):
        for event_id, dispute_nature_id in data:
            self.event_id = event_id
            self.dispute_natures.append(dispute_nature_id)


#--------------
    def get_all(self, event_id):

        s = """SELECT event_id, dispute_nature_id
                FROM event_dispute_natures
                WHERE event_id=%s"""
        self.f.execute(s, (event_id))
        rows = self.f.fetchall()
        return rows


#--------------
    def update_all(self, ):
        
        success = None

        # remove existing ones first
        self.delete(self.event_id)

        for dispute_event_id in self.dispute_natures:
            s = """INSERT INTO event_dispute_natures
                        (event_id, dispute_nature_id)
                        VALUES(%s, %s)
                """
            try:
                self.f.execute(s, (self.event_id, dispute_event_id,))
            except Exception, e:
                success = False
                break
            else:
                success = True

        return success


#--------------
    def delete(self, event_id):

        s = """DELETE FROM event_dispute_natures
                WHERE event_id=%s"""
        self.f.execute(s, (event_id, ))


class JobRole(TrivialData):
    data = {
        1: u'C&E Team Member',
        2: u'C&E Management',
        3: u'Revenue Management',
        4: u'C&E Sales Management',
        5: u'Operations Management',
        6: u'Marketing Management',
        7: u'Business Development Management',
        8: u'CEO/MD',
        9: u'BDRC',
    }


class JobRoleLocation(TrivialData):
    data = {
        1: u'Group/Brand role',
        2: u'Regional role',
        3: u'On property role',
        4: u'BDRC',
    }


class UserJobRole(Base):
    '''store JobRole and JobRoleLocation against user'''
    def __repr__(self, ):
        x = u"%s: id=%s, job_role_id=%s, job_role_location_id=%s" % (self.__class__.__name__, self.user_id, self.job_role_id, self.job_role_location_id)
        return x.encode('utf-8')

    def setup(self, *args, **kwargs):

        user_id = kwargs.get('user_id', None)

        self.user_id = None
        self.job_role_id = None
        self.job_role_location_id = None

        if user_id is not None:
            data = self.get(user_id)
        else:
            data = None

        if data:
            self.set(data)
        else:
            self.reset()


    def reset(self, ):
        self.user_id = None
        self.job_role_id = None
        self.job_role_location_id = None


    def set(self, data):
        self.user_id = data[0]
        self.job_role_id = data[1]
        self.job_role_location_id = data[2]


    def get(self, user_id):
        s = """SELECT user_id, job_role_id, job_role_location_id
                FROM bdrcshared.user_job_role
                WHERE user_id=%s"""
        self.f.execute(s, (user_id,))
        return self.f.fetchone()


    def update(self, ):
        success = None
        update = self.get(self.user_id)

        if update:
            s = """UPDATE bdrcshared.user_job_role SET job_role_id=%s, job_role_location_id=%s WHERE user_id=%s"""
            return self.do_transaction(sql=s, args=[self.job_role_id, self.job_role_location_id, self.user_id, ])

        else:
            s = """INSERT INTO bdrcshared.user_job_role (user_id, job_role_id, job_role_location_id) VALUES(%s, %s, %s)"""
            return self.do_transaction(sql=s, args=[self.user_id, self.job_role_id, self.job_role_location_id ])

    def delete(self, ):
        s = """DELETE FROM bdrcshared.user_job_role WHERE user_id=%s"""
        return self.do_transaction(sql=s, args=[self.user_id, self.job_role_id, ])




class User_demenses:
    def __init__(self, dbConnection, user_id):

        self.table = 'user_demenses'

        if dbConnection:
            self.d = dbConnection
        else:
            import db
            self.d = db.connect()

        self.f = self.d.cursor()

        self.user_id = user_id
        self.demense_ids = self.get_set(user_id)



#--------------
    def get_set(self, user_id):

        demenses = []
        if user_id is None:
            return demenses
        s = "SELECT demense_id FROM %s" % self.table
        s += " WHERE user_id=%s"
        self.f.execute(s, (user_id,))
        for demense_id, in self.f.fetchall():
            demenses.append(demense_id)

        return demenses


#--------------
    def save_set(self, ):
        '''store the current set, assumes existing have been deleted'''

        success = None

        for demense_id in self.demense_ids:
            s = "INSERT INTO %s (user_id, demense_id)" % self.table
            s += " VALUES(%s, %s)"

            try:
                self.f.execute(s, (self.user_id, demense_id))
            except Exception, e:
                success = False
                break
            else:
                success = True

        if success == True:
            self.d.commit()
        elif success == False:
            self.d.rollback()

        return success


#--------------
    def delete_set(self, ):

        s = "DELETE FROM %s" % self.table
        s += " WHERE user_id=%s"
        try:
            self.f.execute(s, (self.user_id, ))
        except:
            success = False
        else:
            success = True
        return success

#--------------
    def update_set(self, ):

        success = None

        success = self.delete_set()
        if success is False:    
            return success

        if not self.demense_ids:
            self.d.commit()
        else:
            success = self.save_set()

        return success


    def single_demense(self, ):
        '''Return demense_id of the only demense this demense level user
        has access to, or None if they have access to more than one'''
        if len(self.demense_ids) == 1:
            return self.demense_ids[0]
        else:
            return None


#    XXX We may need this but we need to limit the response to an appropriate
#    XXX set of brand users.
#    XXX
#    def user_list_obj(self, demense_id, *args, **kwargs):
#        '''present a list of user associated with the demense, along with when each
#        user last logged on. Brand users want this info to keep an eye on their staff'''
#        import user
#        exclude_bdrc = kwargs.get('exclude_bdrc', True)
#        if exclude_bdrc:
#            exclude = '%bdrc%'
#        else:
#            exclude = ''
#
#        s = """SELECT user_id
#                FROM shared.users
#                JOIN %s""" % self.table
#        s += """
#                    ON (id=user_id)
#                WHERE demense_id = %s
#                    AND disable_date IS NULL
#                    AND email NOT LIKE %s
#                ORDER BY last_logon_date"""
#        self.f.execute(s, (demense_id, exclude))
#        objs = []
#        for user_id, in self.f.fetchall():
#            objs.append(user.Users(self.d, user_id))
#
#        return common.format_user_list(objs)

class Brand_demenses:
    def __init__(self, dbConnection, brand_id):

        self.table = 'brand_demenses'

        if dbConnection:
            self.d = dbConnection
        else:
            import db
            self.d = db.connect()

        self.f = self.d.cursor()

        self.brand_id = brand_id
        self.demense_ids = self.get_set(brand_id)



#--------------
    def get_set(self, brand_id):

        demenses = []
        if brand_id is None:
            return demenses
        s = "SELECT demense_id FROM %s" % self.table
        s += " WHERE brand_id=%s"
        self.f.execute(s, (brand_id,))
        for demense_id, in self.f.fetchall():
            demenses.append(demense_id)

        return demenses


#--------------
    def save_set(self, ):
        '''store the current set, assumes existing have been deleted'''

        success = None

        for demense_id in self.demense_ids:
            s = "INSERT INTO %s (brand_id, demense_id)" % self.table
            s += " VALUES(%s, %s)"

            try:
                self.f.execute(s, (self.brand_id, demense_id))
            except Exception, e:
                success = False
                break
            else:
                success = True

        if success == True:
            self.d.commit()
        elif success == False:
            self.d.rollback()

        return success


#--------------
    def delete_set(self, ):

        s = "DELETE FROM %s" % self.table
        s += " WHERE brand_id=%s"
        try:
            self.f.execute(s, (self.brand_id, ))
        except:
            success = False
        else:
            success = True
        return success

#--------------
    def update_set(self, ):

        success = None

        success = self.delete_set()
        if success is False:    
            return success

        if not self.demense_ids:
            self.d.commit()
        else:
            success = self.save_set()

        return success





class SecurityDomains(Base):
    '''email domains against brands/venues that will limit user control's email address'''
    def __repr__(self, ):
        x = u"%s: key_level=%s, key_id=%s, email_domains=%s" % (self.__class__.__name__, self.key_level, 
            self.key_id, self.email_domains)
        return x.encode('utf-8')

    def setup(self, *args, **kwargs):

        self.key_level = kwargs.get('key_level', None)
        self.key_id = kwargs.get('key_id', None)

        self.email_domains = None
        
        self.table = 'security_domains'

        if self.key_level is None or self.key_id is None:
            self.reset_obj()
        else:
            self.set_obj()


    def reset_obj(self,):
        self.email_domains = None

    def set_obj(self, ):
        self.reset_obj()

        s = """SELECT email_domains
                FROM %s""" % self.table
        s += """ WHERE key_level=%s AND key_id=%s"""

        self.f.execute(s, (self.key_level, self.key_id, ))
        data = self.f.fetchone()
        if data:
            self.email_domains = data[0]


    def exists(self,):
        '''return bool on whether row exists for key fields'''
        s = """SELECT key_level FROM %s""" % self.table
        s += """ WHERE key_level=%s AND key_id=%s"""
        self.f.execute(s, (self.key_level, self.key_id, ))
        return bool(self.f.fetchone())


    def update(self, **kwargs):
        if self.email_domains:
            if self.exists():
                s = """UPDATE %s""" % self.table
                s += """ SET email_domains=%s
                          WHERE key_level=%s AND key_id=%s"""
                args = [self.email_domains, self.key_level, self.key_id,]

            else:
                s = """INSERT INTO %s (key_level, key_id, email_domains)""" % self.table
                s += """ VALUES(%s, %s, %s)"""
                args = [self.key_level, self.key_id, self.email_domains, ]
    
            success, exception_text = self.do_transaction(sql=s, args=args, **kwargs)
            return success, exception_text
        # if there are no email domains, we delete any existing
        else:
            return self.delete()


    def delete(self, **kwargs):
        s = """DELETE FROM %s""" % self.table
        s += """ WHERE key_level=%s AND key_id=%s"""
        args = [self.key_level, self.key_id,]

        success, exception_text = self.do_transaction(sql=s, args=args, **kwargs)
        return success, exception_text



class VenueAddress(Base):
    def __repr__(self, ):
        x = u"%s: venue_id=%s, line1=%s, line2=%s, line3=%s" % (self.__class__.__name__, 
            self.venue_id, self.line1, self.line2, self.line3,)
        return x.encode('utf-8')

    def setup(self, *args, **kwargs):
        self.venue_id = kwargs.get('venue_id', None)
        self.table = 'venue_address'

        if self.venue_id:
            self.set_obj()
        else:
            self.reset_obj()


    def reset_obj(self,):
        self.line1 = None
        self.line2 = None
        self.line3 = None
        self.town = None
        self.county = None
        self.postcode = None
        self.telephone = None
        self.website = None

    def set_obj(self, ):
        self.reset_obj()

        s = """SELECT venue_id, line1, line2, line3, town, county,
                postcode, telephone, website
                FROM %s""" % self.table
        s += """ WHERE venue_id=%s"""

        self.f.execute(s, (self.venue_id, ))
        data = self.f.fetchone()
        if data:
            self.venue_id = data[0]
            self.line1 = data[1]
            self.line2 = data[2]
            self.line3 = data[3]
            self.town = data[4]
            self.county = data[5]
            self.postcode = data[6]
            self.telephone = data[7]
            self.website = data[8]


    def exists(self,):
        '''return bool on whether row exists for key fields'''
        s = """SELECT venue_id FROM %s""" % self.table
        s += """ WHERE venue_id=%s"""
        self.f.execute(s, (self.venue_id, ))
        return bool(self.f.fetchone())


    def update(self, **kwargs):
        if self.exists():
            s = """UPDATE %s""" % self.table
            s += """ SET line1=%s, line2=%s, line3=%s, town=%s, county=%s,
                        postcode=%s, telephone=%s, website=%s
                      WHERE venue_id=%s"""
            args = [self.line1, self.line2, self.line3, self.town, self.county,
                self.postcode, self.telephone, self.website, self.venue_id,]

        else:
            s = """INSERT INTO %s (venue_id, line1, line2, line3, town, county,
                postcode, telephone, website)""" % self.table
            s += """ VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            args = [self.venue_id, self.line1, self.line2, self.line3, self.town, 
                self.county, self.postcode, self.telephone, self.website, ]

        success, exception_text = self.do_transaction(sql=s, args=args, **kwargs)
        return success, exception_text


    def delete(self, **kwargs):
        s = """DELETE FROM %s""" % self.table
        s += """ WHERE venue_id=%s"""
        args = [self.venue_id,]

        success, exception_text = self.do_transaction(sql=s, args=args, **kwargs)
        return success, exception_text


class UserGroups(Base):
    def setup(self, *args, **kwargs):

        self.user_id = kwargs.get('user_id', None)
        self.groups = []


        if self.user_id:
            data = self.get(self.user_id)
        else:
            data = None

        if data:
            self.set(data)
        else:
            self.reset()

        import user_types
        self.ut = user_types.User_types(self.d)


    def reset(self, ):
        self.groups = []


    def set(self, data):
        for row in data:
            self.groups.append(row[0])


    def get(self, user_id):

        s = """SELECT user_type
                FROM user_groups
                WHERE user_id=%s"""
        self.f.execute(s, (self.user_id))
        rows = self.f.fetchall()
        return rows


    def groups_text(self, ):
        '''return text list of user groups'''

        if self.groups:
            x = []

            for user_type in self.groups:
                x.append(self.ut.user_types.get(user_type, str(user_type)))
            return ', '.join(x)
        else:
            return '-'

    def update_groups(self, ):
        '''Replace all of the users groups with those in the groups list'''

        success = False

        s = '''DELETE FROM user_groups
                WHERE user_id=%s'''
        self.f.execute(s, (self.user_id))

        if self.groups:
            for group in self.groups:
                s = '''INSERT INTO user_groups
                        VALUES(%s, %s)'''
                try:
                    self.f.execute(s, (self.user_id, group))
                except:
                    import sys
                    sys.stderr.write('%r\n'%sys.exc_info()[1])
                    success = False
                else:
                    success = True

        # else, no groups selected so we says successful
        else:
            success = True


        if success == True:
            self.d.commit()
        elif success == False:
            self.d.rollback()

        return success




class Logo(Base):
    '''Logos are used for branding the email survey invites 
    and questionnaire entry'''
    def setup(self, *args, **kwargs):
        logo_id = kwargs.get('logo_id')
        self.logo_id = None
        self.image_name = None

        if logo_id is not None:
            data = self.get(logo_id)
        else:
            data = None

        if data:
            self.set(data)
        else:
            self.reset()


    def reset(self, ):
        self.logo_id = None
        self.image_name = None


    def set(self, data):
        self.logo_id = data[0]
        self.image_name = data[1]


    def get(self, logo_id):
        s = """SELECT logo_id, image_name
                FROM logos
                WHERE logo_id=%s"""
        self.f.execute(s, (logo_id,))
        return self.f.fetchone()


    def get_all(self, ):
        s = """SELECT logo_id, image_name
                FROM logos
                ORDER BY image_name"""
        self.f.execute(s)
        return self.f.fetchall()

    def add(self, image_name):
        '''add specified image name to the logos table'''
        s = """INSERT INTO logos (image_name) VALUES(%s)"""
        args = [image_name]
        return self.do_transaction(sql=s, args=args)

    def exists(self, image_name):
        '''return bool according to whether the specified image
        exists in the logos table'''
        s = """SELECT image_name
                FROM logos
                WHERE image_name=%s"""
        self.f.execute(s, (image_name,))
        return bool(self.f.fetchone())

    def load_new(self,):
        '''search logos dir for new entries, add them to the table'''
        import glob
        import os
        self.new_tot = 0
        self.new_files = []
        self.failed_tot = 0
        self.failed_files = []
        file_path = '../../htdocs%sbranded_logos/*' % local.docpath
        file_list = glob.glob(file_path)
        for f in file_list:
            file_name = unicode(os.path.basename(f), 'utf-8')
            if not self.exists(file_name):
                success, err_msg = self.add(file_name)
                if success:
                    self.new_tot += 1
                    self.new_files.append(file_name)
                else:
                    self.failed_tot += 1
                    self.failed_files.append([file_name, err_msg])



class  DemensePreferences(Base):


    def set_table(self,**kwargs):
        pass

    def setup(self, *args, **kwargs):
        self.my_id = kwargs.get('id',None)
        
        self.demense_pref = {}
        self.set_table()
        if self.my_id:
            self.demense_pref = dict(self.get_set(self.my_id))



#--------------
    def get_set(self, my_id):

        demenses = []
        if my_id is None:
            return demenses

        s = "SELECT prefered_demense_id , preference FROM %s" % self.table
        s += " WHERE id=%s"

        self.f.execute(s, (my_id,))
        for demense_id,preference in self.f.fetchall():
            demenses.append((demense_id,preference,))

        return demenses


#--------------
    def save_set(self, ):
        '''store the current set, assumes existing have been deleted'''

        success = True
        import sys
        sys.stderr.write("starting update\n")
 
        for demense_id in self.demense_pref:
            s = "INSERT INTO %s (id, prefered_demense_id, preference)" % self.table
            s += " VALUES(%s, %s, %s)"

            sys.stderr.write("%s\n"%s)
            try:
                self.f.execute(s, (self.my_id, demense_id, self.demense_pref[demense_id]))
            except Exception, e:
                import sys
                sys.stderr.write("%s,%s,%s\n"%sys.exc_info())
                success = False
                break
            else:
                success = True


        if success == True:
            self.d.commit()
        elif success == False:
            self.d.rollback()

        return success


#--------------
    def delete_set(self, ):

        s = "DELETE FROM %s" % self.table
        s += " WHERE id=%s"
        try:
            self.f.execute(s, (self.my_id, ))
        except:
            import sys
            sys.stderr.write("%s,%s,%s\n"%sys.exc_info())
            success = False
        else:
            success = True
        return success

#--------------
    def update_set(self, ):

        success = None

        success = self.delete_set()
        
        if not success:
            self.d.rollback()
            return success

        if success:
            success = self.save_set()

        return success





class  Demense_DemensePreferences(DemensePreferences):

    def set_table(self,**kwargs):
        self.table = "demense_demense_prefs"



class  Venue_DemensePreferences(DemensePreferences):

    def set_table(self,**kwargs):
        self.table = "venue_demense_prefs"


class EnquiryScheduleData(Base):
    def setup(self, *args, **kwargs):
        self.id = kwargs.get('id', None)
        self.enq_type = kwargs.get('enq_type', None)
        self.enq_target = kwargs.get('enq_target', None)
        self.value = kwargs.get('value', None)

        self.set_table()

        if self.enq_type is not None and self.enq_target is not None:
            self.set_obj()
        else:
            if self.id and (self.enq_type is not None or self.enq_target is not None):
                self.get_all()

    def reset_obj(self,):
        self.value = None

    def set_obj(self, ):
        self.reset_obj()

        s = """SELECT value
                FROM %s""" % self.table
        s += """ WHERE id =%s and enq_type=%s and enq_target=%s"""

        self.f.execute(s, (self.id, self.enq_type, self.enq_target ))
        data = self.f.fetchone()
        if data:
            self.value = data[0]


    def _missing_arg(self,):
        if self.enq_type is None: return "enq_type"
        if self.enq_target is None: return "enq_target"

    
    
    def get_all(self,):
        s = """SELECT %s, value FROM %s where id = %s """ %(self._missing_arg(),self.table,self.id)
        if self.enq_type is not None:
            s+= " AND enq_type = %s "%self.enq_type
 
        if self.enq_target is not None:
            s+= " AND enq_target = %s "%self.enq_target

        self.f.execute(s)
        self.list =  dict(self.f.fetchall())

    def get(self,**kwargs):
        arg = self._missing_arg()
        try:
            rv =  self.list[kwargs[arg]]
        except:
            rv = None

        return rv


    def update(self, ):
       
        args = (self.value, self.enq_type,self.enq_target,self.id)

        s = "INSERT INTO %s" % self.table
        s += """ (value,enq_type,enq_target,id)
                    VALUES(%s,%s,%s,%s)"""

        import sys
        #sys.stderr.write("%s %s\n"%(s,args))
        success, exception_text = self.do_transaction(sql=s, args=args)
        #sys.stderr.write("\t%r %r\n"%(success,exception_text))

        if not success:
            s = "UPDATE %s" % self.table
            s += """ SET value=%s
                    WHERE enq_type=%s and enq_target=%s and id = %s"""

            #sys.stderr.write("%s %s\n"%(s,args))
             
            success, exception_text = self.do_transaction(sql=s, args=args)

        return success, exception_text


class MainwaveVenueSchedule(EnquiryScheduleData):
    def set_table(self,):
        self.table = "mainwave_venue_schedule"

class AdhocVenueSchedule(EnquiryScheduleData):
    def set_table(self,):
        self.table = "adhoc_venue_schedule"

class BrandQuestionnaireDefaults(EnquiryScheduleData):
    def set_table(self,):
        self.table = "brand_questionnaires"

class VenueLanguageDefaults(EnquiryScheduleData):
    def set_table(self,):
        self.table = "venue_language"



class Default_Schedule(TrivialData):
    data= {
             EnquiryTarget.MEETINGS: {
                EnquiryType.TELEPHONE: 2,
                EnquiryType.EMAIL:     1,
                EnquiryType.RFP  :     1,
                },
             EnquiryTarget.SOCIAL:   {
                EnquiryType.TELEPHONE: 2,
                EnquiryType.EMAIL:     1,
                EnquiryType.RFP  :     1,
            },
             EnquiryTarget.CENTRAL:  {
                EnquiryType.TELEPHONE: 2,
                EnquiryType.EMAIL:     1,
                EnquiryType.RFP  :     1,
            },
             EnquiryTarget.GROUP:    {
                EnquiryType.TELEPHONE: 3,
                EnquiryType.EMAIL:     0,
                EnquiryType.RFP  :     0,
            },
             EnquiryTarget.INDIV:    {
                EnquiryType.TELEPHONE: 3,
                EnquiryType.EMAIL:     0,
                EnquiryType.RFP  :     0,
            },
             EnquiryTarget.LONG:     {
                EnquiryType.TELEPHONE: 3,
                EnquiryType.EMAIL:     3,
                EnquiryType.RFP  :     0,
            },
             EnquiryTarget.AGENCY:   {
                EnquiryType.TELEPHONE: 2,
                EnquiryType.EMAIL:     1,
                EnquiryType.RFP  :     1,
            },
        }


    def setup(self, ):
        if self.key_id is None:
            self.list = None
        else:
            self.list = self.data.get(self.key_id, None)


    def get_default(self,enq_type):
        try:
            rv =  self.list[enq_type]
        except:
            rv = None

        return rv


class EnquiryChannel(object):
    def __init__(self,adhoc,etype,etarget):
        self.adhoc = adhoc
        self.etype = etype
        self.etarget = etarget

    def __repr__(self,):
        return "EnquiryChannel("+",".join([str(self.adhoc) , EnquiryType.names[self.etype] ,EnquiryTarget.names[self.etarget] ]) +")"

    def __hash__(self,):
        return hash((type(self),self.adhoc,self.etype,self.etarget))

    def __ne__(self,other):
        return not (self == other)

    def __eq__(self,other):
        return (self.adhoc,self.etype, self.etarget) == (other.adhoc , other.etype , other.etarget)

    def  get_quest_for_venue(self,v):
        lut = BrandQuestionnaireDefaults( dbConnection = v.d , f =v.f,
                id = v.brand_id, enq_type=self.etype,enq_target =self.etarget)

        if lut.value is None:
            lut.id = 0
            lut.set_obj()

        return lut.value

    def  get_lang_for_venue(self,v):
        lut =VenueLanguageDefaults( dbConnection = v.d , f =v.f,
                id = v.venue_id, enq_type=self.etype,enq_target =self.etarget)

        if lut.value is None:
            lut.id = 0
            lut.set_obj()

        return lut.value


class Criteria(NamedTrivialData): # - or should it be (orm_model.db_table, model.Base):
    """ manages information about different criteria which may be applied to the same questionnaire

    Confused yet?
    """
    NATIVE=0
    BENCHMARK=15
    HILTON=19
    MARRIOTT=20
    CHELSEAFC=21
    IC=24
    KEITHPROWSE=13

    names = [ None, ] * 25
    names[NATIVE]='Native'

    names[KEITHPROWSE] = 'KeithProwse'
    names[BENCHMARK] = 'Standard'
    names[HILTON] = 'Hilton'
    names[IC] = 'IC'

    names_lc = [ x and x.lower() for x in names ]
    data ={
        KEITHPROWSE: "Keith Prowse custom criteria",
        BENCHMARK: "Benchmark criteria",
        HILTON: "Hilton custom criteria",
        IC: "Intercontinental criteria (obsolete)",
        MARRIOTT:"Marriott International",
        CHELSEAFC:"Chelsea FC",
    }

    def setup(self,):
        super(Criteria,self).setup()

        self.criteria_id = self.key_id
        self.criteria_name = self.description

        ##Of course this base Id is wrong for LongStay standard - let's not go into that.
        #  LS std currently uses 36000, not 15000 in case you're wondering..
        self.criteria_base = self.criteria_id and ( 1000 *  self.criteria_id )
        self.consolidated = bool(self.criteria_id)

    def __unicode__(self,):
        return self.criteria_name



class generic_attribute(object):
    """A way of providing read-only access to the saem attribute under multiple names"""
    def __init__(self,src_attr):
        self.nm = src_attr

    def __get__(self,obj,obj_class):
        return getattr(obj,self.nm)

