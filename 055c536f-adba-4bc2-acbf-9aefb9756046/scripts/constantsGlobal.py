#------------------------------------------------------------
# Global Variables
#------------------------------------------------------------
ThreatMarker = ('Threat', '055c536f-adba-4bc2-acbf-9aefb9000001')
DamageMarker = ('Damage', '055c536f-adba-4bc2-acbf-9aefb9000002')
HealthMarker = ('Health', '055c536f-adba-4bc2-acbf-9aefb9000003')
AllPurposeMarker = ('All Purpose', '055c536f-adba-4bc2-acbf-9aefb9000004')
AccelerationMarker = ('Acceleration', '055c536f-adba-4bc2-acbf-9aefb9000005')
StunnedMarker = ('Stunned', '055c536f-adba-4bc2-acbf-9aefb9000006')
ConfusedMarker = ('Confused', '055c536f-adba-4bc2-acbf-9aefb9000007')
ToughMarker = ('Tough', '055c536f-adba-4bc2-acbf-9aefb9000008')


BoardWidth = 800
PlayerY = 120
VillainY = -235
DoneColour = '#D8D8D8' # Grey
WaitingColour = '#FACC2E' # Orange
ActiveColour = '#82FA58' # Green
EliminatedColour = '#FF0000' # Red
BlueColour = "#0059D6"
OrangeColour = "#D68F00"
GreenColour = "#046C06"
PurpleColour = "#3F00BD"
RedColour = "#B80404"
BlackColour = "#000000"
WhiteColour = "#FFFFFF"

showDebug   = False #Can be changed to turn on debug - we don't care about the value on game reconnect so it is safe to use a python global
Website     = "https://twistedsistem.wixsite.com/octgnmarvelchampions"
Github     = "https://github.com/Ouroboros009/OCTGN-Marvel-Champions/issues"

# Table Locations for Cards
tableLocations = {
    'hero': (0, 120),
    'heroPermanent': (120, 120),
    'villain': (0,-235),
    'mainScheme': (45.5, -235),
    'mainSchemeCentered': (-45.5, -235),
    'sideScheme': (80, -215),
    'attachment' : (-240, -235),
    'environment' : (-120, -235)
}

linkedCard = {
    '43021': ['43034', '43035', '43036', '43037']
}
markerSpecificList = ['44053', '44057']


# --------------------------------
# Universal Pre-Built Decks (Aspect Cards Only)
# --------------------------------

universal_prebuilt = {
    '01-Brutish Aggression':        '565634',
    '02-Graceful Aggression':       '87152',
    '03-Warrior\'s Aggression':     '198702',
    '04-X-Men Aggression':          '406565',
    '05-Reckless Aggression':       '87153',
    '06-Defiant Justice':           '87151',
    '07-Evasive Justice':           '87976',
    '08-Guardian Justice':          '198706',
    '09-SHIELD Justice':            '304322',
    '10-Web-Warrior Justice':       '406569',
    '11-Unyielding Protection':     '87124',
    '12-Debilitating Protection':   '87125',
    '13-Assembled Protection':      '480612',
    '14-Web-Warrior Protection':    '406575',
    '15-X-Men Protection':          '406579',
    '16-Courageous Leadership':     '87148',
    '17-Commanding Leadership':     '87130',
    '18-Guardian Leadership':       '198713',
    '19-Sacrificial Leadership':    '304324',
    '20-Champions Leadership':      '565652',
    '21-X-Men Leadership':          '565656'
}

# --------------------------------
# Pre-Built Decks
# --------------------------------

pre_built = {
    # Core Set Hero Out of Box Decks
    'spider_man': {
        '01058':1,
        '01059':1,
        '01060':2,
        '01061':2,
        '01062':2,
        '01063':2,
        '01064':2,
        '01065':2,
        '01083':1,
        '01084':1,
        '01085':1,
        '01086':1,
        '01087':1,
        '01088':1,
        '01089':1,
        '01090':1,
        '01091':1,
        '01092':1,
        '01093':1
    },

    'captain_marvel': {
        '01066':1,
        '01067':1,
        '01068':1,
        '01069':2,
        '01070':2,
        '01071':2,
        '01072':2,
        '01073':1,
        '01074':2,
        '01083':1,
        '01084':1,
        '01085':1,
        '01086':1,
        '01087':1,
        '01088':1,
        '01089':1,
        '01090':1,
        '01091':1,
        '01092':1,
        '01093':1
    },

    'she_hulk': {
        '01050':1,
        '01051':1,
        '01052':2,
        '01053':2,
        '01054':2,
        '01055':2,
        '01056':2,
        '01057':2,
        '01083':1,
        '01084':1,
        '01085':1,
        '01086':1,
        '01087':1,
        '01088':1,
        '01089':1,
        '01090':1,
        '01091':1,
        '01092':1,
        '01093':1
    },

    'iron_man': {
        '01050':1,
        '01051':1,
        '01052':2,
        '01053':2,
        '01054':2,
        '01055':2,
        '01056':2,
        '01057':2,
        '01083':1,
        '01084':1,
        '01085':1,
        '01086':1,
        '01087':1,
        '01088':1,
        '01089':1,
        '01090':1,
        '01091':1,
        '01092':1,
        '01093':1
    },

    'black_panther': {
        '01075':1,
        '01076':1,
        '01077':2,
        '01078':2,
        '01079':2,
        '01080':2,
        '01081':2,
        '01082':2,
        '01083':1,
        '01084':1,
        '01085':1,
        '01086':1,
        '01087':1,
        '01088':1,
        '01089':1,
        '01090':1,
        '01091':1,
        '01092':1,
        '01093':1
    },

    # Captain America Hero Pack
    'captain_america': {
        '01066':1,
        '01071':2,
        '01072':2,
        '01083':1,
        '01088':1,
        '01089':1,
        '01090':1,
        '03011':1,
        '03013':1,
        '03014':1,
        '03015':3,
        '03017':3,
        '03019':3,
        '03024':1,
        '03025':3
    },

    # Ms. Marvel Hero Pack
    'ms_marvel': {
        '01078':2,
        '01079':2,
        '01088':1,
        '01089':1,
        '01090':1,
        '01091':1,
        '05012':1,
        '05014':3,
        '05015':3,
        '05017':3,
        '05018':1,
        '05023':3,
        '05024':3
    },

    # Thor Hero Pack
    'thor': {
        '01052':2,
        '01055':2,
        '01088':1,
        '01089':1,
        '01090':1,
        '01091':1,
        '06011':1,
        '06012':1,
        '06014':3,
        '06015':3,
        '06017':1,
        '06018':3,
        '06019':1,
        '06020':1,
        '06021':3
    },

    # Black Widow Hero Pack
    'black_widow': {
        '01062':2,
        '01063':2,
        '01064':2,
        '01084':1,
        '01088':1,
        '01089':1,
        '01090':1,
        '08011':1,
        '08012':1,
        '08013':3,
        '08017':3,
        '08018':3,
        '08023':1,
        '08024':3
    },

    # Doctor Strange Hero Pack
    'doctor_strange': {
        '01079':2,
        '01080':2,
        '01088':1,
        '01089':1,
        '01090':1,
        '01091':1,
        '09012':1,
        '09013':1,
        '09014':1,
        '09015':3,
        '09016':3,
        '09019':1,
        '09020':3,
        '09021':3,
        '09026':1
    },

    # Hulk Hero Pack
    'hulk': {
        '01055':2,
        '01088':1,
        '01089':1,
        '01090':1,
        '01091':1,
        '01092':1,
        '10011':1,
        '10012':1,
        '10013':1,
        '10014':3,
        '10015':3,
        '10016':3,
        '10018':3,
        '10019':3
    },

    # The Rise of The Red Skull Campaign Expansion
    'hawkeye': {
        '01070':2,
        '01072':2,
        '01088':1,
        '01089':1,
        '01090':1,
        '04011':1,
        '04012':1,
        '04013':1,
        '04014':1,
        '04015':3,
        '04016':3,
        '04017':3,
        '04020':1,
        '03024':1,
        '04022':3
    },

    'spider_woman': {
        '01056':2,
        '01057':2,
        '01063':2,
        '01065':2,
        '01088':1,
        '01089':1,
        '01090':1,
        '04040':1,
        '04043':3,
        '04044':3,
        '04045':1,
        '04047':3,
        '04049':3
    },

    # Ant-man Hero Pack
    'ant': {
        "01086":2,
        "01088":1,
        "01089":1,
        "01090":1,
        "12011":1,
        "12012":1,
        "12013":1,
        "12014":1,
        "12015":3,
        "12016":3,
        "12017":3,
        "12018":3,
        "12020":1,
        "12024":3
    },

    # Wasp Hero Pack
    'wsp': {
        "01055":2,
        "01088":1,
        "01089":1,
        "01090":1,
        "08023":1,
        "13011":1,
        "13012":1,
        "13013":3,
        "13014":3,
        "13016":3,
        "13017":3,
        "13018":1,
        "13019":1,
        "13020":1,
        "13024":2
    },

    # Quicksilver Hero Pack
    'qsv': {
        "01081":2,
        "01088":1,
        "01089":1,
        "01090":1,
        "14012":3,
        "14013":1,
        "14014":3,
        "14015":3,
        "14017":3,
        "14018":1,
        "14022":3,
        "14023":3
    },

    # Scarlet Witch Hero Pack
    'scw': {
        "01088": 1,  # Energy
        "01089": 1,  # Genius
        "01090": 1,  # Strength
        "01062": 2,  # Power Of Justice
        "01065": 2,  # Heroic Intuition
        "14018": 1,  # Order and Chaos
        "15010": 1,  # Speed
        "15011": 1,  # Wiccan
        "15012": 3,  # Crisis Averted
        "15013": 3,  # Multitasking
        "15014": 3,  # Swift Retribution
        "15015": 3,  # Turn the Tide
        "15019": 3   # Spiritual Meditation
    },

    # Galaxy's Most Wanted Campaign Expansion
    'groot': {
        "01079": 2,  # The Power of Protection
        "01082": 2,  # Indomitable
        "01088": 1,  # Energy
        "01089": 1,  # Genius
        "01090": 1,  # Strength
        "09015": 3,  # Desperate Defense
        "16012": 1,  # Starhawk
        "16014": 3,  # Fighting Fit
        "16016": 3,  # Dauntless
        "16017": 3,  # Hard to Ignore
        "16019": 1,  # Rocket Raccoon
        "16020": 1,  # Flora and Fauna
        "16024": 3,  # Deft Focus
    },

    'rocket': {
        "01052": 2,  # Chase Them Down
        "01053": 2,  # Relentless Assault
        "01088": 1,  # Energy
        "01089": 1,  # Genius
        "01090": 1,  # Strength
        "13013": 3,  # Into the Fray
        "16020": 1,  # Flora and Fauna
        "16040": 1,  # Bug
        "16043": 3,  # Looking for Trouble
        "16045": 3,  # Follow Through
        "16046": 3,  # Hand Cannon
        "16047": 1,  # Groot
        "16052": 3,  # Booster Boots
    },

    # Star-Lord Hero Pack
    'stld': {
        "01069": 2,  # Get Ready
        "01072": 2,  # The Power of Leadership
        "17011": 1,  # Adam Warlock
        "17012": 1,  # Beta Ray Bill
        "17013": 1,  # Yondu
        "17014": 3,  # Air Supremacy
        "17015": 3,  # Blaze of Glory
        "17017": 3,  # Target Practice
        "17019": 3,  # Laser Blaster
        "17020": 1,  # Cosmo
        "17021": 1,  # C.I.T.T.
        "17022": 1,  # Knowhere
        "17023": 3  # Pulse Grenade
    },

    # Gamora Hero Pack
    'gam': {
        "01054": 2,  # Uppercut
        "01057": 2,  # Combat Training
        "01088": 1,  # Energy
        "01089": 1,  # Genius
        "01090": 1,  # Strength
        "18011": 1,  # Angela
        "18012": 3,  # Clobber
        "18013": 3,  # Plan of Attack
        "18015": 3,  # First Hit
        "18016": 3,  # Impede
        "18018": 1,  # Godslayer
        "18019": 1,  # Drax
        "18020": 3  # Hit and Run
    },

    # Drax Hero Pack
    'drax': {
        "19012": 1,    # Martyr
        "19013": 1,    # Moondragon
        "01077": 2,    # Contre-Attaque au Poing
        "19015": 3,    # Deflection
        "19016": 3,    # Hard Knocks
        "19017": 3,    # Leading Blow
        "19018": 3,    # Subdue
        "01082": 2,    # Inebranlable
        "19020": 1,    # Gamora
        "13034": 3,    # Remise en Forme
        "01088": 1,    # Energy
        "01089": 1,    # Genius
        "01090": 1    # Strength
    },

    # Venom Hero Pack
    'vnm': {
        "20011": 1,    # Jack Flag
        "20012": 3,    # Scare Tactic
        "20013": 3,    # Making an Entrance
        "01062": 2,    # Le Pouvoir de la Justice
        "20015": 3,    # Sonic Rifle
        "20016": 1,    # Star-Lord
        "01088": 1,    # Energy
        "01089": 1,    # Genius
        "01090": 1,    # Force
        "10032": 3,    # Ingeniosity
        "20021": 3,    # Side Holster
        "20022": 3    # Plasma Pistol
    },

    # Mad Titan's Shadow Campaign Expansion
    'spectrum': {
        '21011':1,
        '21012':1,
        '21013':1,
        '21014':1,
        '21015':3,
        '21016':3,
        '12016':3,
        '21018':3,
        '21019':1,
        '03024':1,
        '01091':1,
        '21022':3,
        '01088':1,
        '01089':1,
        '01090':1
    },

    'warlock': {
        '21041':1,
        '21042':1,
        '21043':1,
        '01054':1,
        '01057':1,
        '21046':1,
        '21047':1,
        '21048':1,
        '01060':1,
        '21050':1,
        '01065':1,
        '21052':1,
        '21053':1,
        '21054':1,
        '21055':1,
        '01071':1,
        '01074':1,
        '21058':1,
        '21059':1,
        '21060':1,
        '21061':1,
        '01077':1,
        '01081':1,
        '21064':1,
        '21065':1
    },

    # Nebula Hero Pack
    'nebu': {
        '22011':1,
        '22012':1,
        '22013':1,
        '22014':3,
        '22015':3,
        '21052':1,
        '01062':2,
        '22018':3,
        '01065':2,
        '17020':1,
        '17022':1,
        '22022':1,
        '01086':2,
        '01088':1,
        '01089':1,
        '01090':1
    },

    # War Machine Hero Pack
    'warm': {
        '23012':1,
        '23013':1,
        '03011':1,
        '04013':1,
        '23016':3,
        '23017':3,
        '23018':3,
        '23019':3,
        '01071':2,
        '21058':1,
        '01083':1,
        '08023':1,
        '23024':1,
        '01088':1,
        '01089':1,
        '01090':1
    },

    # Valkyrie Hero Pack
    'valk': {
        '25013':1,
        '25014':1,
        '18011':1,
        '06017':1,
        '01057':2,
        '25018':3,
        '25019':3,
        '25020':3,
        '01057':2,
        '01055':2,
        '25023':1,
        '25024':3,
        '01088':1,
        '01089':1,
        '01090':1
    },

    # Vision Hero Pack
    'vision': {
        '26013':1,
        '26014':1,
        '26015':1,
        '26016':3,
        '01082':2,
        '26018':3,
        '14015':3,
        '01078':2,
        '21064':1,
        '26022':1,
        '01091':1,
        '26024':3,
        '01088':1,
        '01089':1,
        '01090':1
    },

    # Sinister Motives Campaign Expansion
    'ghost_spider': {
        '27010':1,
        '27011':1,
        '27012':1,
        '15030':3,
        '27014':3,
        '27015':3,
        '27016':3,
        '27017':1,
        '27018':1,
        '27019':1,
        '01088':1,
        '01089':1,
        '01090':1,
        '27023':1,
        '27024':3
    },

    'spider_man_morales': {
        '27040':1,
        '27041':1,
        '27042':3,
        '27043':3,
        '27044':3,
        '01064':2,
        '27046':1,
        '27047':1,
        '27048':1,
        '27049':1,
        '27019':1,
        '01088':1,
        '01089':1,
        '01090':1,
        '27054':3,
        '27055':1
    },

    # Nova Hero Pack
    'nova': {
        '28010':1,
        '01052':2,
        '28012':3,
        '28013':3,
        '28014':3,
        '01055':2,
        '28016':3,
        '28017':3,
        '28018':1,
        '28019':3,
        '28020':1
    },

    # Ironheart Hero Pack
    'ironheart': {
        '29014':1,
        '29015':1,
        '29016':1,
        '29017':3,
        '29018':3,
        '05032':3,
        '29020':3,
        '01072':2,
        '27046':1,
        '29023':1,
        '29024':1,
        '29025':1,
        '01092':1,
        '29027':3
    },

    # Spider-Ham Hero Pack
    'spiderham': {
        '30012':1,
        '30013':1,
        '30014':3,
        '01061':2,
        '20013':3,
        '22015':3,
        '03032':3,
        '30019':3,
        '30020':1,
        '30021':1,
        '12024':3,
        '27023':1
    },

    # SP//dr Hero Pack
    'spdr': {
        '31014':1,
        '31015':1,
        '31016':3,
        '31017':3,
        '05017':3,
        '31019':3,
        '31020':3,
        '31021':1,
        '31022':1,
        '31023':3,
        '31024':3
    },

    # Mutant Genesis Campaign Expansion
    'colossus': {
        '32011':1,
        '32012':1,
        '32013':3,
        '32014':3,
        '32015':3,
        '32016':3,
        '32017':3,
        '32018':2,
        '32019':1,
        '32020':1,
        '32021':1,
        '32022':1,
        '32023':1,
        '32024':1
    },

    'shadowcat': {
        '32041':1,
        '32042':1,
        '32043':3,
        '32044':3,
        '32045':3,
        '32046':3,
        '32047':2,
        '32048':1,
        '32049':1,
        '32021':1,
        '32051':3,
        '32022':1,
        '32023':1,
        '32024':1
    },

    # Cyclops Hero Pack
    'cyclops': {
        '33011':1,
        '33012':1,
        '33013':1,
        '33014':1,
        '33015':3,
        '33016':3,
        '33017':3,
        '33018':2,
        '33019':1,
        '33020':1,
        '33021':1,
        '33022':3,
        '33023':1,
        '32022':1,
        '32023':1,
        '32024':1
    },

    # Phoenix Hero Pack
    'phoenix': {
        '34014':1,
        '34015':1,
        '34016':3,
        '34017':3,
        '34018':3,
        '34019':3,
        '34020':2,
        '34021':1,
        '34022':1,
        '33023':1,
        '34024':3,
        '32022':1,
        '32023':1,
        '32024':1
    },

    # Wolverine Hero Pack
    'wolverine': {
        '35013':1,
        '35014':1,
        '35015':3,
        '35016':3,
        '35017':3,
        '35018':3,
        '35019':3,
        '32047':2,
        '32048':1,
        '35022':1,
        '35023':1,
        '32022':1,
        '32023':1,
        '32024':1
    },

    # Storm Hero Pack
    'storm': {
        '36014':1,
        '36015':1,
        '36016':1,
        '36017':1,
        '36018':3,
        '36019':3,
        '36020':3,
        '33018':2,
        '36022':1,
        '32020':1,
        '33020':1,
        '32049':1,
        '36026':3,
        '32022':1,
        '32023':1,
        '32024':1
    },

    # Gambit Hero Pack
    'gambit': {
        '37011':1,
        '37012':1,
        '37013':3,
        '37014':3,
        '37015':3,
        '34020':2,
        '32019':1,
        '32049':1,
        '37019':1,
        '37020':3,
        '37021':3,
        '32022':1,
        '32023':1,
        '32024':1
    },

    # Rogue Hero Pack
    'rogue': {
        '38010':1,
        '38011':1,
        '38012':1,
        '38013':3,
        '38014':3,
        '38015':3,
        '38016':3,
        '32018':2,
        '38018':1,
        '38019':3,
        '37019':1,
        '32022':1,
        '32023':1,
        '32024':1
    },

    # Next Encounter Campaign Expansion
    'cable': {
        '40014':1,
        '40015':1,
        '40016':1,
        '40017':3,
        '40018':1,
        '40019':1,
        '40020':1,
        '40021':1,
        '40022':3,
        '40023':1,
        '40024':1,
        '40025':1,
        '40026':1,
        '40027':1,
        '40028':3,
        '40029':1,
        '40030':3
    },

    'domino': {
        '40050':1,
        '40051':1,
        '40052':3,
        '40053':3,
        '40054':1,
        '40055':3,
        '40056':1,
        '40057':1,
        '40058':1,
        '40059':1,
        '40060':3,
        '32022':1,
        '32023':1,
        '32024':1,
        '40064':3
    },

    'psylocke': {
        '41012':1,
        '41013':1,
        '41014':3,
        '41015':3,
        '41016':1,
        '41017':3,
        '41018':1,
        '41019':3,
        '41020':1,
        '40028':3,
        '41022':1,
        '41023':1,
        '41024':3
    },

    'angel': {
        '42011':1,
        '42012':1,
        '42013':1,
        '42014':3,
        '42015':3,
        '42016':3,
        '42017':1,
        '42018':1,
        '42019':3,
        '42020':1,
        '41020':1,
        '42022':3,
        '42023':3
    },

    'x23': {
        '43013':1,
        '43014':1,
        '43015':1,
        '43016':3,
        '43017':3,
        '43018':1,
        '43019':3,
        '43020':3,
        '43021':1,
        '32022':1,
        '32023':1,
        '32024':1,
        '41022':1,
        '41023':1,
        '36026':3
    },

    'deadpool': {
        '44013':1,
        '44014':1,
        '44015':1,
        '44016':1,
        '44017':3,
        '44018':1,
        '44019':1,
        '44020':1,
        '44021':3,
        '44022':1,
        '44023':1,
        '44024':1,
        '44025':1,
        '44026':1,
        '44027':1,
        '44028':1,
        '44029':3,
        '44030':1,
        '40026':1
    },

    'bishop': {
        '45011':1,
        '45012':1,
        '45013':3,
        '45014':3,
        '45015':1,
        '45016':3,
        '45017':3,
        '45018':3,
        '45019':2,
        '45020':1,
        '45021':1,
        '32022':1,
        '32023':1,
        '32024':1
    },

    'magik': {
        '45041':1,
        '45042':1,
        '45043':3,
        '45044':3,
        '45045':3,
        '45046':3,
        '45047':2,
        '45048':1,
        '45049':1,
        '45050':1,
        '45051':3,
        '45052':3
    },

    'iceman': {
        '46012':1,
        '46013':1,
        '46014':3,
        '46015':3,
        '46016':3,
        '46017':3,
        '46018':1,
        '46019':1,
        '46020':1,
        '46021':3,
        '46022':3,
        '46023':2
    }
}