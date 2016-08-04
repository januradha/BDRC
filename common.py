# -*- coding: utf-8 -*-

from bdrcshared.zimmer import *

import os, local, binascii, sys, HTMLParser, re
import Cookie
import datetime
import string

full_month_names = ['January','February','March','April','May','June','July','August','September','October','November','December']
short_month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


class _FormCommon(object):
    #get_form_value = ScreenBase.get_form_value
    def get_form_value(self,name, default=None,factory = None):
        try:
            result = self.form[name]
            if hasattr(result,"value"):
                result = result.value.strip()
        except:  result = default

        #Force to unicode to handle any accents or other unicode only
        # glyph which come back from the user.
        if type(result) is str:
            result = result.decode('utf-8')

        if factory:
            #Use factory callable to convert to required type.
            try: result = factory(result)
            except: result = default

        return result


class ScreenBase(_FormCommon):
    '''Check user is logged on and has access to the screen
    '''
    def __init__(self, *args, **kwargs):
        import db
        import gatekeeper
        import cgi
        import sys
        import user
        self.d = db.connect()
        self.f = self.d.cursor()
        ses = user.UserSession(self.d, self.f)
        ses.validate_login()
        self.me = user.Users(self.d, ses.user_id, f=self.f)

        # ensure user has access to this screen before continuing, if they
        # don't they'll automatically be bumped to their default page
        gatekeeper.access_control(self.me)

        # get any incoming args
        self.form = cgi.FieldStorage()
        self.parts = path_info_parts()

        # additional setup
        self.setup(**kwargs)

    def setup(self,):
        pass



    def get_form_value(self,name, default=None,factory = None):
        try:
            result = self.form[name]
            if hasattr(result,"value"):
                result = result.value.strip()
        except:  result = default

        #Force to unicode to handle any accents or other unicode only
        # glyph which come back from the user.
        if type(result) is str:
            result = result.decode('utf-8')

        if factory:
            #Use factory callable to convert to required type.
            try: result = factory(result)
            except: result = default

        return result


    def out_form(self,body,extra_unsafe={},safe_replace={}):
        o = rtvTemplate(self.template)
        o = o.replace('!HEADER!', rtvTemplate('header.html'))
        o = o.replace('$HEADER_TITLE', self.page_title)
        o = o.replace('$HEADER_CENTER', '<td class="header-center">'+self.page_title+'</td>')
        o = o.replace('$BREADCRUMB', self.breadcrumbs())
        o = o.replace('!BREADCRUMB!', self.breadcrumbs())
        o = o.replace('!LIST!', body)

        for tag,text in extra_unsafe.items():
            o = o.replace(tag,text or "")

        t = string.Template(o)
        o = t.safe_substitute(safe_replace)

        stdOutput(o, me=self.me)



class SimpleFormWrapper(_FormCommon):
    '''Wrapper for legacy pages so they can access common controls.'''
    def __init__(self,form):
        self.form = form

#--------------
def stdReplace(o, *args, **kwargs):
    "replace standard place holders"

    me = kwargs.get('me', None)
    if me:
        o = o.replace('$MY_NAME', me.full_name)
        o = o.replace('$MENU_BAR', me.menubar())

    o = o.replace('!HEADER!', rtvTemplate('header.html'))
    o = o.replace('$MY_NAME', '')
    o = o.replace('$HEADER_CENTER', '')
    o = o.replace('!TITLE!', local.title)
    o = o.replace('->&nbsp;', '&#187;')
    o = o.replace('::', '|')
    o = o.replace('!FTPHOST!', "https://%s" % local.ftp_hostname)
    o = o.replace('!DOCPATH!', local.docpath)
    o = o.replace('!CGIPATH!', local.cgipath)
    o = o.replace('$USERS_CSS', local.users_css)
    o = o.replace('!GUESTRATE_CGIPATH!', local.guestrate_cgipath)
    o = o.replace('!VV_CGIPATH!', local.vv_cgipath)
    o = o.replace('$END_JS_BLOB', '')  # end of generic templates to add extra JS etc
    try:
        o = o.replace('!HOST!', 'https://%s' % os.environ["HTTP_HOST"])
    except:
        pass

    # now fake session business to test caching problems that some venues have
    import datetime
    o = o.replace('$SESSION_FOOL', str(datetime.datetime.now()))



    return o

#--------------
def stdOutput(o, *args, **kwargs):
    '''Final loading of substitutions used on every page, replace all the
        strings, and output the final content'''

    o = stdReplace(o, **kwargs)
    
    print "Cache-Control: no-cache"
    print "Content-type: text/html; charset=utf-8\n"
    # use exception to prevent the moaning in the logs when the browser isn't accepting output
    try:
        if type(o) == unicode:
            print o.encode('utf-8')
        else:
            print o
    except:
        pass


    
#--------------
def back_to_user(msg):
    '''simple report the message back to the user, 
        adjusting for the user being online or in a term'''

    if online_mode():
        dm(msg)
    else:
        print msg
    sys.exit()


#--------------
def rtvTemplate(template, *args, **kwargs):
    "retrieve and return the specified template"

    rtn_unicode = kwargs.get('rtn_unicode', True)

# if the template can't be found pick up the default index instead
    x = "templates/%s" % template
    try:
        form_file = open(x)
    except:
        x = "templates/missing.html"
        try:
            form_file = open(x)
        except:
            dm('Error detected when accessing template %(template)s' % locals())

    o = form_file.read()
    form_file.close()

    if rtn_unicode:
        return unicode(o, 'utf-8')
    else:
        return o


#--------------
def rtvFile(file_name):
    "retrieve and return the specified file"

    x = os.path.basename(file_name)
    try:
        form_file = open(file_name)
    except:
        dm('Error detected when accessing file %s' % x)

    o = form_file.read()
    form_file.close()

    return o

#--------------
def rtvCheckTemplate(template, *args, **kwargs):
    """checks for the existence of the specified template"""

# if the template can't be found pick up the default index instead
    x = "templates/%s" % template
    try:
        form_file = open(x)
    except:
        return False
    form_file.close()
    return True



#--------------
def checkFile(file_name):
    "checks for the existence of the file"
    
    try:
        form_file = open(file_name)
    except:
        return False
    form_file.close()
    return True


#--------------
def darkRow(trClass=None):
    if trClass:
        return ''
    else:
        return ' class="alt"'

def send_to_front_page():
    '''Send the user back to the front page, in this case it'll probably
    be the login page. This may be used when cookies go amiss or users
    try and access pages they're not allowed to use etc'''

    # store where we're coming from so we can bounce the user back to where they wanted
    # after they've logged on
    try: uri = os.environ['REQUEST_URI']
    except: uri = None
    else:
       set_cookie_value(name='failed_uri', value=uri) 


    o = 'Location: !HOST!!DOCPATH!\n'
    print stdReplace(o)
    sys.exit()


#--------------
def decode(text):
    return binascii.a2b_base64(text)


#--------------
def encode(text):
    return binascii.b2a_base64(text)




#--------------
def field_message(text, id=None,disabled=False):
    '''Return the specified text in a <span> wrapper formatting the message'''

    insert_id=''
    if id :
        insert_id='id="%s"'%id

    insert_disabled=''
    if disabled:
        insert_disabled='style="display:none;"'

    return '<span class="message-field" %s %s >%s</span>' % ( insert_id , insert_disabled ,text)



#--------------
def period_text(end_month, split=False, **kwargs):

    long_names = kwargs.get('long_names', False)
    single_month = kwargs.get('single_month', False)
    offset_months = kwargs.get('offset_months', 3)
    split_text = kwargs.get('split_text', False)


    'return period text for 3 month span. E.g. "Jul - Sep"'

    if long_names:
        m = full_month_names
    else:
        m = short_month_names

    end = m[end_month-1]

    # don't add 2nd part of period if single_month has been specified
    if single_month:
        return end

    str_month = end_month - offset_months
    if str_month < 1:
        str_month + 12

    start_mn = m[str_month]

    if split:
        return '%s\n%s' % (start_mn, end)
    elif split_text:
        return '%s%s%s' % (start_mn, split_text, end)
    else:
        return '%s - %s' % (start_mn, end)


def previous_period(*args, **kwargs ):
    '''return the previous period based on clocking back the specified criteria'''

    year = kwargs.get('year', None)
    month = kwargs.get('month', None)
    size = kwargs.get('size', 1)

    if year and month:
        month -= size
        while month < 1:
            year -= 1
            month += 12
        
    return year, month




#--------------
def set_month_names(month, offset=3):
    '''return formatted month names for the latest period and the one
    defined by the offset'''

# get the start and end month names which are needed for the mailers
    end_month_name = full_month_names[month-1]

    str_month = month - offset
    if str_month < 1:
        str_month + 12
    start_month_name = full_month_names[str_month]

    return start_month_name, end_month_name




def format_user_list(user_rows, *args, **kwargs):

    import user_types as ut
    me = kwargs.get('me', None)

    edit_link = kwargs.get('edit_link', False)

    x = ['<table id="userList" class="tablesorter">']
    x.append('''<thead><tr>
                <th class="left header">User Name</th>
                <th class="left header">Full Name</th>
                <th class="left header">Email</th>
                <th class="header">Last Login</th>
                </tr></thead><tbody>''')

    for user_id, user_name, full_name, email, last_login in user_rows:

        if me and ut.user_control_admin(me.groups):
            user_name = u'<a href="!CGIPATH!user_control.py?user_id=%s">%s</a>' % (user_id, user_name)
            full_name = u'<a href="!CGIPATH!user_control.py?user_id=%s">%s</a>' % (user_id, full_name)
            cell_padding = u''
        else:
            cell_padding = u'nolink'

        if edit_link:
            user_name = '<a href="!CGIPATH!edit_user.py?user_id=%(user_id)s">%(user_name)s</a>' % locals()
            full_name = '<a href="!CGIPATH!edit_user.py?user_id=%(user_id)s">%(full_name)s</a>' % locals()


        email_link = '<a href="mailto:%(email)s">%(email)s</a>' % locals()
        if last_login is None:
            last_login = '-'
        else:
            last_login = last_login.strftime('%b %d, %Y')

        x.append('''<tr>    
                        <td class="left %(cell_padding)s">%(user_name)s</td>
                        <td class="left %(cell_padding)s">%(full_name)s</td>
                        <td class="left">%(email_link)s</td>
                        <td>%(last_login)s</td>
                    </tr>
                ''' % locals())
    x.append('<tbody></table>')

    return ''.join(x)



def set_one_month_arg(score_type='1'):
    '''return one month arg if the score type is for 1 month calcs, or if no
    score_type specified, default to the one month arg'''
    return ['', '/onemonth'][int(score_type == '1')]


def is_one_month(parts):
    '''return True/False according to whether "onemonth" is in the args'''
    return 'onemonth' in parts


#--------------
def select_num(slt_name, start, end, *args, **kwargs):

    begin_ex_opt = kwargs.get('begin_ex_opt', [] )
    end_ex_opt = kwargs.get('end_ex_opt', [] )
    preselect = kwargs.get('preselect', False)
    onfocus = kwargs.get('onfocus', False)
    disabled = kwargs.get('disabled', '')
    extended_args = kwargs.get('extended_args', '')
    extra_cls = kwargs.get('extra_cls', '')

    if onfocus:
        setinput = '''onFocus="setinput(this, '');" onBlur="setoutput(this, '');"'''
    else:
        setinput = ''
    select = [u'''<select class="text-input  %(extra_cls)s" name="%(slt_name)s" id="%(slt_name)s" %(disabled)s %(extended_args)s %(setinput)s >''' % locals()]
#    select.append('<option value="">---- select ----')

    for txt,val in begin_ex_opt:
        if preselect is not False and val == preselect:
            selected = 'selected'
        else:
            selected = ''
        select.append(u'<option value="%(val)d" %(selected)s>%(txt)s' % locals())


    for x in range(start, end+1):
        if preselect is not False and x == preselect:
            selected = 'selected'
        else:
            selected = ''

        txt = u'%(x)d' % locals()

        select.append(u'<option value="%(x)d" %(selected)s>%(txt)s' % locals())
  
    for txt,val in end_ex_opt:
        if preselect is not False and val == preselect:
            selected = 'selected'
        else:
            selected = ''
        select.append(u'<option value="%(val)d" %(selected)s>%(txt)s' % locals())



    select.append(u'</select>')
    return ''.join(select)



def real_score_tooltip(real_score):
    '''return tool_tip for the real score, no score means no tip'''
    if real_score is None:
        return ''
    else:
        return '''onmouseover="Tip('%(real_score)s', BORDERCOLOR,'#a0a0d0',BGCOLOR, '#ffffe7', BALLOON, false, ABOVE, true )" onmouseout="UnTip()"''' %  locals()


def ovr_result_id(questionnaire_id, result_id, year):
    '''return new key details for the specified key items to allow for tend and comparison
    data when new questions are used but we need to show old results from other questionnaires
    and questions. The specified year is the data year, i.e. looking for 7000 (a 2010) result
    will not exist in 2009, so we override to the 2009 equivalent.
    '''

    # key: quest_id, result id
    #   returns new values to use
    if year == 2009:
        override_sets = {
        (7, 7000): (2, 0),
        (7, 7001): (2, 1),
        (7, 7002): (2, 2),
        (7, 7003): (2, 3),
        (7, 7004): (2, 4),

        (7, 7101): (2, 105),
        (7, 7102): (2, 106),
        (7, 7113): (2, 107),
        (7, 7191): (2, 108),
        (7, 7110): (2, 109),

        (7, 7171): (2, 111),
        (7, 7170): (2, 112),
        (7, 7115): (2, 114),
        (7, 7116): (2, 116),
        (7, 7117): (2, 117),
        (7, 7118): (2, 118),
        (7, 7119): (2, 120),
        (7, 7120): (2, 139),  # NOTE: availability question was in "points raised" pre 2010
        (7, 7180): (2, 160),
        (7, 7181): (2, 137),
        (7, 7141): (2, 142),
        (7, 7142): (2, 143),
        (7, 7143): (2, 145),
        (7, 7144): (2, 147),
        (7, 7145): (2, 148),
        (7, 7146): (2, 149),
        (7, 7147): (2, 150),
        (7, 7148): (2, 151),
        (7, 7152): (2, 152),
        (7, 7149): (2, 153),
        (7, 7153): (2, 158),

# not showing trend data for M&A section
#        (7, 7182): (2, 121),
#        (7, 7183): (2, 122),
#        (7, 7184): (2, 123),
#        (7, 7185): (2, 124),
#        (7, 7186): (2, 125),
#        (7, 7187): (2, 126),
#        (7, 7188): (2, 161),
#        (7, 7190): (2, 159),
#        (7, 7114): (2, 157),

# not showing trend data for follow up section
#        (7, 7192): (2, 156),
        (7, 7241): (2, 131),
        (7, 7242): (2, 132),
        (7, 7243): (2, 133),
        (7, 7244): (2, 134),
        (7, 7245): (2, 135),
        (7, 7246): (2, 136),
        (7, 7250): (2, 130),

        (7, 7340): (2, 162),
        (7, 7341): (2, 163),
        }

    elif year == 2010:
        override_sets = {
        # Tele 2011 -> 2010
        (8, 8000): (7, 7000),
        (8, 8001): (7, 7001),
        (8, 8002): (7, 7002),
        (8, 8003): (7, 7003),
        (8, 8004): (7, 7004),
        (8, 8101): (7, 7101),
        (8, 8102): (7, 7102),
        (8, 8110): (7, 7110),
        (8, 8113): (7, 7113),
        (8, 8114): (7, 7114),
        (8, 8115): (7, 7115),
        (8, 8116): (7, 7116),
        (8, 8117): (7, 7117),
        (8, 8118): (7, 7118),
        (8, 8119): (7, 7119),
        (8, 8120): (7, 7120),
        (8, 8141): (7, 7141),
        (8, 8142): (7, 7142),
        (8, 8143): (7, 7143),
        (8, 8144): (7, 7144),
        (8, 8145): (7, 7145),
        (8, 8146): (7, 7146),
        (8, 8147): (7, 7147),
        (8, 8148): (7, 7148),
        (8, 8149): (7, 7149),
        (8, 8150): (7, 7150),
        (8, 8151): (7, 7151),
        (8, 8152): (7, 7152),
        (8, 8153): (7, 7153),
        (8, 8164): (7, 7164),
        (8, 8165): (7, 7165),
        (8, 8166): (7, 7166),
        (8, 8170): (7, 7170),
        (8, 8171): (7, 7171),
        (8, 8180): (7, 7180),
        (8, 8181): (7, 7181),
        (8, 8182): (7, 7182),
        (8, 8183): (7, 7183),
        (8, 8184): (7, 7184),
        (8, 8185): (7, 7185),
        (8, 8186): (7, 7186),
        (8, 8187): (7, 7187),
        (8, 8188): (7, 7188),
        (8, 8189): (7, 7189),
        (8, 8190): (7, 7190),
        (8, 8191): (7, 7191),
        (8, 8192): (7, 7192),
        (8, 8200): (7, 7200),
        (8, 8242): (7, 7242),
        (8, 8243): (7, 7243),
        (8, 8244): (7, 7244),
        (8, 8245): (7, 7245),
        (8, 8247): (7, 7247),
        (8, 8250): (7, 7250),
        (8, 8340): (7, 7340),
        (8, 8341): (7, 7341),
        (8, 8514): (7, 7514),
        (8, 8582): (7, 7582),
        (8, 8583): (7, 7583),
        (8, 8584): (7, 7584),
        (8, 8585): (7, 7585),
        (8, 8586): (7, 7586),
        (8, 8587): (7, 7587),
        (8, 8588): (7, 7588),
        (8, 8589): (7, 7589),
        (8, 8590): (7, 7590),

        # RFP 2011 - > 2010
        (9, 9000): (3, 300),
        (9, 9004): (3, 304),
        (9, 9007): (3, 307),
        (9, 9008): (3, 308),
        #(9, 9009): (3, 309),
        (9, 9010): (3, 310),
        (9, 9011): (3, 311),
        (9, 9014): (3, 314),
        (9, 9015): (3, 315),
        (9, 9016): (3, 316),
        (9, 9017): (3, 317),
        (9, 9019): (3, 319),
        (9, 9020): (3, 320),
        (9, 9021): (3, 321),
        (9, 9022): (3, 322),
        (9, 9023): (3, 323),
        (9, 9024): (3, 324),

        # Email 2011 - > 2010
        (10, 10000): (4, 400),
        (10, 10004): (4, 404),
        (10, 10007): (4, 407),
        (10, 10008): (4, 408),
        #(10, 10009): (4, 409),
        (10, 10010): (4, 410),
        (10, 10011): (4, 411),
        (10, 10014): (4, 414),
        (10, 10015): (4, 415),
        (10, 10016): (4, 416),
        (10, 10017): (4, 417),
        (10, 10019): (4, 419),
        (10, 10020): (4, 420),
        (10, 10021): (4, 421),
        (10, 10022): (4, 422),
        (10, 10023): (4, 423),
        (10, 10024): (4, 424),

        # Email+RFP 2011 - > 2010
        (11, 11000): (5, 500),
        (11, 11004): (5, 504),
        (11, 11007): (5, 507),
        (11, 11008): (5, 508),
        #(11, 11009): (5, 509),
        (11, 11010): (5, 510),
        (11, 11011): (5, 511),
        (11, 11014): (5, 514),
        (11, 11015): (5, 515),
        (11, 11016): (5, 516),
        (11, 11017): (5, 517),
        (11, 11019): (5, 519),
        (11, 11020): (5, 520),
        (11, 11021): (5, 521),
        (11, 11022): (5, 522),
        (11, 11023): (5, 523),
        (11, 11024): (5, 524),

        # Email+RFP+Tele 2011 - > 2010
        (12, 12000): (6, 600),
        (12, 12004): (6, 604),
        (12, 12007): (6, 6192),
        (12, 12008): (6, 6200),
        (12, 12014): (6, 6242),
        (12, 12015): (6, 6243),
        (12, 12016): (6, 6244),
        (12, 12017): (6, 6245),
        (12, 12020): (6, 6247),
        (12, 12021): (6, 6121),
        (12, 12022): (6, 6122),
        (12, 12023): (6, 623),
        (12, 12024): (6, 624),
        }


        #No Overrides for 2012-> 2011 
        # as the data model changed enough that a data copy
        # and translate was done instead.

    elif year == 2012:
        ## In 2013 we tried to keep the same result_ids
        questionnaire_ov = {
            83:27,
            84:28,
            85:29,
            86:30,
            87:31,
            88:32,
            89:34,
        }
        if questionnaire_id in questionnaire_ov:
            #calcualte the response here..
            return ( questionnaire_ov[questionnaire_id], result_id,)
        else:
            override_sets = {}

    # quite a number of changes/rationalisation for the 2015 surveys
    elif year==2013 or year==2014:
        override_sets = {   # simple mappings
            (156, 15164): (89, 15617),
            (156, 15165): (89, 15624),
            (155, 15210): (90, 15682),
            (155, 15401): (90, 15681),
        }

        if (questionnaire_id,result_id) in override_sets.keys():
            return override_sets[(questionnaire_id,result_id)]

        questionnaire_ov = {
            140:85,
            141:86,
            142:87,
            143:83,
            144:84,
            145:88,
            146:116,
            147:117,
            148:115,
            149:114,
            150:36,
            151:56,
            152:57,
            153:58,
            154:59,
            155:90,
            156:89,
            157:106,
            158:105
        }

        if result_id == 15355:  # follow-up: likelyhood of getting business
            return (questionnaire_ov.get(questionnaire_id,questionnaire_id), 15356)

        result_map = {}

        if questionnaire_id in [140,145,155,156]:
            result_map = {
                15750:15514,
                15751:15582,
                15752:15583,
                15753:15584,
                15754:15585,
                15755:15586,
                15756:15587,
                15757:15588,
                15758:15589,
                15759:15490,

                19750:19514,
                19751:19582,
                19752:19583,
                19753:19584,
                19754:19585,
                19755:19586,
                19756:19587,
                19757:19588,
                19758:19589,
                19759:19490,
            }

        elif questionnaire_id in [141,142,143,144]:
            result_map = {
                19750:19514,
                19751:19582,
                19752:19583,
                19753:19584,
                19754:19585,
                19755:19586,
                19756:19587,
                19757:19588,
                19758:19589,
                19759:19490,
            }

        elif questionnaire_id in [150,151,152,153,154]:
            result_map = {
                15000:36000,
                15001:36001,
                15002:36002,
                15003:36003,
                15004:36004,

                15020:36020,
                15021:36021,
                15022:36022,
                15023:36023,
                15024:36024,


                15101:36101,
                15102:36102,
                15110:36110,
                15113:36113,
                15300:36300,
                15302:36302,
                15304:36304,
                15306:36306,
                15131:36131,
                15116:36116,
                15117:36117,
                15118:36118,
                15119:36119,
                15611:36138,
                15120:36120,
                15313:36313,
                15146:36319,
                15317:36317,
                15149:36323,
                15661:36325,
                15324:36324,
                15157:36315,
                15164:36326,
                15165:36327,
                15166:36328,
                15170:36170,
                15171:36171,
                15181:36181,
                15401:36332,
                15191:36191,
                # manner
                15750:36450,
                15751:36452,
                15752:36453,
                15753:36451,
                15754:36454,
                15755:36455,
                15756:36456,
                15757:36458,
                15758:36457,
                15759:36459,
                # follow-up
                15192:36192,
                15200:36200,
                15250:36250,
                15210:36334,
                15246:36246,
                15233:36339,
                15369:36369,
                15122:36122,
                15364:36364,
                15359:36359,
                15245:36245,
                15370:36354,
                15374:36374,
                15379:36379,
                15384:36384,
                15244:36244,
                15243:36243,
                15249:36249,
#            15210:15682,    # may be wrong
            }

        return (questionnaire_ov.get(questionnaire_id,questionnaire_id), result_map.get(result_id,result_id))

    else:
        override_sets = {}
        


    return override_sets.get((questionnaire_id, result_id), (questionnaire_id, result_id))


def results_table_override(questionnaire_id, result_id):
    '''return true if the specified result can be overridden for league tables
    '''
    return True
    table_results = [7340, 7341, ]

    return bool(result_id in table_results)

    
def result_override(year, month):
    '''return true/false according to whether the specified period has result overrides
    '''
    return True  # 2011 looks like we need permanent override work

def overall_warning():
    '''2010 overall screens warning message'''
    return ''

    return u'''<div class="block left">
    IMPORTANT: NOTES ABOUT JANUARY DATA - FEBRUARY DATA
    <p>
       Please note that the measurement of Electronic, along with Telephone, enquiry handling standards was implemented for the first time in January with the following implications:
    <ul>
    <li>The most recent data represents January - Febrauary only, not the previous 3 months as usually shown, due to the additional measurement of the electronic enquiries and revised telephone criteria
    <li>As a result of this, the number of enquiries received by each group is less than usual. Scores for smaller groups such as IET, Sundial, Apex, Merchant Inns, as well as all venue-level scores must be interpreted with particular caution
    <li>By the end of March we will once again be showing the full 3 months of data
    <li>To appear in the Overall benchmark you must have received an Electronic enquiry as well as a Telephone enquiry
    <li>Use the drop down Menu on the left hand side of the screen to switch between enquiry channel
    </ul>
    </div>'''



def brand_warning(questionnaire_id=None):
    '''2010 early months warning'''
    return ''

    if questionnaire_id==6:
        return overall_warning()

    return u'''<div class="block left">
    IMPORTANT: NOTES ABOUT JANUARY DATA - FEBRUARY DATA
    <p>
        Please note that the measurement of Electronic, along with Telephone, enquiry handling standards was implemented for the first time in January with the following implications:
    <ul>
    <li>The most recent data represents January - February only, not the previous 3 months as usually shown, due to the additional measurement of the electronic enquiries and revised telephone criteria
    <li>As a result of this, the number of enquiries received by each group is less than usual. Scores for smaller groups such as IET, Sundial, Apex, Merchant Inns, as well as all venue-level scores must be interpreted with particular caution
    <li>By the end of March we will once again be showing the full 3 months of data
    <li>Use the drop down Menu on the left hand side of the screen to switch between enquiry channel
    </ul>
    </div>'''

def venue_warning(questionnaire_id=None):
    return ''

    if questionnaire_id==6:
        return overall_warning()

    return u'''<div class="block left">
    IMPORTANT: NOTES ABOUT JANUARY DATA - FEBRUARY DATA
    <p>
        Please note that the measurement of Electronic, along with Telephone, enquiry handling standards was implemented for the first time in January with the following implications:
    <ul>
    <li>The most recent data represents January - February only, not the previous 3 months as usually shown, due to the additional measurement of the electronic enquiries and revised telephone criteria
    <li>As a result of this, the number of enquiries received by each group is less than usual. All venue-level scores must be interpreted with particular caution for this month
    <li>At the end of of March we will once again be showing the full 3 months of data
    <li>Use the drop down Menu on the left hand side of the screen to switch between enquiry channel
    </ul>'''



def new_question_notice():
    return u'''Please note this question was added to the questionnaire in 2011.'''



def language_dropdown(pre_select,name,*args,**kwargs):

    label = kwargs.get('label','Language')
    f     = kwargs.get('f',None)
    extra_opts     = kwargs.get('extra_options',[])

    s = '''SELECT id, name FROM bdrcshared.languages ORDER BY name'''
    f.execute(s)
    opts = list(f.fetchall())
    opts.extend(extra_opts)

    return make_simple_dropdown(opts,pre_select,name,label,*args,**kwargs)

