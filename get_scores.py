import model
from brand_report_overall import set_text
import functools

class Entities(model.NamedTrivialData):
    Venue = 1
    Brand = 2
    Tradingbrand = 3
    Division = 4
    OldDivision = 5
    Demense = 6
    Cluster = 7
    Competitor = 8

    names = [None, 'Venue' , 'Brand', 'Tradingbrand' , 'Division' , 'OldDivision' , 'Demense' , 'Cluster' , 'Competitor' ]
    names_lc = [ x and x.lower() for x in names ]

    def __str__(self,):
        return self.name

    scores_lut = {
            Venue  : lambda x: model.VenueScores,
            Brand  : lambda x: (x and model.Own_Brand_Demense_scores ) or (x or model.Brand_Demense_scores ),
            Tradingbrand  : lambda x: model.Tradingbrand_Demense_scores,
            Division  : lambda x: (x and model.Own_SDivision_Demense_scores) or (x or model.SDivision_Demense_scores ),
            OldDivision  : lambda x:model.Division_scores,
            Demense  : lambda x:model.Demense_scores,
            Cluster  : lambda x:model.Cluster_scores,
            Competitor  : lambda x:model.Competitor_scores,
    }

    ranks_lut = {
            Venue  : functools.partial(model.VenueClusterRanks,cluster_entry="N"),
            Brand  : model.BrandRanks ,
            Cluster:  functools.partial(model.VenueClusterRanks,cluster_entry="Y"),
    }

    def get_score_model(self,own = True):
        return self.__class__.scores_lut[self.key_id](own)

    def get_rank_model(self,):
        return self.__class__.ranks_lut[self.key_id]


def get_score( entity_type, entity_id, year,month, score_type, result_id, questionnaire_id , answer_value = None,
    id_type = 0, demense_id = None, allow_override = True, own_scores = True , return_score = False):

    brand_id = None

    if answer_value is None:
        answer_value = set_text[result_id][1]

    if answer_value is None: raise RuntimeError("cant find answer_value for  %i"%result_id)
    entity_model = entity_type.get_score_model(own_scores)

    if issubclass(entity_model, model.Brand_Demense_scores):
        if demense_id is None: raise RuntimeError("%s scores need demense"%entity_type.name)
        ##Seap these beacuse Brand_demnse_scores is wrong
        entity_id , brand_id   = demense_id, entity_id

    if issubclass(entity_model, model.Demense_enabled_Scores):
        if demense_id is None: raise RuntimeError("%s scores need demense"%entity_type.name)

    s = entity_model(id = entity_id, year = year, month =month, score_type = score_type, questionnaire_id = questionnaire_id,
        answer_value = answer_value, demense_id =demense_id, allow_override = allow_override, id_type =id_type ,result_id = result_id,
        brand_id = brand_id)

    # print s
    if s.id != entity_id :
        #logger.debug("No score found")

        # print entity_model(id = entity_id, year = year, month =month, score_type = score_type, questionnaire_id = questionnaire_id,
        #         answer_value = answer_value, demense_id =demense_id, allow_override = allow_override, id_type =id_type ,result_id = result_id,
        #         brand_id = brand_id, set_mode = True)


        return None

    if return_score:
        return s
    else:
        return s.score, s.occurences, s.base



def get_rank( entity_type, entity_id, year,month, score_type, result_id, questionnaire_id , answer_value = None,
    id_type = 0, demense_id = None,  for_brand = True , grouping_level = 1):


    if answer_value is None:
        answer_value = set_text[result_id][1]

    if answer_value is None: raise RuntimeError("cant find answer_value for  %i"%result_id)
    entity_model = entity_type.get_rank_model()

   

    r = entity_model(id = entity_id, year = year, month =month, score_type = score_type, questionnaire_id = questionnaire_id,
        answer_value = answer_value, demense_id =demense_id, id_type =id_type ,result_id = result_id,
        ranks_for_brand = for_brand, grouping_level = grouping_level)

    # print r
    
    return r.rank ,r.equals, r.set_size
