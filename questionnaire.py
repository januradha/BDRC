
#set  -*- coding: utf-8 -*-

# qsts: qst_id, desc, actual questionnaire to use e.g. 2009 e-enquiries are 
# the same but we need to be able to differentiate between them
# list: description, questionnaire template, dropdown seq
# NOTE: sell call_types in event_scheduler too
import model

qsts = {

    2: ('2009 standard telephone', 2, None),
    3: ('2010 e-enquiry: RFP', 3, 5),
    4: ('2010 e-enquiry: email', 3, 4),
    5: ('2010 [virtual] web and email combined', None, 3),
    6: ('2010 [virtual] tele, web and email combined', None, 1),
    7: ('2010 standard telephone', 7, 2),
    8: ('2011 standard telephone', 8, 2),
    9: ('2011 e-enquiry: RFP', 9, 5),
    10:('2011 e-enquiry: email', 10, 4),
    11:('2011 [virtual] web and email combined', None, 3),
    12:('2011 [virtual] tele, web and email combined', None, 1),
    13:('2011 Keith Prowse tele', 13, 1),  # based on std 2011 tele (8)
    14:('2012 Keith Prowse tele', 13, 1),

#-------------------------------------------------------
# At id 15, these new questionnaires almst all
# use the years master survery.
    15:('2012 Master survey',15 , None ),
    16:('2012 Benchmark telephone',15 , 1 ),
    17:('2012 Benchmark email',15 , 1 ),
    18:('2012 Benchmark rfp',15 , 1 ),

    19:('2012 Hilton telephone',15 , 1 ),
    20:('2012 Hilton email',15 , 1 ),
    21:('2012 Hilton rfp',15 , 1 ),
    22:('2012 Hilton Group reservation (telephone)',15 , 1 ),
    23:('2012 Hilton Individual reservation',37 , 1 ),
    33:('2012 Hilton Events',15 , 1 ),

    24:('2012 Intercontinental telephone',15 , 1 ),
    25:('2012 IC email',15 , 1 ),
    26:('2012 IC rfp',15 , 1 ),

    #These are the available reporting surveys....
    27:('2012 [virtual] Meetings Combined Electronic', None ,2 ),
    28:('2012 [virtual] Meetings Overall' , None ,1 ), 
    29:('2012 [virtual] Telephone meetings', None, 3),
    30:('2012 [virtual] Email meetings', None, 4),
    31:('2012 [virtual] RFP meetings', None, 5),
    32:('2012 [virtual] Group Reservations Telephone', None, 7),
    34:('2012 [virtual] Events Telephone',15 , 6 ),

    35:('2012-4 Standard Long Stay Telephone',35,1),
    36:('2012-4 [virtual] Long Stay Telephone',None,22 ),
    37:('2012 Standard Bedroom Telephone',37 , 6 ),
    38:('2012 [virtual] Bedroom Telephone',38 , 6 ),
    40:('2012-4 Standard Longstay Email',35 , 6 ),
    41:('2012-4 Standard Longstay RFP',35 , 6 ),

    #Long stat virtuals
    56:('2012-4 [virtual] Longstay Email',38 , 24 ),
    57:('2012-4 [virtual] Longstay Rfp',38 , 25 ),
    58:('2012-4 [virtual] Longstay Combined Elec',38 , 23 ),
    59:('2012-4 [virtual] Longstay Combined Alll',38 , 21 ),


    #IMBT legacy imports
    42: ('2009 standard telephone', None, None),
    43: ('2009 e-enquiry: web', None, None),
    44: ('2009 e-enquiry: email', None, None),

	#Hilton Direct
    45:('2012 [virtual] Hilton Direct Telephone',None,9),
    46:('2012 Hilton Direct Telephone',46,7),
    47:('2012 [virtual] Hilton Direct Electronic',None,10),
    48:('2012 Hilton Direct Email',46,7),
    49:('2012 Hilton Direct RFP',46,7),

    50:('2012Q3 Hilton telephone',15 , 1 ),
    51:('Agency Telephone',51 , 1 ),
    52:('2012Q3 Hilton Direct Telephone',46 , 7 ),
    53:('2012Q3 Hilton Group reservation (telephone)',15 , 1 ),
    54:('2012Q3 Hilton Individual reservation',37 , 1 ),
    55:('2012Q3 Hilton Events',15 , 1 ),


    #Competitor shopping is a special case questionnaire.
    60:('Competitor Shopping',60,10 ),

    61:('Agency Email',51 , 1 ),
    62:('Agency RFP',51 , 1 ),


    63: ('[virtual] Hilton Direct Overall', 46 ,8),



# At id 70, these new questionnaires almst all
# use he years master survery.
    70:('2013 Benchmark telephone',70 , 1 ),
    71:('2013/4 Benchmark email',70 , 1 ),
    72:('2013/4 Benchmark rfp',70 , 1 ),
    73:('2013/4 Hilton telephone',70 , 1 ),
    74:('2013/4 Hilton email',70 , 1 ),
    75:('2013/4 Hilton rfp',70 , 1 ),

    76:('2013 Intercontinental telephone',70, 1 ),
    77:('2013 IC email',70 , 1 ),
    78:('2013 IC rfp',70 , 1 ),

    79:('2013/4 Hilton Social Events Telepone',79 ,1 ),
    80:('2013/4 Hilton Groups Telephone',80 , 6 ),
    81:('2013/4 Individual Reservation Telephone', 81, 6 ),
    82:('2013/4 Hilton Individual Reservation Telephone', 81, 6 ),

    #These are the available reporting surveys....
    83:('2013/4 [virtual] Meetings Combined Electronic', None ,3 ),
    84:('2013/4 [virtual] Meetings Overall' , None ,1 ), 
    85:('2013/4 [virtual] Telephone meetings', None, 2),
    86:('2013/4 [virtual] Email meetings', None, 4),
    87:('2013/4 [virtual] RFP meetings', None, 5),

    88:('2013/4 [virtual] Group Reservations Telephone', None, 12),
    89:('2013/4 [virtual] Events Telephone', None, 21 ),

    90:('2013/4 [virtual] Bedroom Telephone', None, 7),
    
    91:('2013/4 Scandic Email',70, 7),
    92:('2013/4 Scandic RFP', 70, 7),

    #Agency 2013
    93:('2013 Agency Telephone', 93, 1),
    94:('2013 Agency RFP', 93 , 1),
    95:('2013 Agency Email', 93 , 1),
    96:('2013 [virtual] Agency Telephone', None, 42),
    97:('2013 [virtual] Agency RFP', None, 45),
    98:('2013 [virtual] Agency Email', None, 44),
    99:('2013 [virtual] Agency Overall', None, 41),
    100:('2013 [virtual] Agency Combined Electronic', None, 43),

    101:('2013 Agency Accommodation', 93, 7 ),
    102:('2013/4 Keith Prowse',102, 1,),
    103:('[virtual] Keith Prowse',None, 1,),
    104:('2013/4 Social Events Email',79 ,1 ),
    105:('[virtual] 2013/4 Social Events Email',None ,22 ),
    106:('[virtual] 2013/4 Social Events Overall',None ,20 ),
    107:('2013/4 Benchmark Social Telephone',79, 1,),

    108:('2014 Benchmark telephone',70 , 1 ),
    109:('2013/4 Benchmark Group Res Telephone',80 ,1 ),
    110:('2014 Agency Telephone', 93, 1),
    111:('2014 Agency Accommodation', 93, 7 ),
    112:('2013/4 Benchmark Group Res Email',80 ,1 ),
    113:('2013/4 Benchmark Group Res RFP',80,1 ),
    114:('2013/4 [virtual] Group Reservations Overall', None, 11),
    115:('2013/4 [virtual] Group Reservations Combined Electronic', None, 13),
    116:('2013/4 [virtual] Group Reservations Email', None, 14),
    117:('2013/4 [virtual] Group Reservations RFP', None, 15),
    118:('2013/4 Hilton (unused) Social Events Email',79 ,1 ),

    ##2015 Data entry / scoring questionnaires.
    120:('2015 Meetings Telephone ' , 120 ,1 ),
    121:('2015 Meetings Email     ' , 120 ,1 ),
    122:('2015 Meetings RFP       ' , 120 ,1 ),
    123:('2015 Hilton Meetings Telephone ' , 120 ,1 ),
    124:('2015 Hilton Meetings Email       ' , 120 ,1 ),
    125:('2015 Hilton Meetings RFP ' , 120 ,1 ),
    ##These are remove and disabled - No login in the virtual members dict either.
#    126:('2015 Intercontinental Meetings Telephone ' , 120 ,1 ),
    127:('2015 Scandic Meetings Email       ' , 120 ,1 ),
    128:('2015 Scandic Meetings RFP ' , 120 ,1 ),

    129: ('2015 Benchmark Group Res Telephone' , 129 ,1 ), 
    130: ('2015 Benchmark Group Res Email    ' , 129 ,1 ), 
    131: ('2015 Benchmark Group Res RFP      ' , 129 ,1 ), 

    132: ('2015 Hilton Group Res Telephone' , 129 ,1 ), 

    133: ('2015 Benchmark Bedroom Telephone' , 133 ,1 ), 
    134: ('2015 Hilton Bedroom Telephone' , 133 ,1 ), 

    135: ('2015 Benchmark Long stay Telephone' , 135 ,1 ),
    136: ('2015 Benchmark Long stay Email    ' , 135 ,1 ),
    137: ('2015 Benchmark Long stay RFP      ' , 135 ,1 ),

    138: ('2015 Benchmark Social Events Telephones', 138, 1),
    139: ('2015 Hilton Social Events Telephones', 138, 1),



    ##2015 Virtual questionnaires.
    140:('2015/6 [virtual] Meetings Telephone',120 , 5),
    141:('2015/6 [virtual] Meetings Email',120 , 4),
    142:('2015/6 [virtual] Meetings Web/RFP',120 , 3),
    143:('2015/6 [virtual] Meetings Electronic',120 , 2),
    144:('2015/6 [virtual] Meetings Overall',120 , 1),

    145:('2015/6 [virtual] Group Res Telephone',129 , 15),
    146:('2015/6 [virtual] Group Res Email',129 , 14),
    147:('2015/6 [virtual] Group Res Web/RFP',129 , 13),
    148:('2015/6 [virtual] Group Res Electronic',129 , 12),
    149:('2015/6 [virtual] Group Res Overall',129 , 11),

    150:('2015/6 [virtual] Long stay Telephone',129 , 25),
    151:('2015/6 [virtual] Long stay Email',129 , 24),
    152:('2015/6 [virtual] Long stay Web/RFP',129 , 23),
    153:('2015/6 [virtual] Long stay Electronic',129 , 22),
    154:('2015/6 [virtual] Long stay Overall',129 , 21),

    155:('2015/6 [virtual] Bedroom Telephone',129,35),

    156:('2015/6 [virtual] Social Events Telephone',129,45),
    157:('2015/6 [virtual] Social Events Overall',129,41),
    158:('2015/6 [virtual] Social Events Email',129,44),

    159:('2015 Benchmark Social Events Email', 138, 1),

    160:('2015 Marriott Meetings Telephone ' , 120 ,1 ),
    161:('2015 Marriott Meetings Email       ' , 120 ,1 ),
    162:('2015 Marriott Meetings RFP ' , 120 ,1 ),

#    163:('2015 Chelsea FC Meetings Telephone ' , 120 ,1 ), # not required
    164:('2015 Chelsea FC Meetings Email       ' , 120 ,1 ),
    165:('2015 Chelsea FC Meetings RFP ' , 120 ,1 ),


    166:('2015 Chelsea FC Bespoke Matchday Telephone ' , 166 ,1 ),
    167:('2015 Chelsea FC Bespoke Matchday Email       ' , 166 ,1 ),
    168:('2015 Chelsea FC Bespoke Matchday RFP ' , 166 ,1 ),

    169:('2016 Meetings short-form telephone' , 120 ,1 ),
    170:('2015/6 [virtual]  Meetings Long & short all' , None ,0 ),
    171:('2016 Hilton Meetings Telephone' , 120,1 ),
    172:('2016 Hilton Meetings Email       ' , 120 ,1 ),
    173:('2016 Hilton Meetings RFP ' ,  120 ,1 ),
    174:('2016 [virtual] Meetings short-form telephone' , 120 ,6 ),
}

##System for 2015 onwards to detect special huilton electronic.
hilton_electronic_qs=[ 124,125, 172, 173]
##System for 2015 onwards to detect special marriott electronic.
marriott_electronic_qs=[161,162]
##System for 2015 onwards to detect special chelsea/matchday electronic.
matchday_electronic_qs=[167,168]

# active real questionnaires
# Pred 2015 Qs commented out
active_qsts = [#3,4,7, 8, 9, 10, 11, 12,
      #Keith prowse
#      	14,102,

        #16,17,18,20,21, 24,25,26, 
 #       35,37,
 #       40,41,

        #48, 49,50,52,53,54,55,
#       #Agency
 #       51,61,62 ,
        #2013 events
 #       71,72,73,74,75,79,80,81,82, 91,92,104, 107,108,109,112,113,
		#2013 Agency
 #       93,94,95, 101,110,111,

        ##Competitor Shops
        60,

        ###2015##
        #meetings
        120,121,122,123,124,125, 160,161, 127,128, 160,161,162,163,164,165, 172,173,
        #group res,
        129,130,131,132,
        #Bedroom
        133,134,
        #Long stay
        135,136,137,
        #Social
        138,139,159,
        #Matchday
        166,167,168,

        ##2016 Updates & new questinnaires.
        169, 171,

        ]


#List of questionnaire's where the responses need to be copied
# for processing.

virtual_qsts = [ 27, 28, 29, 30, 31 ,32 ,34, 36 ,38, 45,47,56,57,58,59 ,63,
                83, 84, 85, 86, 87, 88, 89, 90,
                #96, 97, 98, 99, 100,
                103, 105, 106,
                114,115,116,117,
                #2015
                 140 , 141 , 142 , 143 , 144 ,

                 145 , 146 , 147 , 148 , 149 , 
                 150 , 151 , 152 , 153 , 154 ,

                 155 ,

                 156 ,
                 157, 158 ,
                 170 , 174,
                ]


virtual_members = {
    5: [ 3 ,4 ],
    6: [ 7 , 3, 4],
    11: [ 9, 10],
    12: [ 8, 9, 10 ],
    27: [ 17, 18  ,20 ,21 ,25, 26 , 43, 44 ,],
    28: [ 16, 17 ,18 ,19,20,21 ,24,25,26 ,42,43,44 ,50,],
    29: [ 16, 19 ,24 , 42 ,50],
    30: [ 17, 20, 25 , 44],
    31: [ 18, 21, 26 ,43 ],
    32: [ 22, 53 ],
    36: [ 35 ],
    34: [ 33 ,55 ],
    38: [ 37, 23, 54  ],

    56: [40],
    57: [41],
    58: [40,41],
    59: [35,40,41],

    8: [8],
    9: [9],
    10: [10],
#KP Was never consolidated pre 2013 Q4.
#    13: [13,14,],

    63: [ 46, 52,48,49 ],
    45: [ 46, 52,],
    47: [ 48, 49 ],

    83: [ 71, 72 , 74, 75, 77 ,78 ,91,92],
    84: [ 70, 71 , 72 , 73 ,74, 75, 76, 77, 78,92,91 ,108],
    85: [ 70, 73, 76 ,108 ],
    86: [ 71, 74, 77, 91 ],
    87: [ 72, 75, 78, 92 ],

    88: [ 80, 109 ],
       
    89: [ 79 , 107 ],
    105: [ 104 ],
    106: [ 79, 104 , 107],
    90: [ 81,82 ,],

    #Remove Agency virtual questionnaires so login works for users with these questionnaires! see CMBT-393
    #96: [ 93,110 ],
    #97: [ 94, ],
    #98: [ 95, ],
    #99: [ 93, 94, 95,110 ],
    #100: [ 94, 95,  ],
    103: [102, ],
    
    114: [ 80, 109 ,112,113],
    115: [ 112,113 ],
    116: [ 112 ],
    117: [ 113 ],

    140: [ 120 ,123 , 160, 163 , 171 ] ,
    141: [ 121 ,124 , 127 , 161, 164 ,172] ,
    142: [ 122 ,125 , 128 ,162, 165 , 173] ,
    143: [ 121, 122 , 124, 125, 127,128 ,161, 164 ,162,165 ,172 , 173] ,
    144: [ 120, 121, 122 ,123 ,124 ,125 ,127,128, 160, 163 ,161,164 ,162, 165, 171, 172, 173] ,
    145: [ 129, 132 ] ,
    146: [ 130, ] ,
    147: [ 131, ] ,
    148: [ 130 ,131 ] ,
    149: [ 129, 130, 131 , 132 ] ,
    150: [ 135 ] ,
    151: [ 136 ] ,
    152: [ 137 ] ,
    153: [ 136, 137, ] ,
    154: [ 135, 136, 137, ] ,
    155: [ 133 , 134, ] ,
    156: [ 138, 139,] ,
    157: [ 138, 139, 159 ] ,
    158: [ 159,] ,
    170: [ 120, 121, 122 ,123 ,124 ,125 ,127,128, 160, 163 ,161,164 ,162, 165, 169, 171, 172, 173] ,
    174: [ 169,] ,
}


q_2012_hbaa = [ 51,61,62 ]
q_2012_hiltondirect = [45, 46, 47, 48, 49 , 52]
q_2012_set = [ 16, 17,18 ,19,20,21,22,23,24,25,26,33,35,37,50,53,54,55]
q_2013_set = [ 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 91, 
               92, 93, 94, 95, 101, 102, 104, 107 ,108,110,111 ,109 ,112,113]
q_2015_set = range(120,140) + range(159, 170) +range(171,175)

longstay_set = [ 35 , 40, 41] 
bedroom_set = [ 37 ] 
keithprowse_set = [ 102 ] 


consolidate_questionnaires_2012 = [
#    3, 4, 5, 6, 7, 
#    8, 9, 10, 11, 12,
#     27, 28, 29, 30, 31, 32,34,
    #Longstay
    36 , 56, 57, 58, 59,
    #Bedroom
    38,
    #HIlton direct
    45, 47, 63
]

consolidate_questionnaires_2013 = [
    #Meetings
    84, 85, 83, 86, 87,
    #GoupRes
    88,
    #Social/Events
    89, 105, 106,

    #Longstay
    36 , 56, 57, 58, 59,

    #Individual Res / Bedroom
    90,

    #KP And Hospitality
    103,
]

consolidate_questionnaires_2015 = range(140,159)+[170,174]


currently_active_virtuals = consolidate_questionnaires_2015

# short descriptions for real questionnaires
qst_short_desc = {
    1: 'Telephone',
    2: 'Telephone',
    3: 'RFP',
    4: 'Email',
    7: 'Telephone',
    8: 'Telephone (2011)',
    9: 'RFP (2011)',
    10:'Email (2011)',
    13: '2011 KP Telephone',
    14: '2012 KP Telephone',
    15: 'Master survery (2012)',
    16: 'Telephone (2012)',
    17: 'Email (2012)',
    18: 'RFP (2012)',
    19: 'Telephone (2012)',
    20: 'Email (2012)',
    21: 'RFP (2012)',
    22: 'Group Res',
    23: 'Single Res',
	24: 'Telephone (2012)',
    25: 'Email (2012)',
    26: 'RFP (2012)',
    33: 'Events',
    35: 'Long stay telephone',
    37: 'Bedroom',
    38: 'Bedroom',
    40: 'Longstay Email',
    41: 'Longstay RFP',
    42: 'Telephone',
    43: 'RFP',
    44: 'Email',
    45: 'Hilton Direct Telephone',
    46: 'Hilton Direct Telephone',
    47: 'Hilton Direct Email',
    48: 'Hilton Direct Email',
    49: 'Hilton Direct RFP',

    50: 'Telephone (2012 Q3+)' ,
    51: 'Agency Telephone',
    52: 'Hilton Direct Telephone (2012 Q3+)',
    53: 'Group res (2012 Q3+)',
    54: 'Single res (2012 Q3+)',
    55: 'Events (2012 Q3+)',
    60: 'Competitor Shopping',
    61: 'Agency Email',
    62: 'Agency RFP',
    63: 'Hilton Direct Overall',

    70: '2013 Telephone',
    71: '2013/4 Email',
    72: '2013/4 Rfp',
    73: '2013/4 Telephone',
    74: '2013/4 Email',
    75: '2013/4 Rfp',
 
    76: '2013 Telephone',
    77: '2013 Email',
    78: '2013 Rfp',

    79: '2013/4 Hilton Social Events Telephone',
    80: '2013/4 Groups Telephone',
    81: '2013/4 Individual Reservation Telephone',
    82: '2013/4 Hilton Individual Reservation Telephone',

    91: '2013 Scandic Email',
    92: '2013 Scandic RFP',

    93: '2013 Agency Telephone',
    94: '2013/4 Agency RFP',
    95: '2013/4 Agency Email',
    101: '2013/4 Agency Accommodation',
    102: 'KP Hospitality',

    104: '2013/4 Benchmark Social Events Email',
    107: '2013/4 Benchmark Social Events Telephone',
    108: '2014 Telephone',
	109: '2013/4 Benchmark Group Reservation',
    110: '2014 Agency Telephone',
    111: '2014 Agency Accommodation',
    112: '2013/4 Benchmark Group Reservations Email',
    113: '2013/4 Benchmark Group Res RFP',

    120:'2015 Meetings Telephone',
    121:'2015 Meetings Email' ,
    122:'2015 Meetings RFP' ,
    123:'2015 Hilton Meetings Telephone',
    124:'2015 Hilton Meetings Email',
    125:'2015 Hilton Meetings RFP',
#    126:'2015 Intercontinental Meetings Telephone',
    127:'2015 Scandic Meetings Email',
    128:'2015 Scandic Meetings RFP',

    129:'2015 Benchmark Group Res Telephone',
    130:'2015 Benchmark Group Res Email',
    131:'2015 Benchmark Group Res RFP',

    132:'2015 Hilton Group Res Telephone',

    133:'2015 Benchmark Bedroom Telephone',
    134:'2015 Hilton Bedroom Telephone',

    135:'2015 Benchmark Long stay Telephone',
    136:'2015 Benchmark Long stay Email',
    137:'2015 Benchmark Long stay RFP',

    138:'2015 Benchmark Social Events Telephone',
    139:'2015 Hilton Social Events Telephone',

    159:'2015 Benchmark Social Events Email',

    160:'2015 Marriott Meetings Telephone',
    161:'2015 Marriott Meetings Email',
    162:'2015 Marriott Meetings RFP',

    163:'2015 Chelsea FC Meetings Telephone',
    164:'2015 Chelsea FC Meetings Email',
    165:'2015 Chelsea FC Meetings RFP',

    166:'2015 Chelsea FC Matchday Telephone',
    167:'2015 Chelsea FC Matchday Email',
    168:'2015 Chelsea FC Matchday RFP',
    169:'2016 Meetings - Quick Check',

    171:'2016 Hilton Meetings Telephone',
    172:'2016 Hilton Meetings Email',
    173:'2016 Hilton Meetings RFP',
}

# list of like questionnaire types, helps things like enquiry dropdowns
group_qsts = {
    'Telephone': (1, 2, 7, 8 ,13,14,16 ,19, 23, 24, 35, 37, 42, 46, 50,51 ,52,54, 
                  70,73, 76 , 81 , 82  ,93 ,101,102,108,110,111, 120 , 123, 133 , 134 ,169, 171) ,
    'RFP': (3, 9 , 18, 21, 26, 43, 41, 49 , 62, 72 , 75, 78 , 91, 94, 122, 125, 128, 173 ),
    'Email': (4, 10 , 17, 20, 25, 40, 44, 48  , 61, 71, 74, 77 , 92, 95, 121, 124, 172, 127, ) ,
    'Group Res.': (22,53,80,109,112,113 , 129,130,131,132 , ),
    'Events': (33,55,79,107,104 ,138, 139, 159 ),
    'Long Stay (All)': (35 , 40, 41, 135,136,137 ),
    'Long Stay (Telephone)': (35 , 135 ),
    'Long Stay (Email)': (40,  136 ),
    'Long Stay (RFP)': (41, 137 ),
    'Agency': ( 93,94,95 , 101, 110,111,),
    'Hospitality': (102, )
}


# questionnaires texts to use for user screens. E.g. titles and dropdown options
# online reports
user_desc = {
    2: ('Call results only 2009'),
    3: ('RFP Enquiry Handling (2010)'),
    4: ('Email Enquiry Handling (2010)'),
    5: ('Combined Electronic Enquiries (2010)'),
    6: ('Overall Enquiry Handling (2010)'),
    7: ('Telephone Enquiry Handling (2010)'),
    8: ('Telephone Enquiry Handling (2011)'),
    9: ('RFP Enquiry Handling (2011)'),
    10:('Email Enquiry Handling (2011)'),
    11:('Combined Electronic Enquiries (2011)'),
    12:('Overall Enquiry Handling (2011)'),
    13: ('Keith Prowse: Telephone'),
    14: ('Keith Prowse: Telephone'),
    103: ('Keith Prowse: Telephone'),
    102: ('Keith Prowse: Telephone'),
    16: ('Telephone Enquiry Handling'),
    17: ('RFP Enquiry Handling)'),
    18: ('Email Enquiry Handling'),
    19: ('2012 Hilton telephone'),
    20: ('2012 Hilton email'),
    21: ('2012 Hilton rfp'),
    22: ('2012 Hilton Group reservation (telephone)'),
    23: ('2012 Hilton Individual reservation'),
    24: ('2012 Intercontinental telephone'),
    25: ('2012 IC email'),
    26: ('2012 IC rfp'),
    27: (' - Meetings Combined Electronic (2012)'),
    28 :('Meetings Overall (2012)'),
    29: (' - Meetings Telephone (2012)'),
    30: (' - Meetings Email (2012)'),
    31: (' - RFP Enquiry Handling (2012)'),
    32: ('Group Res Enquiry Handling (2012)'),
    33: ('2012 Hilton Events'),
    34: ('Events telephone (2012)'),
    35: ('Long stay telephone (2012-4)'),
    36: (' - Long stay telephone (2012-4)'),
    56: (' - Long stay Email (2012-4)'),
    57: (' - Long stay RFP (2012-4)'),
    59: ('Long stay Combined (2012-4)'),
    58: ('Long stay Combined Electronic (2012-4)'),
    37: ('Standard Bedroom telephone (2012)'),
    38: ('Bedroom telephone (2012)'),
    40:('2012-4 Standard Longstay Email' ),
    41:('2012-4 Standard Longstay RFP', ),

    45:(' - Hilton Direct Telephone'),
    46:('2012 Hilton Direct Telephone'),

    47:(' - Hilton Direct Email'),
    48: ('Email Enquiry Handling (2012)'),
    49: ('RFP Enquiry Handling (2012)'),
    50:('2012Q3 Hilton telephone'),
    51:('Agency telephone'),
    61:('Agency Email'),
    62:('Agency RFP'),
    52:('2012Q3 Hilton Direct Telephone'),
    53:('2012Q3 Hilton Group reservation (telephone)'),
    54:('2012Q3 Hilton Individual reservation'),
    55:('2012Q3 Hilton Events'),

    63:('Hilton Direct Overall'),


    70:('2013 Benchmark telephone'),
    71:('2013 Benchmark email' ),
    72 :('2013 Benchmark rfp'),
    73:('2013 Hilton telephone' ),
    74:('2013 Hilton email' ),
    75:('2013 Hilton rfp' ),

    76:('2013 Intercontinental telephone' ),
    77:('2013 IC email') ,
    78:('2013 IC rfp' ),

    79:('2013 Social Events Telephone' ),
    80:('2013 Hilton Groups Telephone'),
    81:('2013 Individual Reservation Telephone'),

    82:('2013 Hilton Individual Reservation Telephone'),
    83: (' - Meetings Combined Electronic (2013)'),
    84 :('Meetings Overall (2013)'),
    85: (' - Meetings Telephone (2013)'),
    86: (' - Meetings Email (2013)'),
    87: (' - RFP Enquiry Handling (2013)'),
    88: (' - Group Res Telephone (2013)'),
    89: (' - Events Telephone (2013)'),
    90: ('Individual Reservation'),

    93: ('2013 Agency Telephone'),
    94: ('2013 Agency RFP'),
    95: ('2013 Agency Email'),
    96: ('2013 Agency Telephone'),
    97: ('2013 Agency RFP'),
    98: ('2013 Agency Email'),
    99: ('2013 Agency Overall'),
    100: ('2013 Agency Combined Electronic'),


    101: ('2013 Agency Accommodation'),
    103: ('Hospitality'),
    105:('2013 Social Events Email' ),
    106:('2013 Social Events Overall' ),

    108:('2014 Benchmark telephone'),
    110:('2014 Agency Telephone'),
    111: ('2014 Agency Accommodation'),

    114 :('Group Res Overall (2013)'),
    115: ('Group Res  - Combined Electronic (2013)'),
    116: ('Group Res  - Email (2013)'),
    117: ('Group Res  - RFP  (2013)'),


    140:('2015-6 Meetings - Telephone'),
    141:('2015-6 Meetings -- Email'),
    142:('2015-6 Meetings -- Web/RFP'),
    143:('2015-6 Meetings - Electronic'),
    144:('2015-6 Meetings Overall'),
    170:('2015-6 Meetings Overall inc Quick Check'),
    174:('2015-6 Meetings - Quick Check'),

    145:('2015-6 Group Res - Telephone'),
    146:('2015-6 Group Res -- Email'),
    147:('2015-6 Group Res -- Web/RFP'),
    148:('2015-6 Group Res - Electronic'),
    149:('2015-6 Group Res Overall'),

    150:('2015-6 Long stay - Telephone'),
    151:('2015-6 Long stay -- Email'),
    152:('2015-6 Long stay -- Web/RFP'),
    153:('2015-6 Long stay - Electronic'),
    154:('2015-6 Long stay Overall'),

    155:('2015-6 Bedroom Telephone'),

    156:('2015-6 Social Events  - Telephone'),
    157:('2015-6 Social Events Overall'),
    158:('2015-6 Social Events  - Email'),


}


# overall result_id sets, keyed by questionnaire_id
overall_sets = {
    2: [0, 1, 2, 3, 4],
    3: [300, 304],
    4: [400, 404],
    5: [500, 504],
    6: [600, ],
    7: [7000, 7001, 7002, 7003, 7004],
    8: [8000, 8001, 8002, 8003, 8004],
    9: [9000, 9004],
    10:[10000, 10004],
    11:[11000, 11004],
    12:[12000, ],
    13: [13000, 13001, 13002, 13003, 13004],
    14: [13000, 13001, 13002, 13003, 13004],
    103: [13000, 13001, 13002, 13003, 13004],
    27: [15000, 15004 ,19000 ,19001,19002, 19003, 19004  , 24000, 24004 , 19021,19022, 19023, 19024 ],
    28: [15000, 15004 ,19000 ,19001, 19002, 19003, 19004 , 24000, 24004, 19021,19022, 19023, 19024],
    29: [15000, 15001 ,15002, 15003 ,15004 ,19000 ,19001,19002, 19003, 19004, 24000,24001,24002,24003,24004 , 19021,19022, 19023, 19024],
    30: [15000, 15004 ,19000 ,19001,19002, 19003, 19004 , 24000, 24004, 19021,19022, 19023, 19024],
    31: [15000, 15004 ,19000 ,19001,19002, 19003, 19004 , 24000, 24004, 19021,19022, 19023, 19024],
    32: [15000, 15001 ,15002, 15003 ,15004 ,19000 ,19001,19002, 19003, 19004 , 19021,19022, 19023, 19024],

    34: [15000, 15001 ,15002, 15003 ,15004 ,19000 ,19001,19002, 19003, 19004 , 19021,19022, 19023, 19024],

    36: [36000, 36001, 36002, 36003, 36004 ] , 
    56: [36000,  36004 ] , 
    57: [36000,  36004 ] , 
    58: [36000,  36004 ] , 
    59: [36000,  36004 ] , 
    38: [38000, 38001 ,38002, 38003 ],
    45: [46000, 46001, 46002, 46003 ,46004  ],
    47: [46000, 46001, 46002, 46003 ,46004  ],
    63: [46000, 46001, 46002, 46003 ,46004  ],
    51: [51000, 51001, 51002, 51003 ],
    83: [15000, 15004 ,19000 ,19001, 19002, 19003, 19004, 24000, 24004, 19021, 19022, 19023, 19024 ],
    84: [15000, 15004 ,15005 ,19000 ,19001, 19002, 19003, 19004, 19005, 24000, 24004, 24005, 19021, 19022, 19023, 19024],
    85: [15000, 15001 ,15002 ,15003, 15004, 15005, 19000, 19001, 19002, 19003, 19004, 19005, 24000, 24001, 24002, 24003, 24004,24005, 19021, 19022, 19023, 19024, 19025],
    86: [15000, 15004 ,19000 ,19001, 19002, 19003, 19004, 24000, 24004, 19021, 19022, 19023, 19024],
    87: [15000, 15004 ,19000 ,19001, 19002, 19003, 19004, 24000, 24004, 19021, 19022, 19023, 19024],

    88: [15000, 15001 ,15002, 15003 ,15004 ,15005, 15025, 19000 ,19001,19002, 19003, 19004, 19005, 19021,19022, 19023, 19024, 19025],
    89: [15000, 15001 ,15002, 15003 ,15004 ,15005, 15025, 19000 ,19001,19002, 19003, 19004, 19005, 19021,19022, 19023, 19024, 19025],
    105: [15000, 15004 ,19000 ,19004, 19024, 19025],
    106: [15000, 15004 ,19000 ,19004, 19024, 19025],

    90: [ 15000, 15001, 15002, 15003 ,15004 ,15021,15022,15023,15024,19000, 19001, 19002, 19003 ,19004 ,19021,19022,19023,19024 ],
    96:  [],
    97:  [],
    98:  [],
    99:  [],
    100: [],
    103: [ 15000, 15001, 15002, 15003 ,15004 ,15021,15022,15023,15024,  13000, 13001, 13002, 13003 ,13004 ,13021,13022,13023,13024, ],

    114: [15000, 15001 ,15002, 15003 ,15004 ,15005, 15025, 19000 ,19001,19002, 19003, 19004, 19005, 19021,19022, 19023, 19024, 19025],
    115: [15000, 15001 ,15002, 15003 ,15004 ,15005, 15025, 19000 ,19001,19002, 19003, 19004, 19005, 19021,19022, 19023, 19024, 19025],
    116: [15000, 15001 ,15002, 15003 ,15004 ,15005, 15025, 19000 ,19001,19002, 19003, 19004, 19005, 19021,19022, 19023, 19024, 19025],
    117: [15000, 15001 ,15002, 15003 ,15004 ,15005, 15025, 19000 ,19001,19002, 19003, 19004, 19005, 19021,19022, 19023, 19024, 19025],


    140: [ 15000, 15001 ,15002 ,15003, 15004, 15005, 15006, 19000, 19001, 19002, 19003, 19004, 19005, 19006, 24000, 24001, 24002, 24003, 24004,24005, 24006 , 19021, 19022, 19023, 19024, 19025 , 19026 , 25020, 25021 , 25022, 25023 , 25024, 25025,25026 ] ,
    141: [ 15000, 15004 ,19000 ,19001, 19002, 19003, 19004, 24000, 24004, 19021, 19022, 19023, 19024, 25020, 25021 , 25022, 25023 ,25024, 25025,25026 ],
    142: [ 15000, 15004 ,19000 ,19001, 19002, 19003, 19004, 24000, 24004, 19021, 19022, 19023, 19024, 25020, 25021 , 25022, 25023 ,25024, 25025,25026 ],
    143: [ 15000, 15004 ,19000 ,19001, 19002, 19003, 19004, 24000, 24004, 19021, 19022, 19023, 19024, 25020, 25021 , 25022, 25023 ,25024, 25025,25026 ],
    144: [ 15000, 15004 ,15005 ,15006, 19000 ,19001, 19002, 19003, 19004, 19005, 19006, 24000, 24004, 24005, 24006, 19021, 19022, 19023, 19024, 19026, 25020, 25021 , 25022, 25023 ,25024, 25025,25026 ],
    170: [ 15000, 15004 ,15005 ,15006, 19000 ,19001, 19002, 19003, 19004, 19005, 19006, 24000, 24004, 24005, 24006, 19021, 19022, 19023, 19024, 19026, 25020, 25021 , 25022, 25023 ,25024, 25025,25026 ],
    174: [ 15000, 15004 ,15005 ,15006, 19000 ,19001, 19002, 19003, 19004, 19005, 19006, 24000, 24004, 24005, 24006, 19021, 19022, 19023, 19024, 19026, 25020, 25021 , 25022, 25023 ,25024, 25025,25026 ],

    145: [ 15000, 15001 ,15002 ,15003, 15004, 15005, 15006, 19000, 19001, 19002, 19003, 19004, 19005, 19006, 19021, 19022, 19023, 19024, 19025 , 19026 ,],
    146: [ 15000, 15004 ,19000 ,19001, 19002, 19003, 19004, 19021, 19022, 19023, 19024],
    147: [ 15000, 15004 ,19000 ,19001, 19002, 19003, 19004, 19021, 19022, 19023, 19024],
    148: [ 15000, 15004 ,19000 ,19001, 19002, 19003, 19004, 19021, 19022, 19023, 19024],
    149: [ 15000, 15004 ,15005 ,15006, 19000 ,19001, 19002, 19003, 19004, 19005, 19006, 19021, 19022, 19023, 19024, 19026],

    150: [ 15000, 15001 ,15002 ,15003, 15004, 15005, 15006, ],
    151: [ 15000, 15004 ,],
    152: [ 15000, 15004 ,],
    153: [ 15000, 15004 ,],
    154: [ 15000, 15004 ,15005 ,15006, ],

    155: [ 15000, 15001 ,15002 ,15003, 15004, 15005, 15006, 19000, 19001, 19002, 19003, 19004, 19005, 19006, 19021, 19022, 19023, 19024, 19025 , 19026 ,],
    156: [ 15000, 15001 ,15002 ,15003, 15004, 15005, 15006, 19000, 19001, 19002, 19003, 19004, 19005, 19006, 19021, 19022, 19023, 19024, 19025 , 19026 ,],
    157: [ 15000, 15004, 19000,  19004, 19024,],
    158: [ 15000, 15004, 19000,  19004, 19024,],


}

# each OV result_id keyed by questionnaire_id
overall_result_ids = {
    2: 0,
    3: 300,
    4: 400,
    5: 500,
    6: 600,
    7: 7000,
    8: 8000,
    9: 9000,
    10:10000,
    11:11000,
    12:12000,
    13:13000,
    14:13000,
    27:15000,
    28:15000,
    29:15000,
    30:15000,
    31:15000,
    32:15000,
    34:15000,
    36:36000,
    56:36000,
    57:36000,
    58:36000,
    59:36000,
    38:38000,
    45:46000,
    47:46000,
    63:46000,
    83:15000,
    84:15000,
    85:15000,
    86:15000,
    87:15000,
    88:15000,
    89:15000,
    105:15000,
    106:15000,
    90:15000,
    103:13000,
    105:15000,
    106:15000,
    114:15000,
    115:15000,
    116:15000,
    117:15000,

    140: 15000,
    141: 15000,
    142: 15000,
    143: 15000,
    144: 15000,
    170: 15000,
    174: 15000,
    145: 15000,
    146: 15000,
    147: 15000,
    148: 15000,
    149: 15000,
    150: 15000,
    151: 15000,
    152: 15000,
    153: 15000,
    154: 15000,
    155: 15000,
    156: 15000,
    157: 15000,
    158: 15000,

}


##qst_channel only needs to be defined for REAL questionnaires (eg, non-virtual)
from  model import EnquiryTarget, EnquiryType
_qst_channel = {
    2: ( EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS),
    3: ( EnquiryType.RFP, EnquiryTarget.MEETINGS),
    4: ( EnquiryType.EMAIL, EnquiryTarget.MEETINGS),
    7: ( EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS),
    8: ( EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS),
    9: ( EnquiryType.RFP, EnquiryTarget.MEETINGS),
    10: ( EnquiryType.EMAIL, EnquiryTarget.MEETINGS),
    #Kieth Prowse....
    13: (EnquiryType.TELEPHONE,EnquiryTarget.HOSPITALITY),
    14: (EnquiryType.TELEPHONE, EnquiryTarget.HOSPITALITY ),
    102: (EnquiryType.TELEPHONE, EnquiryTarget.HOSPITALITY ),
    #2012
    16: ( EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS),
    17: ( EnquiryType.EMAIL, EnquiryTarget.MEETINGS),
    18: ( EnquiryType.RFP, EnquiryTarget.MEETINGS),

    19: ( EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS),
    20: ( EnquiryType.EMAIL, EnquiryTarget.MEETINGS),
    21: ( EnquiryType.RFP, EnquiryTarget.MEETINGS),
    22: ( EnquiryType.TELEPHONE, EnquiryTarget.GROUP ),
    23: ( EnquiryType.TELEPHONE, EnquiryTarget.INDIV ),
    24: ( EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS),
    25: ( EnquiryType.EMAIL, EnquiryTarget.MEETINGS),
    26: ( EnquiryType.RFP, EnquiryTarget.MEETINGS),

    33: ( EnquiryType.TELEPHONE, EnquiryTarget.SOCIAL),
    35: ( EnquiryType.TELEPHONE, EnquiryTarget.LONG),
    36: ( EnquiryType.TELEPHONE, EnquiryTarget.LONG),
    37: ( EnquiryType.TELEPHONE, EnquiryTarget.INDIV),
    40: ( EnquiryType.EMAIL, EnquiryTarget.LONG),
    41: ( EnquiryType.RFP, EnquiryTarget.LONG),
    42: ( EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS),
    43: ( EnquiryType.RFP, EnquiryTarget.MEETINGS),
    44: ( EnquiryType.EMAIL, EnquiryTarget.MEETINGS),

    ##HIlton direct.. #???

    
    53: ( EnquiryType.TELEPHONE,  EnquiryTarget.GROUP ),
    54: ( EnquiryType.TELEPHONE,  EnquiryTarget.INDIV ),
    55: ( EnquiryType.TELEPHONE,  EnquiryTarget.SOCIAL ),

    61: ( EnquiryType.EMAIL, EnquiryTarget.AGENCY),
    62: ( EnquiryType.RFP, EnquiryTarget.AGENCY),

    #2013

    70: ( EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS),
    71: ( EnquiryType.EMAIL, EnquiryTarget.MEETINGS),
    72: ( EnquiryType.RFP, EnquiryTarget.MEETINGS),
    73: ( EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS),
    74: ( EnquiryType.EMAIL, EnquiryTarget.MEETINGS),
    75: ( EnquiryType.RFP, EnquiryTarget.MEETINGS),
    76: ( EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS),
    77: ( EnquiryType.EMAIL, EnquiryTarget.MEETINGS),
    78: ( EnquiryType.RFP, EnquiryTarget.MEETINGS),

    79: ( EnquiryType.TELEPHONE, EnquiryTarget.SOCIAL),
    80: ( EnquiryType.TELEPHONE, EnquiryTarget.GROUP),
    81: ( EnquiryType.TELEPHONE, EnquiryTarget.INDIV),
    82: ( EnquiryType.TELEPHONE, EnquiryTarget.INDIV),
    91: ( EnquiryType.EMAIL, EnquiryTarget.MEETINGS),
    92: ( EnquiryType.RFP, EnquiryTarget.MEETINGS),

    104: ( EnquiryType.EMAIL, EnquiryTarget.SOCIAL),
    118: ( EnquiryType.EMAIL, EnquiryTarget.SOCIAL),
    107: ( EnquiryType.TELEPHONE, EnquiryTarget.SOCIAL),
    108: ( EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS),
    109: ( EnquiryType.TELEPHONE, EnquiryTarget.GROUP),
    110: ( EnquiryType.TELEPHONE, EnquiryTarget.AGENCY),
    111: ( EnquiryType.TELEPHONE, EnquiryTarget.AGENCY_ACCOM),
    112: ( EnquiryType.EMAIL,     EnquiryTarget.GROUP),
    113: ( EnquiryType.RFP,       EnquiryTarget.GROUP),

    120:  (  EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS,  ),
    121:  (  EnquiryType.EMAIL,     EnquiryTarget.MEETINGS,  ),
    122:  (  EnquiryType.RFP,       EnquiryTarget.MEETINGS,  ),
    123:  (  EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS,  ),
    124:  (  EnquiryType.EMAIL,     EnquiryTarget.MEETINGS,  ),
    125:  (  EnquiryType.RFP,       EnquiryTarget.MEETINGS,  ),
    126:  (  EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS,  ),
    127:  (  EnquiryType.EMAIL,     EnquiryTarget.MEETINGS,  ),
    128:  (  EnquiryType.RFP,       EnquiryTarget.MEETINGS,  ),
    129:  (  EnquiryType.TELEPHONE, EnquiryTarget.GROUP  ),
    130:  (  EnquiryType.EMAIL,     EnquiryTarget.GROUP  ),
    131:  (  EnquiryType.RFP,       EnquiryTarget.GROUP  ),
    132:  (  EnquiryType.TELEPHONE, EnquiryTarget.GROUP  ),
    133:  (  EnquiryType.TELEPHONE, EnquiryTarget.INDIV,  ),
    134:  (  EnquiryType.TELEPHONE, EnquiryTarget.INDIV,  ),
    135:  (  EnquiryType.TELEPHONE, EnquiryTarget.LONG,  ),
    136:  (  EnquiryType.EMAIL,     EnquiryTarget.LONG,  ),
    137:  (  EnquiryType.RFP,       EnquiryTarget.LONG,  ),
    138:  (  EnquiryType.TELEPHONE, EnquiryTarget.SOCIAL,  ),
    139:  (  EnquiryType.TELEPHONE, EnquiryTarget.SOCIAL,  ),
    159:  (  EnquiryType.EMAIL, EnquiryTarget.SOCIAL,  ),

    ## TODO - remove querying thes via tele_quest formreports
    # and handle it a diferent way.
    ##We include virtual telephone in heser as well for the reporting code t
    # can reason about hilton.
    85: ( EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS),
    88: ( EnquiryType.TELEPHONE, EnquiryTarget.GROUP),
    89: ( EnquiryType.TELEPHONE, EnquiryTarget.SOCIAL),
    90: ( EnquiryType.TELEPHONE, EnquiryTarget.INDIV),

    140: ( EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS),
    141: ( EnquiryType.EMAIL,     EnquiryTarget.MEETINGS),
    142: ( EnquiryType.RFP,       EnquiryTarget.MEETINGS),
    143: ( EnquiryType.ELECTRONIC,EnquiryTarget.MEETINGS),
    144: ( EnquiryType.OVERALL,   EnquiryTarget.MEETINGS),
    145: ( EnquiryType.TELEPHONE, EnquiryTarget.GROUP),
    146: ( EnquiryType.EMAIL,     EnquiryTarget.GROUP),
    147: ( EnquiryType.RFP,       EnquiryTarget.GROUP),
    148: ( EnquiryType.ELECTRONIC,EnquiryTarget.GROUP),
    149: ( EnquiryType.OVERALL,   EnquiryTarget.GROUP),
    150: ( EnquiryType.TELEPHONE, EnquiryTarget.LONG),
    151: ( EnquiryType.EMAIL,     EnquiryTarget.LONG),
    152: ( EnquiryType.RFP,       EnquiryTarget.LONG),
    153: ( EnquiryType.ELECTRONIC,EnquiryTarget.LONG),
    154: ( EnquiryType.OVERALL,   EnquiryTarget.LONG),
    155: ( EnquiryType.TELEPHONE, EnquiryTarget.INDIV),
    156: ( EnquiryType.TELEPHONE, EnquiryTarget.SOCIAL),
    157: ( EnquiryType.OVERALL, EnquiryTarget.SOCIAL),
    158: ( EnquiryType.EMAIL, EnquiryTarget.SOCIAL),

    160:  (  EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS,  ),
    161:  (  EnquiryType.EMAIL,     EnquiryTarget.MEETINGS,  ),
    162:  (  EnquiryType.RFP,       EnquiryTarget.MEETINGS,  ),
    163:  (  EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS,  ),
    164:  (  EnquiryType.EMAIL,     EnquiryTarget.MEETINGS,  ),
    165:  (  EnquiryType.RFP,       EnquiryTarget.MEETINGS,  ),

    166:  (  EnquiryType.TELEPHONE, EnquiryTarget.MATCHDAY,  ),
    167:  (  EnquiryType.EMAIL,     EnquiryTarget.MATCHDAY,  ),
    168:  (  EnquiryType.RFP,       EnquiryTarget.MATCHDAY,  ),

    169:  (  EnquiryType.SHORT_TELE,EnquiryTarget.MEETINGS,  ),
    170:  (  EnquiryType.OVERALL_INC_SF ,EnquiryTarget.MEETINGS,  ),
    171:  (  EnquiryType.TELEPHONE, EnquiryTarget.MEETINGS,  ),
    172:  (  EnquiryType.EMAIL,     EnquiryTarget.MEETINGS,  ),
    173:  (  EnquiryType.RFP,       EnquiryTarget.MEETINGS,  ),
    174:  (  EnquiryType.SHORT_TELE,       EnquiryTarget.MEETINGS,  ),
}

_criteria_lut = {
    71: model.Criteria.BENCHMARK,
    72: model.Criteria.BENCHMARK,
    73: model.Criteria.BENCHMARK,
    74:  model.Criteria.HILTON,
    75:  model.Criteria.HILTON,
    76:  model.Criteria.HILTON,
    77:  model.Criteria.IC,
    78:  model.Criteria.IC,
    79:  model.Criteria.IC,
    80:  model.Criteria.HILTON,
    81:  model.Criteria.HILTON,
    82:  model.Criteria.HILTON,

    91:  model.Criteria.BENCHMARK,
    92:  model.Criteria.BENCHMARK,


    93:  model.Criteria.BENCHMARK,
    94:  model.Criteria.BENCHMARK,
    101:  model.Criteria.BENCHMARK,
    102:  model.Criteria.KEITHPROWSE,

    104:  model.Criteria.BENCHMARK,
    118:  model.Criteria.HILTON,
    107:  model.Criteria.BENCHMARK,
    108:  model.Criteria.BENCHMARK,
    110:  model.Criteria.BENCHMARK,
    111:  model.Criteria.BENCHMARK,

    120:  model.Criteria.BENCHMARK,
    121:  model.Criteria.BENCHMARK,
    122:  model.Criteria.BENCHMARK,
    123:  model.Criteria.HILTON,
    124:  model.Criteria.HILTON,
    125:  model.Criteria.HILTON,
    126:  model.Criteria.IC,
    127:  model.Criteria.BENCHMARK,
    128:  model.Criteria.BENCHMARK,

    129:  model.Criteria.BENCHMARK,
    130:  model.Criteria.BENCHMARK,
    131:  model.Criteria.BENCHMARK,

    132:  model.Criteria.HILTON,

    133: model.Criteria.BENCHMARK,
    134: model.Criteria.HILTON,

    135: model.Criteria.BENCHMARK,
    136: model.Criteria.BENCHMARK,
    137: model.Criteria.BENCHMARK,

    138: model.Criteria.BENCHMARK,
    139: model.Criteria.HILTON,
    159: model.Criteria.BENCHMARK,

    160:  model.Criteria.MARRIOTT,
    161:  model.Criteria.MARRIOTT,
    162:  model.Criteria.MARRIOTT,

    163:  model.Criteria.CHELSEAFC,
    164:  model.Criteria.CHELSEAFC,
    165:  model.Criteria.CHELSEAFC,

    166:  model.Criteria.CHELSEAFC,
    167:  model.Criteria.CHELSEAFC,
    168:  model.Criteria.CHELSEAFC,

    169:  model.Criteria.BENCHMARK,
    171:  model.Criteria.HILTON,
    172:  model.Criteria.HILTON,
    173:  model.Criteria.HILTON,
}

def default_questionnaire(survey_year, type='all'):
    '''return the default questionnaires for each year. Return None for unrecognised type'''

    types =         ['all','elec','tel']

    # lookup         All    Elec    Tel
    map = {
            2015:   (144,   143,    140),
            2013:   (84,    83,     85),
            2012:   (28,    27,     29),
            2011:   (12,    11,     8),
            0:      (12,    11,     8),     # is this correct for data prior to 2011 ?
        }

    if not type in types:   # spanner out in a nice way if asked for an unknown type
        return None

    typ = types.index(type)
    years = map.keys()
    years.sort(reverse=True)    # sort hi->lo

    for year in years[:-1]:     # scan for relevant year
        if survey_year >= year:
            return map[year][typ]

    return map[years[-1]][typ]  # default to oldest in list


# default reporting pages to this questionnaire_id if the questionnaire
# wasn't specified
default_qst = default_questionnaire(2015) # overall enquiry
#default_qst = 144 # 2015 overall enquiry
#default_qst = 84 # 2013 overall enquiry
#default_qst = 28 # 2012 overall enquiry
#default_qst = 12

def tele_quest(questionnaire_id):
    '''Return True/False according to whether the qst is a tele call'''
    return Questionnaires(quest =  questionnaire_id).etype == EnquiryType.TELEPHONE

def electronic_quest(questionnaire_id):
    '''Return True/False according to whether the qst is an electronic call'''
    return  Questionnaires(quest =  questionnaire_id).etype in  [ EnquiryType.EMAIL, EnquiryType.RFP,]


def rfp_quest(questionnaire_id):
    '''Return True/False according to whether the qst is an electronic call'''
    return  Questionnaires(quest =  questionnaire_id).etype == EnquiryType.RFP

class Questionnaires:
    def __init__(self, *args, **kwargs):

        '''
override_flow is used to tell the survey.py process that under certain responses
the flow can alter

   key: page 
        list if lists: (response number, value to check for, page to do if true)


flow determines the order that questionnaire templates are used


expanding_selection are those questions that will cause a sub-question
to appear in the form depending on the question's response. These are
used to trigger onload event to set the dependant sub-question to it's
proper state should the user refresh the page or be coming back in 
from an earlier page, say reviewing. There is a placehold in
the question template that is set to call init(), but we don't want that
in every page, so if the page isn't in this list, the placeholder is cleared.
To find templates needing init() use: grep -l "init(" *    
        '''

        self.override_flow = {}
        self.expanding_questions = []
        self.flow = []

        quest = kwargs.get('quest', None)
        self.brand_id = kwargs.get('brand_id', None)
        self.venue_id = kwargs.get('venue_id', None)
        self.quest  = quest


        self.desc, self.templ_dir , self.order = qsts.get(self.quest,(None,None,None))
        self.is_active = ( self.quest in active_qsts )
        self.is_virtual = (self.quest in virtual_qsts )
        self.user_desc = user_desc.get(self.quest,"missing user description")

        if not self.is_virtual:
            self.short_desc = qst_short_desc.get(self.quest,"missing description")
            self.members = []
            self.overall_sets = []
            self.overall_result_id = None
        else:
            self.short_desc = qst_short_desc.get(self.quest,"virtual")
            self.overall_sets = overall_sets[self.quest]
            self.overall_result_id = overall_result_ids[self.quest]
            self.members = virtual_members.get(self.quest,[])
            self.overall_result_ids = [ self.overall_result_id ]
            if self.overall_result_id == 15000:
                self.overall_result_ids.extend([ 19000, 24000 ])
                if self.brand_id == 225:
                    self.overall_result_id = 19000
                #elif self.brand_id == 5:
                #    self.overall_result_id = 25020



        self.etype , self.etarget = _qst_channel.get(self.quest, (None , None,))

        if quest is None:pass
        elif quest == 1:
            self.flow = ['0', '1', '3b', '4', '5', '6', '6b', '6e', '7', '9', '10', '12', '14', '15', '16', 
                        '19', '20', '21', '25', '26', '28', '29', '32', '99', 'end']

            self.override_flow = {
                             '1' : (('3a', ['1','4'], '5'), ('3a', '3', '4')),
                             '4' : (('4c', '1', '6e'), ),
                             '6' : (('6a', '2', '7'), ),
                             '19' : (('19_4', '1', '32'), ),
                             '21' : (('24', '3', '26'), ),
                             }

            self.expanding_questions = ['10', '26']

        elif quest == 2:
            self.flow = ['start', '0', '1', '3b', '4', '5', '6', '6b', '6e', '7', '9', '10', '12', '14', '15', '16', 
                        '19', '20', '21', '25', '26', '28', '32', '99', 'end']

            self.override_flow = {
                             '1' : (('3a', ['1','4'], '5'), ('3a', '3', '4')),
                             '4' : (('4c', '1', '6e'), ),
                             '6' : (('6a', '2', '7'), ),
                             '19' : (('19_3', '1', '32'), ),
                             '21' : (('24', '3', '26'), ),
                             }

            self.expanding_questions = ['10', '26']

        # electronic questionnaires
        elif quest in (3, 4, 9, 10 ):
            self.flow = ['start', '0', ]
            self.proprietary_pages()
            self.flow.append('end')

        # 2010 Telephone
        elif quest == 7:
            self.flow = ['start', '1', '3b', '4', '5', '6', '6b', '6e', '7', '9', '10', '12', '13', '15', '16', 
                        '19', '20', '21', '24', '25', '32', '99', 'end']

            self.override_flow = {
                             '1' : (('3a', ['1','4'], '5'), ('3a', '3', '4')),
                             '4' : (('4c', '1', '6e'), ),
                             '6' : (('6a', '2', '7'), ),
                             '19' : (('19', '2', '25'), ),
                             }

            self.expanding_questions = ['10', '21']


        # 2011 Telephone
        elif quest == 8:
            
            self.flow = ['start', '1', '3b', '4', '5', '6', '6b', '6e', '7', '9', '10', '12', '13', '15', '16', 
                        '19', '20', '21', '24', '25', '32', '99', ]
            self.proprietary_pages()
            self.flow.append('end')




            self.override_flow = {
                             '1' : (('3a', ['1','4'], '5'), ('3a', '3', '4')),
                             '4' : (('4c', '1', '6e'), ),
                             '6' : (('6a', '2', '7'), ),
                             '19' : (('19', '2', '25'), ),
                             }

            self.expanding_questions = ['10',]


        # 2011/2012 Telephone Keith Prowse only
        elif quest in [ 13 , 14 ]:
            
            self.flow = ['start', '1', '3b', '4', '5', '6', '6b', '6e', '7', '9', '10', '12', '13', '15', '16', 
                        '19', '20', '21', '24', '25', '32', '99', ]
            self.proprietary_pages()
            self.flow.append('end')

            self.override_flow = {
                 '1' : (('3a', ['1','4'], '5'), ('3a', '3', '4')),
                 '4' : (('4c', '1', '6e'), ),
                 '6' : (('6a', '2', '7'), ),
                 '19' : (('19', '2', '25'), ),
             }

            self.expanding_questions = ['10',]

        # 2013 Telephone Keith Prowse
        elif quest in [ 102 ]:
            
            self.flow = ['start', 'connection', 'needs_assesment1', 'needs_assesment2',  'mannerapproach','misc', 'followup'  ]
            self.flow.append('end')

            self.override_flow = { }

            self.expanding_questions = self.flow

        # 2012  Telephones
        elif quest in [15 , 16, 19, 23, 33 , 50,54, 55]:
            self.flow = ['start', 'connection', 'needs_assesment1', 'needs_assesment2',  'mannerapproach','misc', 'followup'  ]
            self.proprietary_pages()
            self.flow.append('end')

            self.override_flow = { }

            self.expanding_questions = ['connection',]

        #2012 Hilton Electronic!
        elif quest in [20, 21 ,]:
            self.flow = ['start', 'misc_electronic','hilton_connection', 'needs_assesment1', 'needs_assesment2', 'mannerapproach_electronic','followup' ,'followup_likelihood']
            self.proprietary_pages()
            self.flow.append('end')

            self.override_flow = { 
                    'hilton_connection': (('8a', ['0'], 'followup'),) ,
                }


            self.expanding_questions = ['connection',]

        #2012 Std Electronic
        elif quest in [17,18, ]:
            self.flow = ['start','misc_electronic', 'followup' ,'followup_likelihood']
            self.proprietary_pages()
            self.flow.append('end')

            self.override_flow = { }

            self.expanding_questions = ['connection',]

        # 2012 IC Telephones
        elif quest in [24]:
            self.flow = ['start', 'connection', 'needs_assesment1', 'needs_assesment2_ic',  'mannerapproach','misc_ic', 'followup_ic'  ]
            self.proprietary_pages()
            self.flow.append('end')

            self.override_flow = { }

            self.expanding_questions = ['connection',]

        #2012 IC Email
        elif quest in [ 25, ]:
            self.flow = ['start','misc_electronic', 'followup_ic' ,'followup_likelihood']
            self.proprietary_pages()
            self.flow.append('end')

            self.override_flow = { }

            self.expanding_questions = ['connection',]


        #2012 IC RFP
        elif quest in [ 26 ]:
            self.flow = ['start','misc_electronic', 'followup_ic_rfp' ,'followup_likelihood']
            self.proprietary_pages()
            self.flow.append('end')

            self.override_flow={ }

            self.expanding_questions = ['connection',]




        #2012 HIlton Group res
        elif quest in [ 22, 53 ]:
            self.flow = ['start', 'connection', 'needs_assesment_gr', 'needs_assesment2', 'mannerapproach','misc_gr', 'followup_gr'  ]
            self.proprietary_pages()
            self.flow.append('end')

            self.override_flow = { }

            self.expanding_questions = ['connection',]
        #2012 Std Electronic
        elif quest in [17,18, 25 ,26]:
            self.flow = ['start', 'followup' ]
            self.proprietary_pages()
            self.flow.append('end')

            self.override_flow = { }

            self.expanding_questions = ['connection',]

        #2012 Std Longstay telephone
        elif quest in [35]:
            self.flow = ['start', 'connection', 'needs_assesment1', 'needs_assesment2', 'mannerapproach','misc', 'followup' ,'misc.b' ]
            self.proprietary_pages()
            self.flow.append('end')

            self.override_flow = { }

            self.expanding_questions = ['connection',]

        #2012 Std Longstay electronic
        elif quest in [40, 41]:
            self.flow = ['start', 'misc.electronic', 'followup' , 'misc.b.electronic' ]
            self.proprietary_pages()
            self.flow.append('end')

            self.override_flow = { }

            self.expanding_questions = ['connection',]


       #2012 Std Bedroom telephone
        elif quest in [ 37 ]:
            self.flow = ['start', 'connection', 'needs_assesment1',  'mannerapproach','misc', ]
            self.proprietary_pages()
            self.flow.append('end')

            self.override_flow = { }

            self.expanding_questions = ['connection',]

       #2012 Hilton Direct telephone
        elif quest in [ 46 ,52]:
            self.flow = ['start', 'connection', 'needs_assesment', 'mannerapproach','misc','followup', ]
            self.proprietary_pages()
            self.flow.append('end')
            self.override_flow = { }
            self.expanding_questions = ['connection','needs_assesment','followup',]
       #2012 Hilton Direct electronic 
        elif quest in [ 48,49 ]:
            self.flow = ['start', 'hilton_connection', 'needs_assesment', 'mannerapproach', 'misc_electronic', 'misc_electronic_b',  'followup_electronic',  ]
            self.proprietary_pages()
            self.flow.append('end')
            self.override_flow = { 
                'hilton_connection': (('8c', ['0'], 'misc_electronic_b'),('8b', ['0'], 'misc_electronic_b'),('8a', ['0'], 'misc_electronic'),) ,
                #FIXME: force move tofollowup_electronic, all option of Q20
                #force skip as we cannot ref previouse answered Q's
                'misc_electronic': (('20', ['1','2'], 'followup_electronic'),) ,
            }
            self.expanding_questions = []

       #2012 Agency
        elif quest in [ 51 ]:
            self.flow = ['start', 'connection', 'needs_assesment',  'mannerapproach','misc','followup' ]
            self.proprietary_pages()
            self.flow.append('end')
            self.override_flow = { }
            self.expanding_questions = ['connection','needs_assesment','followup']


        elif quest in [ 61,62 ]:
            self.flow = ['start', 'misc_electronic','followup_electronic' ]
            self.proprietary_pages()
            self.flow.append('end')
            self.override_flow = { }
            self.expanding_questions = ['followup_elec']

       #2012 Competitor shopping telephone
        elif quest in [ 60 ]:
            self.flow = ['start', 'initial', ]
            #NO proprietary pages for competitor shopping.
            #self.proprietary_pages()
            self.flow.append('end')

            self.override_flow = { }

            self.expanding_questions = []

        #2013  meetings  telephone
        elif quest in [ 70,73,76,108 ]:
            self.flow = ['start', 'connection', 'needs_assesment1', 'needs_assesment2', 'mannerapproach','misc', 'misc2_tele', 'followup'  ]
            self.proprietary_pages()
            self.flow.append('end')
            self.override_flow = { }
            self.expanding_questions = []

        #2013  meeting  electionic ## Scandic don't need a custom flow.
        elif quest in [ 71,72 ,  77,78 ,91,92 ]:
            self.flow = ['start', 'misc', 'misc2_elec','followup' ,'follow_elec2'  ]
            self.proprietary_pages()
            self.flow.append('end')
            self.override_flow = { }
            self.expanding_questions = []

        #2013  Hilton meeting  electionic
        elif quest in [ 74, 75 ]:
            self.flow = ['start', 'hilton_connection' , 'needs_assesment1', 'needs_assesment2', 'mannerapproach',  'misc',  'misc2_elec' , 'followup' ,'follow_elec2'  ]
            self.proprietary_pages()
            self.flow.append('end')
            self.expanding_questions = []

            self.override_flow = { 
                    'hilton_connection': (('hil_1', ['0'], 'misc'),) ,
                }


        #2013  Benchmark group res  electionic
        elif quest in [ 112, 113 ]:
            self.flow = ['start',  'misc', 'misc2_elec', 'followup','follow_elec2'   ]
            self.proprietary_pages()
            self.flow.append('end')
            self.override_flow = { }
            self.expanding_questions = []

        #2013  Hilton group res telephone 
        elif quest in [ 80, 109 ]:
            self.flow = ['start', 'connection' , 'needsassessment1', 'mannerapproach', 'misc', 'misc2_tele', 'followup'   ]
            self.proprietary_pages()
            self.flow.append('end')
            self.override_flow = { }
            self.expanding_questions = []
        #2013  Hilton social  
        elif quest in [ 79, 107 ]:
            self.flow = ['start', 'connection' , 'needsassessment1', 'mannerapproach', 'misc', 'misc2_tele', 'followup'   ]
            self.proprietary_pages()
            self.flow.append('end')
            self.override_flow = { }
            self.expanding_questions = []
        #2013   socia Electronic
        elif quest in [ 104, ]:
            self.flow = ['start', 'misc', 'misc2_elec', 'followup' ,'follow_elec2'  ]
            self.proprietary_pages()
            self.flow.append('end')
            self.override_flow = { }
            self.expanding_questions = []



        #2013 Individual
        elif quest in [ 81, 82 , ]:
            self.flow = ['start', 'connection', 'needs_assesment1', 'mannerapproach', 'misc', 'misc2_tele', 'followup'   ]
            self.proprietary_pages()
            self.flow.append('end')
            self.override_flow = { }
            self.expanding_questions = []

        #2013 Agency
        elif quest in [ 93,110  ]:
            self.flow = ['start', 'connection', 'needs_assesment', 'mannerapproach','misc', 'misc2_tele', 'followup', 'follow_tel2'  ]
            self.proprietary_pages()
            self.flow.extend( ['end',  'misc3' ,'misc3_tele', 'end' ])
            self.override_flow = {
                    'connection': (('8b', ['0'], 'misc3'),) ,
                    'followup': (('37', ['3'], 'end'),) ,
                }
            self.expanding_questions = []
        elif quest in [ 94,95, ]:
            self.flow = [ 'start', 'misc', 'misc2_elec','followup' ,'follow_elec2'  ]
            self.proprietary_pages()
            self.flow.append('end')
            self.override_flow = { }
            self.expanding_questions = []

        elif quest in [ 101,111 ]:
            self.flow = ['start', 'connection', 'needs_assesment_accom', 'mannerapproach','misc', 'misc2_tele', 'followup_accom'   ]
            self.proprietary_pages()
            self.flow.extend( [ 'end', 'misc3' ,'misc3_tele', 'end' ])
            self.override_flow = {
                    'connection': (('8b', ['0'], 'misc3'),) ,
            }
            self.expanding_questions = []


        #
        # TODO REFACTOR - this is gettoing torturous.
        #
        ## 2015 - we make most of these the same if poss.
        elif quest >= 120:
            self.override_flow = { }
            if self.etype == EnquiryType.TELEPHONE:
                self.flow = ['start', 'connection', 'needs_assesment1', 'needs_assesment2', 'mannerapproach','misc', 'misc2_tele', 'followup'  ]
                if self.etarget == EnquiryTarget.MEETINGS:
                    #2016 Hilton telephone = extra special question but are benchmarked so this need to available for available 
                    # to all.
                    pos = self.flow.index( 'needs_assesment1')
                    self.flow.insert(pos + 1 , 'hilton_tele_virt' )
            elif self.etype == EnquiryType.SHORT_TELE:
                self.flow = ['start', 'connection', 'short_needs', 'short_mannerapproach','short_misc', 'misc2_tele', 'short_followup' ]
            else:
                if quest in hilton_electronic_qs :
                    self.flow = ['start', 'hilton_connection' , 'needs_assesment1', 'needs_assesment2', 'mannerapproach',  'misc',  'misc2_elec' , 'followup' ,'follow_elec2'  ]
                    self.override_flow = { 
                        'hilton_connection': (('hil_1', ['0'], 'misc'),) ,
                    }
                elif quest in marriott_electronic_qs :
                    self.flow = ['start', 'marriott_connection' , 'needs_assesment1', 'needs_assesment2', 'mannerapproach',  'misc',  'misc2_elec' , 'followup' ,'follow_elec2'  ]
#                elif quest in matchday_electronic_qs :
#                    self.flow = ['start', 'misc', 'misc2_elec','followup' ,'follow_elec2','follow_elec3'  ]
                    self.override_flow = { 
                        'marriott_connection': (('marriott1a', ['0'], 'misc'),  # skip to misc section if NOT a qualifying call (Telephone)
                                                ('marriott2a', ['0'], 'misc'),  # skip to misc section if NOT a qualifying call (Email)
                                                ) ,
                    }
                else:
                    self.flow = ['start', 'misc', 'misc2_elec','followup' ,'follow_elec2'  ]


            if self.etarget == EnquiryTarget.MEETINGS and self.etype != EnquiryType.SHORT_TELE:
                #2016 Hilton telephone +  competitors = extra special question but are benchmarked so this need to available
                # to all.
                self.flow.append('hilton_virtual')

            ##Remove needs_assessment2 from bedroom enquiries.
            if quest in ( 133, 134):
                self.flow.remove('needs_assesment2')

            self.proprietary_pages()
            self.flow.append('end')
            self.expanding_questions = []

    def proprietary_pages(self,):
        '''add proprietary into questionnaire flow'''

        ###TODO Insted of using _quest() function we should
        #      chnage these to  testing self.etype and self.etarget

        if self.venue_id == 1373: # best western central
            self.flow.append('best_western')

        elif self.brand_id in (2,):
            if tele_quest(self.quest):
                self.flow.append('devere_ven_telephone')
            else:
                self.flow.append('devere_ven_electronic')


        elif self.brand_id in ( 19, 29,): # de vere brands
            if tele_quest(self.quest):
                self.flow.append('devere_vh_telephone')
            else:
                self.flow.append('devere_vh_electronic')

        elif self.brand_id in ( 225,): # Hilton brands
            import globaldb as g
            if g.configuration_option("HILTON_PROP_ON"):
                self.flow.append('hilton_prop')

        elif self.brand_id in ( 240,): # Scandic brands
            if electronic_quest(self.quest):
                self.flow.append('scandic')

        elif self.brand_id in ( 257,): # Malmaison
            if tele_quest(self.quest):
                self.flow.append('malmaison')

        elif self.brand_id in ( 259,): # Hotel du Vin
            if tele_quest(self.quest):
                self.flow.append('duvin')

        elif self.brand_id in ( 266,): # glh Reservations 
            if self.quest in (81,82):
                self.flow.append('glh_prop')

        elif self.brand_id in ( 295,): # Marriott international
            if self.quest in ( 160, 161, 162,):
                self.flow.append('marriott_prop')

        ##Seperate if-elif- block.
        ##SHould we check the chelsea venue_id here
        if self.quest in (164,165,167,168):
            self.flow.append('chelsea_elec')


    def nextPage(self, current_page, form=None):
        '''Determine the next page to present'''

        page = None
        if form:
            responses = self.getResponses(form)  #  dict of response : value
            overrides = self.override_flow.get(current_page, []) # list of overriders
            # iterate over the overriders looking for a response that causes redirection
            for override in overrides:
                resp, values, pg = override
                try:
                    x = responses[resp] in values
                except:
                    pass
                else:
                    if x:
                        page = pg
                        break

        
        # no redirection page set, so just look for the next one
        if not page:
            try:
                page = self.flow[self.flow.index(current_page)+1]
            except:
                page = None
        return page


    def getResponses(self, form):
        '''Extract the standard responses from the form and return them as a dictionary'''

        responses = {}
        k = form.keys()
        for key in k:
            if key and key[:2] in ['r_', 's_', 'c_']:  # need to check non-null thanks to konq!
                response = key[2:]
                responses[response] = form[key].value


        return responses


    def get_results_class(self,**kwargs):


        ## WARNING The order of things in the 
        # monster if is important. As somehting dneed to be in q_sets, but
        # have special handling here
        #


        # generate the scores for this questionnaire, but only for display purposes
        if self.quest == 1:
            import event_results_v1
            er = event_results_v1.Event_results_v1
        elif self.quest == 2:
            import event_results_v2
            er = event_results_v2.Event_results_v2
        elif self.quest in (3,4):
            import event_results_v3
            er = event_results_v3.Event_results_v3
        elif self.quest == 7:
            import event_results_v7
            er = event_results_v7.Event_results_v7
        elif self.quest in (9,10):
            import event_results_2011
            er = event_results_2011.EventResultsQ9
        elif self.quest in (8,):
            import event_results_2011
            er = event_results_2011.EventResultsQ8
        elif self.quest in (13,):
            import event_results_2011
            er = event_results_2011.EventResultsQ13
        elif self.quest in (14,):
            import event_results_2011
            er = event_results_2011.EventResultsQ14
        elif self.quest in longstay_set:
            import event_results_longstay
            er = event_results_longstay.create_results
        elif self.quest in bedroom_set:
            import event_results_bedroom
            er = event_results_bedroom.create_results
        elif self.quest in q_2012_set:
            import event_results2012
            er = event_results2012.create_results


        elif self.quest in [80, 109 ,112,113]:
            import event_results_group
            er = event_results_group.create_results

        elif self.quest in [79,107,104 ]:
            import event_results_social
            er = event_results_social.create_results

        elif self.quest in [81, 82 ,]:
            import event_results_2013_individual
            er = event_results_2013_individual.create_results

        elif self.quest in [91,92]:
            import event_results_scandic
            er = event_results_scandic.create_results
        elif self.quest in [93,94,95,101,110,111]:
            import event_results_2013_agency
            er = event_results_2013_agency.create_results

        elif self.quest in keithprowse_set:
            import event_results_keithprowse
            er = event_results_keithprowse.create_results


        elif self.quest in q_2013_set:
            import event_results_2013
            er = event_results_2013.create_results
        elif self.quest in [42,43,44,]:
            import event_results
            #These are legacy and thus cannot rescore these
            #
            er = event_results.Scored_EventResults
        elif self.quest in [60,]:
            import event_results
            #These are not scored because they a *special*.
            #
            er = event_results.Scored_EventResults
        elif self.quest in q_2012_hiltondirect:
            import event_results_hiltondirect
            er = event_results_hiltondirect.create_results
        elif self.quest in q_2012_hbaa:
            import event_results_hbaa
            er = event_results_hbaa.create_results

        elif self.quest in q_2015_set:
            import event_results_2015
            er = event_results_2015.create_results
        else:
            er = None

        return er

    def get_report_class(self,**kwargs):

        ## WARNING The order of things in the 
        # monster if is important. As somehting dneed to be in q_sets, but
        # have special handling here
        #
        if self.quest == 1 :
            import report_v1
            report = report_v1.report_v1
        elif self.quest == 2:
            import report_v2
            report = report_v2.report_v2
        elif self.quest in (3,4):
            import report_v3
            report = report_v3.report_v3
        elif self.quest == 7:
            import report_v7
            report = report_v7.report_v7
        elif self.quest == 8:
            import report_v8
            report = report_v8.report_v8
        elif self.quest in (9,10):
            import report_v9
            report = report_v9.ReportQ9
        elif self.quest == 13:
            import report_v13
            report = report_v13.report_v13
        elif self.quest == 14:
            import report_v14
            report = report_v14.report_v14
        elif self.quest in bedroom_set:
            import reports_bedroom
            report = reports_bedroom.get_report
        elif self.quest in longstay_set:
            import reports_longstay
            report = reports_longstay.get_report
        elif self.quest in q_2012_set:
            import reports_2012
            report = reports_2012.get_report

        elif self.quest in [80,109,112,113]:
            import reports_group
            report = reports_group.get_report

        elif self.quest in [79,104,107]:
            import reports_social
            report = reports_social.get_report

        elif self.quest in [81, 82,]:
            import reports_2013_individual
            report = reports_2013_individual.get_report
        elif self.quest in (91,92):
            import reports_scandic
            report = reports_scandic.get_report

        elif self.quest in [93,94,95,101,110,111]:
            import reports_2013_agency
            report = reports_2013_agency.get_report

        elif self.quest in keithprowse_set:
            import reports_keithprowse
            report = reports_keithprowse.get_report

        elif self.quest in q_2013_set:
            import reports_2013
            report = reports_2013.get_report

        elif self.quest == 42:
            from report_v42 import report_v1 as report_v42
            report = report_v42
        elif self.quest in [43, 44]:
            from report_v43 import report_v2 as report_v43
            report = report_v43
        elif self.quest in q_2012_hiltondirect:
            import reports_hiltondirect
            report = reports_hiltondirect.get_report
        elif self.quest in q_2012_hbaa:
            import reports_hbaa
            report = reports_hbaa.get_report

        elif self.quest in q_2015_set:
            import reports_2015
            report = reports_2015.get_report
        else:
            report = None
             
        return report


    def get_all_active_obj(self, ):
        for qst_id in qsts.keys():
            if qst_id in active_qsts:
                yield Questionnaires(quest = qst_id)



    def process_virtuals(self, form, ans ):
        """Process 'vritual' questions - a pre interpret like thing  for auto filled questions"""
        response = { }

        ##TODO
        ###Only supported and in use for Hilton meetings Tele/Email/RFP but must 
        # be processes for all no hiltonm meetings for benchmarking.
        # if you add anouther sone split this into an engine/pimpl class
        # for each questionnaire type
        if self.etarget != EnquiryTarget.MEETINGS or self.etype == EnquiryType.SHORT_TELE: return response

        ##QH1
        klen = len('c_10_')
        c_10_rs = set([ k[klen:] for k in form.keys() if k[:klen] == 'c_10_' ])
        test_set = set(['3', '7'])
        relv_set = set(['1','2','3','4','6','7','8','9','A'])

        qh2_set = set(['M','N','T','P','R','E'])

        ##Don't update if c_10 not in the form. SO we only update when c_10 changes
        if c_10_rs:
            if len(relv_set & c_10_rs) < 4:
                response['r_H1'] = '4'
            elif test_set <= c_10_rs:
                response['r_H1'] = '1'
            elif test_set & c_10_rs:
                response['r_H1'] = '2'
            else:
                response['r_H1'] = '3'
      
        ##QH1
            qh2_sz = len(qh2_set & c_10_rs)
            if qh2_sz == 0:
                response['r_H2'] = '3'
            elif qh2_sz == 1:
                response['r_H2'] = '2'
            else:
                response['r_H2'] = '1'


        if 'r_37' in form.keys():
            r37 = form['r_37'].value

            if r37 == '3':
                response['r_H4'] = '5'
            else:
                r38 = form['r_38'].value
                import sys
                sys.stderr.write("R37 - r38 -> %s,%s\n"%(r37,r38))
                if r38 == '9':
                    response['r_H4'] = '4'
                elif r38 in ['7', '8']:
                    response['r_H4'] = '3'
                elif r38 in ['5', '6']:
                    response['r_H4'] = '2'
                elif r38 in ['1','2','3','4']:
                    response['r_H4'] = '1'
                else:
                    response['r_H4'] = 'X'

        if 'r_39' in form.keys() and (
            'r_H3' in ans.full_set.keys() or self.etype != EnquiryType.TELEPHONE 
           ) :
            if self.etype == EnquiryType.TELEPHONE:
                rh3 = ans.full_set['r_H3']
            else:
                rh3 = '1'

            r39 = form['r_39'].value
            if r39 =='3':
                response['r_H5'] = '0'
            elif r39 in ['1','2']:
                response['r_H5'] = rh3
            else:
                #Swap '1' / '2' over
                response['r_H5'] = chr(ord('0')+(1+ord(rh3))%2)

        if 'r_40' in form.keys() and 'r_42' in form.keys():
            r40 = form['r_40'].value
            r42 = form['r_42'].value
            if r40 =='1' and r42 =='1':
                response['r_H6'] = '1'
            elif r40 =='1' and r42 in ['2','0']:
                response['r_H6'] = '2'
            elif r40 in ['2','3'] and r42 == '1':
                response['r_H6'] = '2'
            else:
                response['r_H6'] = '0'

        return response


class ResultType(Questionnaires):
    """ Virtual questionnaires are also known as result types and 
    are used by the score reporting sub system.

    These one can be data entered or have the scorecard views, or even 
    looked at individually as a event - *But*  summary scores are created
    for these questionnaire_id not the real ones.

    This is a 'client' view rather than and admin view,and this 
    class takes a brand or group_obj which is used to determine
    which virtual questionnaires are 'visible'.
    """

    def __init__ (self, d, id=None, f= None , brand_id  = None, **kwargs):
        Questionnaires.__init__(self,quest = id, brand_id = brand_id, **kwargs)

        self.d = d
        if not self.d:
            self.d = db.connect()

        self.f = f
        if not f:
           self.f = self.d.cursor()

        self.id = self.quest
        self.description = self.user_desc
        self.brand_id = brand_id
        self.group_obj = kwargs.get('group_obj',None)

        if not self.group_obj and self.brand_id:
            import brand
            self.group_obj = brand.Brand(self.d,self.brand_id)

        self.questionnaire_id  = self.id


    def __repr__(self):
        return 'ResultType: id: %s   Description: "%s">' % (self.id, self.description)


    def get_all_objs(self, ):

        objs = []
        ##FIXME - look for Virtual Criteria type!.
        k = user_desc.keys()
        k.sort()
        for id in k:
            objs.append(ResultType(id))
        return objs



#--------------
    def get_all_ids(self, ):
        """ This reutrns the list of (virtual) questionnaire_ids available to 
        users who are associated with self.group_obj """


        def make_channel_set(qlist):
            """Turn quest id, in tuple of type, and target - for checking for elibilry for virtual questionnaires """
            q_channels = set()
            for q in qlist:
                try:
                    # We should really construct an object
                    base_channel = _qst_channel[q]
                except KeyError:pass #Ignore uncatergorised quests like compshop.
                else:
                    q_channels.add(base_channel)

            return q_channels

        #
        # We need to revisit this for CMBT-XXX Where we have a full tree structure.
        #
        # This is and override rule for OVERALL enquiries which requires only electronic
        # (of either sort) and telephone enquiries to show.
        #

        Etype_Rules_overrides = {
            EnquiryType.OVERALL :[ set([EnquiryType.TELEPHONE, EnquiryType. EMAIL ])  ,   set([EnquiryType.TELEPHONE, EnquiryType. RFP ])  ]

        }
        def get_q_rules(quest):
            """Get the list of sets of (type, target) tuples which must be made to one venue it the group 
            to satsify the rule. 
            """
            try:
                rules_base = iter(Etype_Rules_overrides[quest.etype])
            except KeyError:
                #Single rule, only allow if all members are used
                return [ make_channel_set(quest.members) ]
            else:
                ##Make a set of rules up form the base set.
                rules = []
                for rule in rules_base:
                    rules.append(set([
                        #Add the target type back in a turn into  a tuple
                        ( etype, quest.etarget,) for etype in rule 
                    ]))
                return rules


        #import sys
        import venue 
        v = venue.Venue(self.d,None)
        venues_list  = self.group_obj.get_all_venues()
        vlist = v.make_in(venues_list)
        if vlist:
            import model
            scores = model.Scores(self.d,None)
            #sys.stderr.write("vl-%s\n"%vlist) 
            year,month = scores.latest_period()
            self.f.execute("""select distinct quest from events
                                 where  status != 'D' and year = %%s and venue_id in ( %s )"""%vlist,(year,))

            def_quests =[ ]
            #Go through the results and find which virtual q's contain the returned ones.
            quests = [ row[0] for row in self.f.fetchall()]
            ##Walk Found questionnaire Id, and Built Type/Target pairs for them.
            quests = make_channel_set(quests)

            for q_id, members in virtual_members.items():
                if q_id not in currently_active_virtuals: continue
                #Apply the basic visibility rules..
                rt = Questionnaires(quest = q_id )
                if self.group_obj.allowed_target(rt.etarget ):
                    rules = get_q_rules(rt)
                    #One or more rules sould pass to allow q_id to show.
                    for rule in rules:
                        if rule <= quests and q_id not in def_quests:
                            def_quests.append(q_id)

            #sys.stderr.write("%s B%s - %s\n"%(year, self.brand_id, def_quests))
        else:
            #sys.stderr.write("Cannot determine brand - defaulting to all meeetings only\n")
            def_quests =  [ 83, 84, 85, 86, 87]

        # sort the questionnaires into seq order
        #Make tuple with sort order, and sort by it.
        qsts_found  = sorted( ( ( qsts[k][2], k)  for k in def_quests ) )
        return [ q[1] for q in qsts_found ]

    def dropdown(self, **kwargs):
        '''return dropdown selection, preselecting specified id'''

        preselect_id = kwargs.get('preselect_id', None)
        disabled = kwargs.get('disabled', '')
        select_arg = kwargs.get('select_arg', '')
        hide_ids = kwargs.get('hide_ids', [])
        dropdown_quests = kwargs.get('quests',None)
        name = kwargs.get('name','questionnaire_id')

        if dropdown_quests is None:
            dropdown_quests = self.get_all_ids()

        # sort the questionnaires into seq order
        qst_list  = sorted( (qsts[k][2], k) for k in dropdown_quests if k not in hide_ids)

        dropdown = [u'<select class="text-input" name="%(name)s" id="%(name)s" %(disabled)s %(select_arg)s>' % locals()]
        for qst in qst_list:
            seq, qst_id = qst
            if preselect_id == qst_id:
                selected = 'selected'
            else:
                selected = ''
                
            dropdown.append(u'<option value="%s" %s>%s' % (qst_id, selected, user_desc[qst_id]))
        dropdown.append(u'</select>')
        return ''.join(dropdown)


import db
class resulttype_control(object):
    @staticmethod
    def _factory(newid):
        if isinstance(newid,ResultType):
            return newid
        else:
            return ResultType(None, id = int(newid) )

    def __init__(self,form,name,default = ResultType(None)):
        self.name = name

        self.value = form.get_form_value(name,default=default,factory=resulttype_control._factory)
        self.text = str(self.value.questionnaire_id)

    def __unicode__(self,):
        return self.value.description or u""

    def get_controls(self,**kwargs):
        return self.value.dropdown(name= self.name,preselect_id=self.value.questionnaire_id,
                                   quests= virtual_qsts, **kwargs)


class resulttype_id_control(resulttype_control):
    def __init__(self,form,name,default = ResultType(None)):
        super(resulttype_id_control,self).__init__(form,name,default=default)
        self.obj = self.value
        self.value = self.obj.questionnaire_id

    def __unicode__(self,):
        return self.obj.description or u""

    def get_controls(self,**kwargs):
        return self.obj.dropdown(name= self.name,preselect_id=self.value,
                                   quests= virtual_qsts, **kwargs)
