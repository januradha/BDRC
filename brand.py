# -*- coding: utf-8 -*-

import local
import model
import common
import currency


class divisional_property(object):
    """Or stuff inherited from out division, or it parents or it's  whaever it inherits from...."""
    def __init__(self,propname):
        self.nm = propname

    def __get__(self, obj, cls):
        import structure as struct
        div = struct.Division(dbConnection  = obj.d , division_id = obj.shareddivision_id)
        if div.division_id != obj.shareddivision_id: raise RuntimeError("No matching (shared) division")

        return  getattr(div,self.nm)

class Brand:
    def __init__(self, dbConnection, id, *args, **kwargs):

        f = kwargs.get('f', None)

        if dbConnection:
            self.d = dbConnection
        else:
            import db
            self.d = db.connect()
            f = None

        if f is not None:
            self.f = f
        else:
            self.f = self.d.cursor()

        self.table = 'brands'

        self.brand_id = None
        self.brand_name = None
        self.logo_id = None
        self.independent = None
        self.exclude_from_main_study = None
        self.brand_delete_date = None 
        self.stealth_mode = None 
        self.has_own_criteria = None
        self.competitor_shop_req = None
        self.competitor_shop_price = None
        self.competitor_shop_currency_code = None
        self.shareddivision_id = None 


        # email security domains
        self.email_domains = None

        if id:
            data = self.get(id)
            self.sd = model.SecurityDomains(dbConnection=self.d, f=self.f, key_level='B', key_id=id)
        else:
            data = None
            self.sd = model.SecurityDomains(dbConnection=self.d, f=self.f)
        self.email_domains = self.sd.email_domains
        
        # make a list of the domains
        if self.email_domains:
            self.email_domains_list = [x for x in self.email_domains.split(' ') if x != ' ']
        else:
            self.email_domains_list = []

        if data:
            self.set(data)
        else:
            self.reset()


    criteria = divisional_property("criteria")
    name = model.generic_attribute("brand_name")
    id = model.generic_attribute("brand_id")

    def __eq__(self,other):
        """Define equivalence based on sharing the same key and table"""
        if not isinstance(self,other.__class__) and not isinstance(other,self.__class__): return False
        return self.make_key_tuple() == other.make_key_tuple()

    def __ne__(self,other):
        return not self == other

    def __hash__(self,):
        return hash(self.make_key_tuple())


    def __repr__(self, ):
        x = u"%s: brand_id=%s, brand_name=%s, independent=%s, exclude_from_main_study=%s, stealth_mode=%s, email_domains=%s" % (self.__class__.__name__, self.brand_id, 
                self.brand_name, self.independent, self.exclude_from_main_study, self.stealth_mode, self.email_domains)
        return x.encode('utf-8')

    def reset(self, ):
        self.brand_id = None
        self.brand_name = None
        self.logo_id = None
        self.independent = None
        self.exclude_from_main_study = None
        self.brand_delete_date = None 
        self.stealth_mode = None 
        self.has_own_criteria = None
        self.competitor_shop_req = None
        self.competitor_shop_price = None
        self.competitor_shop_currency_code = None

        self.shareddivision_id = None 




    def set(self, data):
        self.brand_id = data[0]
        self.brand_name = data[1]
        self.logo_id = data[2]
        self.independent = data[3]
        self.exclude_from_main_study = data[4]
        self.brand_delete_date = data[5]
        self.stealth_mode = data[6]
#        self.has_own_criteria = (self.brand_id == 225) or ( self.brand_id == 152 )
        #FIXME
        self.has_own_criteria = data[7]
        self.competitor_shop_req = data[8]
        self.competitor_shop_price = data[9]
        self.competitor_shop_currency_code = data[10]

        self.shareddivision_id = data[11]

      

    def get(self, id):
        if id is None:
            return None


        s = """SELECT brand_id, brand_name, logo_id, independent, exclude_from_main_study,
                    brand_delete_date, stealth_mode, own_criteria,cs_request,cs_price,cs_currency_code,
                    division_id
                FROM brands
                WHERE brand_id=%s""" % id

        self.f.execute(s)
        row = self.f.fetchone()
        return row


#--------------
    def get_all(self, **kwargs  ):

        include_disabled = kwargs.get('include_disabled', False)
        if include_disabled:
            inc = ''
        else:
            inc = 'WHERE brand_delete_date IS NULL'

        s = """SELECT brand_id, brand_name, logo_id, independent, exclude_from_main_study
                FROM brands
                    %s
                    ORDER by brand_name"""%inc

        self.f.execute(s)
        rows = self.f.fetchall()
        return rows

#--------------
    def get_all_main_study(self, ):


        s = """SELECT brand_id, brand_name, logo_id, independent, exclude_from_main_study
                FROM brands
                    WHERE exclude_from_main_study IS NULL
                        AND brand_delete_date IS NULL
                    ORDER by brand_name"""

        self.f.execute(s)
        rows = self.f.fetchall()
        return rows


    def get_all_obj(self, **kwargs ):
        s = kwargs.get('sql', None)
        args = kwargs.get('args', [])

        if s is None:
            s = """SELECT brand_id
                    FROM brands
                    WHERE brand_delete_date IS NULL
                    ORDER BY brand_name"""
        self.f.execute(s, args)

        objs = []
        for brand_id, in self.f.fetchall():
            objs.append(Brand(self.d, brand_id, f=self.f))
        return objs




#--------------
    def get_by_name(self, brand_name):
        '''get the brand details using the brand name for retrieval'''

        s = """SELECT  brand_id, brand_name, logo_id, independent, exclude_from_main_study
                FROM brands
                WHERE brand_name=%s"""

        self.f.execute(s, (brand_name,))
        row = self.f.fetchone()

        return row



#--------------
    def get_by_user(self, user_id):
        '''Return list of brands that the specified user has access to'''

        s = """SELECT b.brand_id, brand_name, logo_id, independent, exclude_from_main_study,
                    brand_delete_date, stealth_mode, own_criteria,cs_request,cs_price,cs_currency_code,
                    division_id

                FROM user_brands u, brands b
                WHERE user_id=%s
                    AND u.brand_id=b.brand_id"""

        self.f.execute(s, (user_id, ))
        row = self.f.fetchone()

        return row
 
#--------------
    def disable(self, ):
        '''disable the current brand'''

        s = """UPDATE brands SET brand_delete_date=NOW() WHERE brand_id=%s"""

        try:
            self.f.execute(s, (self.brand_id,))
        except :
            success = False
        else:
            success = True

        if success == True:
            self.d.commit()
        elif success == False:
            self.d.rollback()
        return success

#--------------
    def enable(self, ):
        '''enable the current brand'''

        s = """UPDATE brands SET brand_delete_date=NULL WHERE brand_id=%s"""

        try:
            self.f.execute(s, (self.brand_id,))
        except :
            success = False
        else:
            success = True

        if success == True:
            self.d.commit()
        elif success == False:
            self.d.rollback()
        return success

   
#--------------
    def count_events_in_quarter(self, year, quarter):
        '''returns number of events in the passed quarter'''
        sql = """SELECT count(event_id) FROM events JOIN venues USING(venue_id)
                 WHERE delete_date IS NULL AND adhoc='N'
                 AND brand_id = %s AND year = %s AND status <> 'D'"""
        
        sql1 = """ AND month IN (%s) """
        months = ['1,2,3','4,5,6','7,8,9','10,11,12']# TODO REMOVE TO ELSEWHERE
        sql1 %= months[int(quarter)-1]
        self.f.execute(sql+sql1,(self.brand_id,year,))
        row = self.f.fetchone()
        if row:
            return row[0]
        else:
            return 0

#--------------
    def count_prov_events_in_quarter(self, year, quarter):
        '''returns number of provisional events in the passed quarter'''
        sql = """SELECT count(prov_event_id) FROM prov_events JOIN venues USING(venue_id)
                 WHERE delete_date IS NULL 
                 AND brand_id = %s AND year = %s """
        
        sql1 = """ AND month IN (%s) """
        months = ['1,2,3','4,5,6','7,8,9','10,11,12']# TODO REMOVE TO ELSEWHERE
        sql1 %= months[int(quarter)-1]
        self.f.execute(sql+sql1,(self.brand_id,year,))
        row = self.f.fetchone()
        if row:
            return row[0]
        else:
            return 0
        
#--------------
    def count_venues(self, ):
        '''Return the number of venues associated with this brand'''
        #PL20071015 accounted for disabled date:
        s = """SELECT COUNT(*)
                FROM venues
                WHERE brand_id=%s
                AND delete_date IS NULL"""
        self.f.execute(s, (self.brand_id, ))
        row = self.f.fetchone()
        if row:
            return row[0]
        else:
            return 0

#--------------
    def get_venues_id(self, ):
        '''Return the list of venue ids associated with this brand'''
        #PL20071015 accounted for disabled date:
        s = """SELECT venue_id
                FROM venues
                WHERE brand_id=%s
                AND delete_date IS NULL"""
        self.f.execute(s, (self.brand_id, ))
        rows = self.f.fetchall()
        if len(rows) > 0:
            return rows
        else:
            return []


    def last_insert_id(self, ):
        s = "SELECT LAST_INSERT_ID() FROM %s" % self.table
        self.f.execute(s)
        r = self.f.fetchone()
        if r:
            return r[0]
        else:
            return None


#--------------
    def update(self, ):
        '''Update the brand with the currently stored details, and if it doesn't exist, add it!'''
        
        success = None
        update = self.get(self.brand_id)


        if update:

            s = """UPDATE brands
                SET brand_name=%s,
                    logo_id=%s,
                    independent=%s,
                    exclude_from_main_study=%s,
                    brand_delete_date=%s,
                    stealth_mode=%s,
                    own_criteria=%s,
                    cs_request=%s,
                    cs_price=%s,
                    cs_currency_code=%s,
                    division_id=%s

                WHERE brand_id=%s"""
            try:
                import sys
                sys.stderr.write("%s;\n%s,%s,%s\n"%(s,self.competitor_shop_req,self.competitor_shop_price,self.competitor_shop_currency_code))

                self.f.execute(s, (self.brand_name, self.logo_id,
                                    self.independent, self.exclude_from_main_study,
                                    self.brand_delete_date, self.stealth_mode,
                                    self.has_own_criteria,self.competitor_shop_req,
                                    self.competitor_shop_price,self.competitor_shop_currency_code,
                                    self.shareddivision_id,
                                    self.brand_id
                    ))
            except :
                success = False
                import sys
                sys.stderr.write("%s\n"%sys.exc_info()[1])
            else:
                success = True

        else:
            s = """INSERT INTO brands
                        (brand_name, logo_id, independent, exclude_from_main_study, stealth_mode, 
                            own_criteria,cs_request,cs_price,cs_currency_code, division_id)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s , %s )
                """
            try:
                self.f.execute(s, (self.brand_name, self.logo_id, 
                                    self.independent, self.exclude_from_main_study,
                                    self.stealth_mode,
                                    self.has_own_criteria,self.competitor_shop_req,
                                    self.competitor_shop_price,self.competitor_shop_currency_code,
                                    self.shareddivision_id))
            except:
                success = False
                import sys
                sys.stderr.write(str(sys.exc_info()[1]))
            else:
                success = True
                self.brand_id = self.last_insert_id()
        if success:
            # also update email security domains
            self.sd.key_level = 'B'
            self.sd.key_id = self.brand_id
            self.sd.email_domains = self.email_domains
            success, err_txt = self.sd.update()

        if success == True:
            self.d.commit()
        elif success == False:
            self.d.rollback()


        return success




    def edit_form(self, *args, **kwargs ):
        '''return a form to allow editing of the brand details.'''


        x = []
        if self.brand_name: brand_name = self.brand_name
        else: brand_name = ''

        if self.independent: indy_select = 'checked'
        else: indy_select = ''

        if self.exclude_from_main_study: exclude_select = 'checked'
        else: exclude_select = ''

        if self.stealth_mode: stealth_select = 'checked'
        else: stealth_select = ''

        if self.brand_delete_date is not None: disabled = 'disabled'
        else: disabled = ''

        if self.email_domains: email_domains = self.email_domains
        else: email_domains = ''

        if self.has_own_criteria: own_crit_select = 'checked'
        else: own_crit_select = ''

        if self.competitor_shop_req: cs_req_select = 'checked'
        else: cs_req_select = ''
      
        if self.competitor_shop_price: competitor_shop_price =self.competitor_shop_price
        else: competitor_shop_price = ''


        curr = currency.Currency(self.d,self.competitor_shop_currency_code)
        currency_dropdown = curr.dropdown(curr.currency_code,"competitor_shop_currency","", no_label=True )
   
        import bdrcshared.structure
        division = bdrcshared.structure.Division(self.d, division_id = self.shareddivision_id)
        division_tree = division.generate_menu_tree("division_id" , disabled = bool(disabled))

        x.append(u'<form method="post" action="!CGIPATH!edit_brand.py">')
        x.append(u'$TOP_MESSAGE')

        x.append(u'''<p>
                    <div id="brand_details">
                    <span class="sub-block">Brand Details</span>
                        <div class="sub-block">''')
        

        x.append(u'<table>')
        x.append(u'''<tr>
                        <td class=left>Brand Name:</td>
                    <td class=left><input class="text-input $NAME_ERROR_CLASS" name="brand_name" type=text size=50 maxlength=80 value="%(brand_name)s" %(disabled)s> $NAME_ERROR_TEXT</td>
                    </tr>
                    <tr>
                        <td class=left><label for="independent">Independent:</label></td>
                        <td class=left><input id="independent" name="independent" type=checkbox %(indy_select)s %(disabled)s></td>
                    </tr>
                    <tr>
                        <td class=left><label for="exclude">Exclude from main study:</label></td>
                        <td class=left><input id="exclude" name="exclude" type=checkbox %(exclude_select)s %(disabled)s></td>
                    </tr>
                    <tr>
                        <td class=left><label for="stealth_mode">Stealth mode:</label></td>
                        <td class=left><input id="stealth_mode" name="stealth_mode" type="checkbox" %(stealth_select)s %(disabled)s></td>
                    </tr>
                    <tr>
                        <td class=left>Email domains:</td>
                        <td class=left><input class="text-input" name="email_domains" type="text" size="80" maxlength="4000" value="%(email_domains)s" %(disabled)s></td>
                    </tr>
                    <tr>
                        <td class=left><label for="stealth_mode">Has own criteria:</label></td>
                        <td class=left><input id="has_own_criteria" name="has_own_criteria" type="checkbox" %(own_crit_select)s %(disabled)s></td>
                    </tr>
                    <tr>
                        <td class=left>Competitor Shop Requests<label for="competitor_shop_request">:</label></td>
                        <td class=left><input id="competitor_shop_request" name="competitor_shop_request" type="checkbox" %(cs_req_select)s %(disabled)s></td>
                    </tr>

                    <div id="competitor_shop_details">
                     <tr>
                        <td class=left>Competitor shop price:</td>
                        <td class=left><input class="text-input $CS_PRICE_ERROR_CLASS"  name="competitor_shop_price" type="text" size="8" maxlength="4000" value="%(competitor_shop_price)s" %(disabled)s> $CS_PRICE_ERROR_TEXT </td>
                    </tr>
                     <tr>
                        <td class=left>Competitor shop currency:</td>
                        <td class=left>%(currency_dropdown)s </td>
                    </tr>
                     <tr>
                        <td class=left>Equivalent division:</td>
                        <td class=left>%(division_tree)s </td>
                    </tr>
                    </div>
                    ''' % locals())


        x.append(u'</table>')
        x.append(u'</div></div>')
        
        # Which supernational localites does this brand appear in the league tables for.
        x.append(u'''<p>
                    <div id="brand_details">
                    <span class="sub-block">League Tables</span>
                        <div class="sub-block">''')

        x.append('''<p>Select regions in whose league table you wish this brand to appear<p>''')
        bd = model.Brand_demenses(self.d, self.brand_id)
        ds = self.get_all_supernations()
        ds.extend(self.get_all_nations())
        for d in sorted(ds, key=lambda sn:sn.demense_id ):

            demense_id = d.demense_id
            name = d.demense_name

            if demense_id in bd.demense_ids:
                selected = 'checked'
            else: selected =''

            label = 'demense_select_%(demense_id)d' % locals()
            x.append('''<br>
                            <input name="%(label)s" id="%(label)s" type="checkbox" %(selected)s>
                            <label for="%(label)s"> %(name)s </label>
                     ''' % locals())


        x.append(u'</div></div>')



        # disable save button if the venue is disabled
        if self.brand_delete_date:
            x.append(u'<p><input class="button" type=submit name="update" value="save details" disabled>')
        else:
            x.append(u'<p><input class="button" type=submit name="update" value="save details">')

        # if we're not creating an add screen, set the enable/disable buttons accordingly
        if self.brand_id is not None:
            if self.brand_delete_date:
                x.append(u' <input class="button" type=submit name="enable" value="enable">')
            else:
                x.append(u' <input class="button" type=submit name="disable" value="disable">')

                ##




        if self.brand_id:
            x.append(u'<input type=hidden name="brand_id" value="%s">' % self.brand_id)
        x.append(u'</form>')

        x.append(u'$USER_LIST')

        return ''.join(x)


#--------------
    def dropdown(self, current_brand_id=None, select_arg='', id_extension='', *args, **kwargs):
        x = [u'''<select class="text-input $BRAND_ERROR_CLASS" name="brand_id%(id_extension)s" id="brand_dropdown%(id_extension)s" %(select_arg)s>''' % locals()]


        limit_slt = kwargs.get('limit_slt', None)
        select_opt = kwargs.get('select_opt', True)

        if select_opt:
            x.append(u'''<option value=''>---Select---</option>''')


        for brand_id, brand_name, logo_id, independent, exclude_from_main_study in self.get_all():

            # use the limited selection list, if specified
            if limit_slt:
                if brand_id not in limit_slt: continue

            if current_brand_id == brand_id:
                y = 'selected'
            else:
                y = ''
            x.append(u"<option value='%s' %s>%s</option>" % (brand_id, y, brand_name))

        x.append(u'</select>')

        return ''.join(x)


#--------------
    def check_brand(self, brand_id, user_id, groups=None):
        '''Return true if the user is allowed to access the brand'''
        import user_types as ut

        if ut.bdrc_admin(groups):
            return True

        if ut.brand_user(groups):
            s = """SELECT user_id
                FROM user_brands JOIN brands USING (brand_id)
                WHERE user_id=%s AND brand_id=%s"""
            self.f.execute(s, (user_id, brand_id))
        else:
            s = """SELECT user_id FROM user_brands
                    WHERE user_id=%s AND brand_id=%s"""
            self.f.execute(s, (user_id, brand_id))
        row = self.f.fetchone()

        return bool(row is not None)


#--------------
    def has_clusters(self, ):
        '''Return True/False accordingly if the brand has any clusters'''

        s = """SELECT venue_id
                    FROM venues
                    WHERE brand_id=%s
                        AND cluster_id IS NOT NULL
                    LIMIT 1"""

        self.f.execute(s, (self.brand_id, ))
        row = self.f.fetchone()
        return bool(row)

    def list_all(self, URL, search=None, *args, **kwargs):
        '''Create a simple list of brands and a link to the spcified URL
        using the brand_id as an arg'''
    

        form = kwargs.get('form', None)
        if form:
            inc_dlt = form.getfirst('inc_dlt', False)
        else:
            inc_dlt = None
   
     
        # if search specified, build search AND clause
        if search:
            srch = '%' + search + '%'
        else:
            srch = '%'
    
        common.set_cookie_value(name='search', value=search)
    
        if inc_dlt: 
            s = """SELECT brand_id FROM brands WHERE (brand_name LIKE %s) ORDER BY brand_name"""
        else:
            s = """SELECT brand_id FROM brands WHERE (brand_name LIKE %s) AND brand_delete_date IS NULL ORDER BY brand_name"""
        args = (srch, )
        objs = self.get_all_obj(sql=s, args=args)


        x = [u'Found: %s' % len(objs)]
        if objs:
            x.append(u'<table id="searchList" class="tablesorter">')
            x.append(u'<thead>')
            x.append(u'''<tr>
                        <th class="left">Brand Name</th>
                        <th>Independent</th>
                        <th>Exclude From Main Study</th>
                        <th>Stealth Mode</th>
                        </tr>''')
            x.append(u'</thead>')
            x.append(u'<tbody>')
    
            for b in objs:
                brand_id = b.brand_id
                brand_name = b.brand_name
                dlt = ['', u' strike'][int(bool(b.brand_delete_date))]

                indy = ['','Yes'][int(bool(b.independent))]
                exclude = ['','Yes'][int(bool(b.exclude_from_main_study))]
                stealth_mode = ['','Yes'][int(bool(b.stealth_mode))]
                link_cell = u'<td class="left %(dlt)s"><a href="!CGIPATH!%(URL)s?brand_id=%(brand_id)s">%(brand_name)s</a></td>' % locals()
                x.append(u'''<tr>
                            %(link_cell)s
                            <td>%(indy)s</td>
                            <td>%(exclude)s</td>
                            <td>%(stealth_mode)s</td>
                         </tr>''' % locals())
    
            x.append(u'</tbody>')
            x.append(u'</table>')
    
        return ''.join(x)
    
    def get_all_nations(self,):
        """Gets all national localitues this brand has a venue in"""
        import venue
        v = venue.Venue(self.d,None)
        vens = v.all_brand_obj(self.brand_id)
        nations =[ v.get_nation_obj() for v in vens ]
        #Collapse to unique by id
        nations = dict([ (ven.demense_id,ven )  for ven in nations if ven is not None]) 
        return nations.values()

    def get_all_supernations(self, ):
        """Get all parents of all our nations"""
        sn = []
        for nation in self.get_all_nations():
            sn.extend(nation.get_all_parent_obj())

        import sys
        supernations = dict([ (n.demense_id,n )  for n in sn]) 
        return supernations.values()


    def support_path(self,):
        sub_path = "std"
        if self.has_own_criteria:
           sub_path = str(self.brand_id)

        import os
        return os.path.join(local.static_doc_path,sub_path)


    def get_all_venues(self, demense_id = None):
        import venue
        v = venue.Venue(self.d,None)
        if demense_id is None:
            return v.all_brand_obj(self.brand_id)
        else:
            return v.all_demense_obj(demense_id, brand_id =self.brand_id)

    def allowed_target(self,target_id):
        """For compatibility with trading brands"""
        return True

    def get_root_parent(self,):
        """Fake tree info method"""
        return self

    def distance(self,other):
        """Fake tree info method"""
        if self.brand_id != other.brand_id: raise RuntimeError("unreachable")
        return 0

    def make_key_tuple(self,):
        return (self.brand_id,)


    def scoring_help(self,**kwargs):
        dm =kwargs.get('demense',None)
        own_score =kwargs.get('own_score',False)

        if own_score:
            score_table = model.Own_Brand_Demense_scores
        else:
            score_table = model.Brand_Demense_scores

        import demense
        if dm is None:
            dm = demense.Global(self.d)

        label = self.brand_name + u" in "+dm.demense_name
        idargs = { 'brand_id':self.brand_id, 'id':dm.demense_id}
        return score_table, idargs, label 


    def score_fn(self,**kwargs):
        cls , args_upd ,label = self.scoring_help(**kwargs)
        kwargs2 = dict(kwargs)
        kwargs2.update(args_upd)
        return cls(**kwargs2)

    def get_demenses(self,):
        import itertools
        return itertools.chain(self.get_all_nations(),self.get_all_supernations())

    def get_all_parent_brand(self,):

        s = """SELECT brand_id,brand_name 
                  FROM brands JOIN bdrcshared.divisions USING(division_id) 
                     WHERE own_criteria ='Y'"""

        self.f.execute(s)
        rows = self.f.fetchall()
        return rows
        
