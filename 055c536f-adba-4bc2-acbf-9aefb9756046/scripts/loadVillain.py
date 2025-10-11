import clr
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer

#!/usr/bin/python
# -*- coding: utf-8 -*-
#------------------------------------------------------------
# 'Load Villain' event
#------------------------------------------------------------

def loadFanmadeVillain(group, x = 0, y = 0, setupType = "fm_villain_setup"):
    mute()
    loadVillain(group, x = 0, y = 0, setupType = "fm_villain_setup")

def loadVillain(group, x = 0, y = 0, setupType = "villain_setup"):
    mute()
    villainName = ''

    if me._id != 1:
        msg = """You're not the game host\n
Only the host is allowed to load a scenario."""
        askChoice(msg, [], [], ["Close"])
        return

    if not deckNotLoaded(group, 0, 0, villainDeck()):
        msg = """Cannot generate a deck: You already have cards loaded.\n
Reset the game in order to generate a new deck."""
        askChoice(msg, [], [], ["Close"])
        return

    # Choose Villain and set Villain global variables.
    if setupType == "fm_villain_setup":
        fanmade = True
    else:
        fanmade = False
    update()
    cardSelected = dialogBox_Setup(setupPile(), setupType, None, "Which villain would you like to defeat ?", "Select Scenario :", min = 1, max = 1, isFanmade = fanmade)
    if cardSelected is None:
        return
    villainSet = cardSelected[0].Owner
    villainName = cardSelected[0].Name
    setGlobalVariable("villainSetup", villainName)
    nbModular = cardSelected[0].nbModular
    setGlobalVariable("nbModular", nbModular)
    if cardSelected[0].hasProperty("recommendedModular"):
        setGlobalVariable("recommendedModular", cardSelected[0].recommendedModular)
    if cardSelected[0].hasProperty("CW_Side"):
        setGlobalVariable("CW_Side", cardSelected[0].CW_Side)

    # Delete cards in Setup pile, choose Difficulty and load villain Cards.
    deleteCards(setupPile())
    if not loadDifficulty(): return #Difficulty need 'villainSetup' GlobalVariable to be set.
    createCardsFromSet(encounterDeck(), villainSet, villainName, True)
    update()

    # Load mandatory modulars for the scenario.
    if cardSelected[0].hasProperty("mandatoryModular"):
        mandatoryDict = cardSelected[0].mandatoryModular
        mandatoryDict = mandatoryDict.replace("True", "true").replace("False", "false")
        mandatoryDict = dict(JavaScriptSerializer().DeserializeObject(mandatoryDict))
        for k, i in mandatoryDict.items():
            setName = i[0]
            pile = shared.piles[i[1]]
            toShuffle = i[2]
            createCardsFromSet(pile, k, setName, True)
            showGroup(pile, toShuffle)

    # Load other modulars then setup Scenario.
    nbModular = int(getGlobalVariable("nbModular"))
    if not loadEncounter(encounterDeck(), nbModular): return
    campaignEncounter(villainSet)
    update()

    # Setup Scenario
    if fanmade:
        scenarioSetup_fm()
    else:
        scenarioSetup()
    getSetupCards()
    notify('{} loaded {}, Good Luck!'.format(me, villainName))
    checkSetup()


def loadDifficulty():
    mute()
    vName = getGlobalVariable("villainSetup")
    gameDifficulty = getGlobalVariable("difficulty")

    x = tableLocations['environment'][0] - 90
    y = tableLocations['environment'][1]

    if vName == 'The Wrecking Crew':
        choice = askChoice("What difficulty would you like to play at?", ["Standard", "Expert"])
        if choice == 0:
            deleteAllSharedCards()
            return
        if choice == 2:
            setGlobalVariable("difficulty", "1")
        return True

    else:
        if vName == 'Defense Tower' or vName == 'Sinister Six' or vName == 'Four Horsemen':
            x = 0
            y = 0

        cardsSelected = dialogBox_Setup(setupPile(), "difficulty_setup", None, "Difficulty selection", "Which set would you like to use ?", min = 0, max = 50, isFanmade = True)

        for card in cardsSelected:
            createCardsFromSet(encounterDeck(), card.Owner, card.Name, True)
            if card.Owner[0:3] == "exp":
                setGlobalVariable("difficulty", "1")
                gameDifficulty = getGlobalVariable("difficulty")
        update()
        
        EnvCard = sorted(filter(lambda card: card.CardNumber == "24049a", encounterDeck()))
        if len(EnvCard) != 0:
            EnvCard[0].moveToTable(x, y) # Do not override other environment cards from scenario (if any)
            x = x - 90
            if gameDifficulty == "1":
                EnvCard[0].alternate = 'b'

        EnvCard = sorted(filter(lambda card: card.CardNumber == "45075a", encounterDeck()))
        if len(EnvCard) != 0:
            EnvCard[0].moveToTable(x, y) # Do not override other environment cards from scenario (if any)

        deleteCards(setupPile())
        return True

def getSetupCards():
    shift = 0
    for c in encounterAndDiscardDeck():
        if lookForSetup(c):
            c.moveToTable(0 + shift, tableLocations['villain'][1] + 100)
            shift += 20

def deleteAllSharedCards():
    for pl in shared.piles:
        deleteCards(shared.piles[pl])