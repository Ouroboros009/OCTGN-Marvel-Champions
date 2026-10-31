import re
import clr
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer

showDebug = False #Can be changed to turn on debug - we don't care about the value on game reconnect so it is safe to use a python global

def debug(str):
    if showDebug:
        whisper(str)

def toggleDebug(group, x=0, y=0):
    global showDebug
    showDebug = not showDebug
    if showDebug:
        notify("{} turns on debug".format(me))
    else:
        notify("{} turns off debug".format(me))

#Return the default x coordinate of the players hero
def playerX(player):
    pLeft = ((BoardWidth * -1) / 2) + ((BoardWidth/len(getPlayers())) * player)
    pRight = ((BoardWidth * -1) / 2) + ((BoardWidth/len(getPlayers())) * (player + 1))
    pWidth = pLeft - pRight
    pCenter = pLeft - (pWidth / 2)
    return (pCenter - 35)

#Return the default x coordinate of the villain
def villainX(villainCount, villain):
    pLeft = ((BoardWidth * -1) / 2) + ((BoardWidth/villainCount) * villain)
    pRight = ((BoardWidth * -1) / 2) + ((BoardWidth/villainCount) * (villain + 1))
    pWidth = pLeft - pRight
    pCenter = pLeft - (pWidth / 2)
    return (pCenter - 35)


#------------------------------------------------------------
# Card Type Checks
#------------------------------------------------------------

def isScheme(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != 'main_scheme' and c.Type != 'side_scheme' and c.Type != 'player_side_scheme':
            return False
    return True

def isMainScheme(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != 'main_scheme':
            return False
    return True

def isSideScheme(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != 'side_scheme':
            return False
    return True

def isPlayerScheme(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != 'player_side_scheme':
            return False
    return True

def isHero(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != 'hero' and c.Type != 'alter_ego':
            return False
    return True

def isPlayerCard(card):
    return card.owner in getPlayers()

def isVillain(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != 'villain' and c.Type != 'leader':
            return False
    return True

def isAttackable(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != 'villain' and c.Type != 'leader' and c.Type != 'hero' and c.Type != 'minion' and c.Type != 'ally' and c.Type != 'alter_ego':
            return False
    return True

def exhaustable(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != "hero" and c.Type != "alter_ego" and c.Type != "ally" and c.Type != "minion"  and c.Type != "upgrade" and c.Type != "support":
            return False
    return True

def isEncounter(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != "minion" and c.Type != "attachment" and c.Type != "treachery" and c.Type != "environment" and c.Type != "side_scheme" and c.Type != "obligation":
            return False
    return True

def isPermanent(card):
    return re.search('.*Permanent.*', card.properties["Text"])

def hasVictory(card):
    return re.search('.*Victory \d+.*', card.properties["Text"], re.IGNORECASE)

def hasDefaultDiscardPile(card):
    return card.hasProperty("DefaultDiscardPile")


#------------------------------------------------------------
# Shared Piles
#------------------------------------------------------------

def mainSchemeDeck():
    return shared.piles['Scheme']

def villainDeck():
    return shared.piles['Villain']

def encounterDeck():
    return shared.piles['Encounter']

def encounterDiscardDeck():
    return shared.piles['Encounter Discard']

def encounterAndDiscardDeck():
    deck = list(shared.piles['Encounter'])
    deck.extend(shared.piles['Encounter Discard'])
    return deck

def sideDeck():
    return shared.piles['Side']

def sideDeckDiscard():
    return shared.piles['Side Discard']

def specialDeck():
    return shared.piles['Special']

def specialDeckDiscard():
    return shared.piles['Special Discard']

def removedFromGameDeck():
    return shared.piles['Removed']

def campaignDeck():
    return shared.piles['Campaign']

def victoryDisplay():
    return shared.piles['Victory']

def setupPile():
    return shared.piles['Setup']

def tempPile(isShared = True):
    if isShared:
        return shared.piles['Temporary']
    else:
        return me.piles['Temporary']

#------------------------------------------------------------
# Global variable manipulations function
#------------------------------------------------------------

def getLock():
    lock = getGlobalVariable("lock")
    if lock == str(me._id):
        return True

    if len(lock) > 0: #Someone else has the lock
        return False

    setGlobalVariable("lock", str(me._id))
    if len(getPlayers()) > 1:
        update()
    return getGlobalVariable("lock") == str(me._id)

def clearLock():
    lock = getGlobalVariable("lock")
    if lock == str(me._id):
        setGlobalVariable("lock", "")
        update()
        return True
    debug("{} id {} failed to clear lock id {}".format(me, me._id, lock))
    return False

#Store this player's starting position (players ID for this game)
#The first player is 0, the second 1 ....
#These routines set global variables so should be called within getLock() and clearLock()
#After a reset, the game count will be updated by the first player to setup again which invalidates all current IDs
def myID():
    if me.getGlobalVariable("game") == getGlobalVariable("game") and len(me.getGlobalVariable("playerID")) > 0:
        return playerID(me) # We already have a valid ID for this game

    g = getGlobalVariable("playersSetup")
    if len(g) == 0:
        id = 0
    else:
        id = num(g)
    me.setGlobalVariable("playerID", str(id))
    game = getGlobalVariable("game")
    me.setGlobalVariable("game", game)
    setGlobalVariable("playersSetup", str(id+1))
    update()
    debug("Player {} sits in position {} for game {}".format(me, id, game))
    return id

def playerID(p):
    return num(p.getGlobalVariable("playerID"))

#Returns player object based on the customer playerIDs givine from the myID() function default returns player 0
def getPlayerByID(id):
    for p in players:
        if num(p.getGlobalVariable("playerID")) == num(id):
            return p
        elif num(id) >= len(getPlayers()) and num(p.getGlobalVariable("playerID")) == 0:
            return p

def deckLocked():
    return me.getGlobalVariable("deckLocked") == "1"

def lockDeck():
    me.setGlobalVariable("deckLocked", "1")

def unlockDeck():
    me.setGlobalVariable("deckLocked", "0")

def deckNotLoaded(group, x = 0, y = 0, checkGroup = me.Deck):
    if len(checkGroup) > 0:
        return False
    return True

def setFirstPlayer(group = table, x = 0, y = 0):
    """
    Sets firstPlayer variable as a string to look into playerList to know which player is the first player.
    """
    mute()

    playerList = list(JavaScriptSerializer().DeserializeObject(getGlobalVariable("playerList")))
    currentFirstPlayer = num(getGlobalVariable("firstPlayer"))
    # Check if first player is set (should be called only when game start) else change the first player
    if turnNumber() == 0:
        newFirstPlayer = 0
    # Give first player to the next one in order of deck loading at the start of the game.
    elif (currentFirstPlayer + 1) >= len(getPlayers()):
        newFirstPlayer = 0
    else:
        newFirstPlayer = currentFirstPlayer + 1
    setGlobalVariable("firstPlayer", str(newFirstPlayer))

    # If first player token doesn't exist then create a new one.
    firstPlayerToken = [card for card in table if card.Type == 'first_player']
    if len(firstPlayerToken) == 0:
        firstPlayerToken = [table.create("65377f60-0de4-4196-a49e-96a550b4df81", 0, 0, 1, True)]
    firstPlHero = list(JavaScriptSerializer().DeserializeObject(getGlobalVariable("heroesPlayed")))[newFirstPlayer]
    firstPlHeroCard = [c for c in table if (c.Type == 'hero' or c.Type == 'alter_ego') and c.Owner == firstPlHero]
    update()
    firstPlayerToken[0].controller = me
    firstPlayerToken[0].moveToTable(firstPlHeroCard[0].position[0], firstPlHeroCard[0].position[1]-40)
    firstPlayerToken[0].sendToBack()

def getFirstPlayerPosition(group = table, x = 0, y = 0):
    """
    Gets firstPlayer position.
    """
    mute()
    
    firstPlayer = int(JavaScriptSerializer().DeserializeObject(getGlobalVariable("firstPlayer")))
    firstPlHero = list(JavaScriptSerializer().DeserializeObject(getGlobalVariable("heroesPlayed")))[firstPlayer]
    firstPlHeroCard = [c for c in table if (c.Type == 'hero' or c.Type == 'alter_ego') and c.Owner == firstPlHero]
    update()
    return firstPlHeroCard[0].position[0], firstPlHeroCard[0].position[1]

def setActiveVillain(card, x = 0, y = 0):
    if isVillain([card]):
        vCards = filter(lambda card: card.Type == "villain", table)
        for c in vCards:
            c.highlight = None
        card.highlight = ActiveColour

def getActiveVillain(group = table, x = 0, y = 0):
    vCards = filter(lambda card: card.Type == "villain" or card.Type == "leader", table)
    for c in vCards:
        if str(c.highlight).upper() == ActiveColour:
            return c


#------------------------------------------------------------
# Functions triggered by Events
#------------------------------------------------------------

#Triggered event OnTableLoad
# args: no args are passed with this event call
def initializeGame():
    """
    Happens when the table first loads, and never again.
    """
    mute()
    if table.isTwoSided():
        warning("This game is designed to be played on a single-sided table.\n\nPlease start a new game and make sure the option 'Two Side Table' is disabled.")
    showWelcomeScreen()
    update()

#Triggered event OnLoadDeck
def deckLoaded(args):
    whisper("The plugin has implemented a custom loading deck mechanic, so the default loading deck process has been disabled")

#Triggered event OnPlayerGlobalVariableChanged
#We use this to manage turn and phase management by tracking changes to the player "done" variable
def globalChanged(args):
    debug("globalChanged(Variable {}, from {}, to {})".format(args.name, args.oldValue, args.value))
    # if args.name == "playerList":
        # notify("Player List : {}".format(args.value))
    # if args.name == "heroesPlayed":
        # notify("Heroes List : {}".format(args.value))
    # if args.name == "firstPlayer":
        # notify("First player : {}".format(args.value))

def markersUpdate(args):
    mute()
    # if args.marker == "Damage" and args.card.Type == "villain":
        # shared.counters["HP"].value = shared.counters["HP"].value - (args.card.markers[DamageMarker] - args.value)
    # elif args.marker == "Damage" and (args.card.Type == "hero" or args.card.Type == "alter_ego"):
        # args.card.owner.counters["HP"].value = args.card.owner.counters["HP"].value - (args.card.markers[DamageMarker] - args.value)

def setCounter(group = None, x = 0, y = 0):
    """
    Set one of your own counters from a menu, by typing its new value.
    The +/- buttons of the counter row can stop responding, on any counter:
    the OCTGN client lays the hand area 200 px over that row
    (PlayerControl.xaml, Margin="0,-200,0,0") and CardScroller grabs every
    click inside the bounding box of its content, so the lower half of the
    row - the "-" buttons - gets swallowed. A menu entry does not go through
    those buttons. Counters are listed from me.counters in definition order,
    so a counter added later shows up by itself; only your own. askInteger
    only accepts positive numbers, which suits every counter of this game.
    Origine : Merlin - taille de main temporaire (2026).
    """
    mute()
    counters = sorted(me.counters.values(), key=lambda c: c._id)
    if not counters:
        return
    choice = askChoice("Which counter do you want to set?",
                       ["{} ({})".format(c.name, c.value) for c in counters])
    if not choice:
        return
    counter = counters[choice - 1]
    value = askInteger("New value for {}:".format(counter.name), counter.value)
    if value is None:
        return
    counter.value = value

#Triggered even OnCardDoubleClicked
def defaultCardAction(args):
    mute()
    if args.card.group == table:
        # Double-click on ANY special token resets it to its base face (value
        # 0, or every box off) - one single rule across the whole family, per
        # Merlin. Stepping the value stays on the Up/Down arrows. Mouse
        # buttons themselves cannot be rebound in OCTGN - left is select/drag,
        # right opens the context menu - so double-click is the only pointer
        # gesture available.
        # Origine : Merlin - jetons de stat (2026), etendu aux jetons speciaux.
        # Le test passe par isSpecialToken et n'enumere PAS les types ici :
        # la famille etait ecrite en clair a quatre endroits, et l'ajout des
        # jetons de ressource en a oublie trois - dont ce double-clic.
        if isSpecialToken([args.card]):
            resetSpecialToken(args.card)
            return
        if not args.card.isFaceUp or isScheme([args.card]):
             remoteCall(args.card.controller, "revealHide", args.card)
        else:
            if args.card.Type == "villain" or args.card.Type == "leader" or lookForVillainous(args.card):
                villainBoost(args.card)
            elif args.card.Owner == "infinity_gauntlet":
                infinityGauntletBoost(args.card)
            elif exhaustable([args.card]):
                readyExhaust(args.card)

#Triggered event OnOverRideTurnPassed
def overrideTurnPass(args):
    whisper("Plugin has built a custom turn and phase mechanic so the default turn process has been disabled")
    return

#Triggered event OnPhasePassed
def phasePassed(args):
    debug("phasePassed triggered")
    mute()
    thisPhase = currentPhase()
    newPhase = thisPhase[1]

    if newPhase == 1:
        setGlobalVariable("phase", "Hero Phase")
    elif newPhase == 2:
        setGlobalVariable("phase", "Villain Phase")

#Triggered event OnTurnPassed
def turnPassed(args):
    debug("turnPassed triggered")
    setPhase(1)

#Triggered event OnScriptedCardsMoved and OnCardsMoved
def moveCards(args):
    mute()
    magneticGrid(args)
    autoCharges(args)
    magikDeck(args)

def magneticGrid(args):
    for card in args.cards:
        if card.controller == me:
            x, y = card.position
            cardIndex = card.index
            if isinstance(args.toGroups[0], Table) and (x % 10 <> 0 or y % 10 <> 0):
                x = round(x / 10) * 10
                y = round(y / 10) * 10 
                card.moveToTable(x, y)
                card.index = cardIndex

#------------------------------------------------------------
# Game Flow functions
#------------------------------------------------------------

def dialogBox_Setup(group, type, nameList, title, text, min = 1, max = 1, isFanmade = False):
    cw_Side = getGlobalVariable("CW_Side")

    if not isFanmade:
		orderChoice = askChoice("Choose sorting order :", ["Release order", "Alphabetical"]) 
    else:
		orderChoice = 2
    
    if nameList == None:
        setup_cards = queryCard({"Type":type}, True)
    elif type == None:
        setup_cards = queryCard({"Name":nameList}, True)
    else:
        setup_cards = queryCard({"Type":type, "Name":nameList}, True)
    for i in setup_cards:
        group.create(i, 1)
    update()

    for c in group:
        if cw_Side <> "" and c.hasProperty("CW_Side"):
            if c.CW_Side <> cw_Side:
                c.delete()

    if orderChoice == 2:
        cardsList = sorted(group, key=lambda c: c.Name)
        dlg = cardDlg(cardsList)
    else:
        dlg = cardDlg(group)
    dlg.title = title
    dlg.text = text
    dlg.min = min
    dlg.max = max
    cardsSelected = dlg.show()
    deleteCards(group)
    if cardsSelected is None:
        return
    else:
        return cardsSelected

def checkSetup(group = None, x = 0, y = 0):
    g = getGlobalVariable("playersSetup")
    v = getGlobalVariable("villainSetup")
    if num(g) == len(getPlayers()) and len(v) > 0:
        startGame()

def startGame(group = None, x = 0, y = 0):
    setFirstPlayer()
    for p in getPlayers():
        p_hand_size = countHandSize(p.piles['Hand'])
        remoteCall(p, "shuffle", [p.piles['Deck']])
        remoteCall(p, "drawMany", [p.piles['Deck'], maxHandSize(p) - p_hand_size, True])
        remoteCall(p, "addObligationsToEncounter", [p.piles["Nemesis"]])
        checkPoolcards(p.piles['Deck'])
    update()
    advanceGame()

def addObligationsToEncounter(group = me.piles["Nemesis"]):
    vName = getGlobalVariable("villainSetup")
    update()
    if vName == 'The Wrecking Crew' or vName == 'Kang': return
    playerOblCard = filter(lambda card: card.Type == 'obligation', group)
    for c in playerOblCard:
        c.moveTo(encounterDeck())
    shuffle(encounterDeck())

def checkPoolcards(group = me.piles["Deck"]):
    for c in group:
        if c.Faction == 'pool' and len(shared.piles["Dreadpool"]) == 0:
            createCardsFromSet(shared.piles["Dreadpool"], "dreadpool", "Dreadpool", True)
            for c in shared.piles["Dreadpool"]:
                if c.CardNumber == '44037':
                    c.moveTo(encounterDeck())   
    shuffle(encounterDeck())

def advanceGame(group = None, x = 0, y = 0):
    # Check if we should pass the turn or just change the phase
    debug("advanceGame triggered")
    if turnNumber() == 0:
        firstPlinList = num(getGlobalVariable("firstPlayer"))
        firstPl = num(list(JavaScriptSerializer().DeserializeObject(getGlobalVariable("playerList")))[firstPlinList])
        Player(firstPl).setActive()
    elif currentPhase()[1] == 1:
        doEndHeroPhase()
        remoteCall(getActivePlayer(), "setPhase", [2]) #Must be triggered by active player
    elif currentPhase()[1] == 2:
        setFirstPlayer()
        setGlobalVariable("phase", "Hero Phase")
        firstPlinList = num(getGlobalVariable("firstPlayer"))
        firstPl = num(list(JavaScriptSerializer().DeserializeObject(getGlobalVariable("playerList")))[firstPlinList])
        remoteCall(getActivePlayer(), "nextTurn", [Player(firstPl), True]) #Must be triggered by active player to add +1 to turn counter
        notify("Next Player is {}".format(Player(firstPl)))
        update()
        shared.counters['Round'].value += 1
        saveTable(getGlobalVariable("phase"))

    update()

def doEndHeroPhase():
    mute()
    debug("doEndHeroPhase()")

    #------------------------------------------------------------
    # Each player now refills their own hand on their own client (refillHand),
    # instead of this loop reading every player's counters from the client
    # that advanced the phase, and showing everybody's discard dialog there.
    # OCTGN counters are per-client copies synced with a delay: read by its
    # owner, a counter is always up to date; reset by its owner (Temporary
    # Hand Size), it never races with the owner's own clicks.
    # Origine : Merlin - taille de main temporaire (2026).
    #------------------------------------------------------------
    for p in players:
        remoteCall(p, "clearTargets", [])
        remoteCall(p, "readyAll", [])
        remoteCall(p, "refillHand", [])

def refillHand():
    """
    End of the player phase, run by each player on their own client: draw up to
    the hand size, then spend the one-shot Temporary Hand Size bonus.
    No discard-down step: in Marvel Champions the hand size is only a draw
    target, a hand may stay above it (unlike Arkham Horror LCG). The former
    doEndHeroPhase loop offered to discard the excess; that prompt is gone.
    Origine : Merlin - taille de main temporaire (2026).
    """
    mute()
    handSize = countHandSize(me.piles['Hand'])
    maxSize = maxHandSize(me)
    if maxSize > handSize:
        drawMany(me.piles['Deck'], maxSize - handSize, True)

    # The temporary bonus only lasts until this refill.
    temporary = me.counters["Temporary Hand Size"].value
    if temporary != 0:
        notify("{}'s temporary hand size ({}{}) is spent and reset to 0.".format(me, "+" if temporary > 0 else "", temporary))
        me.counters["Temporary Hand Size"].value = 0

def passSharedControl(group, x=0, y=0):
    notify(me.name + " takes control of targeted cards")
    mute()
    #Take control of each not player card on table
    for card in table:
        if card.targetedBy == me:
            card.controller = me

def readyAll(group = table, x = 0, y = 0):
    mute()
    for c in table:
        if c.controller == me and c.orientation != Rot0 and isEncounter([c]) != True and c.Type != "encounter" and c.Type != "villain" and c.Type != "main_scheme" and c.Type != "player_side_scheme":
            c.orientation = Rot0
    notify("{} readies all their cards.".format(me))

def getPosition(card,x=0,y=0):
    t = getPlayers()
    notify("This cards position is {}".format(card.position))

def createCardsFromSet(group, owner, name, isShared = True, setupPileOnly = False):
    cardsFromSet = queryCard({"Owner":owner}, True)
    gameDifficulty = int(getGlobalVariable("difficulty"))
    all_cards = []
    pile = group.name
    if len(cardsFromSet) == 0:
        notifyBar("#FF0000", "No Cards found in xml files for {} set.".format(owner))
        notify("No Cards found in xml files for {} set.".format(owner))
        return
    for g in cardsFromSet:
        tempPile(isShared).create(g, 1)
    for c in tempPile(isShared):
        # pile Definition
        if c.hasProperty("DefaultSetupPile"):
            pile = c.properties["DefaultSetupPile"]
        else:
            pile = group.name

        # standard/expert Definition
        if c.hasProperty("Standard") and gameDifficulty == 0:
            standard = c.properties["Standard"].strip().lower() == "true"
        else:
            standard = True
        if c.hasProperty("Expert") and gameDifficulty == 1:
            expert = c.properties["Expert"].strip().lower() == "true"
        else:
            expert = True

        # quantity Definition
        if c.hasProperty("Quantity"):
            quantity = int(c.properties["Quantity"])
        else:
            quantity = 1

        # setupPileOnly: only create the cards that declare an out-of-deck
        # location (DefaultSetupPile) - obligations, extra hero forms like
        # Ironheart's or SP//dr's. Used by the online deck loading, where the
        # deck cards themselves now come from the marvelcdb/mc4db API and the
        # set must NOT re-create them (it would duplicate the deck, and undo
        # any signature card the deck legitimately replaced).
        # Origine : Merlin - trust-the-API deck loading rework (2026).
        if setupPileOnly and not c.hasProperty("DefaultSetupPile"):
            continue

        # Create set cards
        if c.Type[-5:] != "setup" and standard and expert:
            if isShared:
                shared.piles[pile].collapsed = False
                cards = shared.piles[pile].create(c.model, quantity)
            else:
                me.piles[pile].collapsed = False
                cards = me.piles[pile].create(c.model, quantity)
            if quantity == 1:
                all_cards.append(cards)
            else:
                all_cards.extend(cards)
    update()
    deleteCards(tempPile(isShared))
    notify("Cards from {} set added to {} deck.".format(name, pile))

    return all_cards

def createCards(group, list, dict):
    all_cards = []
    for i in list:
        cardModel = queryCard({"CardNumber":i}, True)
        cards = group.create(cardModel[0], dict[i])
        if dict[i] == 1:
            all_cards.append(cards)
        else:
            all_cards.extend(cards)
    return all_cards

def deleteCards(group):
    mute()
    for card in group:
        card.delete()

def changeForm(card, x = 0, y = 0):
    mute()
    if len(card.alternates) > 2:
        curAlt = card.alternate
        altNames = []
        for alt in card.alternates:
            card.alternate = alt
            altName = card.name
            notify("{}".format(altName))
            altNames.append(altName)
        card.alternate = curAlt
        altChoice = askChoice("Which form would you like to change into: ", altNames)
        if altChoice == 0: return
        elif altChoice != 0:
            card.alternate = card.alternates[altChoice-1]
    elif "b" in card.alternates:
        if card.alternate == "":
            card.alternate = "b"
        else:
            card.alternate = ""

    if card.Type == "hero" or card.Type == "alter_ego":
        me.setGlobalVariable("cardForm", card.Type)
        me.counters["Default Card Draw"].value = num(card.HandSize)
    else:
        lookForToughness(card)

def specific_hero_flip(card, x = 0, y = 0):
    mute()
    if card.Owner == 'warm':
        if card.Type == "hero":
            card.markers[AllPurposeMarker] = 5
            notify("{} adds 5 Marker on {}.".format(me, card))
        if card.Type == "alter_ego":
            card.markers[AllPurposeMarker] = 0
            notify("{} removes all Marker from {}.".format(me, card))
    if card.Owner == 'vision':
        upgradeCard = filter(lambda c: c.CardNumber == "26002a", table)
        if card.Type == "alter_ego" and len(upgradeCard) != 0:
            me.counters["Default Card Draw"].value += 1
    if card.Owner == 'spdr':
        heroCard = filter(lambda c: c.CardNumber == "31001a", table)
        supportCard = filter(lambda c: c.CardNumber == "31001b", table)
        alteregoCard = filter(lambda c: c.CardNumber == "31002a", table)
        upgradeCard = filter(lambda c: c.CardNumber == "31002b", table)
        if card.CardNumber == "31001a":
            heroCard[0].alternate = "b"
            upgradeCard[0].alternate = ""
            switchCards(heroCard[0], upgradeCard[0], h = 1, t = 1, s = 1, c = 1, a = 1)
            me.setGlobalVariable("cardForm", "alter_ego")
            me.counters["Default Card Draw"].value = num(upgradeCard[0].HandSize)
        elif card.CardNumber == "31001b":
            supportCard[0].alternate = ""
            alteregoCard[0].alternate = "b"
            switchCards(alteregoCard[0], supportCard[0], h = 1, t = 1, s = 1, c = 1, a = 1)
            me.setGlobalVariable("cardForm", "hero")
            me.counters["Default Card Draw"].value = num(supportCard[0].HandSize)
        elif card.CardNumber == "31002a":
            alteregoCard[0].alternate = "b"
            supportCard[0].alternate = ""
            switchCards(alteregoCard[0], supportCard[0], h = 1, t = 1, s = 1, c = 1, a = 1)
            me.setGlobalVariable("cardForm", "hero")
            me.counters["Default Card Draw"].value = num(supportCard[0].HandSize)
        elif card.CardNumber == "31002b":
            upgradeCard[0].alternate = ""
            heroCard[0].alternate = "b"
            switchCards(heroCard[0], upgradeCard[0], h = 1, t = 1, s = 1, c = 1, a = 1)
            me.setGlobalVariable("cardForm", "alter_ego")
            me.counters["Default Card Draw"].value = num(upgradeCard[0].HandSize)
    if card.Owner == 'magik':
        if card.Type == "hero":
            me.Deck.top().isFaceUp = True
        if card.Type == "alter_ego":
            me.Deck.top().isFaceUp = False


def villainBoost(card, x=0, y=0, who=me):
    mute()

    vName = getGlobalVariable("villainSetup")
    if card == table and vName != 'The Wrecking Crew':
        vCard = filter(lambda card: card.Type == "villain", table)
        card = vCard[0]
    elif card == table:
        vCard = filter(lambda card: getActiveVillain(), table)
        card = vCard[0]
    cardX = card.position[0] + 20
    cardY = card.position[1] + 20

    if card.controller != me:
        remoteCall(card.controller, "villainBoost", [card, x, y, me])
        return

    if vName != 'The Wrecking Crew':
        boostList = encounterDeck().top()
        boostList.moveToTable(cardX,cardY,True)
        boostList.controller = who
        if len(encounterDeck()) == 0:
            notifyBar("#FF0000", "Encounter pile is empty.")
            shuffleDiscardIntoDeck(encounterDiscardDeck())
    else:
        setActiveVillain(card, x, y)
        encCards = filter(lambda card: card.Owner == getActiveVillain().Owner, encounterDeck())
        boostList = encCards[0]
        boostList.moveToTable(cardX,cardY,True)
        boostList.controller = who
        newEncCards = filter(lambda card: card.Owner == getActiveVillain().Owner, encounterDeck())
        disEncCards = filter(lambda card: card.Owner == getActiveVillain().Owner, encounterDiscardDeck())
        if len(newEncCards) == 0:
            notifyBar("#FF0000", "{} encounter pile is empty.".format(getActiveVillain()))
            for c in disEncCards:
                c.moveTo(encounterDeck())
            shuffle(encounterDeck())

def infinityGauntletBoost(card, x=0, y=0, who=me):
    mute()

    cardX = card.position[0] + 20
    cardY = card.position[1] + 20

    if card.controller != me:
        remoteCall(card.controller, "infinityGauntletBoost", [card, x, y, me])
        return

    boostList = specialDeck().top()
    boostList.moveToTable(cardX,cardY,True)
    boostList.controller = who
    boostList.isFaceUp = True
    if len(specialDeck()) == 0:
        notifyBar("#FF0000", "Special pile is empty.")
        shuffleDiscardIntoDeck(specialDeckDiscard())

def addDamage(card, x = 0, y = 0):
    mute()
    card.markers[DamageMarker] += 1
    notify("{} adds 1 Damage on {}.".format(me, card))

def addAnyMarker(card, x = 0, y = 0, qty = 1):
    mute()
    card.controller = me
    marker, quantity = askMarker()
    if quantity == 0: return
    card.markers[marker] += quantity

def addMarker(card, x = 0, y = 0, qty = 1):
    mute()
    # Up arrow doubles as "+1" on a value token (stat, clock): same gesture
    # players already use for hit points. Checklist tokens are inert here -
    # their boxes toggle from the menu, and a marker dropped on them would
    # read as a second confusing value.
    # Origine : Merlin - jetons de stat (2026), etendu aux jetons speciaux.
    if card.Type in valueTokenMax:
        modifyStatToken(card, qty)
        return
    if card.Type == 'checklist_token':
        return
    card.controller = me
    if card.hasProperty("DefaultMarkerType"):
        if card.DefaultMarkerType == "Any":
            marker, quantity = askMarker()
            if quantity == 0: return
            card.markers[marker] += quantity
        else:
            markerName = card.DefaultMarkerType + "Marker"
            markerKey = globals()[markerName]
            card.markers[markerKey] += qty
            notify("{} adds {} {} on {}.".format(me, qty, card.DefaultMarkerType, card))
    elif isScheme([card]):
        card.markers[ThreatMarker] += qty
        notify("{} adds {} Threat on {}.".format(me, qty, card))
    elif card.Type in ["hero", "alter_ego", "villain", "leader"]:
        card.markers[HealthMarker] += qty
        notify("{} adds {} Hit Point on {}.".format(me, qty, card))
    elif isAttackable([card]):
        card.markers[DamageMarker] += qty
        notify("{} adds {} Damage on {}.".format(me, qty, card))
    else:
        card.markers[AllPurposeMarker] += qty
        notify("{} adds {} Marker on {}.".format(me, qty, card))

def removeMarker(card, x = 0, y = 0, qty = 1):
    mute()
    # Down arrow doubles as "-1" on a value token; inert on a checklist.
    # Origine : Merlin - jetons de stat (2026), etendu aux jetons speciaux.
    if card.Type in valueTokenMax:
        modifyStatToken(card, -qty)
        return
    if card.Type == 'checklist_token':
        return
    card.controller = me
    if card.hasProperty("DefaultMarkerType"):
        if card.DefaultMarkerType == "Any":
            marker, quantity = askMarker()
            if quantity == 0: return
            card.markers[marker] -= quantity
        else:
            markerName = card.DefaultMarkerType + "Marker"
            markerKey = globals()[markerName]
            card.markers[markerKey] -= qty
            notify("{} removes {} {} on {}.".format(me, qty, card.DefaultMarkerType, card))
    elif isScheme([card]):
        card.markers[ThreatMarker] -= qty
        notify("{} removes {} Threat on {}.".format(me, qty, card))
    elif card.Type in ["hero", "alter_ego", "villain", "leader"]:
        card.markers[HealthMarker] -= qty
        notify("{} removes {} Hit Point on {}.".format(me, qty, card))
    elif isAttackable([card]):
        card.markers[DamageMarker] -= qty
        notify("{} removes {} Damage on {}.".format(me, qty, card))
    else:
        card.markers[AllPurposeMarker] -= qty
        notify("{} removes {} Marker on {}.".format(me, qty, card))

def clearMarker(card, x = 0, y = 0):
    mute()
    card.controller = me
    if isScheme([card]):
        card.markers[ThreatMarker] = 0
        notify("{} removes all Threat on {}.".format(me, card))
    elif card.Type in ["hero", "alter_ego", "villain"]:
        card.markers[HealthMarker] = 0
        notify("{} removes all Hit Point on {}.".format(me, card))
    elif isAttackable([card]):
        card.markers[DamageMarker] = 0
        notify("{} removes all Damage on {}.".format(me, card))
    else:
        card.markers[AllPurposeMarker] = 0
        notify("{} removes all Markers on {}.".format(me, card))

def add3Marker(card, x = 0, y = 0, qty = 3):
    mute()
    if isScheme([card]):
        card.markers[ThreatMarker] += qty
        notify("{} adds 3 Threats on {}.".format(me, card))
    elif card.Type in ["hero", "alter_ego", "villain"]:
        card.markers[HealthMarker] += qty
        notify("{} adds 3 Hit Points on {}.".format(me, card))
    elif isAttackable([card]):
        card.markers[DamageMarker] += qty
        notify("{} adds 3 Damages on {}.".format(me, card))
    else:
        card.markers[AllPurposeMarker] += qty
        notify("{} adds 3 Markers on {}.".format(me, card))

def removeDamage(card, x = 0, y = 0):
    mute()
    card.markers[DamageMarker] -= 1
    notify("{} removes 1 Damage from {}.".format(me, card))

def clearDamage(card, x = 0, y = 0):
    mute()
    card.markers[DamageMarker] = 0
    notify("{} removes all Damage from {}.".format(me, card))

def addThreat(card, x = 0, y = 0):
    mute()
    card.markers[ThreatMarker] += 1
    notify("{} adds 1 Threat on {}.".format(me, card))

def removeThreat(card, x = 0, y = 0):
    mute()
    card.markers[ThreatMarker] -= 1
    notify("{} removes 1 Threat from {}.".format(me, card))

def clearThreat(card, x = 0, y = 0):
    mute()
    card.markers[ThreatMarker] = 0
    notify("{} removes all Threat from {}.".format(me, card))

def addAcceleration(card, x = 0, y = 0):
    mute()
    card.markers[AccelerationMarker] += 1
    notify("{} adds 1 Acceleration on {}.".format(me, card))

def removeAcceleration(card, x = 0, y = 0):
    mute()
    card.markers[AccelerationMarker] -= 1
    notify("{} removes 1 Acceleration from {}.".format(me, card))

def clearAcceleration(card, x = 0, y = 0):
    mute()
    card.markers[AccelerationMarker] = 0
    notify("{} removes all Acceleration from {}.".format(me, card))

# Free-standing stat tokens (THW/ATK/DEF/REC), one card each in the hidden
# "Stat Tokens" set. The displayed value (0-9) IS the card alternate - base
# face is 0, alternates "b".."j" are 1..9 - so the state needs no marker, no
# extra card property, and survives save/load with the card itself. Same
# pattern as the villain stage b-sides already used across the engine.
# Origine : Merlin - suivi visuel des stats modifiees en partie (2026),
# principe repris du mod Tainted Grail (jetons a valeur par alternates).
statTokenIds = {
    "THW": "7babd7f2-dcfd-4037-aef2-7fa08d2af7dd",
    "ATK": "3dc2a6bd-a2be-41c1-902c-34affe007df6",
    "DEF": "e854c4e1-fd4f-42ce-966e-4325fa85abf7",
    "REC": "9e461229-09ce-45ac-8e14-76f08e77b47a",
}

# Two more free-standing token families, same alternate-as-state pattern:
# - clock_token: a 0-6 action clock. The alternate IS the value ("1".."6").
# - checklist_token: independent boxes. The alternate is the sorted digits
#   of the lit boxes ("13" = boxes 1 and 3) - the XSD allows any string as
#   an alternate type, so the code needs no lookup table. Aspects come as
#   two tokens (the four classic ones, plus a 2-box one for 'Pool and
#   Determination) rather than one 6-box token: 2^6 faces was a gas factory.
# Everything stays manual: the tokens are visual reminders the player drives,
# no game rule is wired to them.
# Origine : Merlin - jetons speciaux (horloge, compteurs a cases), 2026.
# One counting token per resource, 0-5, same grammar as the stat tokens: some
# cards ask the player to accumulate resources of a given type on them (Deadpool's
# Blackout and Tic-Tac-Toe), and the printed card has no room to show it.
# Origine : Merlin - jetons de ressource (2026).
resourceTokenIds = {
    "Physical": "fcb21620-0398-4b7d-b191-d9c0f16766a4",
    "Energy": "ead1d5fe-c6de-4d09-a4cf-cdc51dff8874",
    "Mental": "d063bef3-690b-471a-9303-d20107ee2ed4",
    "Wild": "18a521b2-e7c3-4782-ad90-c0fd01a4a9ef",
}

specialTokenIds = {
    "Action Clock": "4f2a322f-0d3a-4315-ad65-e046b9805e47",
    "Aspect Counter": "7e23fb75-f532-43c3-9a0f-575c9876b9d2",
    "Extra Aspect Counter": "b2b1a6c7-2aa1-45dd-adfc-e4bc0479d05f",
    "Resource Counter": "071e3cef-963e-44fb-bd14-642003c96b80",
}

# Highest value per counting token type (stat tokens 0-9, clock 0-6).
valueTokenMax = {
    'stat_token': 9,
    'clock_token': 6,
    'resource_token': 5,
}

def isStatToken(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != 'stat_token':
            return False
    return True

def isValueToken(cards, x = 0, y = 0):
    """showIf: tokens holding a single value (stat 0-9, clock 0-6)."""
    for c in cards:
        if c.Type not in valueTokenMax:
            return False
    return True

def isChecklistToken(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != 'checklist_token':
            return False
    return True

def isSpecialToken(cards, x = 0, y = 0):
    for c in cards:
        if c.Type not in ('stat_token', 'clock_token', 'checklist_token', 'resource_token'):
            return False
    return True

def statTokenValue(card):
    """Reads a value token's value from its current alternate.

    Stat tokens use the historical letters ("b".."j" = 1..9), the clock uses
    the value itself ("1".."6"); base face is always 0.
    """
    alt = card.alternate
    if alt == "":
        return 0
    if alt[0].lower().isalpha():
        return ord(alt[0].lower()) - ord('a')
    return num(alt)

def modifyStatToken(card, delta):
    """Steps a value token by delta, clamped to its own 0-max range."""
    mute()
    maxValue = valueTokenMax.get(card.Type, 9)
    old = statTokenValue(card)
    new = max(0, min(maxValue, old + delta))
    if new == old:
        return
    if new == 0:
        card.alternate = ""
    elif card.Type == 'clock_token':
        card.alternate = str(new)
    else:
        card.alternate = chr(ord('a') + new)
    notify("{} sets {} to {}.".format(me, card.Name.split(" (")[0], new))

def resetSpecialToken(card, x = 0, y = 0):
    """Back to the base face: value 0, or every box off."""
    mute()
    if card.alternate == "":
        return
    card.alternate = ""
    notify("{} resets {}.".format(me, card.Name.split(" (")[0]))

def checklistBoxCount(card):
    """4 boxes on the standard counters, 2 on the extra-aspects one."""
    return 2 if "Extra" in card.Name else 4

def toggleTokenBox(card, box):
    """Lights or clears one box of a checklist token by rebuilding the code."""
    mute()
    # A box the token does not have (5-6 on a 4-box counter) would point to a
    # non-declared alternate: refuse it instead of blanking the token.
    if box > checklistBoxCount(card):
        whisper("{} has no box {}.".format(card.Name.split(" (")[0], box))
        return
    lit = set(int(c) for c in card.alternate) if card.alternate != "" else set()
    if box in lit:
        lit.discard(box)
    else:
        lit.add(box)
    card.alternate = "".join(str(b) for b in sorted(lit))
    state = "lights box" if box in lit else "clears box"
    notify("{} {} {} on {}.".format(me, state, box, card.Name.split(" (")[0]))

def toggleBox1(card, x = 0, y = 0): toggleTokenBox(card, 1)
def toggleBox2(card, x = 0, y = 0): toggleTokenBox(card, 2)
def toggleBox3(card, x = 0, y = 0): toggleTokenBox(card, 3)
def toggleBox4(card, x = 0, y = 0): toggleTokenBox(card, 4)

def createSpecialToken(tokenName, x, y):
    mute()
    ids = dict(statTokenIds)
    ids.update(specialTokenIds)
    ids.update(resourceTokenIds)
    table.create(ids[tokenName], x, y, 1, True)
    notify("{} creates a {} token.".format(me, tokenName))

def createTokenTHW(group=None, x=0, y=0): createSpecialToken("THW", x, y)
def createTokenATK(group=None, x=0, y=0): createSpecialToken("ATK", x, y)
def createTokenDEF(group=None, x=0, y=0): createSpecialToken("DEF", x, y)
def createTokenREC(group=None, x=0, y=0): createSpecialToken("REC", x, y)
def createTokenClock(group=None, x=0, y=0): createSpecialToken("Action Clock", x, y)
def createTokenAspects(group=None, x=0, y=0): createSpecialToken("Aspect Counter", x, y)
def createTokenAspectsExtra(group=None, x=0, y=0): createSpecialToken("Extra Aspect Counter", x, y)
def createTokenResources(group=None, x=0, y=0): createSpecialToken("Resource Counter", x, y)
def createTokenPhysical(group=None, x=0, y=0): createSpecialToken("Physical", x, y)
def createTokenEnergy(group=None, x=0, y=0): createSpecialToken("Energy", x, y)
def createTokenMental(group=None, x=0, y=0): createSpecialToken("Mental", x, y)
def createTokenWild(group=None, x=0, y=0): createSpecialToken("Wild", x, y)

def addAPCounter(card, x=0, y=0, qty=1):
    mute()
    # Right/Left stay inert on every special token: without this guard they
    # drop All Purpose markers on it, which reads as a second, confusing
    # value next to the one the token displays.
    # Origine : Merlin - jetons de stat (2026), etendu aux jetons speciaux.
    if isSpecialToken([card]):
        return
    card.controller = me
    card.markers[AllPurposeMarker] += qty
    notify("{} adds {} Marker(s) on {}.".format(me, qty, card))

def removeAPCounter(card, x = 0, y = 0):
    mute()
    # Same guard as addAPCounter: no All Purpose markers on a special token.
    # Origine : Merlin - jetons de stat (2026), etendu aux jetons speciaux.
    if isSpecialToken([card]):
        return
    card.controller = me
    card.markers[AllPurposeMarker] -= 1
    notify("{} removes 1 Marker from {}.".format(me, card))

def clearAPCounter(card, x = 0, y = 0):
    mute()
    card.controller = me
    card.markers[AllPurposeMarker] = 0
    notify("{} removes all Marker from {}.".format(me, card))

def stun(card, x = 0, y = 0):
    mute()
    card.markers[StunnedMarker] += 1
    notify("{} gains a stunned marker.".format(card))

def confuse(card, x = 0, y = 0):
    mute()
    card.markers[ConfusedMarker] += 1
    notify("{} gains a confused marker.".format(card))

def tough(card, x = 0, y = 0):
    mute()
    card.markers[ToughMarker] += 1
    notify("{} gains a tough marker.".format(card))

def removeStun(card, x = 0, y = 0):
    mute()
    card.markers[StunnedMarker] -= 1
    notify("{} removes 1 Stunned marker from {}.".format(me, card))

def removeConfuse(card, x = 0, y = 0):
    mute()
    card.markers[ConfusedMarker] -= 1
    notify("{} removes 1 Confused marker from {}.".format(me, card))

def removeTough(card, x = 0, y = 0):
    mute()
    card.markers[ToughMarker] -= 1
    notify("{} removes 1 Tough marker from {}.".format(me, card))

def flipCoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
        notify("{} flips heads.".format(me))
    else:
        notify("{} flips tails.".format(me))

def randomNumber(group, x=0, y=0):
    mute()
    max = askInteger("Random number range (1 to ....)", 6)
    if max == None: return
    notify("{} randomly selects {} (1 to {})".format(me, rnd(1,max), max))

def randomPlayer(group, x=0, y=0):
    mute()
    players = getPlayers()
    if len(players) <= 1:
        notify("{} randomly selects {}".format(me, me))
    else:
        n = rnd(0, len(players)-1)
        notify("{} randomly selects {}".format(me, players[n]))

def readyExhaust(card, x = 0, y = 0):
    mute()
    if card.orientation == Rot0:
        card.orientation = Rot90
        notify("{} exhausts {}.".format(me, card))
    else:
        card.orientation = Rot0
        notify("{} readies {}.".format(me, card))

def revealHide(card, x = 0, y = 0):
    mute()
    if "b" in card.alternates:
        if card.CardNumber == "31001a" or card.CardNumber == "31001b" or card.CardNumber == "31002a" or card.CardNumber == "31002b":
            specific_hero_flip(card)
        else:
            changeForm(card)
            specific_hero_flip(card)
            if isScheme([card]):
                placeThreatOnScheme(card)

            if isVillain([card]):
                setHPOnCharacter(card)

            # Handle environments with counters (such as Criminal Enterprise, Avengers Tower, Bell Tower, ...)
            # Some of them enters play with X counters
            if card.Type == "environment":
                lookForCounters(card)

    else:
        if card.isFaceUp:
            card.isFaceUp = False
            clearMarker(card)
            notify("{} hides {}.".format(me, card))
        else:
            card.isFaceUp = True
            notify("{} reveals {}.".format(me, card))
            lookForToughness(card)
            lookForCounters(card)
            placeThreatOnScheme(card)
            setHPOnCharacter(card)

def discard(card, x = 0, y = 0):
    mute()
    # A special token is not a card. It has no deck to go back to, so the
    # generic branch at the end of this function used to drop it into the
    # player's Deck Discard, where it sat among real cards and came back in the
    # deck at the next reshuffle. Discarding one means taking it off the table.
    # Checked first: none of the tests below mean anything for a token.
    # Origine : Merlin - jetons speciaux (2026).
    if isSpecialToken([card]):
        notify("{} removes the {} token.".format(me, card.Name.split(" (")[0]))
        card.delete()
        return
    card.controller = me

    # A player card can name the pile of its OWN player it goes back to when it
    # leaves play. Needed by side decks that never lose their cards: Daredevil's
    # identity reads "When a [[SENSE]] upgrade would leave play, place it on the
    # bottom of the [[SENSE]] deck instead", and Iceman's Frostbite reads "set
    # this card aside" - both go back to their own pile, never to a discard one.
    # The optional ":Bottom" suffix carries that "under": moveTo() alone would
    # put the card back on top.
    # Checked BEFORE the Permanent guard on purpose. A card that says where it
    # returns to is not being discarded, it is being recycled, and the guard -
    # which is there to stop an accidental discard - would otherwise make the
    # move impossible: Frostbite carries the Permanent keyword.
    # Deliberately NOT the existing DefaultDiscardPile property, which names a
    # SHARED pile (20 player side schemes already point it at "Side Discard", a
    # pile the player does not have): reusing it here would break them.
    # Doctor Strange's Invocation keeps its hard-coded branch below.
    # Origine : Merlin - side decks that recycle their cards, introduced with
    # Daredevil's SENSE deck (Fear No Evil).
    if card.hasProperty("PlayerDiscardPile"):
        target = card.properties["PlayerDiscardPile"]
        if ":" in target:
            pileName, position = target.split(":", 1)
            pileName, position = pileName.strip(), position.strip().lower()
        else:
            pileName, position = target.strip(), ""
        notify("{} puts {} back into {}.".format(me, card, pileName))
        if position == "bottom":
            card.moveToBottom(me.piles[pileName])
        else:
            card.moveTo(me.piles[pileName])
        return

    if isPermanent(card):
        notify("{} has 'Permanent' keyword and cannot be discarded!".format(card.name))
        return
    if card.Type == "hero" or card.Type == "alter_ego":
        return
    elif isVillain([card]):
        nextVillainStage()
    elif card.Type == "main_scheme":
        nextSchemeStage()
    elif card.Owner == 'infinity_gauntlet':
        notify("{} discards {} from {}.".format(me, card, card.group.name))
        card.moveTo(specialDeckDiscard())
    elif isEncounter([card]):
        if isScheme([card]) and getGlobalVariable("villainSetup") == "Red Skull":
            notify("{} sent back to side schemes deck!".format(card))
            card.moveTo(sideDeckDiscard())
        elif hasVictory(card):
            discardChoice = 2
            if card.markers[DamageMarker] == 0 or card.markers[ThreatMarker] != 0 or card.markers[AllPurposeMarker] != 0:
                discardChoice = askChoice("Do you want to discard it or add it to Victory Display ?", ["Encounter Discard Pile", "Victory Pile"])
                if discardChoice == 1:
                    discardPile = encounterDiscardDeck()
            if discardChoice == 2:
                discardPile = victoryDisplay()
                notify("{} has 'Victory' keyword and is then sent to Victory Display!".format(card))
            card.moveTo(discardPile)
            if discardChoice == 2 and isSideScheme([card]) and getGlobalVariable("villainSetup") == "Hela":
                vCard = filter(lambda card: card.Type == "villain" and card.alternate == "", table)
                if len(vCard) > 0:
                    gameDifficulty = getGlobalVariable("difficulty")
                    others_hp = 3 if gameDifficulty == "1" else 2
                    addMarker(vCard[0], x=0, y=0, qty=others_hp * len(getPlayers()))
        elif hasDefaultDiscardPile(card):
            discardPile = card.properties["DefaultDiscardPile"]
            card.moveTo(shared.piles[discardPile])
        else:
            card.moveTo(encounterDiscardDeck())
    elif card.Owner == 'invocation':
        notify("{} discards {} from {}.".format(me, card, card.group.name))
        card.moveTo(me.piles["Special Discard"])
    else:
        if hasVictory(card):
            discardChoice = 2
            if card.markers[DamageMarker] == 0 or card.markers[ThreatMarker] != 0 or card.markers[AllPurposeMarker] != 0:
                discardChoice = askChoice("Do you want to discard it or add it to Victory Display ?", ["Discard Pile", "Victory Pile"])
                if discardChoice == 1:
                    discardPile = me.piles["Deck Discard"]
            if discardChoice == 2:
                discardPile = victoryDisplay()
                notify("{} has 'Victory' keyword and is then sent to Victory Display!".format(card))
            card.moveTo(discardPile)
        else:
            pile = card.owner.piles["Deck Discard"]
            who = pile.controller

            notify("{} discards {} from {}.".format(me, card, card.group.name))
            card.moveTo(me.piles["Deck Discard"])

            if who != me:
                card.setController(who)
                remoteCall(who, "doDiscard", [card, pile])
            else:
                doDiscard(card, pile)

def doDiscard(card, pile):
    card.moveTo(pile)

def draw(group, x = 0, y = 0):
    mute()
    drawCard(group, False)
    notify("{} draws a card.".format(me))

def drawMany(group, count = None, checkHandSize = False):
    mute()
    if len(group) == 0:
        notifyBar("#FF0000", "Deck {} is empty!".format(group.name))
        return
    if deckLocked():
        whisper("Your deck is locked, you cannot draw cards at this time")
        return
    if count is None:
        count = askInteger("Draw how many cards?", 6)
    if count is None or count < 0:
        whisper("drawMany: invalid card count")
        return
    for i in range(0, count):
        drawCard(group, checkHandSize)

def drawCard(group, checkHandSize = False):
    mute()
    # For special deck we shuffle when we need to draw and deck is empty
    if group.name == 'Special':
        if len(me.piles[group.name]) == 0:
            for c in me.piles["Special Discard"]: c.moveTo(c.owner.piles["Special"])
            shuffle(me.piles["Special"])
            notifyBar("#0000FF", "Special Deck for player {} has been created from discard and shuffled!".format(me.name))
            rnd(1,1)

        card = me.piles["Special"][0]
        card.moveToTable(0,0,False)
    # For player deck, we draw and if deck is empty after (or while) drawing, we notify + recreate deck from its discard (shuffle it)
    else:
        card = me.deck[0]
        # Mysterio can put some encounter cards in players decks:
        if isEncounter([card]) and getGlobalVariable("villainSetup") == "Mysterio":
            posX = playerX(int(me.getGlobalVariable("playerID"))) - 35
            posY = 100
            # Deal as a facedown card and draw another one as a replacement
            drawUnrevealed(group, posX, posY)
            drawCard(group, checkHandSize)
        else:
            card.moveTo(me.hand)
            if noCountInHandSize(card) and checkHandSize:
                drawCard(group, checkHandSize)
        checkDeckRemainingCards(group)


def switchCard(card, x = 0, y = 0):
    mute()
    card_deck = me.deck[0]
    if card.group == table:
        x, y = card.position
        card_deck.moveToTable(x, y, False)
    elif card.group == me.hand:
        card_deck.moveTo(me.hand)
    card.moveTo(me.deck)

def drawManyUnrevealed(group, count = None, x=0, y=0):
    mute()
    if len(group) == 0:
        notifyBar("#FF0000", "Deck {} is empty!".format(group.name))
        return
    if deckLocked():
        whisper("Your deck is locked, you cannot draw cards at this time")
        return
    if count is None:
        count = askInteger("Draw how many cards?", 6)
    if count is None or count < 0:
        whisper("drawManyUnrevealed: invalid card count")
        return
    for i in range(0, count):
        drawUnrevealed(group, x= i*10, y=0)

def drawUnrevealed(group=None, x=0, y=0):
    mute()
    if len(group) == 0:
        notify("{} is empty.".format(group.name))
        return
    if deckLocked():
        whisper("Your deck is locked, you cannot draw cards at this time")
        return

    card = group[0]
    card.moveToTable(x, y, True)
    checkDeckRemainingCards(group)
    notify("{} draws an unrevealed card from the {}.".format(me, group.name))
    return card

def checkDeckRemainingCards(group):
    """
    Check how many remaining cards in the given group. Warn in notification bar if empty + recreate and shuffle
    """
    if len(me.piles[group.name]) == 0:
        for c in me.piles["Deck Discard"]:
            c.moveTo(me.Deck)
        shuffle(me.Deck)
        notifyBar("#FF0000", "{}'s deck has been created from discard and shuffled!".format(me.name))
        rnd(1,1)

def mulligan(group, x = 0, y = 0):
    mute()
    dlg = cardDlg(me.hand)
    dlg.min = 0
    dlg.max = len(me.hand)
    dlg.text = "Select which cards you would like to mulligan"
    mulliganList = dlg.show()
    if not mulliganList:
        return
    if not confirm("Confirm Mulligan?"):
        return
    notify("{} mulligans.".format(me))
    for card in mulliganList:
        card.moveTo(me.piles["Deck Discard"])
    drawMany(me.Deck, len(mulliganList), True)

def FlipDeckTopCard(group=None, x=0, y=0):
    mute()
    if len(group) == 0:
        notify("{} is empty.".format(group.name))
        return
    if deckLocked():
        whisper("Your deck is locked, you cannot draw cards at this time")
        return

    card = group[0]
    if card.isFaceUp:
        card.isFaceUp = False
        notify("{} hides {} from the {}.".format(me, card, group))
    else:
        card.isFaceUp = True
        notify("{} reveals {} from the {}.".format(me, card.name, group.name))
    return card

def bottomPlayerDeck(card, x = 0, y = 0):
    mute()
    card.moveToBottom(me.Deck)

def removeTopXCards(group):
    mute()
    nbCards = askInteger("How many cards to remove from the game ?", len(group))
    if nbCards == None: return
    while nbCards > 0:
        group[0].moveTo(me.piles['Removed'])
        nbCards -= 1
    notify("{} moves all cards from {} to the Removed pile".format(me, group.name))

def bottomEncounterDeck(card, x = 0, y = 0):
    mute()
    card.moveToBottom(encounterDeck())

def moveAllToEncounter(group):
    mute()
    if confirm("Shuffle all cards from {} to Encounter Deck?".format(group.name)):
        for c in group:
            c.moveTo(encounterDeck())
        notify("{} moves all cards from {} to the Encounter Deck".format(me, group.name))
        shuffle(encounterDeck())

def moveAllToEncounterTop(group):
    mute()
    if confirm("Move all cards from {} to the top of the Encounter Deck?".format(group.name)):
        for c in group:
            c.moveTo(encounterDeck())
            notify("{} moves all cards from {} to the top of the Encounter Deck".format(me, group.name))

def moveAllToEncounterBottom(group):
    mute()
    if confirm("Move all cards from {} to the bottom of the Encounter Deck?".format(group.name)):
        for c in group:
            c.moveToBottom(encounterDeck())
            notify("{} moves all cards from {} to the bottom of the Encounter Deck".format(me, group.name))

def shuffle(group, x = 0, y = 0, silence = False):
    mute()
    for card in group:
        if card.isFaceUp:
            card.isFaceUp = False
    group.shuffle()
    heroPlayed = me.getGlobalVariable("heroPlayed")
    cardForm = me.getGlobalVariable("cardForm")
    if heroPlayed == "magik" and cardForm == "hero" and group == me.piles["Deck"] and not group.top().isFaceUp:
        group.top().isFaceUp = True  
    if silence == False:
        notify("{} shuffled their {}".format(me, group.name))

def randomDiscard(group, x = 0, y = 0):
    mute()
    card = group.random()
    if card == None:
        return
    card.moveTo(card.owner.piles["Deck Discard"])
    notify("{} randomly discards {} from {}.".format(me, card, group.name))

def shuffleDiscardIntoDeck(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    if group == me.piles["Deck Discard"]:
        if len(me.piles["Deck"]) > 0:
            if askChoice("There are still {} card(s) in your Deck. Are you sure you want to shuffle your discard pile into your Deck ?".format(len(me.piles["Deck"])), ["Yes", "No"]) != 1:
                return
        for card in group:
            card.moveTo(me.piles["Deck"])
        shuffle(me.piles["Deck"])
        notify("{} shuffles their discard pile into their Deck.".format(me))
    if group == encounterDiscardDeck():
        if len(encounterDeck()) > 0:
            if askChoice("There are still {} card(s) in Encounter Deck. Are you sure you want to shuffle discard pile into this Deck ?".format(len(encounterDeck())), ["Yes", "No"]) != 1:
                return
        for card in group:
            card.moveTo(encounterDeck())
        shuffle(encounterDeck())
        notify("{} shuffles the encounter discard pile into the encounter Deck.".format(me))
    if group == sideDeckDiscard():
        if len(sideDeck()) > 0:
            if askChoice("There are still {} card(s) in Side Deck. Are you sure you want to shuffle discard pile into this Deck ?".format(len(sideDeck())), ["Yes", "No"]) != 1:
                return
        for card in group:
            card.moveTo(sideDeck())
        shuffle(sideDeck())
        notify("{} shuffles the Side discard pile into the Side Deck.".format(me))
    if group == specialDeckDiscard():
        if len(specialDeck()) > 0:
            if askChoice("There are still {} card(s) in Special Deck. Are you sure you want to shuffle discard pile into this Deck ?".format(len(specialDeck())), ["Yes", "No"]) != 1:
                return
        for card in group:
            card.moveTo(specialDeck())
        shuffle(specialDeck())
        notify("{} shuffles the Special discard pile into the Special Deck.".format(me))
    if group == me.piles["Special Discard"]:
        for card in group:
            card.moveTo(me.piles["Special"])
        shuffle(me.piles["Special"])
        notify("{} shuffles the special discard pile into the special Deck.".format(me))
    if group == specialDeckDiscard():
        for card in group:
            card.moveTo(specialDeck())
        shuffle(encounterDeck())
        notify("{} shuffles the special discard pile into the special Deck.".format(me))

def shuffleSetIntoEncounter(group, x = 0, y = 0, random = False):
    mute()
    if len(group) == 0: return

    # Global Variable
    vName = getGlobalVariable("villainSetup")
    ownerList = []

    for card in group:
        ownerExistsInList = ownerList.count(card.Owner)
        if ownerExistsInList == 0:
            ownerList.append(card.Owner)
    if random:
        ownerChoice = 1
    else:
        ownerChoice = askChoice("Which encounter set would you like to shuffle into deck?", ["Random"] + ownerList)

    if ownerChoice == 0: return
    if ownerChoice == 1:
        ownerSelected = rnd(0, len(ownerList)-1)
    else:
        ownerSelected = ownerChoice-2

    for card in group:
        if card.Owner == ownerList[ownerSelected]:
            if card.Type == "environment" and (vName == "Mojo" or vName == "Dark Beast"):
                card.moveToTable(tableLocations['environment'][0]-70, tableLocations['environment'][1])
            elif vName == "Mojo":
                card.moveTo(sideDeckDiscard())
            else:
                card.moveTo(encounterDeck())

    if vName == "Mojo":
        shuffle(sideDeckDiscard())
        for card in sideDeckDiscard():
            card.moveTo(encounterDeck())
        notify("{} put {} cards on top of the Encounter Deck.".format(me, ownerList[ownerSelected]))
    else:
        shuffle(encounterDeck())
        notify("{} shuffles {} into the Encounter Deck.".format(me, ownerList[ownerSelected]))

def viewGroup(group, x = 0, y = 0):
    group.lookAt(-1)

def showGroup(group, gShuffle = False):
    mute()
    group.collapsed = False
    if gShuffle:
        shuffle(group)

def pluralize(num):
   if num == 1:
       return ""
   else:
       return "s"

def createCard(group=None, x=0, y=0):
    cardID, quantity = askCard()
    cards = table.create(cardID, x, y, quantity, True)
    try:
        iterator = iter(cards)
    except TypeError:
        # not iterable
        notify("{} created {}.".format(me, cards))
    else:
        # iterable
        for card in cards:
            notify("{} created {}.".format(me, card))

def num(s):
   if not s: return 0
   try:
      return int(s)
   except ValueError:
      return 0

def moveToVictory(card, x=0, y=0):
    mute()
    card.moveTo(victoryDisplay())
    notify("{} adds '{}' to the Global Victory Display".format(me, card))


#------------------------------------------------------------
# Global variable manipulations function
#------------------------------------------------------------

def nextSchemeStage(group=None, x=0, y=0):
    mute()

    # Global Variable
    vName = getGlobalVariable("villainSetup")

    # We need a new Scheme card
    if group is None or group == table:
        group = mainSchemeDeck()
    if len(group) == 0: return

    if group.controller != me:
        remoteCall(group.controller, "nextSchemeStage", [group, x, y])
        return

    if vName == 'Kang':
        whisper("You can't advance to next scheme using \"Next Scheme\" function for Kang. Use \"Next Villain\" instead")
    else:
        choice = askChoice("Do you want to reveal the next sequential stage of the scheme deck ?", [], [], ["Yes", "No"])
        if choice != -1: return

    nextSchemeStageSetup(vName)


def nextVillainStage(group=None, x=0, y=0):
    mute()

    # Global Variable
    vName = getGlobalVariable("villainSetup")
    gameDifficulty = getGlobalVariable("difficulty")

    # We need a new Villain card
    if group is None or group == table:
        group = villainDeck()
        whisper("group Next Villain")
    if len(group) == 0 and vName != "Apocalypse": return

    if group.controller != me:
        whisper("Remote call Next Villain")
        remoteCall(group.controller, "nextVillainStage", [group, x, y])
        return

    if vName not in ('The Wrecking Crew', 'Loki', 'God of Lies'):
        choice = askChoice("Do you want to reveal the next sequential stage of the villain deck ?", [], [], ["Yes", "No"])
        if choice != -1: return

    nextVillainStageSetup(vName)


def clearTargets(group=table, x=0, y=0):
    for c in group:
        if c.controller == me or (c.targetedBy is not None and c.targetedBy == me):
            c.target(False)

def switchCards(oldCard, newCard, h = 1, t = 1, s = 1, c = 1, a = 1):
    if h == 1:
        newCard.markers[HealthMarker] = oldCard.markers[HealthMarker]
    if t == 1:
        newCard.markers[ToughMarker] = oldCard.markers[ToughMarker]
    if s == 1:
        newCard.markers[StunnedMarker] = oldCard.markers[StunnedMarker]
    if c == 1:
        newCard.markers[ConfusedMarker] = oldCard.markers[ConfusedMarker]
    if a == 1:
        newCard.markers[AllPurposeMarker] = oldCard.markers[AllPurposeMarker]
    oldCard.markers[HealthMarker] = 0
    oldCard.markers[ToughMarker] = 0
    oldCard.markers[StunnedMarker] = 0
    oldCard.markers[ConfusedMarker] = 0
    oldCard.markers[AllPurposeMarker] = 0

#------------------------------------------------------------
# Highlight
#------------------------------------------------------------

def blueHighlight(card, x=0 , y=0):
    card.highlight = BlueColour

def orangeHighlight(card, x=0 , y=0):
    card.highlight = OrangeColour

def greenHighlight(card, x=0 , y=0):
    card.highlight = GreenColour

def purpleHighlight(card, x=0 , y=0):
    card.highlight = PurpleColour

def redHighlight(card, x=0 , y=0):
    card.highlight = RedColour

def blackHighlight(card, x=0 , y=0):
    card.highlight = BlackColour

def whiteHighlight(card, x=0 , y=0):
    card.highlight = WhiteColour

def clearHighlight(card, x=0, y=0):
    card.highlight = None

#------------------------------------------------------------
# Automation
#------------------------------------------------------------
def autoCharges(args):
    mute()
    # Only for move card from Pile to Table
    if isinstance(args.fromGroups[0],Pile) and isinstance(args.toGroups[0],Table):
        if len(args.cards) == 1:
            card = args.cards[0]
            if card.controller == me and card.isFaceUp:
                lookForCounters(card)
                lookForToughness(card)
                placeThreatOnScheme(card)
                setHPOnCharacter(card)

def magikDeck(args):
    mute()
    card = args.cards[0] # card being moved
    heroPlayed = me.getGlobalVariable("heroPlayed") 
    cardForm = me.getGlobalVariable("cardForm") 
    if heroPlayed == "magik" and cardForm == "hero" and card.controller == me: # if card being moved belongs to Magik player
        if args.fromGroups[0] == card.controller.deck or args.toGroups[0] == card.controller.deck:
            if not(len(card.controller.deck)):
                return
            if len(card.controller.deck) >= 2:
                if card.controller.deck[1].isFaceUp: # checks if second top is face up and turns it down if so
                    card.controller.deck[1].isFaceUp = False
            if not card.controller.deck.top().isFaceUp: # Flips first card of the deck faceup
                card.controller.deck.top().isFaceUp = True

def noCountInHandSize(card):
    """
    Return boolean value to specify if the given card should be taken into account when computing hand size
    """
    return re.search('.*does not count toward your hand size.*', card.properties["Text"], re.IGNORECASE)

def countHandSize(hand_group):
    """
    Return the number of cards in given hand, taking into account that some cards may be ignored in this process
    """
    return len([c for c in hand_group if not noCountInHandSize(c)])

def maxHandSize(p):
    """
    Return the maximum number of cards a player can have in hand.
    """
    additionnal_handSize = p.counters["Additionnal Alter-Ego Card Draw"].value
    if p.getGlobalVariable("cardForm") != "alter_ego":
        additionnal_handSize = p.counters["Additionnal Hero Card Draw"].value
    handSize = p.counters["Default Card Draw"].value + additionnal_handSize
    # One-shot bonus for the current round, in either form; spent by
    # refillHand() at the end of the player phase.
    # Origine : Merlin - taille de main temporaire (2026).
    handSize += p.counters["Temporary Hand Size"].value
    return handSize

def lookForAttribute(card, attrib):
    """
    Look for attribute
    """
    return re.search('.*' + attrib + '.*', card.properties["Attribute"], re.IGNORECASE) if card.hasProperty("Attribute") else False

def lookForSetup(card):
    """
    Look for Villainous keyword => for boost card purpose
    """
    return re.search('.*Setup.*', card.properties["Text"])

def lookForStarting(card):
    """
    Look for the "Starting." keyword => card joins the player's starting hand
    Anchored on purpose: an unanchored search would match any card whose text
    merely mentions "starting" (e.g. "your starting hand") and wrongly pull it
    out of the deck.
    The markup in front of the keyword is skipped, because card text is not
    consistent about it - Innate Aggression writes "Starting." plain while
    Innate Perception, in the SAME set, writes "<b>Starting.</b>". Matching
    on the bare word leaves those cards sitting in the deck, silently.
    Origine : Merlin - keyword introduced with Fear No Evil.
    """
    return re.match('\\s*(<[^>]+>\\s*)*Starting\\.', card.properties["Text"])

def lookForToughness(card):
    """
    Adds a Tough status card to a character if such ability is found in card's text
    """
    if card.Type in ["villain", "leader", "minion", "ally"]:
        description_search = re.search('.*Toughness.*', card.properties["Text"], re.IGNORECASE)
        if description_search:
            tough(card)

def lookForVillainous(card):
    """
    Look for Villainous keyword => for boost card purpose
    """
    return re.search('.*Villainous.*', card.properties["Text"], re.IGNORECASE) if card.Type in ["minion"] else False

def lookForCounters(card):
    """
    Init the number of counters (all purpose) on a given card
    """
    #Capture text between "(. counters)"
    if card.markers[AllPurposeMarker] == 0:
        nb_players = len(getPlayers())

        # This should match all "Uses (x whatever counters)" cases. Warning: some of them are based on number of players (such as Crossbone's Machine Gun)
        description_search = re.search('.*Uses \((\d+)(.?\[per_.*\])?.*counters\)*.', card.properties["Text"], re.IGNORECASE)
        if description_search:
            nb_base_counters = int(description_search.group(1))
            # If more than one group found, then the number of counters changes with number of players
            is_per_player = description_search.group(2) is not None

            nb_counters = (nb_base_counters * nb_players) if is_per_player else nb_base_counters
            log_msg = "Initializing {} with {} counter(s)".format(card.name, nb_counters)

            # Some cards add additional counters based on number of players (such as Fanaticism)
            additional_search = re.search('.*(\d+).?\[per_.*\] additional*.', card.properties["Text"], re.IGNORECASE)
            additional_counters = 0
            if additional_search:
                additional_counters = int(additional_search.group(1)) * nb_players
                log_msg += " + {} additional counter(s)".format(additional_counters)

            notify(log_msg)
            total_counters = nb_counters + additional_counters
            addAPCounter(card, x=0, y=0, qty=total_counters)

        description_search = re.search('.*enters play with (\d+).?(\[per_.*\])?.*counters on.*', card.properties["Text"], re.IGNORECASE)
        if description_search:
            nb_base_counters = int(description_search.group(1))
            # If more than one group found, then the number of counters changes with number of players
            is_per_player = description_search.group(2) is not None

            nb_counters = (nb_base_counters * nb_players) if is_per_player else nb_base_counters
            addAPCounter(card, x=0, y=0, qty=nb_counters)

def placeThreatOnScheme(card):
    """
    Init the number of threats on main & side schemes
    """
    if isScheme([card]) and card.markers[ThreatMarker] == 0:
        if card.properties["BaseThreat"] is not None and card.properties["BaseThreat"] != '' and card.properties["BaseThreatFixed"] is not None:
            init_val = int(card.properties["BaseThreat"])
            is_base_fixed = card.properties["BaseThreatFixed"] == "True"
            nb_players = len(getPlayers())
            scheme_txt = card.properties["Text"]
            log_msg = "Initializing {} with ".format(card.name)

            # Initial value
            base_threats = init_val
            if not is_base_fixed:
                base_threats = init_val * nb_players
            log_msg += "{} base threats".format(base_threats)

            # Handle 'Hinder' (Hinder 3[per_player])
            add_hinder = 0
            description_search = re.search('.*Hinder (\d+).?\[per_.*\].*', card.properties["Text"], re.IGNORECASE)
            if description_search:
                # Some main schemes only GAIN the keyword beyond one player: "If there
                # is more than 1 player on your team, this stage gains hinder 2[per_hero]."
                # The search above matches the keyword wherever it sits in the text, so
                # the condition in front of it was ignored and a solo game started with
                # 2 threats that the card never asks for. Ten cards are worded this way,
                # every stage 1B of Civil War and Synthezoid Smackdown - the leader
                # scenarios, always played against one of these schemes.
                # Origine : Merlin - constate en jeu en solo (Valkyrie, puis She-Hulk),
                # 2026.
                conditional = re.search('more than 1 player|more than one player', card.properties["Text"], re.IGNORECASE)
                if conditional and nb_players < 2:
                    log_msg += " + no threat from Hinder (the card only gains it beyond one player)"
                else:
                    add_hinder = int(description_search.group(1)) * nb_players
                    log_msg += " + {} threats from Hinder keyword".format(add_hinder)

            # Edge cases: add threats when revealed (but only if not already found Hinder text because the reminder contains the searched text)
            # This is mainly due to inconsistent wording between beginning of the game before Hinder keyword arrived
            add_others = 0
            description_search = re.search('.*Place an additional (\d+).?\[per_.*\] threat here.*', card.properties["Text"], re.IGNORECASE)
            if description_search and add_hinder == 0:
                add_others = int(description_search.group(1)) * nb_players
                log_msg += " + {} threats from card text".format(add_others)

            total_threats = base_threats + add_hinder + add_others
            notify(log_msg)
            addMarker(card, x=0, y=0, qty=int(total_threats))

def setHPOnCharacter(card):
    """
    Sets Damage markers on characters based on their defined HP value
    """
    # Handle edge case: exchange Loki with another one, all HP and status cards must be kept
    if card.Type == "villain" and getGlobalVariable("villainSetup") == "Loki":
        lokis_on_table = [c for c in table if c.Type == 'villain']
        if len(lokis_on_table) == 2: # There should be 2 Loki cards on table: the previous one and the new one
            # The 'previous' one is the one that has still some HP, the 'new' one enters play and then has not yet defined HP
            previous_loki = [c for c in lokis_on_table if c.markers[HealthMarker] > 0]
            new_loki = [c for c in lokis_on_table if c.markers[HealthMarker] == 0]
            if len(previous_loki) == 1 and len(new_loki) == 1:
                notify("Copy all markers from actual Loki to new one!")
                switchCards(previous_loki[0], new_loki[0], h = 1, t = 1, s = 1, c = 1, a = 1)

    if card.Type == "villain" and card.Attribute == "Avatar of Loki." and getGlobalVariable("villainSetup") == "God of Lies":
        lokis_on_table = [c for c in table if c.Type == 'villain' and c.Attribute == 'Avatar of Loki.']
        if len(lokis_on_table) == 2: # There should be 2 Loki cards on table: the previous one and the new one
            # The 'previous' one is the one that has still some HP, the 'new' one enters play and then has not yet defined HP
            previous_loki = [c for c in lokis_on_table if c.markers[HealthMarker] > 0]
            new_loki = [c for c in lokis_on_table if c.markers[HealthMarker] == 0]
            if len(previous_loki) == 1 and len(new_loki) == 1:
                notify("Copy all markers from actual Loki to new one!")
                switchCards(previous_loki[0], new_loki[0], h = 1, t = 1, s = 1, c = 1, a = 1)
                previous_loki[0].moveTo(villainDeck())
                shuffle(villainDeck())

    if (card.Type == "hero" or card.Type == "alter_ego") and card.Owner == "ironheart":
        ironheart_on_table = [c for c in table if (c.Type == 'hero' or c.Type == 'alter_ego') and c.Owner == "ironheart"]
        if len(ironheart_on_table) == 2: # There should be 2 Ironheart cards on table: the previous one and the new one
            # The 'previous' one is the one that has still some HP, the 'new' one enters play and then has not yet defined HP
            previous_ironheart = [c for c in ironheart_on_table if c.markers[HealthMarker] > 0]
            new_ironheart = [c for c in ironheart_on_table if c.markers[HealthMarker] == 0]
            if len(previous_ironheart) == 1 and len(new_ironheart) == 1:
                notify("Copy all markers from actual Ironheart to new one!")
                switchCards(previous_ironheart[0], new_ironheart[0], h = 1, t = 1, s = 1, c = 1, a = 1)
                me.setGlobalVariable("cardForm", new_ironheart[0].Type)
                me.counters['Default Card Draw'].value = num(new_ironheart[0].HandSize)
                previous_ironheart[0].moveToBottom(me.piles['Special'])
                description_search = re.search('.*Version 3.*', new_ironheart[0].properties["Attribute"], re.IGNORECASE)
                if description_search and new_ironheart[0].markers[ToughMarker] == 0:
                    tough(new_ironheart[0])

    if card.Type in ["hero", "alter_ego", "villain", "leader"] and card.markers[HealthMarker] == 0:
        nb_players = len(getPlayers())
        base_hp = int(card.properties["HP"])
        is_per_hero = card.properties["HP_Per_Hero"] == "True"
        total_base_hp = base_hp * nb_players if is_per_hero else base_hp
        add_others = 0
        if card.Type == "villain" and getGlobalVariable("villainSetup") == "Hela" and card.alternate == "":
            sideSchemeInVictory = filter(lambda card: card.Type == "side_scheme", victoryDisplay())
            gameDifficulty = getGlobalVariable("difficulty")
            add_others = (3 if gameDifficulty == "1" else 2) * len(sideSchemeInVictory) * nb_players
        total_hp = total_base_hp + add_others
        addMarker(card, x=0, y=0, qty=int(total_hp))