#------------------------------------------------------------
# 'Load Villain' event
#------------------------------------------------------------

def loadVillain(group, x = 0, y = 0):
    mute()
    villainName = ''
    nbModular = 1
    nbVillain = 1

    if not deckNotLoaded(group,0,0,shared.villain):
        confirm("Cannot generate a deck: You already have cards loaded. Reset the game in order to generate a new deck.")
        return

    villainList = ["Rhino", "Klaw", "Ultron", "Green Goblin: Mutagen Formula", "Green Goblin: Risky Business", "The Wrecking Crew", "Baron Zemo: Firestarter (By: FelixFactory)", "Crossbones", "Absorbing Man", "Taskmaster", "Zola", "Red Skull", "Kang", "Drang", "Collector 1", "Collector 2", "Nebula", "Ronan", "Ebony Maw", "Tower Defense", "Thanos", "Hela", "Loki"]
    choice = askChoice("Which villain would you like to defeat?", villainList)
    passSharedControl(group)
    update()
    if choice == 0: return

    if choice == 1:
        createCards(shared.villain,sorted(rhino.keys()),rhino)

    if choice == 2:
        createCards(shared.villain,sorted(klaw.keys()),klaw)

    if choice == 3:
        createCards(shared.villain,sorted(ultron.keys()),ultron)

    if choice == 4:
        createCards(shared.villain,sorted(mutagen_formula.keys()),mutagen_formula)

    if choice == 5:
        createCards(shared.villain,sorted(risky_business.keys()),risky_business)

    if choice == 6:
        createCards(shared.villain,sorted(the_wrecking_crew.keys()),the_wrecking_crew)
        nbModular = 0

    if choice == 7:
        createCards(shared.villain,sorted(baron_zemo_firestarter.keys()),baron_zemo_firestarter)
        createCards(shared.villain,sorted(baron_zemo_firestarter_modules.keys()),baron_zemo_firestarter_modules)
        createCards(shared.villain,sorted(legions_of_hydra.keys()),legions_of_hydra)
        createCards(shared.villain,sorted(bomb_scare.keys()),bomb_scare)

    if choice == 8:
        createCards(shared.villain,sorted(crossbones.keys()),crossbones)
        createCards(shared.special,sorted(exper_weapon.keys()),exper_weapon)
        shared.piles['Special'].collapsed = False
        createCards(shared.campaign,sorted(trors_campaign.keys()),trors_campaign)
        nbModular = 3

    if choice == 9:
        createCards(shared.villain,sorted(absorbing_man.keys()),absorbing_man)
        createCards(shared.campaign,sorted(trors_campaign.keys()),trors_campaign)

    if choice == 10:
        createCards(shared.villain,sorted(taskmaster.keys()),taskmaster)
        createCards(shared.villain,sorted(hydra_patrol.keys()),hydra_patrol)
        createCards(shared.campaign,sorted(trors_campaign.keys()),trors_campaign)
        for c in filter(lambda card: card.Type == "ally", villainDeck()):
            c.moveTo(specialDeck())
        shared.Special.shuffle()
        shared.piles['Special'].collapsed = False

    if choice == 11:
        createCards(shared.villain,sorted(zola.keys()),zola)
        createCards(shared.campaign,sorted(trors_campaign.keys()),trors_campaign)

    if choice == 12:
        createCards(shared.villain,sorted(red_skull.keys()),red_skull)
        createCards(shared.campaign,sorted(trors_campaign.keys()),trors_campaign)
        for c in filter(lambda card: card.Type == "side_scheme", villainDeck()):
            c.moveTo(specialDeck())
        shared.Special.shuffle()
        shared.piles['Special'].collapsed = False
        shared.piles['Special Discard'].collapsed = False
        for c in filter(lambda card: card.CardNumber == "04130", villainDeck()):
            c.moveTo(removedFromGameDeck())
        shared.piles['Removed'].collapsed = False
        nbModular = 2

    if choice == 13:
        createCards(shared.villain,sorted(the_once_and_future_kang.keys()),the_once_and_future_kang)
        for c in filter(lambda card: card.CardNumber == "11023", villainDeck()):
            c.moveTo(removedFromGameDeck())
        shared.piles['Removed'].collapsed = False

    if choice == 14:
        createCards(shared.villain,sorted(brotherhood_of_badoon.keys()),brotherhood_of_badoon)
        createCards(shared.villain,sorted(ship_command.keys()),ship_command)
        for c in filter(lambda card: card.CardNumber == "16142", encounterDeck()):
            c.moveToTable(0, 0)
        createCards(shared.campaign,sorted(gmw_campaign_market.keys()),gmw_campaign_market)
        createCards(shared.campaign,sorted(gmw_campaign_challenge.keys()),gmw_campaign_challenge)

    if choice == 15:
        createCards(shared.villain,sorted(collector1.keys()),collector1)
        createCards(shared.villain,sorted(galactic_artifacts.keys()),galactic_artifacts)
        createCards(shared.campaign,sorted(gmw_campaign_market.keys()),gmw_campaign_market)
        createCards(shared.campaign,sorted(gmw_campaign_challenge.keys()),gmw_campaign_challenge)

    if choice == 16:
        createCards(shared.villain,sorted(collector2.keys()),collector2)
        createCards(shared.villain,sorted(galactic_artifacts.keys()),galactic_artifacts)
        createCards(shared.special,sorted(ship_command.keys()),ship_command)
        shared.piles['Special'].collapsed = False
        createCards(shared.campaign,sorted(gmw_campaign_market.keys()),gmw_campaign_market)
        createCards(shared.campaign,sorted(gmw_campaign_challenge.keys()),gmw_campaign_challenge)

    if choice == 17:
        createCards(shared.villain,sorted(nebula.keys()),nebula)
        createCards(shared.villain,sorted(power_stone.keys()),power_stone)
        for c in filter(lambda card: card.CardNumber == "16149", villainDeck()):
            c.moveToTable(0, 0)
        createCards(shared.villain,sorted(ship_command.keys()),ship_command)
        for c in filter(lambda card: card.CardNumber == "16142", villainDeck()):
            c.moveToTable(20, 20)
        createCards(shared.campaign,sorted(gmw_campaign_market.keys()),gmw_campaign_market)
        createCards(shared.campaign,sorted(gmw_campaign_challenge.keys()),gmw_campaign_challenge)

    if choice == 18:
        createCards(shared.villain,sorted(ronan.keys()),ronan)
        createCards(shared.villain,sorted(power_stone.keys()),power_stone)
        for c in filter(lambda card: card.CardNumber == "16149", villainDeck()):
            c.moveToTable(0, 0)
        createCards(shared.villain,sorted(ship_command.keys()),ship_command)
        for c in filter(lambda card: card.CardNumber == "16142", villainDeck()):
            c.moveToTable(20, 20)
        createCards(shared.campaign,sorted(gmw_campaign_market.keys()),gmw_campaign_market)
        createCards(shared.campaign,sorted(gmw_campaign_challenge.keys()),gmw_campaign_challenge)

    if choice == 19:
        createCards(shared.villain,sorted(ebony_maw.keys()),ebony_maw)
        createCards(shared.campaign,sorted(mts_campaign.keys()),mts_campaign)
        nbModular = 2

    if choice == 20:
        createCards(shared.villain,sorted(tower_defense.keys()),tower_defense)
        createCards(shared.campaign,sorted(mts_campaign.keys()),mts_campaign)

    if choice == 21:
        createCards(shared.villain,sorted(thanos.keys()),thanos)
        createCards(shared.piles['Special'],sorted(infinity_gauntlet.keys()),infinity_gauntlet)
        shared.Special.shuffle()
        shared.piles['Special'].collapsed = False
        shared.piles['Special Discard'].collapsed = False
        createCards(shared.campaign,sorted(mts_campaign.keys()),mts_campaign)
        nbModular = 2

    if choice == 22:
        createCards(shared.villain,sorted(hela.keys()),hela)
        createCards(shared.piles['Removed'],sorted(hela_setup.keys()),hela_setup)
        createCards(shared.campaign,sorted(mts_campaign.keys()),mts_campaign)
        nbModular = 2

    if choice == 23:
        createCards(shared.villain,sorted(loki.keys()),loki)
        shared.piles['Villain'].collapsed = False
        createCards(shared.piles['Special'],sorted(infinity_gauntlet.keys()),infinity_gauntlet)
        shared.Special.shuffle()
        shared.piles['Special'].collapsed = False
        shared.piles['Special Discard'].collapsed = False
        createCards(shared.campaign,sorted(mts_campaign.keys()),mts_campaign)
        nbModular = 2


    villainName = villainList[choice-1]
    setGlobalVariable("villainSetup",str(villainName))
    update()
    loadDifficulty()
    loadEncounter(shared.encounter, nbEncounter = nbModular)
    notify('{} loaded {}, Good Luck!'.format(me, villainName))
    tableSetup(doPlayer=False,doEncounter=True)


def loadDifficulty():
    vName = getGlobalVariable("villainSetup")
    choice = askChoice("What difficulty would you like to play at?", ["Standard", "Expert"])

    if vName == 'The Wrecking Crew':
        if choice == 0: return
        if choice == 1: return
        if choice == 2:
            setGlobalVariable("difficulty", "1")
            return

    else:
        if choice == 0: return
        if choice == 1:
            createCards(shared.encounter,sorted(standard.keys()),standard)
        if choice == 2:
            createCards(shared.encounter,sorted(standard.keys()),standard)
            createCards(shared.encounter,sorted(expert.keys()),expert)
            setGlobalVariable("difficulty", "1")



def villainSetup(group=table, x = 0, y = 0):
    # Global Variables
    gameDifficulty = getGlobalVariable("difficulty")
    vName = getGlobalVariable("villainSetup")

    # Move cards from Villain Deck to Encounter and Scheme Decks
    encounterDeckCards = filter(lambda card: card.Type != "villain" and card.Type != "main_scheme", villainDeck())
    mainSchemeCards = filter(lambda card: card.Type == "main_scheme", villainDeck())
    villainCards = filter(lambda card: card.Type == "villain", villainDeck())

    for c in encounterDeckCards:
        c.moveTo(encounterDeck())
    for c in mainSchemeCards:
        c.moveTo(mainSchemeDeck())

    villainCards = sorted(villainCards)
    villainEnvCards = sorted(filter(lambda card: card.Type == "environment", encounterDeck()))
    villainAttCards = sorted(filter(lambda card: card.Type == "attachment", encounterDeck()))

    if vName == 'The Wrecking Crew':
        # If we loaded the encounter deck - add the first main scheme card to the table
        sorted(mainSchemeCards)[0].moveToTable(tableLocations['mainSchemeCentered'][0],tableLocations['mainSchemeCentered'][1])
        sorted(mainSchemeCards)[0].anchor = False
        sorted(mainSchemeCards).pop(0)
        if gameDifficulty == "1":
            vCards = villainCards[1::2]
        else:
            vCards = villainCards[::2]
        for idx, c in enumerate(vCards):
            c.moveToTable(villainX(4,idx),tableLocations['villain'][1])
            if idx == 0:
                c.highlight = ActiveColour
        ssCards = filter(lambda card: card.Type == "side_scheme", encounterDeck())
        for idx, c in enumerate(sorted(ssCards)):
            c.moveToTable(villainX(4,idx)-10,tableLocations['villain'][1]+100)

    elif vName == 'Kang':
        sorted(mainSchemeCards)[0].moveToTable(tableLocations['mainScheme'][0],tableLocations['mainScheme'][1])
        sorted(mainSchemeCards)[0].anchor = False
        sorted(mainSchemeCards).pop(0)
        loop = 6
        if gameDifficulty == "1":
            while loop > 0:
                villainCards[0].delete()
                villainCards.pop(0)
                loop -= 1
        else:
            while loop > 0:
                villainCards[6].delete()
                villainCards.pop(6)
                loop -= 1
        villainCards = villainCards[0:6]
        villainCards[0].moveToTable(villainX(1,0),tableLocations['villain'][1])
        villainCards[0].anchor = False

    elif vName == 'Tower Defense':
        if gameDifficulty == "1":
            villainCards[3].delete()
            villainCards.pop(3)
            villainCards[0].delete()
            villainCards.pop(0)
        else:
            villainCards[5].delete()
            villainCards.pop(5)
            villainCards[2].delete()
            villainCards.pop(2)
        vCardsProxima = villainCards[0:2]
        vCardsCorvus = villainCards[2:]
        vCardsProxima[0].moveToTable(villainX(2,0),tableLocations['villain'][1])
        vCardsCorvus[0].moveToTable(villainX(2,1),tableLocations['villain'][1])
        villainEnvCards[0].moveToTable(villainX(1,0),tableLocations['villain'][1])
        villainAttCards[0].moveToTable(villainX(2,1)-90,tableLocations['villain'][1]+75)

        for idx, c in enumerate(sorted(mainSchemeCards)):
            c.moveToTable(villainX(2,idx)-10,tableLocations['villain'][1]+100)

    elif vName == 'Loki':
        # If we loaded the encounter deck - add the first main scheme card to the table
        sorted(mainSchemeCards)[0].moveToTable(tableLocations['mainScheme'][0],tableLocations['mainScheme'][1])
        sorted(mainSchemeCards)[0].anchor = False
        sorted(mainSchemeCards).pop(0)
        randomLoki = rnd(0, 4) # Returns a random INTEGER value and use it to choose which Loki will be loaded
        villainCards[randomLoki].moveToTable(villainX(1,0),tableLocations['villain'][1])
        villainCards[randomLoki].anchor = False

    else:
        # If we loaded the encounter deck - add the first main scheme card to the table
        sorted(mainSchemeCards)[0].moveToTable(tableLocations['mainScheme'][0],tableLocations['mainScheme'][1])
        sorted(mainSchemeCards)[0].anchor = False
        sorted(mainSchemeCards).pop(0)
        # If we loaded the encounter deck - add the villain(s) card(s) to the table
        if gameDifficulty == "1":
            villainCards[0].delete()
            villainCards.pop(0)
        else:
            villainCards[len(villainCards) - 1].delete()
            villainCards.pop(len(villainCards) - 1)
        villainCards[0].moveToTable(villainX(1,0),tableLocations['villain'][1])
        villainCards[0].anchor = False


    shared.counters["HP"].value = int(villainCards[0].properties["HP"]) * len(players)
    shared.encounter.shuffle()

    SpecificVillainSetup(vName)



#------------------------------------------------------------
# 'Load Villain' specific functions
#------------------------------------------------------------
#------------------------------------------------------------
# Specific Villain setup
#------------------------------------------------------------

def SpecificVillainSetup(vName = ''):

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
            ssCard = filter(lambda card: card.CardNumber == "01107", encounterDeck()) # Breakin' & Takin' side scheme 
            if len(ssCard) == 0:
                ssCard = filter(lambda card: card.CardNumber == "01107", encounterDiscardDeck())
            ssCard[0].moveToTable(ssX, ssY)


    if vName == 'Klaw':
        ssCard1 = filter(lambda card: card.CardNumber == "01125", encounterDeck()) # Defense Network side scheme
        ssCard2 = filter(lambda card: card.CardNumber == "01127", encounterDeck()) # The "Immortal" Klaw side scheme

        if msCardOnTable[0].CardNumber == "01116a" and len(ssCard1) > 0: # Stage 1 main scheme
            ssCard1[0].moveToTable(ssX, ssY)

        if vCardOnTable[0].CardNumber == "01114": # Klaw II
            ssCard1_OnTable = filter(lambda card: card.CardNumber == "01125", table)
            if len(ssCard2) == 0:
                ssCard2 = filter(lambda card: card.CardNumber == "01127", encounterDiscardDeck())
            if len(ssCard1_OnTable) == 0:
                ssCard2[0].moveToTable(ssX, ssY)
            if len(ssCard1_OnTable) > 0:
                ssCard2[0].moveToTable(ssCard1_OnTable[0].position[0] + 100, ssCard1_OnTable[0].position[1])


    if vName == 'Ultron':
        EnvCard = sorted(filter(lambda card: card.CardNumber == "01140", encounterDeck())) # Ultron Drone environment
        if msCardOnTable[0].CardNumber == "01137a" and len(EnvCard) > 0: # Stage 1 main scheme
            EnvCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])

        if vCardOnTable[0].CardNumber == "01136": # Ultron III
            ssCard = filter(lambda card: card.CardNumber == "01150", encounterDeck()) # Ultron's Imperative side scheme
            if len(ssCard) == 0:
                ssCard = filter(lambda card: card.CardNumber == "01150", encounterDiscardDeck())
            ssCard[0].moveToTable(ssX, ssY)


    if vName == 'Risky Business':
        EnvCard = sorted(filter(lambda card: card.CardNumber == "02006a", encounterDeck())) # Criminal Enterprise environment
        if msCardOnTable[0].CardNumber == "02004a" and len(EnvCard) > 0: # Stage 1 main scheme
            EnvCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])


    if vName == 'Baron Zemo: Firestarter':
        EnvCard = sorted(filter(lambda card: card.CardNumber == "91006", encounterDeck())) # environement card
        if msCardOnTable[0].CardNumber == "91004a" and len(EnvCard) > 0: # Stage 1 main scheme
            EnvCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])
            ssCard = filter(lambda card: card.CardNumber == "01109", encounterDeck()) # Bomb Scare side scheme
            ssCard[0].moveToTable(ssX, ssY)
            minionCard = filter(lambda card: card.CardNumber == "01182", encounterDeck()) # Hydra Soldier minion
            minionCard[0].moveToTable(tableLocations['environment'][0] - 90, tableLocations['environment'][1])


    if vName == 'Crossbones':
        if vCardOnTable[0].CardNumber == "04059": # Crossbones II
            AttachmentCard = filter(lambda card: card.CardNumber == "04064", encounterDeck()) # Crossbones' Machine Gun attachment
            if len(AttachmentCard) == 0:
                AttachmentCard = filter(lambda card: card.CardNumber == "04064", encounterDiscardDeck())
            AttachmentCard[0].moveToTable(vilX-25, vilY+5)
            AttachmentCard[0].sendToBack()


    if vName == 'Taskmaster':
        if msCardOnTable[0].CardNumber == "04096a": # Stage 1 main scheme
            ssCard = filter(lambda card: card.CardNumber == "04154", encounterDeck()) # Hydra Patrol side scheme
            if len(ssCard) == 0:
                ssCard = filter(lambda card: card.CardNumber == "04154", encounterDiscardDeck())
            ssCard[0].moveToTable(ssX, ssY)


    if vName == 'Zola':
        ssCard1 = filter(lambda card: card.CardNumber == "04122", encounterDeck()) # Hydra Prison side scheme
        ssCard2 = filter(lambda card: card.CardNumber == "04123", encounterDiscardDeck()) # Test Subject side scheme
        minionCard = filter(lambda card: card.CardNumber == "04114", encounterDeck()) # Ultimate Bio-Servant minion

        if msCardOnTable[0].CardNumber == "04112a" and len(ssCard1) > 0: # Stage 1 main scheme
            ssCard1[0].moveToTable(ssX, ssY)
            minionCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])

        if vCardOnTable[0].CardNumber == "04110": # Zola II
            ssCard1_OnTable = filter(lambda card: card.CardNumber == "04122", table)
            if len(ssCard2) == 0:
                ssCard2 = filter(lambda card: card.CardNumber == "04123", encounterDeck())
            if len(ssCard1_OnTable) == 0:
                ssCard2[0].moveToTable(ssX, ssY)
            if len(ssCard1_OnTable) > 0:
                ssCard2[0].moveToTable(ssCard1_OnTable[0].position[0]+100, ssCard1_OnTable[0].position[1])


    if vName == 'Red Skull':
        ssCard = filter(lambda card: card.CardNumber == "04139", specialDeck()) # The Red House side scheme

        if msCardOnTable[0].CardNumber == "04128a" and len(ssCard) > 0: # Stage 1 main scheme
            ssCard[0].moveToTable(ssX, ssY)


    if vName == 'Drang':
        EnvCard = sorted(filter(lambda card: card.CardNumber == "16063", encounterDeck())) # Badoon Ship environment
        if msCardOnTable[0].CardNumber == "16061a" and len(EnvCard) > 0: # Stage 1 main scheme
            EnvCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])


    if vName == 'Collector 2':
        EnvCard = sorted(filter(lambda card: card.CardNumber == "16085a", encounterDeck())) # Library Labyrinth environment
        if msCardOnTable[0].CardNumber == "16082a" and len(EnvCard) > 0: # Stage 1 main scheme
            EnvCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])


    if vName == 'Nebula':
        EnvCard = sorted(filter(lambda card: card.CardNumber == "16093", encounterDeck())) # Nebula's Ship environment
        if msCardOnTable[0].CardNumber == "16091a" and len(EnvCard) > 0: # Stage 1 main scheme
            EnvCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])


    if vName == 'Ronan':
        ssCard1 = filter(lambda card: card.CardNumber == "16111", encounterDiscardDeck()) # Cut the Power side scheme
        ssCard2 = filter(lambda card: card.CardNumber == "16113", encounterDiscardDeck()) # Superior Tactics side scheme
        
        EnvCard = sorted(filter(lambda card: card.CardNumber == "16108", encounterDeck())) # Kree Command Ship environment
        if msCardOnTable[0].CardNumber == "16106a" and len(EnvCard) > 0: # Stage 1 main scheme
            EnvCard[0].moveToTable(tableLocations['environment'][0] - 20, tableLocations['environment'][1])
            AttachmentCard = filter(lambda card: card.CardNumber == "16109", encounterDeck()) # Universal Weapon attachment
            AttachmentCard[0].moveToTable(vilX-25, vilY+5)
            AttachmentCard[0].sendToBack()

        if vCardOnTable[0].CardNumber == "16104": # Ronan II
            ssCard1_OnTable = filter(lambda card: card.CardNumber == "16111", table)
            if len(ssCard1_OnTable) == 0:
                if len(ssCard1) == 0:
                    ssCard1 = filter(lambda card: card.CardNumber == "16111", encounterDeck())
                    ssCard1[0].moveToTable(ssX, ssY)

        if vCardOnTable[0].CardNumber == "16105": # Ronan III
            ssCard2_OnTable = filter(lambda card: card.CardNumber == "16113", table)
            if len(ssCard2_OnTable) == 0:
                if len(ssCard2) == 0:
                    ssCard2 = filter(lambda card: card.CardNumber == "16113", encounterDeck())
                    if len(ssCard1_OnTable) == 0:
                        ssCard2[0].moveToTable(ssX, ssY)
                    if len(ssCard1_OnTable) > 0:
                        ssCard2[0].moveToTable(ssCard1_OnTable[0].position[0]+100, ssCard1_OnTable[0].position[1])

    if vName == 'Tower Defense':
        if msCardOnTable[0].CardNumber == "21098a" or msCardOnTable[1].CardNumber == "21099a": # Stage 1 main scheme
            loop = len(getPlayers())
            if loop == None:
                loop = 1
            while loop > 0:
                minionCard = filter(lambda card: card.CardNumber == "21102", encounterDeck()) # Black Order Besieger
                minionCard[0].moveToTable(villainX(1,0)-30+10*loop, 0)
                loop -= 1

    if vName == 'Thanos':
        ssCard = filter(lambda card: card.CardNumber == "21116", encounterDeck()) # Sanctuary side scheme
        attCard1 = filter(lambda card: card.CardNumber == "21118", encounterDiscardDeck()) # Thanos's Helmet attachment
        attCard2 = filter(lambda card: card.CardNumber == "21117", encounterDiscardDeck()) # Thanos's Armor attachment
        infinityCard = sorted(filter(lambda card: card.CardNumber == "21129", specialDeck())) # Infinity Gauntlet attachment

        if msCardOnTable[0].CardNumber == "21114a": # Stage 1 main scheme
            infinityCard[0].moveToTable(tableLocations['environment'][0]-20, tableLocations['environment'][1])
            ssCard[0].moveToTable(ssX, ssY)

        if vCardOnTable[0].CardNumber == "21112": # Thanos II
            attCard1_OnTable = filter(lambda card: card.CardNumber == "21118", table)
            if len(attCard1_OnTable) == 0:
                if len(attCard1) == 0:
                    attCard1 = filter(lambda card: card.CardNumber == "21118", encounterDeck())
                    attCard1[0].moveToTable(vilX-15, vilY+5)

        if vCardOnTable[0].CardNumber == "21113": # Thanos III
            attCard2_OnTable = filter(lambda card: card.CardNumber == "21117", table)
            if len(attCard2_OnTable) == 0:
                if len(attCard2) == 0:
                    attCard2 = filter(lambda card: card.CardNumber == "21117", encounterDeck())
                    attCard2[0].moveToTable(vilX-30, vilY+10)

    if vName == 'Hela':
        if msCardOnTable[0].CardNumber == "21138a": # Stage 1 main scheme
            odinCard = filter(lambda card: card.CardNumber == "21139a", removedFromGameDeck()) # Odin ally captive side
            odinCard[0].moveToTable(msX, msY)
            ssCard = filter(lambda card: card.CardNumber == "21140", removedFromGameDeck()) # Gnipahelir side scheme
            ssCard[0].moveToTable(ssX, ssY)
            garmCard = filter(lambda card: card.CardNumber == "21143", removedFromGameDeck()) # Garm (minion)
            garmCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])

    if vName == 'Loki':
        ssCard = filter(lambda card: card.CardNumber == "21167", encounterDeck()) # War in Asgard side scheme
        infinityCard = sorted(filter(lambda card: card.CardNumber == "21129", specialDeck())) # Infinity Gauntlet attachment

        if msCardOnTable[0].CardNumber == "21165a": # Stage 1 main scheme
            infinityCard[0].moveToTable(tableLocations['environment'][0]-20, tableLocations['environment'][1])
            ssCard[0].moveToTable(ssX, ssY)