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
        if c.Type != 'villain':
            return False
    return True

def isAttackable(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != 'villain' and c.Type != 'hero' and c.Type != 'minion' and c.Type != 'ally' and c.Type != 'alter_ego':
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
    vCards = filter(lambda card: card.Type == "villain", table)
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

#Triggered even OnCardDoubleClicked
def defaultCardAction(args):
    mute()
    if args.card.group == table:
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

    for p in players:
        p_hand_size = countHandSize(p.piles['Hand'])
        remoteCall(p, "clearTargets", [])
        remoteCall(p, "readyAll", [])
        remoteCall(p, "drawMany", [p.piles['Deck'], maxHandSize(p) - p_hand_size, True])

        # Check for hand size!
        if p_hand_size > maxHandSize(p):
            discardCount = p_hand_size - maxHandSize(p)
            dlg = cardDlg(p.piles['Hand'])
            dlg.title = "You have more than the allowed cards in hand."
            dlg.text = "Select " + str(discardCount) + " Card(s) to discard :"
            dlg.min = 0
            dlg.max = discardCount
            cardsSelected = dlg.show()
            if cardsSelected is not None:
                for card in cardsSelected:
                    remoteCall(p,"discard",[card])

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

def createCardsFromSet(group, owner, name, isShared = True):
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
    elif card.Type in ["hero", "alter_ego", "villain"]:
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
    elif card.Type in ["hero", "alter_ego", "villain"]:
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

def addAPCounter(card, x=0, y=0, qty=1):
    mute()
    card.controller = me
    card.markers[AllPurposeMarker] += qty
    notify("{} adds {} Marker(s) on {}.".format(me, qty, card))

def removeAPCounter(card, x = 0, y = 0):
    mute()
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

            if card.Type == "villain":
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
    card.controller = me

    if isPermanent(card):
        notify("{} has 'Permanent' keyword and cannot be discarded!".format(card.name))
        return
    if card.Type == "hero" or card.Type == "alter_ego":
        return
    elif card.Type == "villain":
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
    if len(group) == 0 and vName != "Apocalypse": return

    if group.controller != me:
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

def lookForToughness(card):
    """
    Adds a Tough status card to a character if such ability is found in card's text
    """
    if card.Type in ["villain", "minion", "ally"]:
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

    if card.Type in ["hero", "alter_ego", "villain"] and card.markers[HealthMarker] == 0:
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