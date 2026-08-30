import clr
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer

#------------------------------------------------------------
# 'Load Hero' event
#------------------------------------------------------------

# Fanmade heroes only exist on mc4db, so the fanmade flow only accepts deck
# URLs from that site - a marvelcdb URL cannot know these heroes. The local
# hosts are accepted too: they are the mc4db development instance, used to
# test API changes before they are deployed.
# Origine : Merlin - fanmade deck loading rework (2026).
FANMADE_DECK_HOSTS = ["mc4db.merlindumesnil.net", "localhost", "127.0.0.1"]

def loadFanmadeHero(group, x = 0, y = 0):
    mute()
    loadHero(group, x, y, True, 0, "fm_hero_setup")

def loadHero(group, x = 0, y = 0, askMethod = True, choice = 0, setupType = "hero_setup"):
    mute()
    if not deckNotLoaded(group, checkGroup = [c for c in me.Deck if not isEncounter([c])]):
        msg = """Cannot generate a deck: You already have cards loaded.\n
Reset the game in order to generate a new deck."""
        askChoice(msg, [], [], ["Close"])
        return

    if setupType == "fm_hero_setup":
        fanmade = True
        cardSelected = dialogBox_Setup(me.piles["Setup"], setupType, None, "Select your Hero", "Select your Hero :", min = 1, max = 1, isFanmade = fanmade)
        if cardSelected is None: return
        heroSet = cardSelected[0].Owner
        heroName = cardSelected[0].Name
        me.setGlobalVariable("heroPlayed", heroSet)
    else:
        fanmade = False
    update()

    # Choose where to take other aspect cards from
    if askMethod:
        if fanmade:
            choice = askChoice("Select source for other aspect cards:", ["A downloaded deck (.o8d file)", "A marvelcdb deck (URL)", "A Universal Pre-Built deck"])
            if choice != 0:
                choice = choice + 1
        else:
            choice = askChoice("Select source for other aspect cards:", ["An out of the box deck", "A downloaded deck (.o8d file)", "A marvelcdb deck (URL)", "A Universal Pre-Built deck"])

    if choice == 0: return

    if choice == 1:
        cardSelected = dialogBox_Setup(me.piles["Setup"], setupType, None, "Select your Hero", "Select your Hero :", min = 1, max = 1, isFanmade = fanmade)
        if cardSelected is None: return
        heroSet = cardSelected[0].Owner
        heroName = cardSelected[0].Name
        me.setGlobalVariable("heroPlayed", heroSet)
        aspectCardsList = createCards(me.Deck, pre_built[heroSet].keys(), pre_built[heroSet])
        deleteCards(me.piles["Setup"])

    if choice == 2:
        filename = openFileDlg('', '', 'o8d Files|*.o8d')
        if filename == "":
            whisper("No file chosen. Script will end here. Try to Load your hero again.")
            return

        aspectCardsList = o8dLoad(filename, fanmade)
        if not fanmade:
            cardSelected = me.piles["Setup"].top()
            heroSet = cardSelected.Owner
            heroName = cardSelected.Name
            me.setGlobalVariable("heroPlayed", heroSet)
        deleteCards(me.piles["Setup"])

    if choice == 3:
        url = askString("Please enter the URL of the deck you wish to load.", "")
        if url == None: return
        # Fanmade flow: only an mc4db address is valid (see FANMADE_DECK_HOSTS).
        # Origine : Merlin - fanmade deck loading rework (2026).
        if fanmade and not any(host in url for host in FANMADE_DECK_HOSTS):
            whisper("Error: Fanmade decks can only be loaded from {}.".format(FANMADE_DECK_HOSTS[0]))
            return
        if not "view/" in url:
            whisper("Error: Invalid URL.")
            return

        # The fanmade flow passes the hero picked in the selection dialog so
        # the API load can refuse a deck built for another hero - without it
        # the mix would load silently.
        # Origine : Merlin - trust-the-API deck loading rework (2026).
        if fanmade:
            aspectCardsList = RemoteCallBlocker.createAPICards(url, False, heroSet)
        else:
            aspectCardsList = RemoteCallBlocker.createAPICards(url, False)
        # Abort cleanly when the online load failed or was refused - the code
        # below would crash iterating None.
        # Origine : Merlin - trust-the-API deck loading rework (2026).
        if aspectCardsList is None:
            deleteCards(me.piles["Setup"])
            return
        if not fanmade:
            cardSelected = me.piles["Setup"].top()
            heroSet = cardSelected.Owner
            heroName = cardSelected.Name
            me.setGlobalVariable("heroPlayed", heroSet)
        deleteCards(me.piles["Setup"])

    if choice == 4:
        if not fanmade:
            cardSelected = dialogBox_Setup(me.piles["Setup"], setupType, None, "Select your Hero", "Select your Hero :", min = 1, max = 1, isFanmade = fanmade)
            if cardSelected is None: return
            heroSet = cardSelected[0].Owner
            heroName = cardSelected[0].Name
            me.setGlobalVariable("heroPlayed", heroSet)
        universal_prebuilt_List = sorted(universal_prebuilt.keys())
        prebuilt_Choice = askChoice("What Universal Pre-Built deck do you want to load?", universal_prebuilt_List)
        aspectCardsList = RemoteCallBlocker.createAPICards("https://marvelcdb.com/deck/view/{}".format(universal_prebuilt[universal_prebuilt_List[prebuilt_Choice-1]]), True)
        # Abort cleanly when the online load failed - the code below would
        # crash iterating None.
        # Origine : Merlin - trust-the-API deck loading rework (2026).
        if aspectCardsList is None:
            deleteCards(me.piles["Setup"])
            return

    # Set all player variables
    pList = list(JavaScriptSerializer().DeserializeObject(getGlobalVariable("playerList")))
    pList.append(me._id)
    setGlobalVariable("playerList", str(pList))
    heroesPlayed = list(JavaScriptSerializer().DeserializeObject(getGlobalVariable("heroesPlayed")))
    heroesPlayed.append(heroSet)
    setGlobalVariable("heroesPlayed", str(heroesPlayed))

    # Load hero cards
    # URL loading (choice 3): the online deck already provided the identity
    # and the signature cards (see createAPICards), so re-creating the whole
    # set here would duplicate them - and would also undo any signature card
    # the deck legitimately replaced (e.g. an ally swapped for a team-up
    # card, a deck option marvelcdb-style slots can express). Only the set
    # cards that declare an out-of-deck location (DefaultSetupPile:
    # obligations, extra hero forms like Ironheart's) are still created,
    # since no deck can ever carry those. Every other source keeps the full
    # set creation: out-of-the-box and o8d decks do not bring the extra
    # cards, and Universal Pre-Built decks bring no hero cards at all.
    # Origine : Merlin - trust-the-API deck loading rework (2026).
    if choice == 3:
        heroCards = createCardsFromSet(me.Deck, heroSet, heroName, False, setupPileOnly = True)
    else:
        heroCards = createCardsFromSet(me.Deck, heroSet, heroName, False)
    nemesisCards = createCardsFromSet(me.Nemesis, heroSet + "_nemesis", heroName + "'s Nemesis", False)

    # Change Owner for all cards
    changeOwner(heroCards, heroSet)
    changeOwner(aspectCardsList, heroSet)
    if nemesisCards is not None:
        changeOwner(nemesisCards, heroSet)

    # Check for linked cards  
    for c in me.piles["Deck"]:
        if c.CardNumber in linkedCard.keys():
            for lnkC in linkedCard[c.CardNumber]:
                cardModel = queryCard({"CardNumber":lnkC}, True)
                if len(cardModel) == 0:
                    notify("Card not found in octgn database. Code from marvelcdb url : {}.".format(cardid))
                    continue 
                cards = me.piles["Removed"].create(cardModel[0], 1)            

    heroSetup()
    checkSetup()

def heroSetup(group=table, x = 0, y = 0):

    id = myID() # This ensures we have a unique ID based on our position in the setup order
    heroCount = countHeros(me)
    heroPlayed = me.getGlobalVariable("heroPlayed")

    # Find any Permanent cards
    #permanents = filter(lambda card: "Permanent" in card.Keywords or "Permanent." in card.Text, me.deck)

    # Move Hero to the table
    newHero = False
    hero = filter(lambda card: card.Type == "hero", me.Deck)
    if hero:
        heroCount += 1
        newHero = True
        heroCard = hero[0]
        heroCard.moveToTable(playerX(id),tableLocations['hero'][1])
        heroCard.alternate = 'b'
        me.counters['Max HP'].value = num(heroCard.HP)
        me.counters['Default Card Draw'].value = num(heroCard.HandSize)
        notify("{} places his Hero on the table".format(me))

    if newHero:
        shuffle(me.deck)

        #------------------------------------------------------------
        # Specific Hero setup
        #------------------------------------------------------------

        # Spectrum
        if heroPlayed == 'spectrum':
            for c in filter(lambda card: card.Type == "upgrade", me.Deck):
                if c.CardNumber == "21002" or c.CardNumber == "21003" or c.CardNumber == "21004":
                    c.moveTo(me.piles['Special'])
            showGroup(me.piles['Special'], False)
            me.piles['Special'].visibility = "all"

        # Valkyrie
        if heroPlayed == 'valk':
            for c in filter(lambda card: card.CardNumber == "25002", me.Deck):
                c.moveTo(me.piles['Special'])
            showGroup(me.piles['Special'], False)
            me.piles['Special'].visibility = "all"

        # Ironheart
        if heroPlayed == 'ironheart':
            showGroup(me.piles['Special'], False)
            me.piles['Special'].visibility = "all"

        # SP//dr
        if heroPlayed == 'spdr':
            for c in me.piles['Special']:
                c.moveToTable(playerX(id)+70,tableLocations['hero'][1])

        # Rogue
        if heroPlayed == 'rogue':
            for c in filter(lambda card: card.CardNumber == "38002", me.Deck):
                c.moveTo(me.piles['Special'])
            showGroup(me.piles['Special'], False)
            me.piles['Special'].visibility = "all"

        # Psylocke
        if heroPlayed == 'psylocke':
            i = 1
            for c in filter(lambda card: card.CardNumber == "41002a", me.Special):
                c.moveToTable(playerX(id)+(70*i),tableLocations['hero'][1])
                i += 1

        #------------------------------------------------------------
        # Specific Fanmade Hero setup
        #------------------------------------------------------------

        # Luke Cage (by Rainy)
        if heroPlayed == 'luke_cage_by_rainy':
            for c in filter(lambda card: card.CardNumber == "203601b", table):
                tough(c)

        #------------------------------------------------------------
        # moveToTable Hero setup cards
        #------------------------------------------------------------
        shift = 0
        for c in me.Deck:
            if lookForSetup(c):
                c.moveToTable(playerX(id)+70+shift,tableLocations['hero'][1])
                shift += 70

        #------------------------------------------------------------
        # Cards that declare their own setup location in the set xml
        #------------------------------------------------------------
        # Some cards must be put into play at setup even though their own text
        # holds no "Setup" keyword, because the instruction sits on the identity
        # instead: Jessica Jones' alter-ego reads "Setup: Put the Alias
        # Investigations support into play", while the support itself only reads
        # "Permanent.". lookForSetup() scans the deck and can never match those,
        # which is why every such hero used to need its own hard-coded block,
        # with the card number written in the engine.
        # Letting the card state its own intent - same spirit as the existing
        # DefaultSetupPile / DefaultDiscardPile properties - means a new pack
        # ships with its set.xml alone, without patching the engine.
        # The seven per-hero blocks that used to do this by card number
        # (Wolverine, Vision, Shadowcat, Phoenix, X-23, Wonder Man, Nick Fury)
        # were removed and their cards now carry the property in their
        # set.xml, so every hero goes through this single loop (convergence
        # requested by the maintainer in the PR #21 review). A card must never
        # be covered by both a hard-coded block and the property, or it would
        # be put into play twice.
        # DefaultSetupMarkers places the markers such a card starts with:
        # Jean Grey reads "Setup: Put your Phoenix Force upgrade into play
        # [...] Place 4 power counters on it.". The marker type follows the
        # card's DefaultMarkerType when it declares one, like addMarker()
        # does, and falls back on the all-purpose marker - exactly what the
        # old Phoenix block placed.
        # The shift is shared with the "Setup" loop above so the cards line up
        # next to the hero instead of stacking on each other.
        # Origine : Merlin - generic replacement for the per-hero permanent
        # setup blocks, introduced with the Jessica Jones pack; the seven
        # existing blocks converted at the maintainer's request (2026).
        for c in me.Deck:
            if c.hasProperty("DefaultSetupLocation") and c.properties["DefaultSetupLocation"].strip().lower() == "table":
                c.moveToTable(playerX(id)+70+shift,tableLocations['hero'][1])
                shift += 70
                if c.hasProperty("DefaultSetupMarkers") and c.properties["DefaultSetupMarkers"].strip() != "":
                    if c.hasProperty("DefaultMarkerType") and c.DefaultMarkerType not in ["", "Any"]:
                        markerKey = globals()[c.DefaultMarkerType + "Marker"]
                    else:
                        markerKey = AllPurposeMarker
                    c.markers[markerKey] = num(c.properties["DefaultSetupMarkers"])
                notify("{} puts {} into play (setup).".format(me, c))
        # "Starting." cards go to the player's hand
        #------------------------------------------------------------
        # Done here, during hero setup, so the cards are already in hand when
        # startGame() runs: it draws maxHandSize(p) - countHandSize(p), so the
        # player ends up at their normal hand size, holding these cards.
        # Origine : Merlin - keyword introduced with Fear No Evil.
        for c in me.Deck:
            if lookForStarting(c):
                c.moveTo(me.hand)
                notify("{} adds {} to their starting hand (Starting.)".format(me, c))
        # A few heroes start with a side deck of their own: Doctor Strange's
        # Invocation, Storm's Weather, Iceman's Frostbite, Hercules' Labor and
        # Gift decks, Daredevil's SENSE deck. All of them now load through the
        # HeroSideDeck property on the identity card - the per-hero blocks
        # that used to sit above are gone, so a hero must never both carry
        # the property and keep a block, or its deck is loaded twice.
        # Value is a comma separated list of set Owners, each optionally
        # followed by ":<pile>" when it must not land in the Special pile,
        # and by ":hidden" when the pile's cards must stay secret: Hercules
        # needs both, his Labor and Gift decks are face-down draw decks
        # ("reveal the top card" / "put the top card into play"), where a
        # SENSE deck is played from the top, so its cards must be readable.
        # Without the flag the pile is opened to everyone, as before.
        # WARNING: keep this property ALONE. Declaring HeroSideDeckShuffle and
        # HeroSideDeckVisibility beside it, carried by no card, reproducibly
        # broke the card database: the game threw "object reference not set"
        # on any group iteration, so loadHero() died on an empty me.Deck
        # before any setup ran. Removing them fixed it, twice. The mechanism
        # is not understood - DefaultSetupPile has the same shape and is fine.
        # The ":hidden" flag lives inside the same value for that reason.
        # Origine : Merlin - generic replacement for the per-hero side deck
        # blocks, introduced with Daredevil's SENSE deck (Fear No Evil);
        # the five original blocks migrated at the maintainer's request
        # (follow-up to the HeroSideDeck PR).
        if hero and heroCard.hasProperty("HeroSideDeck"):
            for entry in heroCard.properties["HeroSideDeck"].split(","):
                entry = entry.strip()
                if not entry:
                    continue
                parts = [p.strip() for p in entry.split(":")]
                deckOwner = parts[0]
                if len(parts) > 1 and parts[1]:
                    pileName = parts[1]
                else:
                    pileName = "Special"
                hidden = len(parts) > 2 and parts[2].lower() == "hidden"
                deckName = deckOwner.replace("_", " ").title()
                createCardsFromSet(me.piles[pileName], deckOwner, deckName, False)
                showGroup(me.piles[pileName], True)
                if hidden:
                    me.piles[pileName].visibility = "none"
                else:
                    me.piles[pileName].visibility = "all"

def countHeros(p):
    heros = 0
    for card in table:
        if card.controller == p and (card.Type == "hero" or card.Type == "alter_ego"):
            heros += 1
    return heros

#------------------------------------------------------------
# 'Load Hero' specific functions
#------------------------------------------------------------
def o8dLoadAsDict(o8d):
    """
    Load an .o8d file and build a global dict where keys are sections. It will then look like:
    {
        section_id_1: {
            "section": the section name,
            "shared": boolean True/False,
            "cards": {
                "card_id": qty,
                "card_id": qty,
            }
        },
        section_id_2: {
            "section": the section name,
            "shared": boolean True/False,
            "cards": {
                "card_id": qty,
            }
        },
        ...
    }
    where section_id is the concatenation of section name and value of shared (as we can have section
    with same names in both shared and not shared piles)
    """
    with open(o8d, "rt") as f:
        lines = f.readlines()

    full_dict = {}
    current_section = ""
    for line in lines:
        if line.strip().startswith("<section"):
            name_matches = re.search('name="([a-zA-Z_]+)"', line, re.IGNORECASE)
            shared_matches = re.search('shared="([a-zA-Z]+)"', line, re.IGNORECASE)
            shared = False
            if shared_matches:
                shared = shared_matches.group(1) == "True"
            if name_matches:
                section = name_matches.group(1)
                section_id = section + "_" + str(shared)
                full_dict[section_id] = {"section": section, "shared": shared, "cards": {}}
                current_section = section_id
        if line.strip().startswith("<card"):
            matches = re.search('<card qty="(\d+)" id="([a-zA-Z0-9-]+)"', line, re.IGNORECASE)
            if matches:
                if matches.group(1) is not None and matches.group(2) is not None:
                    qty = int(matches.group(1))
                    card_id = matches.group(2)
                    full_dict[current_section]["cards"][card_id] = qty
    return full_dict

def o8dLoad(o8d, fanmade = False):
    """
    Load a local .o8d file
    Decks downloaded from marvelcdb have only one section named "Cards" with shared="False", so we can directly grab cards from this section
    """
    full_dict = o8dLoadAsDict(o8d)

    all_cards = []

    isAspectCard = False
    for card_id, qty in full_dict["Cards_False"]["cards"].items():
        cards = me.Deck.create(card_id, qty)
        if qty == 1:
            if cards is None:
                notify("{} card(s) not found in octgn database. Code from marvelcdb o8d : {}.".format(qty, card_id))
                continue            
            if cards.Type == 'hero':
                if not fanmade:
                    setupCardModel = queryCard({"Type":"hero_setup", "Owner":cards.Owner}, True)
                    setupCard = me.Setup.create(setupCardModel[0], 1)
            isAspectCard = cards.Owner == ""
            if isAspectCard:
                all_cards.append(cards)
            else:
                cards.delete()
        else:
            if len(cards) == 0:
                notify("{} card(s) not found in octgn database. Code from marvelcdb o8d : {}.".format(qty, card_id))
                continue   
            if cards[0].Type == 'hero':
                if not fanmade:
                    setupCardModel = queryCard({"Type":"hero_setup", "Owner":cards[0].Owner}, True)
                    setupCard = me.Setup.create(setupCardModel[0], 1)
            isAspectCard = cards[0].Owner == ""
            if isAspectCard:
                all_cards.extend(cards)
            else:
                [c.delete() for c in cards]
    return all_cards

def changeOwner(cards, hero_id):
    """
    Change Owner property of a given list of cards if Owner is unknown (or aspect card).
    """
    for card in cards:
        if card.Owner is None or card.Owner in ["", "basic", "justice", "leadership", "protection", "aggression"]:
            card.Owner = hero_id

class RemoteCallBlocker:
    """Methods in this class cannot be remote called because calling them requires using the '.' character, which isn't allowed in remote calls."""
    @staticmethod
    def createAPICards(url, aspectOnly = False, expectedHero = None):
        """
        Create the deck by loading cards from a marvelcdb-compatible URL
        (marvelcdb.com or mc4db).
        aspectOnly: keep only the aspect/basic cards from the slots. Used by
        the Universal Pre-Built decks, which are built on some hero whose
        signature cards must not leak into the player's deck.
        expectedHero: when given, refuse a deck whose hero is not this one
        (fanmade flow: the player picked a hero in the dialog, the pasted
        URL must match it).
        Origine : Merlin - trust-the-API deck loading rework (2026): the
        parameter 'fanmade' was renamed 'aspectOnly' to say what it does,
        and the hero cards from the slots are no longer deleted and
        re-created from the set (see loadHero, choice 3).
        """
        notify("Looking {} for deck.".format(url))
        all_cards = []

        protocol = url.split("://")[0]
        if "marvelcdb.com/" in str(url):
            webadress = "marvelcdb.com"
        else:
            webadress = url.split("://")[1].split("/")[0]

        deckid = url.split("view/")[1].split("/")[0]
        if "decklist/" in str(url):
            data, code = webRead("{}://{}/api/public/decklist/{}".format(protocol, webadress, deckid))
        elif "deck/" in str(url):
            data, code = webRead("{}://{}/api/public/deck/{}".format(protocol, webadress, deckid))
        if code != 200:
            whisper("Error retrieving online deck data, please try again.")
            return
        try:
            apiData = JavaScriptSerializer().DeserializeObject(data)
            deckname = apiData["hero_name"]
            deck = apiData["slots"]
            hero_id = apiData["hero_code"]
            # mc4db adds an out-of-format field 'sideSlots' carrying the
            # player-built side deck; marvelcdb has no such field. A missing
            # or unreadable field means no side deck - never an error.
            # Origine : Merlin - mc4db side deck loading (2026).
            try:
                sideDeck = apiData["sideSlots"]
            except:
                sideDeck = None
            if not aspectOnly:
                # The identity card is not part of the slots, so it is created
                # here from hero_code - directly in the player's deck, where it
                # used to be re-created from the set: the set creation is now
                # limited to the out-of-deck cards (see loadHero, choice 3).
                # Origine : Merlin - trust-the-API deck loading rework (2026).
                heroModels = queryCard({"Type":"hero", "CardNumber":hero_id}, True)
                if len(heroModels) == 0:
                    whisper("Hero not found in octgn database. Code from marvelcdb url : {}.".format(hero_id))
                    return
                heroCard = me.Deck.create(heroModels[0], 1)
                if expectedHero is not None and heroCard.Owner != expectedHero:
                    whisper("The deck at this URL is for {}, not for the hero you selected. Load aborted.".format(deckname))
                    heroCard.delete()
                    return
                setupCardModel = queryCard({"Type":"hero_setup", "Owner":heroCard.Owner}, True)
                if len(setupCardModel) == 0:
                    setupCardModel = queryCard({"Type":"fm_hero_setup", "Owner":heroCard.Owner}, True)
                setupCard = me.Setup.create(setupCardModel[0], 1)
            chars_to_remove = ['[',']']
            rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
            for id in deck:
                line = re.sub(rx,'',str(id))
                line = line.split(',')
                cardid = line[0]
                qty = int(line[1].strip())
                cardModel = queryCard({"CardNumber":cardid}, True)
                if len(cardModel) == 0:
                    notify("Card not found in octgn database. Code from marvelcdb url : {}.".format(cardid))
                    continue 
                cards = me.Deck.create(cardModel[0], qty)
                # Hero-owned cards from the slots used to be deleted here and
                # re-created from the set. They are now kept as the online
                # deck states them, so a deck that replaces a signature card
                # (e.g. an ally swapped for a team-up card) loads as built.
                # Only the Universal Pre-Built path still strips them
                # (aspectOnly), see the docstring.
                # Origine : Merlin - trust-the-API deck loading rework (2026).
                if qty == 1:
                    isAspectCard = cards.Owner == ""
                    if isAspectCard or not aspectOnly:
                        all_cards.append(cards)
                    else:
                        cards.delete()
                else:
                    isAspectCard = cards[0].Owner == ""
                    if isAspectCard or not aspectOnly:
                        all_cards.extend(cards)
                    else:
                        [c.delete() for c in cards]
            # Side deck (mc4db only, see above): the cards go to the player's
            # 'Side Deck' pile, added to definition.xml with this feature.
            # They join all_cards so changeOwner() marks them like the rest of
            # the deck. Not applicable to Universal Pre-Built decks.
            # Origine : Merlin - mc4db side deck loading (2026).
            if sideDeck is not None and not aspectOnly:
                for id in sideDeck:
                    line = re.sub(rx,'',str(id))
                    line = line.split(',')
                    cardid = line[0]
                    qty = int(line[1].strip())
                    cardModel = queryCard({"CardNumber":cardid}, True)
                    if len(cardModel) == 0:
                        notify("Card not found in octgn database. Code from mc4db side deck : {}.".format(cardid))
                        continue
                    cards = me.piles["Side Deck"].create(cardModel[0], qty)
                    if qty == 1:
                        all_cards.append(cards)
                    else:
                        all_cards.extend(cards)
            return all_cards
        except ValueError:
            whisper("Error retrieving online deck data, please try again. If you are trying to load a non published deck make sure you have edited your account to select 'Share Your Decks'")