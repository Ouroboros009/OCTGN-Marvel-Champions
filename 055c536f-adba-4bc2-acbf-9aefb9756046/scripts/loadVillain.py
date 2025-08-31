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

    # Setup Scenario
    if fanmade:
        villainSetup_fm()
    else:
        villainSetup()
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

def villainSetup(group=table, x = 0, y = 0):
    # Global Variables
    gameDifficulty = getGlobalVariable("difficulty")
    vName = getGlobalVariable("villainSetup")

    # Move cards from Villain Deck to Encounter and Scheme Decks
    villainCards = sorted(filter(lambda card: card.Type == "villain", villainDeck()), key=lambda c: c.CardNumber)
    mainSchemeCards = sorted(filter(lambda card: card.Type == "main_scheme", mainSchemeDeck()), key=lambda c: c.CardNumber)
    villainEnvCards = sorted(filter(lambda card: card.Type == "environment", encounterDeck()))
    villainAttCards = sorted(filter(lambda card: card.Type == "attachment", encounterDeck()))

    if vName == 'The Wrecking Crew':
        # If we loaded the encounter deck - add the first main scheme card to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainSchemeCentered'][0], tableLocations['mainSchemeCentered'][1])
        for idx, c in enumerate(villainCards):
            c.moveToTable(villainX(4, idx), tableLocations['villain'][1])
            if idx == 0:
                c.highlight = ActiveColour
        ssCards = sorted(filter(lambda card: card.Type == "side_scheme", encounterDeck()), key=lambda c: c.CardNumber)
        for idx, c in enumerate(ssCards):
            c.moveToTable(villainX(4,idx)-10, tableLocations['villain'][1]+100)

    elif vName == "Red Skull":
        for c in filter(lambda card: card.Type == "side_scheme", encounterDeck()):
            c.moveTo(sideDeck())
        showGroup(sideDeck(), True)
        showGroup(sideDeckDiscard(), False)
        showGroup(removedFromGameDeck(), False)
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])

    elif vName == 'Tower Defense':
        vCardsProxima = villainCards[0:2]
        vCardsCorvus = villainCards[2:]
        vCardsProxima[0].moveToTable(villainX(2,0), tableLocations['villain'][1])
        vCardsCorvus[0].moveToTable(villainX(2,1), tableLocations['villain'][1])
        villainEnvCards[0].moveToTable(villainX(1,0), tableLocations['villain'][1])
        villainAttCards[0].moveToTable(villainX(2,1)-90, tableLocations['villain'][1]+75)

        for idx, c in enumerate(sorted(mainSchemeCards)):
            c.moveToTable(villainX(2,idx)-10, tableLocations['villain'][1]+100)

    elif vName == "Thanos":
        showGroup(specialDeckDiscard(), False)
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])

    elif vName == "Hela":
        sideDeck().visibility = "all"
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])

    elif vName == 'Loki':
        showGroup(specialDeck(), True)
        showGroup(specialDeckDiscard(), False)
        # If we loaded the encounter deck - add the first main scheme card to the table
        sorted(mainSchemeCards)[0].moveToTable(tableLocations['mainScheme'][0],tableLocations['mainScheme'][1])
        randomLoki = rnd(0, 4) # Returns a random INTEGER value and use it to choose which Loki will be loaded
        villainCards[randomLoki].moveToTable(villainX(1,0),tableLocations['villain'][1])

    elif vName == 'Sinister Six':
        for idx, c in enumerate(villainCards):
            c.moveToTable(villainX(6,idx),tableLocations['villain'][1])
        loop = 6 - (1 + len(players))
        while loop > 0:
            vCardsOnTable = filter(lambda card: card.Type == "villain" and card.alternate == "", table)
            randomVillain = rnd(0, len(vCardsOnTable) - 1)
            vCardsOnTable[randomVillain].alternate = "b"
            clearMarker(vCardsOnTable[randomVillain], x = 0, y = 0)
            loop -= 1

        # If we loaded the encounter deck - add the first main scheme card to the table
        sorted(mainSchemeCards)[0].moveToTable(tableLocations['mainSchemeCentered'][0]-100,tableLocations['villain'][1]+100)

    elif vName == 'Mansion Attack':
        # If we loaded the encounter deck - add the first main scheme card to the table
        sorted(mainSchemeCards)[0].moveToTable(tableLocations['mainScheme'][0],tableLocations['mainScheme'][1])
        randomVillain = rnd(0, 3) # Returns a random INTEGER value and use it to choose which Loki will be loaded
        villainCards[randomVillain].moveToTable(villainX(1,0),tableLocations['villain'][1])
        if gameDifficulty == "1":
            villainCards[randomVillain].alternate = "b"

    elif vName == "Magneto":
        sideDeck().visibility = "all"
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])

    elif vName == 'MaGog':
        # If we loaded the encounter deck - add the first main scheme card to the table
        sorted(mainSchemeCards)[0].moveToTable(tableLocations['mainScheme'][0],tableLocations['mainScheme'][1])
        randomVillain = rnd(0, 3) # Returns a random INTEGER value and use it to choose which Loki will be loaded
        villainCards[0].moveToTable(villainX(1,0),tableLocations['villain'][1])
        if gameDifficulty == "1":
            villainCards[0].alternate = "b"

    elif vName == "Spiral":
        recommendedEncounter(encounterDeck(), villainName='Spiral')
        showGroup(sideDeck(), False)
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])

    elif vName == "Mojo":
        recommendedEncounter(sideDeck(), villainName='Mojo')
        showGroup(sideDeck(), False)
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])

    elif vName == "Morlock Siege":
        villainDeck().visibility = "none"
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCard = villainDeck().random()
        villainCard.moveToTable(villainX(1, 0), tableLocations['villain'][1])
        envCard = revealCardOnSetup("Routed", "40081a", tableLocations['environment'][0], tableLocations['environment'][1])
        if gameDifficulty == "1":
            villainCard.alternate = "b"
            envCard.alternate = "b"

    elif vName == "On the Run":
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCard = villainDeck().random()
        villainCard.moveToTable(villainX(1, 0), tableLocations['villain'][1])
        envCard = revealCardOnSetup("Hope's Captor", "40105a", tableLocations['environment'][0], tableLocations['environment'][1])
        if gameDifficulty == "1":
            villainCard.alternate = "b"
        revealedVilName = villainCard.Name
        for c in encounterDeck():
            if c.Name == revealedVilName:
                c.moveTo(removedFromGameDeck())
        for c in villainDeck():
            c.moveTo(removedFromGameDeck())

    elif vName == "Juggernaut":
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        villainCards[0].markers[AllPurposeMarker] += 1
        tough(villainCards[0], 0, 0)
        revealCardOnSetup("Juggernaut's Helmet", "40122a", villainX(1, 0)-35, tableLocations['villain'][1]+5, isAttachment=True)
        revealCardOnSetup("Hope Summers", "40130", 0, 0, isAttachment=False, inSideDeck=True)

    elif vName == "Mister Sinister":
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        revealCardOnSetup("Hope Summers", "40130", 0, 0, isAttachment=False, inSideDeck=True)
        msCards = sorted(filter(lambda card: card.Type == "main_scheme" and card.Stage == "2", mainSchemeDeck()), key=lambda c: c.CardNumber)
        if len(msCards) > 0:
            randomScheme = rnd(0, len(msCards)-1)
            msCards[randomScheme].moveTo(removedFromGameDeck())

    elif vName == "Stryfe":
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        revealCardOnSetup("Hope Summers", "40130", 0, 0, isAttachment=False, inSideDeck=True)
        revealCardOnSetup("Stryfe's Grasp", "40168a", tableLocations['sideScheme'][0], tableLocations['sideScheme'][1])

    elif vName == "Four Horsemen":
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        loop = 4
        while loop > 0:
            villainCard = villainDeck().random()
            villainCard.moveToTable(villainX(4, loop-1), tableLocations['villain'][1])
            if gameDifficulty == "1":
                villainCard.alternate = "b"
            loop -= 1

        # If we loaded the encounter deck - add the first main scheme card to the table
        sorted(mainSchemeCards)[0].moveToTable(tableLocations['mainSchemeCentered'][0]-100,tableLocations['villain'][1]+100)

    elif vName == "Apocalypse":
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        if gameDifficulty == "0":
            villainCards[0].alternate = "b"        

    elif vName == "Batroc":
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        if gameDifficulty == "1":
            villainCards[0].alternate = "b"
        envCard = revealCardOnSetup("Alert Level", "50090a", tableLocations['environment'][0], tableLocations['environment'][1])
        if gameDifficulty == "1":
            envCard.markers[AllPurposeMarker] += 2 * len(players)
        sideDeck().visibility = "all"

    elif vName == "M.O.D.O.K.":
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        if gameDifficulty == "1":
            villainCards[0].alternate = "b"
        # Shuffle Holding Cell cards then put into play next to main scheme.
        shuffle(sideDeck())
        for c in sideDeck():
            c.moveToTable(tableLocations['mainScheme'][0]+100, tableLocations['mainScheme'][1])
        for c in encounterDeck():
            if c.Type == "environment" and c.Attribute.find("Adaptoid.") != -1:
                c.moveTo(sideDeck())
        shuffle(sideDeck())
        envCardCount = 0
        shift = 0
        while envCardCount <= int(gameDifficulty):
            envCard = sideDeck().top()
            envCard.moveToTable(tableLocations['environment'][0]+shift, tableLocations['environment'][1])
            shift -= 70
            envCardCount += 1

        # Adaptoid engaged with each player
        minionCard = filter(lambda card: card.CardNumber == "50113", encounterDeck())
        for i in range(0, len(getPlayers())):
            minionCard[i].moveToTable(playerX(i), 0)

    elif vName == "Thunderbolts":
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        if gameDifficulty == "1":
            villainCards[0].alternate = "b"
        envCard = revealCardOnSetup("Justice, Like Lightning", "50131a", tableLocations['environment'][0], tableLocations['environment'][1])
        envCard.alternate = "b"
        for c in encounterDeck():
            if c.Type == "minion" and c.Attribute.find("Elite.") != -1 and c.Attribute.find("Thunderbolt.") != -1:
                c.moveTo(sideDeck())
        shuffle(sideDeck())
        # Thunderbolt minion engaged with each player and the last one attached to environment
        for i in range(0, len(getPlayers())):
            minionCard = sideDeck().top()
            minionCard.moveToTable(playerX(i), 0)
            if gameDifficulty == "1":
                tough(minionCard, 0, 0)
        minionCard = sideDeck().top()
        minionCard.moveToTable(tableLocations['environment'][0]+15, tableLocations['environment'][1]+15)
        if gameDifficulty == "1":
            tough(minionCard, 0, 0)

    elif vName == "Baron Zemo":
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        execCard = revealCardOnSetup("Chief Medical Officer", "50181a", tableLocations['mainScheme'][0]+280, tableLocations['mainScheme'][1])
        execCard.markers[AllPurposeMarker] += 2
        execCard = revealCardOnSetup("Chief Surveillance Officer", "50182a", tableLocations['mainScheme'][0]+350, tableLocations['mainScheme'][1])
        execCard.markers[AllPurposeMarker] += 2
        execCard = revealCardOnSetup("Chief Tactical Officer", "50183a", tableLocations['mainScheme'][0]+420, tableLocations['mainScheme'][1])
        execCard.markers[AllPurposeMarker] += 2
        evidMeansCards = sorted(filter(lambda card: card.Type == "evidence_means", sideDeck()), key=lambda c: c.CardNumber)
        evidMotiveCards = sorted(filter(lambda card: card.Type == "evidence_motive", sideDeck()), key=lambda c: c.CardNumber)
        evidOppCards = sorted(filter(lambda card: card.Type == "evidence_opportunity", sideDeck()), key=lambda c: c.CardNumber)
        if len(evidMeansCards) > 0:
            cardRnd = rnd(0, len(evidMeansCards)-1)
            evidMeansCards[cardRnd].moveTo(shared.piles['Temporary'])
        if len(evidMotiveCards) > 0:
            cardRnd = rnd(0, len(evidMotiveCards)-1)
            evidMotiveCards[cardRnd].moveTo(shared.piles['Temporary'])
        if len(evidOppCards) > 0:
            cardRnd = rnd(0, len(evidOppCards)-1)
            evidOppCards[cardRnd].moveTo(shared.piles['Temporary'])
        shared.piles['Temporary'].visibility = "none"
        shared.piles['Temporary'].collapsed = False
        shuffle(sideDeck())

    elif vName == "God of Lies":
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        mainSchemeCards[1].moveToTable(tableLocations['mainScheme'][0] + 100, tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        for i in range(0, len(getPlayers())):
            vCards = sorted(filter(lambda card: card.Type == "villain", villainDeck()), key=lambda c: c.CardNumber)
            randomLoki = rnd(0, len(vCards)-1)
            vCards[randomLoki].moveToTable(playerX(i), -100)
        
        vCards = sorted(filter(lambda card: card.Type == "villain", villainDeck()), key=lambda c: c.CardNumber)
        for c in vCards:
            c.moveTo(sideDeck())
        
        # Put each Synergy cards into play.
        synergyCards = sorted(filter(lambda card: card.Attribute == "Synergy.", encounterDeck()), key=lambda c: c.CardNumber)
        synergyX = tableLocations['villain'][0] - 100
        synergyY = tableLocations['villain'][1]
        for c in synergyCards:
           synergyX = synergyX - 70
           c.moveToTable(synergyX, synergyY)
        
        # In standard mode, set the Intense Focus attachment aside. In expert mode, attach it to the [[Avatar of Loki]] villain in play
        if gameDifficulty == "1":
            revealCardOnSetup("Intense Focus", "55034a", tableLocations['villain'][0]-55, tableLocations['villain'][1]+15, True, True)
            vCardOnTable = sorted(filter(lambda card: card.Type == "villain" and card.Attribute == "Avatar of Loki.", table), reverse=True)
            for c in vCardOnTable:
                addMarker(c, 0, 0, 17 * len(getPlayers()))

    else:
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])

    update()
    shuffle(encounterDeck())
    SpecificVillainSetup(vName)

def villainSetup_fm(group=table, x = 0, y = 0):
    # Global Variables
    gameDifficulty = getGlobalVariable("difficulty")
    vName = getGlobalVariable("villainSetup")

    # Move cards from Villain Deck to Encounter and Scheme Decks
    villainCards = sorted(filter(lambda card: card.Type == "villain", villainDeck()), key=lambda c: c.CardNumber)
    mainSchemeCards = sorted(filter(lambda card: card.Type == "main_scheme", mainSchemeDeck()), key=lambda c: c.CardNumber)
    villainEnvCards = sorted(filter(lambda card: card.Type == "environment", encounterDeck()))
    villainAttCards = sorted(filter(lambda card: card.Type == "attachment", encounterDeck()))

    if vName == 'Celestial Messiah (By CptScorp)':
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        deadlyVineCards = filter(lambda card: card.Name == "Deadly Vines", sideDeck())
        for i in range(0, len(getPlayers())):
            deadlyVineCards[i].moveToTable(playerX(i), 0)

    elif vName == 'Fin Fang Foom (By Nugget)':
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[2].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        villainCards[0].moveToTable(villainX(1, 0)+11, tableLocations['villain'][1]+23)
        villainCards[1].moveToTable(villainX(1, 0)+17, tableLocations['villain'][1]+53)
        villainCards[3].moveToTable(villainX(1, 0)+14, tableLocations['villain'][1]+73)

    elif vName == "Graviton (By XB)":
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        envCard = filter(lambda card: card.Name == "Dark Matter", encounterDeck())
        envCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])
        ssCard = filter(lambda card: card.Name == "Seismic Uprising", encounterDeck())
        ssCard[0].moveToTable(tableLocations['mainScheme'][0] + 100, tableLocations['mainScheme'][1])

    elif vName == "Dragon's Madripoor (By Merlin)":
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        minionCards = filter(lambda card: card.Name == "Hand Soldier", encounterDeck())
        for i in range(0, len(getPlayers())):
            minionCards[i].moveToTable(playerX(i), 0)
 
    elif vName == "Killmonger (By JustATuna)":
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        envCards = filter(lambda card: card.Attribute == "Objective.", encounterDeck())
        for i in range(0, len(envCards)):
            envCards[i].moveToTable(-140 + 70 * i, -130)

    elif vName == "Minotaur (By Jammydude44)":
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        envCard = filter(lambda card: card.Name == "Roxxon Energy", sideDeck())
        envCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])
        showGroup(sideDeck(), True)
        update()
        ssCard = sideDeck().top()
        ssCard.moveToTable(tableLocations['mainScheme'][0] + 100, tableLocations['mainScheme'][1])

    elif vName == "Laufey (By Jammydude44)":
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        thorCard = filter(lambda card: card.Name == "Thor", sideDeck())
        thorCard[0].moveToTable(villainX(1, 0), tableLocations['villain'][1]+100)
        envCard = filter(lambda card: card.Name == "King of the Frost Giants", sideDeck())
        envCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])
        minionCards = filter(lambda card: card.Name == "Frost Giant Archer", encounterDeck())
        for i in range(0, len(getPlayers())):
            minionCards[i].moveToTable(playerX(i), 0)
        showGroup(sideDeck(), True)
        showGroup(sideDeckDiscard(), False)

    elif vName == "Malekith (By Jammydude44)":
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        ssCards = sorted(filter(lambda card: card.Type == "side_scheme", sideDeck()), key=lambda c: c.CardNumber)
        for idx, c in enumerate(ssCards):
            c.moveToTable(villainX(len(ssCards),idx)-15, tableLocations['villain'][1]+90)

    elif vName == "Mandarin (By Designhacker)":
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        envCard = filter(lambda card: card.Name == "E.M.P. Disruption", sideDeck())
        envCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])

    elif vName == "Mister Negative (By Andy)":
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        ssCard = filter(lambda card: card.Name == "Demons Unleashed", encounterDeck())
        ssCard[0].moveToTable(tableLocations['mainScheme'][0] + 100, tableLocations['mainScheme'][1])

    elif vName == "Purple Man (By Designhacker)":
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        envCard = filter(lambda card: card.Name == "Villains For Hire", sideDeck())
        envCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])

    elif vName == "The Zodiac (By TopBanana)":
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])
        showGroup(sideDeck(), True)

    else:
        # If we loaded the encounter deck - add the first villain and main scheme cards to the table
        mainSchemeCards[0].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])
        villainCards[0].moveToTable(villainX(1, 0), tableLocations['villain'][1])

    update()
    shuffle(encounterDeck())


#------------------------------------------------------------
# 'Load Villain' specific functions
#------------------------------------------------------------
#------------------------------------------------------------
# Specific Villain setup
#------------------------------------------------------------
def revealCardOnSetup(ssName, ssCardNumber, posX, posY, isAttachment=False, inSideDeck=False):
    if not inSideDeck:
        card = filter(lambda c: c.CardNumber == ssCardNumber, encounterAndDiscardDeck())
    else:
        card = filter(lambda c: c.CardNumber == ssCardNumber, sideDeck())
    if len(card) > 0:
        card[0].moveToTable(posX, posY)
        if isAttachment:
            card[0].sendToBack()
        return card[0]
    else:
        notify("{} card not found in encounter deck nor encounter discard!".format(ssName))

def SpecificVillainSetup(vName = ''):
    # Global Variables
    gameDifficulty = getGlobalVariable("difficulty")

    vCardOnTable = sorted(filter(lambda card: card.Type == "villain", table), reverse=True)
    msCardOnTable = sorted(filter(lambda card: card.Type == "main_scheme", table))
    villainEnvCards = sorted(filter(lambda card: card.Type == "environment", encounterDeck()))
    villainAttCards = sorted(filter(lambda card: card.Type == "attachment", encounterDeck()))
    vilX, vilY = vCardOnTable[0].position
    msX, msY = msCardOnTable[0].position
    ssX = msX + 100
    ssY = msY

    if vName == 'Rhino':
        if vCardOnTable[0].CardNumber == "01095": # Rhino II
            revealCardOnSetup("Breakin' & Takin'", "01107", ssX, ssY)


    if vName == 'Klaw':
        if msCardOnTable[0].CardNumber == "01116a": # Stage 1 main scheme
            revealCardOnSetup("Defense Network", "01125", ssX, ssY)

        if vCardOnTable[0].CardNumber == "01114": # Klaw II
            ssCard1_OnTable = filter(lambda card: card.CardNumber == "01125", table)
            # Check if Defense Network already on table to adapt card's position for 2nd side scheme
            if len(ssCard1_OnTable) > 0:
                ssX = ssCard1_OnTable[0].position[0] + 100
                ssY = ssCard1_OnTable[0].position[1]
            revealCardOnSetup("'Immortal' Klaw", "01127", ssX, ssY)
            if vCardOnTable[0].markers[HealthMarker] == 0:
                setHPOnCharacter(vCardOnTable[0])
            addMarker(vCardOnTable[0], 0, 0, qty = 10)


    if vName == 'Ultron':
        if msCardOnTable[0].CardNumber == "01137a": # Stage 1 main scheme
            revealCardOnSetup("Ultron Drones", "01140", tableLocations['environment'][0], tableLocations['environment'][1])
        if vCardOnTable[0].CardNumber == "01136": # Ultron III
            revealCardOnSetup("Ultron's Imperative'", "01150", ssX, ssY)


    if vName == 'Green Goblin: Risky Business':
        if msCardOnTable[0].CardNumber == "02004a": # Stage 1 main scheme
            c = revealCardOnSetup("Criminal Enterprise", "02006a", tableLocations['environment'][0], tableLocations['environment'][1])
            addMarker(c, 0, 0, qty = 2 * len(getPlayers()))


    if vName == 'Green Goblin: Mutagen Formula':
        if msCardOnTable[0].CardNumber == "02017a": # Stage 1 main scheme
            minionCard = filter(lambda card: card.CardNumber == "02024", encounterDeck()) # Goblin Thrall minion
            for i in range(0, len(getPlayers())):
                minionCard[i].moveToTable(playerX(i), 0)


    if vName == 'Absorbing Man':
        if vCardOnTable[0].CardNumber == "04077": # Absorbing Man II
            revealCardOnSetup("Super Absorbing Power", "04092", ssX, ssY)


    if vName == 'Crossbones':
        if vCardOnTable[0].CardNumber == "04059": # Crossbones II
            revealCardOnSetup("Crossbones' Machine Gun", "04064", vilX-35, vilY+5, isAttachment=True)


    if vName == 'Taskmaster':
        if msCardOnTable[0].CardNumber == "04096a": # Stage 1 main scheme
            revealCardOnSetup("Hydra Patrol", "04154", ssX, ssY)


    if vName == 'Zola':
        if msCardOnTable[0].CardNumber == "04112a": # Stage 1 main scheme
            revealCardOnSetup("Hydra Prison", "04122", ssX, ssY)

            # Ultimate Bio-Servant minion engaged with each player
            minionCard = filter(lambda card: card.CardNumber == "04114", encounterDeck())
            for i in range(0, len(getPlayers())):
                minionCard[i].moveToTable(playerX(i), 0)

        if vCardOnTable[0].CardNumber == "04110": # Zola II
            ssCard1_OnTable = filter(lambda card: card.CardNumber == "04122", table)
            # Check if Hydra Prison already on table to adapt card's position for 2nd side scheme
            if len(ssCard1_OnTable) > 0:
                ssX = ssCard1_OnTable[0].position[0] + 100
                ssY = ssCard1_OnTable[0].position[1]
            revealCardOnSetup("Test Subjects", "04123", ssX, ssY)


    if vName == 'Red Skull':
        ssCard = filter(lambda card: card.CardNumber == "04139", sideDeck()) # The Red House side scheme
        if msCardOnTable[0].CardNumber == "04128a" and len(ssCard) > 0: # Stage 1 main scheme
            ssCard[0].moveToTable(ssX, ssY)


    if vName == 'Drang':
        if msCardOnTable[0].CardNumber == "16061a": # Stage 1 main scheme
            revealCardOnSetup("Badoon Ship", "16063", tableLocations['environment'][0], tableLocations['environment'][1])
            revealCardOnSetup("Milano", "16142", playerX(0), 0) # Give Milano to 1st player

        if vCardOnTable[0].CardNumber == "16059": # Drang II
            revealCardOnSetup("Drang's Spear", "16064", vilX-20, vilY+5, isAttachment=True)


    if vName == 'Collector 2':
        if msCardOnTable[0].CardNumber == "16082a": # Stage 1 main scheme
            revealCardOnSetup("Library Labyrinth", "16085a", tableLocations['environment'][0], tableLocations['environment'][1])


    if vName == 'Nebula':
        if msCardOnTable[0].CardNumber == "16091a": # Stage 1 main scheme
            revealCardOnSetup("Nebula's Ship", "16093", tableLocations['environment'][0], tableLocations['environment'][1])
            revealCardOnSetup("Milano", "16142", playerX(0), 0) # Give Milano to 1st player
            revealCardOnSetup("Power Stone", "16149", vilX-20, vilY+10, isAttachment=True)


    if vName == 'Ronan':
        if msCardOnTable[0].CardNumber == "16106a": # Stage 1 main scheme
            revealCardOnSetup("Kree Command Ship", "16108", tableLocations['environment'][0] - 20, tableLocations['environment'][1])
            revealCardOnSetup("Milano", "16142", playerX(0), 0) # Give Milano to 1st player
            revealCardOnSetup("Universal Weapon", "16109", vilX-25, vilY+5, isAttachment=True)
            revealCardOnSetup("Power Stone", "16149", playerX(0) - 20, tableLocations['hero'][1]+5, isAttachment=True) # Attach Power Stone to 1st player

        if vCardOnTable[0].CardNumber == "16104": # Ronan II
            revealCardOnSetup("Cut the Power", "16111", ssX, ssY)

        if vCardOnTable[0].CardNumber == "16105": # Ronan III
            ssCard1_OnTable = filter(lambda card: card.CardNumber == "16111", table)
            # Check if 'Cut the Power' already on table to adapt card's position for 2nd side scheme
            if len(ssCard1_OnTable) > 0:
                ssX = ssCard1_OnTable[0].position[0] + 100
                ssY = ssCard1_OnTable[0].position[1]
            revealCardOnSetup("Superior Tactics", "16113", ssX, ssY)


    if vName == 'Tower Defense':
        if msCardOnTable[0].CardNumber == "21098a" or msCardOnTable[1].CardNumber == "21099a": # Stage 1 main scheme
            minionCard = filter(lambda card: card.CardNumber == "21102", encounterDeck()) # Black Order Besieger
            for i in range(0, len(getPlayers())):
                minionCard[i].moveToTable(playerX(i), 0)


    if vName == 'Thanos':
        if msCardOnTable[0].CardNumber == "21114a": # Stage 1 main scheme
            infinityCard = sorted(filter(lambda card: card.CardNumber == "21129", specialDeck())) # Infinity Gauntlet attachment
            infinityCard[0].moveToTable(tableLocations['environment'][0]-20, tableLocations['environment'][1])
            revealCardOnSetup("Sanctuary", "21116", ssX, ssY)

        if vCardOnTable[0].CardNumber == "21112": # Thanos II
            revealCardOnSetup("Thanos's Helmet", "21118", vilX-15, vilY+5, isAttachment=True)

        if vCardOnTable[0].CardNumber == "21113": # Thanos III
            revealCardOnSetup("Thanos's Armor", "21117", vilX-30, vilY+10, isAttachment=True)


    if vName == 'Hela':
        if msCardOnTable[0].CardNumber == "21138a": # Stage 1 main scheme
            odinCard = filter(lambda card: card.CardNumber == "21139a", sideDeck()) # Odin ally captive side
            odinCard[0].moveToTable(msX - 15, msY - 15)
            odinCard[0].sendToBack()
            ssCard = filter(lambda card: card.CardNumber == "21140", sideDeck()) # Gnipahellir side scheme
            ssCard[0].moveToTable(ssX, ssY)
            garmCard = filter(lambda card: card.CardNumber == "21143", sideDeck()) # Garm (minion)
            garmCard[0].moveToTable(playerX(0), 0) # Engage with 1st player


    if vName == 'Loki':
        if msCardOnTable[0].CardNumber == "21165a": # Stage 1 main scheme
            infinityCard = sorted(filter(lambda card: card.CardNumber == "21129", specialDeck())) # Infinity Gauntlet attachment
            infinityCard[0].moveToTable(tableLocations['environment'][0]-20, tableLocations['environment'][1])
            revealCardOnSetup("War in Asgard", "21167", ssX, ssY)


    if vName == 'Sandman':
        if msCardOnTable[0].CardNumber == "27064a": # Stage 1 main scheme
            c = revealCardOnSetup("City Streets", "27065", tableLocations['environment'][0], tableLocations['environment'][1])
            addMarker(c, 0, 0, 4)


    if vName == 'Venom':
        if msCardOnTable[0].CardNumber == "27076a": # Stage 1 main scheme
            revealCardOnSetup("Bell Tower", "27077a", tableLocations['environment'][0], tableLocations['environment'][1])

        if vCardOnTable[0].CardNumber == "27074": # Venom II
            revealCardOnSetup("Tooth and Nail", "27081", ssX, ssY)


    if vName == 'Mysterio':
        if msCardOnTable[0].CardNumber == "27087a": # Stage 1 main scheme
            minionCard = filter(lambda card: card.CardNumber == "27091", encounterDeck()) # Shifting Apparition minion
            for i in range(0, len(getPlayers())):
                minionCard[i].moveToTable(playerX(i), 0)

            if vCardOnTable[0].CardNumber == "27085": # Mysterio II
                for p in getPlayers():
                    first_encounter_card = encounterDeck()[0]
                    first_encounter_card.moveTo(p.Deck)

                    # If players have been loaded before Villain: reset their hand and draw again
                    if len(p.piles['Hand']) > 0:
                        notify("{} cards already in {}'s hand - Shuffle back into deck and draw a new hand (Mysterio II setup)".format(len(p.piles['Hand']), me.name))
                        for c in p.piles['Hand']:
                            c.moveTo(p.Deck)
                            shuffle(p.Deck)
                        drawMany(p.deck, maxHandSize(p), True)
                notifyBar("#0000FF", "Mysterio II: first encounter card has been shuffled into players deck!")


    if vName == 'Sinister Six':
        if msCardOnTable[0].CardNumber == "27100a": # Stage 1 main scheme
            revealCardOnSetup("Light at the End", "27102a", tableLocations['mainSchemeCentered'][0]+100, tableLocations['villain'][1]+100)


    if vName == 'Venom Goblin':
        if msCardOnTable[0].CardNumber == "27116a": # Stage 1 main scheme
            msCards = filter(lambda card: card.Type == "main_scheme", mainSchemeDeck())
            for idx, c in enumerate(msCards):
                c.moveToTable(villainX(3, idx), tableLocations['villain'][1]+100)


    if vName == 'Sabretooth':
        if msCardOnTable[0].CardNumber == "32063a": # Stage 1 main scheme
            revealCardOnSetup("Robert Kelly", "32066", ssX, ssY)
            revealCardOnSetup("Find the Senator", "32065a", ssX, ssY)


    if vName == 'Project Wideawake':
        if msCardOnTable[0].CardNumber == "32087a": # Stage 1 main scheme
            revealCardOnSetup("Operation Zero Tolerance", "32104", ssX, ssY)
            revealCardOnSetup("Mutants at the Mall", "32088a", ssX+100, ssY)


    if vName == 'Master Mold':
        if msCardOnTable[0].CardNumber == "32112a": # Stage 1 main scheme
            magnetoAlly = table.create("47d34c5d-5319-45a9-a2d6-1fb975032172", 0, 0, 1, True)
            magnetoAlly.alternate = "b"


    if vName == 'Mansion Attack':
        if msCardOnTable[0].CardNumber == "32125a": # Stage 1 main scheme
            revealCardOnSetup("Save The School", "32130", tableLocations['environment'][0], tableLocations['environment'][1])


    if vName == 'Magneto':
        if msCardOnTable[0].CardNumber == "32141a": # Stage 1 main scheme
            revealCardOnSetup("Operation Zero Tolerance", "32144a", ssX, ssY)


    if vName == 'MaGog':
        if msCardOnTable[0].CardNumber == "39002a": # Stage 1 main scheme
            revealCardOnSetup("The Champion (Booing Crowd)", "39003a", tableLocations['environment'][0] - 70, tableLocations['environment'][1])
            revealCardOnSetup("The Challengers (Booing Crowd)", "39004a", tableLocations['environment'][0], tableLocations['environment'][1])


    if vName == 'Spiral':
        if msCardOnTable[0].CardNumber == "39015a": # Stage 1 main scheme
            revealCardOnSetup("The Search for Spiral", "39016", ssX, ssY)
            envCards = [c for c in encounterDeck() if (c.Type == "environment" and lookForAttribute(c, "Show"))]
            for c in envCards:
                c.moveTo(sideDeck())
            rndCard = sideDeck().random()
            rndCard.moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])
            corneredCard = [c for c in encounterDeck() if (c.CardNumber == "39017")]
            corneredCard[0].moveTo(sideDeck())
            update()
            sideDeck().shuffle


    if vName == 'Mojo':
        if msCardOnTable[0].CardNumber == "39025a": # Stage 1 main scheme
            revealCardOnSetup("Wheel of Genres (Spinning)", "39026a", tableLocations['environment'][0], tableLocations['environment'][1])


    if vName == 'Unus':
        if msCardOnTable[0].CardNumber == "45062a": # Stage 1 main scheme
            revealCardOnSetup("Gene Pool", "45071", ssX, ssY)


    if vName == 'Four Horsemen':
        if msCardOnTable[0].CardNumber == "45085a": # Stage 1 main scheme
            loop = len(getPlayers())
            while loop > 0:
                ssCards = sorted(filter(lambda card: card.Type == "side_scheme" and card.Owner == "four_horsemen", encounterDeck()), key=lambda c: c.CardNumber)
                randomScheme = rnd(0, len(ssCards)-1)
                ssCards[randomScheme].moveToTable(tableLocations['mainSchemeCentered'][0]+80*loop, tableLocations['villain'][1]+100)
                loop -= 1


    if vName == 'Apocalypse':
        if msCardOnTable[0].CardNumber == "45103a": # Stage 1 main scheme
            revealCardOnSetup("Heart of the Empire", "45104a", ssX, ssY, inSideDeck=True)
            # The first player reveals a random, set-aside [[Prelate]] minion
            minionCards = filter(lambda card: card.Type == "minion", sideDeck())
            randomMinion = rnd(0, len(minionCards)-1)
            minionCards[randomMinion].moveToTable(playerX(0), 0)
            minionCards[randomMinion].alternate = "b"


    if vName == 'Dark Beast':
        if msCardOnTable[0].CardNumber == "45121a" and gameDifficulty == "1": # Stage 1 main scheme
            revealCardOnSetup("High-Tech Goggles", "45122", vilX-15, vilY+5, isAttachment=True)
        for c in table:
            if c.Type == 'environment' and lookForAttribute(c, "Setting."):
                c.moveTo(encounterDiscardDeck())
        shuffleSetIntoEncounter(sideDeck(), x = 0, y = 0, random = True)


    if vName == 'Enchantress':
        if msCardOnTable[0].CardNumber == "55004a": # Stage 1 main scheme
            # Hypnotic Gaze attached to each player
            for i in range(0, len(getPlayers())):
                attCards = filter(lambda card: card.Type == "attachment", sideDeck())
                rndCard = rnd(0, len(attCards)-1)
                attCards[rndCard].moveToTable(playerX(i), -70)

        if vCardOnTable[0].CardNumber == "55002" and gameDifficulty == "0": # Enchantress II
            c = revealCardOnSetup("Future of Despair", "55006", ssX, ssY, False, True)
            addMarker(c, 0, 0, 5 * len(getPlayers()))

        if vCardOnTable[0].CardNumber == "55003" and gameDifficulty == "1": # Enchantress II
            c = revealCardOnSetup("Future of Despair", "55006", ssX, ssY, False, True)
            addMarker(c, 0, 0, 6 * len(getPlayers()))