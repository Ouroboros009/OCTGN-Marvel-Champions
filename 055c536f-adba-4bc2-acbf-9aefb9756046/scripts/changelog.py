changelog = {
    '0000104': ("0.0.1.4", "16 December 2019", [
        "Welcome to the Marvel Champions OCTGN Plugin!",
        "Added Changelog",
        "Updated obligation cards to properly get generated",
        "Fixed issue with being able to use Deck Editor",
        "Player setup is now triggered automatically after a hero deck is loaded",
        "Promp users to load a hero deck after the game initializes",
        "Default double click option for face down cards now flips them over.",
        "Default double click option for scheme cards now flips them to the other side",
        "New Add card option added in case a card is needed in the game and can't be found",
        "New option to add 3 markers to a card for quick marker additions",
        "Updated some grammar on prompts"
        ]),
    '0000105': ("0.0.1.5", "16 December 2019", [
        "Fixed a bug that would not load the full encounter deck when loading a villain after the hero deck has been loaded first"
        ]),
    '0000106': ("0.0.1.6", "2 January 2020", [
        "Everyone who already had the image pack installed needs to redownload and install the new one as there were fixes put in place for certain cards like Wakanda Forever!",
        "Added Captain America Hero Pack",
        "Added Ms. Marvel Hero Pack",
        "Added Green Goblin Scenario Pack",
        "Fixed function to reshuffle encounter cards into encounter deck to only pull discarded cards and not all encounter cards on the table",
        "Added ability to load non published decks from marvelcdb. User needs to edit marvelcdb to check the 'Share Your Decks' option in your profile preferences",
        "Added right click option to add acceleration marker"
        ]),
    '0000107': ("0.0.1.7", "2 January 2020", [
        "Fixed flipping over cards that have an alternate back",
        "Fixed Captain America and Ms. Marvel decks being fliped while loading"
        ]),
    '0000108': ("0.0.1.8", "31 January 2020", [
        "Reworked the gameflow mecahnics with the turns and phases making the entire game move foward with pressing 'f12' when finished with current turn or villain action. Active player is now going to be highlighted in green and players that have finished their turn are going to be highlighted in gray.  Active player is the only one that can advance the game with the next 'f12' press.",
        "Fixed Green Goblin villains that have alternate backs",
        "Fixed a bug where you could discard cards from the table that should never be discarded",
        "Fixed a bug where the next scheme was pulling out in wrong order and rotating the card sideways",
        "Fixed a bug where moving to the next villain stage was not maintaining the status/markers of the previous villain",
        "Added a new keyboard shortcut to add an all purpose marker to any card by pressing Right",
        "Added a new keyboard shortcut to remove an all purpose marker to any card by pressing Left",
        "Added aspect type to the owner property on the cards to allow for easier Deck Building",
        "Change the table background to be two images that overlay so zooming in on the board will keep the cards in the designated positions on the image",
        "Expansion pack images have been uploaded to the website"
        ]),
    '0000109': ("0.0.1.9", "8 February 2020", [
        "The Wrecking Crew Scenario Pack added",
        "Fixed bug where first player was being set twice on setup",
        "Fixed bug where card control was not being passed on turn pass",
        "Fixed Green Goblin Environment cards not working as double sided",
        "Reworked the game setup to dynamically place the villain since wrecking crew has 4",
        "Removed the set table positions",
        "Added default double click action to the villains to draw the next encounter card",
        "Active villain is highlighted in green for The Wrecking Crew and a right click menu has been added to the cards to set a villain as active",
        "The Wrecking Crew Scenario Pack images have been uploaded to the website"
        ]),
    '0000110': ("0.0.1.10", "18 March 2020", [
        "Thor Hero Pack added",
        "Thor Hero Pack images have been uploaded to the website"
        ]),
    '0000111': ("0.0.1.11", "11 April 2020", [
        "Fixed Thor nemesis cards having the wrong backing",
        "Added option to move a card to the bottom of the hero deck",
        "Added option to move a card to the bottom of the encounter deck",
        "Changed the marker right click options to be shown on all cards to allow for adding damage tokens on cards that usually wouldn't take damage"
        ]),
    '0000112': ("0.0.1.12", "17 June 2020", [
        "Black Widow Hero Pack added",
        "Black Widow Hero Pack images have been uploaded to the website",
        "Changed game URL to point to new website",
        "Updated the rules PDF - thank you ZATGamer from github",
        "Updated some keyboard shortcuts to align better with the Arkham Horror OCTGN module - thank you pilunte23 from github",
        "Fixed player group definition in the definition.xml per OCTGN update",
        "Moved Marker definition to be in the definition.xml per OCTGN update"
        ]),
    '0000113': ("0.0.1.13", "18 June 2020", [
        "Fixed Black Widow Nemesis Deck"
        ]),
    '0000114': ("0.0.1.14", "9 July 2020", [
        "Doctor Strange Hero Pack added",
        "Doctor Strange Hero Pack images have been uploaded to the website",
        "Fixed reported bug when advancing the game with f12 and all players cards would not ready and would not automatically draw new hand - thank you bugu57 from github"
        ]),
    '0000115': ("0.0.1.15", "13 July 2020", [
        "Fixed Doctor Strange to allow for the Invocation Deck"
        ]),
    '0000116': ("0.0.1.16", "20 August 2020", [
        "Hulk Hero Pack added",
        "Hulk Hero Pack images have been uploaded to the website",
        "FFG Print and Play module Ronan added",
        "Ronan module images have been uploaded to the website",
        "Community Content Baron Zemo: Firestarter villain added - thank you FelixFactory from discord",
        "Baron Zemo: Firestarter images have been uploaded to the website - thank you FelixFactory from discord"
        ]),
    '0000117': ("0.0.1.17", "12 November 2020", [
        "The Rise of Red Skull added",
        "The Rise of Red Skull images have been uploaded to the website"
        ]),
    '0000118': ("0.0.1.18", "14 November 2020", [
        "Fixed issue where Standard and Expert encounter cards were not being created for the Red Skull villains.",
        "Set visibility for all global decks to ALL by default."
        ]),
    '0000119': ("0.0.1.19", "3 December 2020", [
        "Ant-Man Hero Pack added",
        "Ant-Man Hero Pack images have been uploaded to the website."
        ]),
    '0000120': ("0.0.1.20", "22 February 2021", [
        "Updated Ant-Man image pack to have Swarm Tactics. You will need to redownload and install the image pack",
        "Wasp Hero Pack added",
        "Wasp Hero Pack images have been uploaded to the website.",
        "Quicksilver Hero Pack added",
        "Quicksilver Hero Pack images have been uploaded to the website."
        ]),
    '0000200': ("0.0.2.00", "30 July 2021", [
        "Scheme size fixed",
        "Draw unrevealed action on player deck added",
        "Flip top card action on player/special/encounter deck added",
        "Kang Villain Pack added",
        "Galaxy's Most Wanted Extension added",
        "Scarlet Witch Hero Pack added",
        "Groot Hero Pack added",
        "Rocket Racoon Hero Pack added",
        "Star-Lord Hero Pack added",
        "Gamora Hero Pack added",
        "Drax Hero Pack added",
        "Venom Hero Pack added"
        ]),
    '0000201': ("0.0.2.01", "7 August 2021", [
        "Background changed",
        "Markers changed",
        "Fixed loading .o8d in actions.py per OCTGN update"
        ]),
    '0000202': ("0.0.2.02", "9 August 2021", [
        "Load encounter with default modular or custom setup",
        "Shared campaign deck added"
        ]),
    '0000203': ("0.0.2.03", "19 August 2021", [
        "Updated last published hero image packs to fix alter-ego/hero card coming the wrong side. You will need to redownload and install the image pack",
        "Updated image pack released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "Turn counter fixed",
        "Notification added when encounter deck is empty",
        "Shuffle into deck fixed when used on Dr Strange special deck",
        "Shortcuts for status card changed : use \"alt\" instead of \"ctrl\" and \"ctrl+alt\" instead of \"ctrl+shift\"",
        "NEW! Save and load table option added - thanks to authors of the Arkham Horror OCTGN module that make most of it",
        "NEW! Highlight option added using numpad as shortcuts",
        "NEW! Take global control added using F8 as shortcuts to take control on all shared cards and piles"
        ]),
    '0000204': ("0.0.2.04", "20 August 2021", [
        "Fixed Pull Boost/encounter card when using right-click on table",
        "Fixed loading Kang not working"
        ]),
    '0000205': ("0.0.2.05", "27 September 2021", [
        "The Mad Titan's Shadow added",
        "Nebula Hero pack added",
        "Image packs released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "Full custom setup for modulars encounters added",
        "Reworked the game setup for Kang to randomly place Kang II villain(s) when using \"Defeat Villain\" (\"Next Scheme\" is disabled for Kang)",
        "Random Loki generated while setting up and using \Defeat Villain\"",
        "Right-click on Special shared pile to load any modular encounter set after initial setup",
        "Double-click on Infinity Gauntlet encounter card on table to draw a card from the Special Deck"
        ]),
    '0000206': ("0.0.2.06", "3 October 2021", [
        "Fixed issue with Hela setup"
        ]),
    '0000207': ("0.0.2.07", "3 October 2021", [
        "Fixed issue where some Ebony Maw cards were discarded in player discard pile"
        ]),
    '0000208': ("0.0.2.08", "6 October 2021", [
        "Campaign cards size from MTS fixed (Cosmo, Black Swan and Jormungand)",
        "Fixed issues with pass shared control in multiplayer",
        "Spectrum permanent upgrade cards are now created in special Deck"
        ]),
    '0000209': ("0.0.2.09", "1 November 2021", [
        "Fixed issue where Nebula encounter cards are discarded in the player pile",
        "Victory display pile added"
        ]),
    '0000210': ("0.0.2.10", "11 November 2021", [
        "Fixed some minor issues"
        ]),
    '0000211': ("0.0.2.11", "04 December 2021", [
        "War Machine Hero pack added",
        "War Machine ENG image pack released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "War Machine FR image pack released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "The Hood scenario pack added",
        "The Hood ENG image pack (Low Quality) released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "The Hood FR image pack released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "Valkyrie Hero pack added",
        "Valkyrie ENG image pack (Low Quality) released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "Valkyrie FR image pack released at https://twistedsistem.wixsite.com/octgnmarvelchampions"
        ]),
    '0000212': ("0.0.2.12", "07 December 2021", [
        "Improved quality for Valkyrie Hero ENG image pack",
        "Updated image pack released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "NEW!! Option added when right-clicking on shared Special Deck to choose 1 set or at random in this deck and shuffle it in encounter deck"
        ]),
    '0000213': ("0.0.2.13", "21 January 2022", [
        "Vision Hero pack added",
        "Vision ENG image pack not released (no good image scan available)",
        "Vision FR image pack released at https://twistedsistem.wixsite.com/octgnmarvelchampions"
        ]),
    '0000214': ("0.0.2.14", "31 January 2022", [
        "The Hood ENG image pack (better quality) released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "Vision ENG image pack released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "Fixed issue where \"Draw Unrevealed\" displays card name in chat box",
        "Fixed issue where cards from Badoon Headhunter modular behaved as player cards",
        "Badoon Headhunter modular can be picked during the main villain setup" 
        ]),
    '0000215': ("0.0.2.15", "20 February 2022", [
        "Fixed issue where \"Viper's Ambition\" from Spider-Women Nemesis set were not displayed correctly",
        "Fixed default modular encounter setup for Crossbones"
        ]),
    '0000300': ("0.0.3.00", "08 April 2022", [
        "Sinister Motives expansion added",
        "Fixed issue where only one obligation from Scarlet Witch nemesis set is shuffled into encounter deck",
        "Fixed the discard of player cards when playing solo multihand (thanks to alwaysfish)",
        "2 stun or confuse cards can be added now (only 1 before)",
        "Added some visuals when loading pre-built Hero, Villain and modular"
        ]),
    '0000310': ("0.0.3.10", "29 April 2022", [
        "Fix Sinister Six setup : Randomly choose active villains",
        "Fix Sandman City street environment taking 4 markers when Sandman was defeated",
        "Better Loki villain management",
        "Add osborn tech module to Sinister Motives campaign cards",
        "BROUGHT TO YOU BY bidousagittarius96 (BIG THANKS!!) :",
        "Feature: Automation for threats markers",
        "Feature: Automation for damage markers on Hero and Villain",
        "Feature: cards with \"Permanent\" keyword cannot be discarded",
        "Feature: cards with \"Victory\" keyword are discarded in victory pile",
        "Feature: load .o8d deck files when using \"Load Hero\"",
        "Fix Tough status card and counters when encounter card is revealed",
        "Fix number of counters on Crossbones's Machine gun in multiplayer",
        "Fix Drang setup (Spear in Expert + Milano support)",
        "Fix Risky Business setup (Criminal Enterprise environment added)",
        "Fix Red Skull setup: all side schemes go in special deck",
        "Fix Mutagen Formula setup: engage Goblin Thrall minion with each player",
        "Fix Zola setup: engage Ultimate Bio-Servant minion with each player",
        "Fix: Venom expert setup",
        "Fix: Formidable Foe (Standard II) location override villain environments",
        "Fix: Power Stone attached to Nebula",
        "Fix: Ronan setup multiplayer (Milano and Power stone to 1st player)",
        "Fix: bad card verso for some SinisterMotives campaign cards"
        ]),
    '0000311': ("0.0.3.11", "30 April 2022", [
        "Fix: Collector/Hela : HP was added when flipping to there infinite health side",
        "Fix: Acceleration Markers was not transferred to the next Main Scheme",
        "Fix: Modular Encounters was shuffled in encounter deck in The Hood scenario",
        "Feature: ask choice when discarding Cards with \"Victory\" keyword and still having Markers",
        "Fix: Hela HP added when side scheme discarded into victory pile"
        ]),
    '0000312': ("0.0.3.12", "06 May 2022", [
        "Fix: First Player Token position when going from one character to one another",
        "Fix: Vision max hand size when flipping to alter-ego",
        "Fix: \"Assault Training\" card counters",
        "Fix: Wrong modular encounter name in image pack for \"Symbiotic Strength\"",
        "Fixed issue where control on a side scheme card was lost when revealed"
        ]),
    '0000313': ("0.0.3.13", "26 May 2022", [
        "Nova Hero pack added",
        "Ironheart Hero pack added",
        "Feature: Mysterio scenario improved : encounter cards are now automatically shuffled in players deck at Expert setup",
        "Feature: Mysterio scenario improved : encounter cards are now automatically moved to table when drew in players hand",
        "Feature: Nova \"Connection to the Worldmind\" card will not count in player hand when drawing cards",
        "Feature: Ironheart's Suit Version swapped when moved from Special Pile to Table",
        "Feature: Boost card when double-clicking on villainous minion",
        "Feature: \"Unload Hero Deck\" without resetting table (right-click on table: Setup & Save Tools)",
        "Feature[Work In Progress]: We can now load fanmade. (right-click on table: Setup & Save Tools)",
        "Some fanmade examples: https://tinyurl.com/mcfanmade",
        "Fix: Modular selection box allowed only 1 modular despite some scenario needs 3 (when not taking recommended)"
        ]),
    '0000314': ("0.0.3.14", "26 May 2022", [
        "Fix: Ironheart deck from marvelcdb wasn't loading version 2 and 3 hero card."
        ]),
    '0000315': ("0.0.3.15", "29 May 2022", [
        "fix: Hela Gjallerbru and Hall of Nostrond side schemes mixed. You will need to redownload and install the MTS image pack",
        "fix: Drawing cards with ctrl+D no longer draw 2 cards with Nova \"Connection to the Worldmind\"",
        "fix: Ironheart version swap discarded other heroes"
        ]),
    '0000316': ("0.0.3.16", "17 July 2022", [
        "Spider-Ham Hero pack added",
        "SP/dr Hero pack added",
        "Fix: Ironheart version didn't swap in multiplayer",
        "Stun/Confuse/Tough status no longer stuck to 1 or 2 cards"
        ]),
    '0000320': ("0.0.3.20", "03 August 2022", [
        "Feature: Welcome Screen added to help new people starting a game. It also provides usefull links. You can also access it right click onto the table.",
        "Feature: Card info function added when right-clicking on a card. It provides rules information on some keywords.",
        "Feature: Counters added to adjust your hand size in Hero form and Alter-ego form (usefull for Iron Man or when playing cards like \"Symbiote Suit\" or \"The Sorcerer Supreme\").",
        "Feature: Warning message if a player want to shuffle his discard pile into his deck if his deck is still containing cards.",
        "Feature: Warning message if a player want to shuffle encounter discard pile into encounter deck if this deck is still containing cards.",
        "Fix: Some workaround about first player behaviour that might still needs some tests. Players order is based on loaded deck order.",  
        "Fix: Hawkeye prebuild deck missing 1 card.",
        "Shortcut: F8 shortcut for taking control of targeted (shift + mouse left-click) cards.",
        "Shortcut: F9 shortcut for random number function",
        "Fonts changed to Elektra Medium Pro Regular"
        ]),
    '0000321': ("0.0.3.21", "07 August 2022", [
        "Hotfix: Saving tools didn't work since update 3.20"
        ]),
    '0000330': ("0.0.3.30", "14 October 2022", [
        "Mutant Genesis expansion added",
        "Cyclops Hero pack added",
        "Phoenix Hero pack added"
        ]),
    '0000331': ("0.0.3.31", "15 October 2022", [
        "Fix on some Magneto side scheme (missing threat)"
        ]),
    '0000332': ("0.0.3.32", "16 October 2022", [
        "Fix: Wrecking Crew Scenario wasn't loading during setup"
        ]),
    '0000334': ("0.0.3.34", "7 November 2022", [
        "Fix: Sabretooth scenario missing 1 card (Medical Emergency)",
        "Fix: Future Past module missing in campaign cards."        
        ]),
    '0000340': ("0.0.3.40", "19 November 2022", [
        "Wolverine Hero pack added",
        "Storm Hero pack added",
        "Mojo Mania Scenario pack added"     
        ]),
    '0000345': ("0.0.3.45", "04 March 2023", [
        "Gambit Hero pack added",
        "Rogue Hero pack added" 
        ]),
    '0000346': ("0.0.3.46", "31 May 2023", [
        "Fanmade Hero and Fanmade scenario can be loaded from the Welcome Screen",
        "Fanmade installation tool added into octgn data folder to make zip installation easier",
        "New card type added (player side scheme)"
        ]),
    '0000360': ("0.0.3.60", "2 September 2023", [
        "NeXt Evolution added",
		"Feature: Hero, Villain and Encounters can now be selected either alphabetically or by release date",
		"Feature: Nemesis sets added as a choice among all other Encounter sets",
		"Fix: All data updated from marvelcdb",
		"Fix: Changed the way FanMade is loaded. Please re-download ZIP files from GDrive as previous one won't work anymore",
        "Major updates: A lot of changes have been made to the various scripts in order to improve MC module behaviour, future updates and fanmade integration. Although I conducted a lot of tests, bugs could reappear. Please let me know if this is the case."
        ]),
    '0000363': ("0.0.3.63", "1 October 2023", [
        "Psylocke Hero pack added",
        "Angel Hero pack added",
        "NeXt Evolution data updated",
        "This update also fix some bugs and errors introduced with v3.60 update"
        ]),
    '0000365': ("0.0.3.65", "29 November 2023", [
        "X-23 Hero pack added",
        "Deadpool Hero pack added"
        ]),
    '0000366': ("0.0.3.66", "29 November 2023", [
        "Fix: Sci-Fi modular set was not loading properly",
        "Fix: Villainous keyword on Exodus minion",
        "Fix: Magneto I, II, III was loaded in standard and expert",
        "Fix: Orbital Decay side scheme threat fixed"
        ]),
    '0000372': ("0.0.3.72", "08 April 2024", [
        "Age of Apocalypse added",
        "Feature: Standard I, II, III and Expert I, II sets can be mixed. That changed the way those sets are selected.",
        "Fanmade: From now on, some fanmade villain scenario are included in octgn. You still need to apply image packs as always."
        ]),
    '0000374': ("0.0.3.74", "18 May 2024", [
        "Iceman Hero pack added"
        ]),
    '0000375': ("0.0.3.75", "27 July 2024", [
        "Jubilee Hero pack added",
		"Feature: new card action (right-click): Switch card with the top one of your deck."
        ]),
    '0000376': ("0.0.3.76", "27 July 2024", [
        "Hotfix: jubilee cards was mixed-up in her set"
        ]),
    '0000377': ("0.0.3.77", "04 October 2024", [
        "Nightcrawler Hero pack added"
        ]),
    '0000378': ("0.0.3.78", "30 November 2024", [
        "Magneto Hero pack added",
        "Fix: Shuffle discard pile into deck didn't work with Side and Special deck.",
        "Feature: new card action (right-click): Add any marker from all available ones"
        ]),
    '0000379': ("0.0.3.79", "23 February 2025", [
        "Hotfix: Fix for the loading method from marvelcdb.com following an API change.",
        "Fix: alternative resource images from Mutant Genesis wasn't loading from marvelcdb."
        ]),
    '0000381': ("0.0.3.81", "16 March 2025", [
        "Agents of Shield expansion added",
        "Feature: Standard I, II, III and Expert I, II sets can be mixed. That changed the way those sets are selected.",
        "Fanmade: Determination faction set added."
        ]),
    '0000382': ("0.0.3.82", "19 March 2025", [
        "Feature: Added a new way to use correct markers on some cards instead of All Purpose markers by default",
        "Fix: HP value of Black Widow III villain was incorrect",
        "Fix: Counters on the Holding Cell cards did not take the number of players into account."
        ]),
    '0000383': ("0.0.3.83", "10 May 2025", [
        "Shuri Hero pack added",
        "Silk Hero pack added"
        ]),
    '0000384': ("0.0.3.84", "26 June 2025", [
        "Falcon Hero pack added",
        "Winter Soldier Hero pack added"
        ]),
    '0000385': ("0.0.3.85", "28 June 2025", [
        "Fix: Captain America's Shield Linked keyword wasn't implemented"
        ]),
    '0000386': ("0.0.3.86", "12 August 2025", [
        "Feature: Added a function to draw multiple unrevealed cards.",
        "Security: This update addresses a recently reported security issue."
        ]),
    '0000387': ("0.0.3.87", "31 August 2025", [
        "Trickster Takeover Scenario pack added",
        "Security: This update addresses another recently reported security issue."
        ]),
    '0000388': ("0.0.3.88", "02 September 2025", [
        "Fix: Loki, God of Lies setup."
        ]),
    '0000389': ("0.0.3.89", "21 September 2025", [
        "Enhancement: Add magnetic grid for card positioning.",
        "Fanmade: Hunting Season (By Nugget) scenarios added.",
        "Fanmade: Blink (By Kajislav) hero added.",
        "Fanmade: Destiny (By Merlin) hero added.",
        "Fanmade: Ghost Rider (By Swept & Jiub) hero added.",
        "Fanmade: Iron Fist (By Merlin) hero added.",
        "Fanmade: Manifold (By BlueHG) hero added.",
        "Fanmade: Mantis (By BlueHG) hero added.",
        "Fanmade: Mighty Thor (By Rainy) hero added.",
        "Fanmade: Moon Knight (By Hax) hero added.",
        "Fanmade: Ms Marvel (By CptScorp) hero added.",
        "Fanmade: Mystique (By Merlin) hero added.",
        "Fanmade: Polaris (By JackHKP) hero added.",
        "Fanmade: Rescue (By Rainy) hero added.",
        "Fanmade: Rom (By Alias & Merlin) hero added.",
        "Fanmade: Ser Reddwyn (By JustATuna) hero added.",
        "Fanmade: Singularity (By Phenexian) hero added.",
        "Fanmade: Spider-Man 2099 (By Rainy) hero added.",
        "Fanmade: Weapon Hex (By Merlin) hero added.",
        "Fanmade: Yondu (By Hax) hero added."
        ]),
    '0000390': ("0.0.3.90", "11 October 2025", [
        "Hotfix : Loki, God of Lies missing modular encounter at setup.",
        "Hotfix : Unexpected behaviour and error messages with magnetic grid features"
        ]),
    '0000391': ("0.0.3.91", "08 November 2025", [
        "Civil War added (PvE only. PvP won't be added)."
        ])
}