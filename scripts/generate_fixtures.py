"""
Script to generate high-fidelity synthetic TMDB 5000 fixtures.
Creates 40 diverse movies with matching schema for tests, CI, and local fallback.
"""
import csv
import json
from pathlib import Path

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "backend" / "tests" / "fixtures"
FIXTURES_DIR.mkdir(parents=True, exist_ok=True)

# 40 carefully crafted synthetic movies spanning various genres, directors, and cast
# with cross-movie relationships (franchise sequels, common directors, common genres)
SYNTHETIC_MOVIES = [
    {
        "id": 10001,
        "title": "Quantum Horizon",
        "tagline": "Beyond the event horizon lies human destiny.",
        "overview": "A team of astrophysicists and deep-space explorers journey through an unstable wormhole in search of a habitable sanctuary as Earth's magnetic core weakens.",
        "genres": [{"id": 878, "name": "Science Fiction"}, {"id": 12, "name": "Adventure"}, {"id": 18, "name": "Drama"}],
        "keywords": [{"id": 1, "name": "wormhole"}, {"id": 2, "name": "space exploration"}, {"id": 3, "name": "astrophysics"}, {"id": 4, "name": "time dilation"}],
        "release_date": "2021-11-05",
        "runtime": 148,
        "popularity": 85.4,
        "vote_average": 8.3,
        "vote_count": 4200,
        "director": "Elena Vance",
        "cast": [
            {"name": "Marcus Aurelius Reed", "character": "Dr. Joseph Brand"},
            {"name": "Sarah Chen", "character": "Commander Amelia Thorne"},
            {"name": "David Oyelowo", "character": "Doyle Harris"},
            {"name": "Jessica Chastain", "character": "Dr. Murph Vance"},
            {"name": "Michael Caine", "character": "Professor Charles Vance"}
        ]
    },
    {
        "id": 10002,
        "title": "Quantum Horizon: Singularity",
        "tagline": "Time was never on our side.",
        "overview": "Following the discovery of the Eden system, surviving colonists confront a temporal anomaly that threatens to collapse both timeline branches.",
        "genres": [{"id": 878, "name": "Science Fiction"}, {"id": 12, "name": "Adventure"}, {"id": 9648, "name": "Mystery"}],
        "keywords": [{"id": 1, "name": "wormhole"}, {"id": 4, "name": "time dilation"}, {"id": 5, "name": "alternate timeline"}, {"id": 6, "name": "survival"}],
        "release_date": "2024-03-15",
        "runtime": 155,
        "popularity": 92.1,
        "vote_average": 8.1,
        "vote_count": 3100,
        "director": "Elena Vance",
        "cast": [
            {"name": "Marcus Aurelius Reed", "character": "Dr. Joseph Brand"},
            {"name": "Sarah Chen", "character": "Commander Amelia Thorne"},
            {"name": "Oscar Isaac", "character": "Cipher Valerius"},
            {"name": "Florence Pugh", "character": "Aria Brand"},
            {"name": "Hiroyuki Sanada", "character": "Kenji Sato"}
        ]
    },
    {
        "id": 10003,
        "title": "Neon Syndicate",
        "tagline": "In the city of chrome, memories are currency.",
        "overview": "A memory extractor in a rain-soaked neo-Tokyo metropolis uncovers a high-level government conspiracy involving synthetic human souls and rogue AI oligarchs.",
        "genres": [{"id": 878, "name": "Science Fiction"}, {"id": 28, "name": "Action"}, {"id": 53, "name": "Thriller"}],
        "keywords": [{"id": 7, "name": "cyberpunk"}, {"id": 8, "name": "artificial intelligence"}, {"id": 9, "name": "dystopia"}, {"id": 10, "name": "memory theft"}],
        "release_date": "2020-08-21",
        "runtime": 122,
        "popularity": 78.5,
        "vote_average": 7.9,
        "vote_count": 2800,
        "director": "Kenji Watanabe",
        "cast": [
            {"name": "Dev Patel", "character": "Ren Takahashi"},
            {"name": "Ana de Armas", "character": "Kira 9"},
            {"name": "Hiroyuki Sanada", "character": "Lord Takeshi"},
            {"name": "Gemma Chan", "character": "Sloan Vane"},
            {"name": "Pedro Pascal", "character": "Agent Cross"}
        ]
    },
    {
        "id": 10004,
        "title": "Neon Syndicate: Overdrive",
        "tagline": "Upgrade or terminate.",
        "overview": "When an aggressive neural virus spreads through Tokyo's cyber-net, Ren Takahashi must partner with a former bounty hunter to neutralize the mainframe core.",
        "genres": [{"id": 878, "name": "Science Fiction"}, {"id": 28, "name": "Action"}, {"id": 80, "name": "Crime"}],
        "keywords": [{"id": 7, "name": "cyberpunk"}, {"id": 8, "name": "artificial intelligence"}, {"id": 11, "name": "cyber warfare"}, {"id": 12, "name": "bounty hunter"}],
        "release_date": "2023-09-12",
        "runtime": 128,
        "popularity": 81.0,
        "vote_average": 7.6,
        "vote_count": 2150,
        "director": "Kenji Watanabe",
        "cast": [
            {"name": "Dev Patel", "character": "Ren Takahashi"},
            {"name": "Florence Pugh", "character": "Vesper Volt"},
            {"name": "Pedro Pascal", "character": "Agent Cross"},
            {"name": "Hiroyuki Sanada", "character": "Lord Takeshi"},
            {"name": "Karl Urban", "character": "Briggs"}
        ]
    },
    {
        "id": 10005,
        "title": "Shadows of the Crown",
        "tagline": "Treason is an art practiced behind velvet curtains.",
        "overview": "During the turbulent succession crisis of 16th century England, a cunning royal spymaster navigates betrayal, forbidden romance, and shifting alliances to protect the young monarch.",
        "genres": [{"id": 18, "name": "Drama"}, {"id": 36, "name": "History"}, {"id": 53, "name": "Thriller"}],
        "keywords": [{"id": 13, "name": "royal court"}, {"id": 14, "name": "conspiracy"}, {"id": 15, "name": "espionage"}, {"id": 16, "name": "political intrigue"}],
        "release_date": "2019-10-18",
        "runtime": 138,
        "popularity": 64.2,
        "vote_average": 8.0,
        "vote_count": 1950,
        "director": "Arthur Sterling",
        "cast": [
            {"name": "Emma Thompson", "character": "Queen Regent Eleanor"},
            {"name": "Tom Hiddleston", "character": "Lord Francis Walsingham"},
            {"name": "Saoirse Ronan", "character": "Lady Mary Grey"},
            {"name": "Benedict Cumberbatch", "character": "Earl of Warwick"},
            {"name": "Charles Dance", "character": "Archbishop Cranmer"}
        ]
    },
    {
        "id": 10006,
        "title": "The Glass Fortress",
        "tagline": "Power has no allies.",
        "overview": "A gripping boardroom thriller centered around the ruthless hostile takeover of the world's most powerful renewable energy conglomerate by a renegade private equity founder.",
        "genres": [{"id": 18, "name": "Drama"}, {"id": 53, "name": "Thriller"}],
        "keywords": [{"id": 17, "name": "wall street"}, {"id": 18, "name": "corporate greed"}, {"id": 19, "name": "hostile takeover"}, {"id": 20, "name": "corruption"}],
        "release_date": "2022-04-08",
        "runtime": 126,
        "popularity": 58.7,
        "vote_average": 7.7,
        "vote_count": 1420,
        "director": "Arthur Sterling",
        "cast": [
            {"name": "Jeremy Strong", "character": "Julian Vance"},
            {"name": "Cate Blanchett", "character": "Victoria Sterling"},
            {"name": "Brian Cox", "character": "Alastair Vance"},
            {"name": "Nicholas Hoult", "character": "Peter Finch"},
            {"name": "Laura Dern", "character": "Evelyn Ross"}
        ]
    },
    {
        "id": 10007,
        "title": "Midnight in Marseille",
        "tagline": "Every secret has an expiration date.",
        "overview": "A disillusioned former interpol detective is drawn into the perilous Mediterranean underworld when his estranged daughter disappears while investigating an international cargo cartel.",
        "genres": [{"id": 80, "name": "Crime"}, {"id": 53, "name": "Thriller"}, {"id": 28, "name": "Action"}],
        "keywords": [{"id": 21, "name": "marseille"}, {"id": 22, "name": "kidnapping"}, {"id": 23, "name": "underworld"}, {"id": 24, "name": "interpol"}],
        "release_date": "2021-06-18",
        "runtime": 115,
        "popularity": 69.8,
        "vote_average": 7.4,
        "vote_count": 1850,
        "director": "Jean-Luc Moreau",
        "cast": [
            {"name": "Vincent Cassel", "character": "Marc Delacroix"},
            {"name": "Marion Cotillard", "character": "Camille Bouchard"},
            {"name": "Daniel Bruhl", "character": "Victor Kholer"},
            {"name": "Adele Exarchopoulos", "character": "Lea Delacroix"},
            {"name": "Mads Mikkelsen", "character": "Baron Moreau"}
        ]
    },
    {
        "id": 10008,
        "title": "Corsica Vendetta",
        "tagline": "Blood remembers.",
        "overview": "Following the assassination of a local port union leader, an ex-special forces officer returns to the rugged cliffs of Corsica to exact retribution on a ruthless syndicate.",
        "genres": [{"id": 80, "name": "Crime"}, {"id": 28, "name": "Action"}, {"id": 18, "name": "Drama"}],
        "keywords": [{"id": 23, "name": "underworld"}, {"id": 25, "name": "revenge"}, {"id": 26, "name": "special forces"}, {"id": 27, "name": "mafia"}],
        "release_date": "2023-10-06",
        "runtime": 110,
        "popularity": 63.5,
        "vote_average": 7.2,
        "vote_count": 1340,
        "director": "Jean-Luc Moreau",
        "cast": [
            {"name": "Vincent Cassel", "character": "Luc Antonetti"},
            {"name": "Mads Mikkelsen", "character": "Stefan Grimaldi"},
            {"name": "Lea Seydoux", "character": "Helene Rossi"},
            {"name": "Tahar Rahim", "character": "Youssef"},
            {"name": "Jean Reno", "character": "Don Salvatore"}
        ]
    },
    {
        "id": 10009,
        "title": "Starlight Odyssey",
        "tagline": "Friendship is the ultimate coordinates.",
        "overview": "An eccentric starship mechanic and her chatterbox robot companion take on an intergalactic courier mission across treacherous nebula belts to save an endangered alien ecosystem.",
        "genres": [{"id": 16, "name": "Animation"}, {"id": 35, "name": "Comedy"}, {"id": 10751, "name": "Family"}, {"id": 878, "name": "Science Fiction"}],
        "keywords": [{"id": 2, "name": "space exploration"}, {"id": 28, "name": "robot"}, {"id": 29, "name": "alien creatures"}, {"id": 30, "name": "intergalactic"}],
        "release_date": "2022-12-16",
        "runtime": 98,
        "popularity": 95.6,
        "vote_average": 8.4,
        "vote_count": 3900,
        "director": "Maya Lin",
        "cast": [
            {"name": "Awkwafina", "character": "Pip (voice)"},
            {"name": "Bill Hader", "character": "Bolt-9 (voice)"},
            {"name": "Taika Waititi", "character": "Captain Barnaby (voice)"},
            {"name": "Kristen Schaal", "character": "Zephyr (voice)"},
            {"name": "Keanu Reeves", "character": "The Cosmic Sage (voice)"}
        ]
    },
    {
        "id": 10010,
        "title": "Nebula Knights",
        "tagline": "Assemble across the star system.",
        "overview": "Pip and Bolt-9 team up with a quirky squad of planetary outcasts to stop an interstellar scrap baron from dismantling a luminous living comet.",
        "genres": [{"id": 16, "name": "Animation"}, {"id": 12, "name": "Adventure"}, {"id": 35, "name": "Comedy"}, {"id": 10751, "name": "Family"}],
        "keywords": [{"id": 28, "name": "robot"}, {"id": 29, "name": "alien creatures"}, {"id": 30, "name": "intergalactic"}, {"id": 31, "name": "teamwork"}],
        "release_date": "2024-07-04",
        "runtime": 102,
        "popularity": 88.2,
        "vote_average": 8.0,
        "vote_count": 2200,
        "director": "Maya Lin",
        "cast": [
            {"name": "Awkwafina", "character": "Pip (voice)"},
            {"name": "Bill Hader", "character": "Bolt-9 (voice)"},
            {"name": "Jack Black", "character": "Baron Krag (voice)"},
            {"name": "Taika Waititi", "character": "Captain Barnaby (voice)"},
            {"name": "Zendaya", "character": "Princess Lyra (voice)"}
        ]
    },
    {
        "id": 10011,
        "title": "The Whispering Hollow",
        "tagline": "Silence is when they listen.",
        "overview": "A sound engineer inherits a secluded cabin deep in the Black Forest, only to discover audio frequencies recorded on vintage reel tapes that summon ancient apparitions.",
        "genres": [{"id": 27, "name": "Horror"}, {"id": 9648, "name": "Mystery"}, {"id": 53, "name": "Thriller"}],
        "keywords": [{"id": 32, "name": "haunted house"}, {"id": 33, "name": "audio frequencies"}, {"id": 34, "name": "supernatural"}, {"id": 35, "name": "isolation"}],
        "release_date": "2020-10-30",
        "runtime": 104,
        "popularity": 71.4,
        "vote_average": 7.3,
        "vote_count": 2100,
        "director": "Julian Graves",
        "cast": [
            {"name": "Toni Collette", "character": "Dr. Eleanor Vance"},
            {"name": "Dan Stevens", "character": "Thomas Ward"},
            {"name": "Mia Goth", "character": "Greta Holt"},
            {"name": "Stellan Skarsgard", "character": "Pastor Heinrich"},
            {"name": "Bill Skarsgard", "character": "The Entity"}
        ]
    },
    {
        "id": 10012,
        "title": "Echoes in the Fog",
        "tagline": "The lake never forgets.",
        "overview": "A folklore researcher investigates the vanishing of a fishing village in 1952, unleashing malevolent water spirits trapped within the glacial mist.",
        "genres": [{"id": 27, "name": "Horror"}, {"id": 9648, "name": "Mystery"}],
        "keywords": [{"id": 34, "name": "supernatural"}, {"id": 35, "name": "isolation"}, {"id": 36, "name": "folklore"}, {"id": 37, "name": "lake"}],
        "release_date": "2022-10-14",
        "runtime": 99,
        "popularity": 66.8,
        "vote_average": 7.1,
        "vote_count": 1650,
        "director": "Julian Graves",
        "cast": [
            {"name": "Mia Goth", "character": "Astrid Lind"},
            {"name": "Dan Stevens", "character": "Father Caleb"},
            {"name": "Rebecca Hall", "character": "Sheriff Nora"},
            {"name": "Stellan Skarsgard", "character": "Old Man Halvard"},
            {"name": "Anya Taylor-Joy", "character": "The Drowned Girl"}
        ]
    },
    {
        "id": 10013,
        "title": "Autumn in Verona",
        "tagline": "Some melodies take a lifetime to compose.",
        "overview": "A celebrated concert pianist who lost his inspiration meets an energetic architectural restorer in the sun-drenched courtyards of northern Italy.",
        "genres": [{"id": 10749, "name": "Romance"}, {"id": 18, "name": "Drama"}, {"id": 10402, "name": "Music"}],
        "keywords": [{"id": 38, "name": "piano"}, {"id": 39, "name": "classical music"}, {"id": 40, "name": "italy"}, {"id": 41, "name": "soulmates"}],
        "release_date": "2021-09-24",
        "runtime": 118,
        "popularity": 62.1,
        "vote_average": 7.8,
        "vote_count": 1780,
        "director": "Sofia Bertolucci",
        "cast": [
            {"name": "Timothee Chalamet", "character": "Matteo Rossi"},
            {"name": "Dakota Johnson", "character": "Clara Bell"},
            {"name": "Luca Marinelli", "character": "Gianluca"},
            {"name": "Isabella Rossellini", "character": "Nonna Maria"},
            {"name": "Stanley Tucci", "character": "Maestro Lorenzo"}
        ]
    },
    {
        "id": 10014,
        "title": "Postcards from Capri",
        "tagline": "Love is always worth the detour.",
        "overview": "Two estranged writers are accidentally double-booked at a cliffside villa in Capri, forced to collaborate on a screenplay about second chances.",
        "genres": [{"id": 10749, "name": "Romance"}, {"id": 35, "name": "Comedy"}, {"id": 18, "name": "Drama"}],
        "keywords": [{"id": 40, "name": "italy"}, {"id": 41, "name": "soulmates"}, {"id": 42, "name": "writer"}, {"id": 43, "name": "villa"}],
        "release_date": "2023-05-19",
        "runtime": 106,
        "popularity": 60.5,
        "vote_average": 7.5,
        "vote_count": 1510,
        "director": "Sofia Bertolucci",
        "cast": [
            {"name": "Dakota Johnson", "character": "Gwen Howard"},
            {"name": "Andrew Garfield", "character": "Julian Thorne"},
            {"name": "Stanley Tucci", "character": "Enzo"},
            {"name": "Rachel McAdams", "character": "Sophie"},
            {"name": "Luca Marinelli", "character": "Marco"}
        ]
    },
    {
        "id": 10015,
        "title": "Ironclad Protocol",
        "tagline": "Duty has no exit strategy.",
        "overview": "When rogue operatives hijack an autonomous stealth submarine carrying nuclear launch triggers, a lone Navy SEAL officer trapped inside must dismantle the threat.",
        "genres": [{"id": 28, "name": "Action"}, {"id": 53, "name": "Thriller"}],
        "keywords": [{"id": 44, "name": "submarine"}, {"id": 45, "name": "navy seal"}, {"id": 46, "name": "hostage crisis"}, {"id": 47, "name": "military"}],
        "release_date": "2019-07-12",
        "runtime": 124,
        "popularity": 75.3,
        "vote_average": 7.1,
        "vote_count": 2600,
        "director": "Chadwick Stone",
        "cast": [
            {"name": "Gerard Butler", "character": "Commander James Kelly"},
            {"name": "Michael B. Jordan", "character": "Lieutenant Tyler Cross"},
            {"name": "Gary Oldman", "character": "Admiral Henderson"},
            {"name": "Common", "character": "Chief Hayes"},
            {"name": "Toby Kebbell", "character": "Vargas"}
        ]
    },
    {
        "id": 10016,
        "title": "Ironclad: Apex Strike",
        "tagline": "The sky is the battlefield.",
        "overview": "Commander James Kelly leads a rapid-response aerial assault team to recapture a hijacked Himalayan satellite control station before global air grids fail.",
        "genres": [{"id": 28, "name": "Action"}, {"id": 53, "name": "Thriller"}, {"id": 12, "name": "Adventure"}],
        "keywords": [{"id": 45, "name": "navy seal"}, {"id": 47, "name": "military"}, {"id": 48, "name": "himalayas"}, {"id": 49, "name": "satellite"}],
        "release_date": "2022-11-18",
        "runtime": 120,
        "popularity": 73.0,
        "vote_average": 6.9,
        "vote_count": 1980,
        "director": "Chadwick Stone",
        "cast": [
            {"name": "Gerard Butler", "character": "Commander James Kelly"},
            {"name": "Frank Grillo", "character": "Colonel Stone"},
            {"name": "Michael B. Jordan", "character": "Tyler Cross"},
            {"name": "Olga Kurylenko", "character": "Agent Danica"},
            {"name": "Hiroyuki Sanada", "character": "General Kudo"}
        ]
    },
    {
        "id": 10017,
        "title": "The Cipher of Alexandria",
        "tagline": "History's greatest puzzle is armed.",
        "overview": "An adventurous cryptographer and a sarcastic rogue antiquities dealer race across Egypt and Greece to decode a lost papyrus containing the formula for Greek fire.",
        "genres": [{"id": 12, "name": "Adventure"}, {"id": 28, "name": "Action"}, {"id": 9648, "name": "Mystery"}],
        "keywords": [{"id": 50, "name": "cryptography"}, {"id": 51, "name": "archaeology"}, {"id": 52, "name": "ancient relics"}, {"id": 53, "name": "treasure hunt"}],
        "release_date": "2021-05-28",
        "runtime": 132,
        "popularity": 86.9,
        "vote_average": 7.8,
        "vote_count": 3400,
        "director": "Harrison Blake",
        "cast": [
            {"name": "Tom Holland", "character": "Leo Vance"},
            {"name": "Zendaya", "character": "Dr. Miriam Fay"},
            {"name": "Harrison Ford", "character": "Professor Harold Fay"},
            {"name": "Antonio Banderas", "character": "Don Rafael Montero"},
            {"name": "Mark Wahlberg", "character": "Victor Sully"}
        ]
    },
    {
        "id": 10018,
        "title": "The Cipher of Babylon",
        "tagline": "The cradle of civilization holds its darkest secret.",
        "overview": "Leo Vance and Miriam reunite in the deserts of Mesopotamia when a secret society excavates a ziggurat concealing an ancient electromagnetic engine.",
        "genres": [{"id": 12, "name": "Adventure"}, {"id": 9648, "name": "Mystery"}, {"id": 878, "name": "Science Fiction"}],
        "keywords": [{"id": 50, "name": "cryptography"}, {"id": 51, "name": "archaeology"}, {"id": 52, "name": "ancient relics"}, {"id": 54, "name": "secret society"}],
        "release_date": "2024-04-19",
        "runtime": 136,
        "popularity": 89.4,
        "vote_average": 7.7,
        "vote_count": 2750,
        "director": "Harrison Blake",
        "cast": [
            {"name": "Tom Holland", "character": "Leo Vance"},
            {"name": "Zendaya", "character": "Dr. Miriam Fay"},
            {"name": "Oscar Isaac", "character": "Malik Al-Sayed"},
            {"name": "Harrison Ford", "character": "Professor Harold Fay"},
            {"name": "Riz Ahmed", "character": "Tariq"}
        ]
    },
    {
        "id": 10019,
        "title": "Cul-de-sac Chaos",
        "tagline": "Good fences make bad neighbors.",
        "overview": "An overzealous suburban homeowner's association president sparks an escalating neighborhood turf war over an artisanal backyard pizza oven.",
        "genres": [{"id": 35, "name": "Comedy"}],
        "keywords": [{"id": 55, "name": "suburbia"}, {"id": 56, "name": "neighborhood rivalry"}, {"id": 57, "name": "pranks"}, {"id": 58, "name": "absurd comedy"}],
        "release_date": "2020-07-17",
        "runtime": 96,
        "popularity": 54.3,
        "vote_average": 6.8,
        "vote_count": 1300,
        "director": "Greg Daniels",
        "cast": [
            {"name": "Steve Carell", "character": "Arthur Pendelton"},
            {"name": "Paul Rudd", "character": "Dave Miller"},
            {"name": "Kathryn Hahn", "character": "Brenda Pendelton"},
            {"name": "Will Ferrell", "character": "Officer Bob"},
            {"name": "Maya Rudolph", "character": "Karen Miller"}
        ]
    },
    {
        "id": 10020,
        "title": "The Backyard Olympics",
        "tagline": "Glory. Pride. Lawn chairs.",
        "overview": "When the city cancels the annual community fair, rival dads Dave Miller and Arthur Pendelton turn their suburban street into a fierce tournament of ridiculous games.",
        "genres": [{"id": 35, "name": "Comedy"}, {"id": 10751, "name": "Family"}],
        "keywords": [{"id": 55, "name": "suburbia"}, {"id": 56, "name": "neighborhood rivalry"}, {"id": 59, "name": "sports parody"}, {"id": 58, "name": "absurd comedy"}],
        "release_date": "2022-08-05",
        "runtime": 94,
        "popularity": 56.1,
        "vote_average": 6.7,
        "vote_count": 1180,
        "director": "Greg Daniels",
        "cast": [
            {"name": "Steve Carell", "character": "Arthur Pendelton"},
            {"name": "Paul Rudd", "character": "Dave Miller"},
            {"name": "Jason Sudeikis", "character": "Coach Ted"},
            {"name": "Kathryn Hahn", "character": "Brenda Pendelton"},
            {"name": "Will Ferrell", "character": "Officer Bob"}
        ]
    },
    {
        "id": 10021,
        "title": "Dune of Ash",
        "tagline": "Power belongs to those who control the dust.",
        "overview": "On an arid, resource-starved desert colony, a young visionary prince must wage an asymmetrical guerrilla campaign against imperial legions to liberate the indigenous clans.",
        "genres": [{"id": 878, "name": "Science Fiction"}, {"id": 12, "name": "Adventure"}, {"id": 18, "name": "Drama"}],
        "keywords": [{"id": 60, "name": "desert planet"}, {"id": 61, "name": "prophecy"}, {"id": 62, "name": "imperial war"}, {"id": 63, "name": "spice"}],
        "release_date": "2021-10-22",
        "runtime": 156,
        "popularity": 98.7,
        "vote_average": 8.5,
        "vote_count": 5200,
        "director": "Denis Villeneuve",
        "cast": [
            {"name": "Timothee Chalamet", "character": "Paul Atreides"},
            {"name": "Zendaya", "character": "Chani"},
            {"name": "Rebecca Ferguson", "character": "Lady Jessica"},
            {"name": "Oscar Isaac", "character": "Duke Leto"},
            {"name": "Josh Brolin", "character": "Gurney Halleck"}
        ]
    },
    {
        "id": 10022,
        "title": "Dune of Ash: Prophecy",
        "tagline": "Destiny is carved in sand.",
        "overview": "Paul unites the Fremen tribes across the northern dunes to march on the imperial throne, balancing the vengeance of his family with visions of galactic holy war.",
        "genres": [{"id": 878, "name": "Science Fiction"}, {"id": 12, "name": "Adventure"}, {"id": 28, "name": "Action"}],
        "keywords": [{"id": 60, "name": "desert planet"}, {"id": 61, "name": "prophecy"}, {"id": 62, "name": "imperial war"}, {"id": 64, "name": "revolution"}],
        "release_date": "2024-03-01",
        "runtime": 166,
        "popularity": 104.2,
        "vote_average": 8.7,
        "vote_count": 6100,
        "director": "Denis Villeneuve",
        "cast": [
            {"name": "Timothee Chalamet", "character": "Paul Atreides"},
            {"name": "Zendaya", "character": "Chani"},
            {"name": "Florence Pugh", "character": "Princess Irulan"},
            {"name": "Austin Butler", "character": "Feyd-Rautha"},
            {"name": "Javier Bardem", "character": "Stilgar"}
        ]
    },
    {
        "id": 10023,
        "title": "Sicario: Borderline",
        "tagline": "The border is a mirage.",
        "overview": "An idealistic FBI agent is enlisted by an enigmatic government task force operating in the lawless border zone between Texas and Mexico to hunt a shadowy cartel kingpin.",
        "genres": [{"id": 80, "name": "Crime"}, {"id": 18, "name": "Drama"}, {"id": 53, "name": "Thriller"}],
        "keywords": [{"id": 65, "name": "drug cartel"}, {"id": 66, "name": "fbi"}, {"id": 67, "name": "border"}, {"id": 68, "name": "moral ambiguity"}],
        "release_date": "2015-10-02",
        "runtime": 121,
        "popularity": 82.3,
        "vote_average": 8.0,
        "vote_count": 4100,
        "director": "Denis Villeneuve",
        "cast": [
            {"name": "Emily Blunt", "character": "Kate Macer"},
            {"name": "Benicio del Toro", "character": "Alejandro Gillick"},
            {"name": "Josh Brolin", "character": "Matt Graver"},
            {"name": "Daniel Kaluuya", "character": "Reggie Wayne"},
            {"name": "Jon Bernthal", "character": "Ted"}
        ]
    },
    {
        "id": 10024,
        "title": "Labyrinth of Solitude",
        "tagline": "In the maze of the mind, every mirror lies.",
        "overview": "A psychoanalyst enters the surreal dreamscape of a comatose billionaire to extract the launch codes for a global neurological network.",
        "genres": [{"id": 878, "name": "Science Fiction"}, {"id": 9648, "name": "Mystery"}, {"id": 53, "name": "Thriller"}],
        "keywords": [{"id": 69, "name": "dreams"}, {"id": 70, "name": "subconscious"}, {"id": 71, "name": "virtual reality"}, {"id": 72, "name": "psychological thriller"}],
        "release_date": "2018-09-07",
        "runtime": 134,
        "popularity": 77.2,
        "vote_average": 8.1,
        "vote_count": 3300,
        "director": "Elena Vance",
        "cast": [
            {"name": "Leonardo DiCaprio", "character": "Dr. Cobb"},
            {"name": "Marion Cotillard", "character": "Mal"},
            {"name": "Joseph Gordon-Levitt", "character": "Arthur"},
            {"name": "Elliot Page", "character": "Ariadne"},
            {"name": "Tom Hardy", "character": "Eames"}
        ]
    },
    {
        "id": 10025,
        "title": "Spectral Shift",
        "tagline": "They hear what light cannot reveal.",
        "overview": "A deep-sea acoustic research station records rhythmic bio-signals in the Mariana Trench that originate from an ancient non-terrestrial civilization beneath the oceanic crust.",
        "genres": [{"id": 878, "name": "Science Fiction"}, {"id": 27, "name": "Horror"}, {"id": 9648, "name": "Mystery"}],
        "keywords": [{"id": 73, "name": "deep sea"}, {"id": 74, "name": "alien contact"}, {"id": 75, "name": "claustrophobia"}, {"id": 76, "name": "trench"}],
        "release_date": "2020-01-10",
        "runtime": 112,
        "popularity": 70.1,
        "vote_average": 7.2,
        "vote_count": 2200,
        "director": "Julian Graves",
        "cast": [
            {"name": "Kristen Stewart", "character": "Norah Price"},
            {"name": "Vincent Cassel", "character": "Captain Lucien"},
            {"name": "T.J. Miller", "character": "Paul"},
            {"name": "John Gallagher Jr.", "character": "Liam"},
            {"name": "Jessica Henwick", "character": "Emily"}
        ]
    },
    {
        "id": 10026,
        "title": "Catering to Chaos",
        "tagline": "Too many cooks burn down the kitchen.",
        "overview": "A high-strung Michelin star chef takes a job catering an eccentric billionaire's three-day yacht wedding, where mafia enforcers and runaway pet tigers ruin the souffles.",
        "genres": [{"id": 35, "name": "Comedy"}, {"id": 18, "name": "Drama"}],
        "keywords": [{"id": 77, "name": "cooking"}, {"id": 78, "name": "restaurant"}, {"id": 79, "name": "yacht"}, {"id": 80, "name": "wedding chaos"}],
        "release_date": "2022-11-25",
        "runtime": 105,
        "popularity": 61.2,
        "vote_average": 7.3,
        "vote_count": 1450,
        "director": "Greg Daniels",
        "cast": [
            {"name": "Jeremy Allen White", "character": "Chef Carmy Thorne"},
            {"name": "Ayo Edebiri", "character": "Sydney"},
            {"name": "Ebon Moss-Bachrach", "character": "Richie"},
            {"name": "Paul Rudd", "character": "Groom Bradley"},
            {"name": "Kathryn Hahn", "character": "Wedding Planner Viv"}
        ]
    },
    {
        "id": 10027,
        "title": "Serengeti Solitude",
        "tagline": "The wild keeps its own score.",
        "overview": "A wildlife cinematographer tracking an elusive snow leopard in the high Himalayas finds unexpected kinship with a local nomadic elder protecting a sacred valley.",
        "genres": [{"id": 99, "name": "Documentary"}, {"id": 12, "name": "Adventure"}, {"id": 18, "name": "Drama"}],
        "keywords": [{"id": 81, "name": "wildlife"}, {"id": 82, "name": "himalayas"}, {"id": 83, "name": "nature"}, {"id": 84, "name": "nomad"}],
        "release_date": "2021-04-16",
        "runtime": 92,
        "popularity": 51.4,
        "vote_average": 8.2,
        "vote_count": 980,
        "director": "Maya Lin",
        "cast": [
            {"name": "Sylvain Tesson", "character": "Narrator"},
            {"name": "Vincent Munier", "character": "Self"},
            {"name": "David Attenborough", "character": "Special Voice"}
        ]
    },
    {
        "id": 10028,
        "title": "The Heist at Grand Palais",
        "tagline": "Steal the painting. Keep the glory.",
        "overview": "A charming international art thief assembles a crew of specialists to swap the Mona Lisa's secret companion portrait during the Parisian fashion week gala.",
        "genres": [{"id": 80, "name": "Crime"}, {"id": 35, "name": "Comedy"}, {"id": 28, "name": "Action"}],
        "keywords": [{"id": 85, "name": "art heist"}, {"id": 86, "name": "paris"}, {"id": 87, "name": "con artist"}, {"id": 88, "name": "caper"}],
        "release_date": "2023-01-27",
        "runtime": 117,
        "popularity": 76.8,
        "vote_average": 7.5,
        "vote_count": 2100,
        "director": "Jean-Luc Moreau",
        "cast": [
            {"name": "Vincent Cassel", "character": "Pierre Beaumont"},
            {"name": "Marion Cotillard", "character": "Gisele"},
            {"name": "George Clooney", "character": "Danny Ocean"},
            {"name": "Brad Pitt", "character": "Rusty Ryan"},
            {"name": "Matt Damon", "character": "Linus Caldwell"}
        ]
    },
    {
        "id": 10029,
        "title": "Midnight Run to Monte Carlo",
        "tagline": "Two thieves. One diamond. Zero rules.",
        "overview": "Pierre Beaumont returns to the French Riviera for a high-stakes duel against his former mentor, aiming to steal the Blue Regent diamond from a floating casino.",
        "genres": [{"id": 80, "name": "Crime"}, {"id": 35, "name": "Comedy"}, {"id": 53, "name": "Thriller"}],
        "keywords": [{"id": 85, "name": "art heist"}, {"id": 89, "name": "casino"}, {"id": 90, "name": "monaco"}, {"id": 87, "name": "con artist"}],
        "release_date": "2024-06-21",
        "runtime": 114,
        "popularity": 74.3,
        "vote_average": 7.3,
        "vote_count": 1620,
        "director": "Jean-Luc Moreau",
        "cast": [
            {"name": "Vincent Cassel", "character": "Pierre Beaumont"},
            {"name": "Lea Seydoux", "character": "Madeline"},
            {"name": "Jean Reno", "character": "Casino Inspector Leclair"},
            {"name": "Daniel Bruhl", "character": "Klaus"},
            {"name": "Mads Mikkelsen", "character": "The Banker"}
        ]
    },
    {
        "id": 10030,
        "title": "The Last Samurai of Kyoto",
        "tagline": "Honor outlives empires.",
        "overview": "During the Meiji restoration, an aging samurai swordsman protects an orphanage against corrupt industrial barons attempting to seize historical temple grounds.",
        "genres": [{"id": 28, "name": "Action"}, {"id": 18, "name": "Drama"}, {"id": 36, "name": "History"}],
        "keywords": [{"id": 91, "name": "samurai"}, {"id": 92, "name": "kyoto"}, {"id": 93, "name": "martial arts"}, {"id": 94, "name": "bushido"}],
        "release_date": "2019-11-22",
        "runtime": 142,
        "popularity": 80.9,
        "vote_average": 8.3,
        "vote_count": 3100,
        "director": "Kenji Watanabe",
        "cast": [
            {"name": "Hiroyuki Sanada", "character": "Jubei Yamada"},
            {"name": "Ken Watanabe", "character": "Lord Katsumoto"},
            {"name": "Tadanobu Asano", "character": "Inspector Kato"},
            {"name": "Koji Yakusho", "character": "Master Zen"},
            {"name": "Rinko Kikuchi", "character": "Chiyo"}
        ]
    },
    {
        "id": 10031,
        "title": "Shadow Blade",
        "tagline": "The sword remembers every tear.",
        "overview": "Jubei Yamada's final disciple travels into Edo to avenge her slaughtered clan, confronting ruthless ninjas employed by the Shogunate.",
        "genres": [{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 18, "name": "Drama"}],
        "keywords": [{"id": 91, "name": "samurai"}, {"id": 93, "name": "martial arts"}, {"id": 95, "name": "ninja"}, {"id": 25, "name": "revenge"}],
        "release_date": "2022-09-09",
        "runtime": 130,
        "popularity": 79.4,
        "vote_average": 7.9,
        "vote_count": 2250,
        "director": "Kenji Watanabe",
        "cast": [
            {"name": "Rinko Kikuchi", "character": "Kaede"},
            {"name": "Hiroyuki Sanada", "character": "Jubei Yamada (Ghost)"},
            {"name": "Tadanobu Asano", "character": "Shadow Lord"},
            {"name": "Anna Sawai", "character": "Yukiko"},
            {"name": "Andrew Koji", "character": "Ren"}
        ]
    },
    {
        "id": 10032,
        "title": "Sunset over the Seine",
        "tagline": "Paris was never just a city.",
        "overview": "A bookstore clerk in the Latin Quarter and a touring cellist strike up an unforgettable 24-hour romance walking along the bridges of Paris before sunrise.",
        "genres": [{"id": 10749, "name": "Romance"}, {"id": 18, "name": "Drama"}],
        "keywords": [{"id": 86, "name": "paris"}, {"id": 41, "name": "soulmates"}, {"id": 96, "name": "brief encounter"}, {"id": 97, "name": "philosophy"}],
        "release_date": "2020-02-14",
        "runtime": 101,
        "popularity": 65.4,
        "vote_average": 8.0,
        "vote_count": 2150,
        "director": "Sofia Bertolucci",
        "cast": [
            {"name": "Timothee Chalamet", "character": "Etienne"},
            {"name": "Saoirse Ronan", "character": "Claire"},
            {"name": "Vincent Cassel", "character": "Cafe Proprietor"},
            {"name": "Marion Cotillard", "character": "Madame Vivienne"},
            {"name": "Ethan Hawke", "character": "Writer in Residence"}
        ]
    },
    {
        "id": 10033,
        "title": "Aetherium: The Sky Islands",
        "tagline": "Look up. That is where we belong.",
        "overview": "In a steampunk fantasy realm where magnetic islands float among the clouds, a young skyship captain and an alchemist race against an iron sky armada.",
        "genres": [{"id": 14, "name": "Fantasy"}, {"id": 12, "name": "Adventure"}, {"id": 16, "name": "Animation"}],
        "keywords": [{"id": 98, "name": "steampunk"}, {"id": 99, "name": "floating islands"}, {"id": 100, "name": "airships"}, {"id": 101, "name": "alchemy"}],
        "release_date": "2023-08-18",
        "runtime": 115,
        "popularity": 87.3,
        "vote_average": 8.2,
        "vote_count": 3100,
        "director": "Maya Lin",
        "cast": [
            {"name": "Florence Pugh", "character": "Captain Zephyr"},
            {"name": "Dev Patel", "character": "Alchemist Kaelen"},
            {"name": "Mark Hamill", "character": "Iron Chancellor (voice)"},
            {"name": "Cate Blanchett", "character": "Queen of Clouds (voice)"},
            {"name": "Taika Waititi", "character": "Gimmick (voice)"}
        ]
    },
    {
        "id": 10034,
        "title": "Aetherium: Clockwork Realm",
        "tagline": "The sky is winding down.",
        "overview": "Zephyr and Kaelen seek the subterranean clockwork gears that anchor the floating islands before the atmospheric core runs out of steam.",
        "genres": [{"id": 14, "name": "Fantasy"}, {"id": 12, "name": "Adventure"}, {"id": 28, "name": "Action"}],
        "keywords": [{"id": 98, "name": "steampunk"}, {"id": 99, "name": "floating islands"}, {"id": 100, "name": "airships"}, {"id": 102, "name": "clockwork"}],
        "release_date": "2025-02-14",
        "runtime": 120,
        "popularity": 91.5,
        "vote_average": 8.0,
        "vote_count": 1890,
        "director": "Maya Lin",
        "cast": [
            {"name": "Florence Pugh", "character": "Captain Zephyr"},
            {"name": "Dev Patel", "character": "Alchemist Kaelen"},
            {"name": "Gary Oldman", "character": "Arch-Mechanic Chronos"},
            {"name": "Cate Blanchett", "character": "Queen of Clouds (voice)"},
            {"name": "Zendaya", "character": "Tink (voice)"}
        ]
    },
    {
        "id": 10035,
        "title": "The Crimson Vanguard",
        "tagline": "In the trenches of tomorrow, humanity fights for dawn.",
        "overview": "Elite mechanized infantry soldiers defend the outer perimeter of human civilization against an alien swarm that adapts instantly to every ballistic projectile.",
        "genres": [{"id": 28, "name": "Action"}, {"id": 878, "name": "Science Fiction"}, {"id": 53, "name": "Thriller"}],
        "keywords": [{"id": 103, "name": "mecha"}, {"id": 104, "name": "alien invasion"}, {"id": 105, "name": "military sci-fi"}, {"id": 106, "name": "swarm"}],
        "release_date": "2021-08-06",
        "runtime": 125,
        "popularity": 83.7,
        "vote_average": 7.5,
        "vote_count": 2700,
        "director": "Chadwick Stone",
        "cast": [
            {"name": "Tom Cruise", "character": "Major Bill Cage"},
            {"name": "Emily Blunt", "character": "Rita Vrataski"},
            {"name": "Michael B. Jordan", "character": "Sergeant Vance"},
            {"name": "Bill Paxton", "character": "Master Sergeant Farell"},
            {"name": "Brendan Gleeson", "character": "General Brigham"}
        ]
    },
    {
        "id": 10036,
        "title": "Vanguard: Extinction Code",
        "tagline": "The swarm has evolved.",
        "overview": "Major Cage and Sergeant Vance launch a covert orbital insertion directly into the extraterrestrial hive node to detonate an antimatter EMP.",
        "genres": [{"id": 28, "name": "Action"}, {"id": 878, "name": "Science Fiction"}],
        "keywords": [{"id": 103, "name": "mecha"}, {"id": 104, "name": "alien invasion"}, {"id": 105, "name": "military sci-fi"}, {"id": 107, "name": "emp weapon"}],
        "release_date": "2023-11-10",
        "runtime": 128,
        "popularity": 80.2,
        "vote_average": 7.3,
        "vote_count": 2100,
        "director": "Chadwick Stone",
        "cast": [
            {"name": "Tom Cruise", "character": "Major Bill Cage"},
            {"name": "Emily Blunt", "character": "Rita Vrataski"},
            {"name": "Michael B. Jordan", "character": "Sergeant Vance"},
            {"name": "Frank Grillo", "character": "Commander Gage"},
            {"name": "Hiroyuki Sanada", "character": "General Kudo"}
        ]
    },
    {
        "id": 10037,
        "title": "The Scottish Playwright",
        "tagline": "All the world is a stage, and bloody is its curtain.",
        "overview": "A historical dark comedy following a struggling Edinburgh theater troupe staging Macbeth while accidentally getting entangled in real royal regicide.",
        "genres": [{"id": 35, "name": "Comedy"}, {"id": 18, "name": "Drama"}, {"id": 36, "name": "History"}],
        "keywords": [{"id": 108, "name": "shakespeare"}, {"id": 109, "name": "theater troupe"}, {"id": 110, "name": "edinburgh"}, {"id": 111, "name": "macbeth"}],
        "release_date": "2022-03-11",
        "runtime": 110,
        "popularity": 59.4,
        "vote_average": 7.6,
        "vote_count": 1350,
        "director": "Arthur Sterling",
        "cast": [
            {"name": "Benedict Cumberbatch", "character": "Hamish MacLeod"},
            {"name": "David Tennant", "character": "Rory Stewart"},
            {"name": "Emma Thompson", "character": "Duchess Margaret"},
            {"name": "Saoirse Ronan", "character": "Fiona"},
            {"name": "Tom Hiddleston", "character": "Lord Archibald"}
        ]
    },
    {
        "id": 10038,
        "title": "Whispers of the Deep",
        "tagline": "The abyss has a voice.",
        "overview": "Submarine oceanographers discover an ancient pre-human submerged necropolis broadcasting mathematical radio tones that trigger auditory hallucinations.",
        "genres": [{"id": 27, "name": "Horror"}, {"id": 878, "name": "Science Fiction"}, {"id": 9648, "name": "Mystery"}],
        "keywords": [{"id": 73, "name": "deep sea"}, {"id": 112, "name": "lovecraftian"}, {"id": 34, "name": "supernatural"}, {"id": 75, "name": "claustrophobia"}],
        "release_date": "2021-10-08",
        "runtime": 109,
        "popularity": 73.6,
        "vote_average": 7.4,
        "vote_count": 1940,
        "director": "Julian Graves",
        "cast": [
            {"name": "Rebecca Hall", "character": "Dr. Miriam Stern"},
            {"name": "Dan Stevens", "character": "Dr. Alan Cross"},
            {"name": "Toni Collette", "character": "Director Sarah Miller"},
            {"name": "Stellan Skarsgard", "character": "Chief Engineer Sven"},
            {"name": "Mia Goth", "character": "The Voice"}
        ]
    },
    {
        "id": 10039,
        "title": "Sovereignty: The Fall of Carthage",
        "tagline": "Empires are built on bone, not stone.",
        "overview": "The epic historical chronicle of Hannibal Barca's legendary tactical campaign across the Alps against the encroaching legions of Scipio Africanus.",
        "genres": [{"id": 28, "name": "Action"}, {"id": 18, "name": "Drama"}, {"id": 36, "name": "History"}, {"id": 10752, "name": "War"}],
        "keywords": [{"id": 113, "name": "ancient rome"}, {"id": 114, "name": "hannibal"}, {"id": 115, "name": "alps"}, {"id": 116, "name": "military tactics"}],
        "release_date": "2020-11-13",
        "runtime": 164,
        "popularity": 84.1,
        "vote_average": 8.2,
        "vote_count": 3600,
        "director": "Harrison Blake",
        "cast": [
            {"name": "Oscar Isaac", "character": "Hannibal Barca"},
            {"name": "Christian Bale", "character": "Scipio Africanus"},
            {"name": "Pedro Pascal", "character": "Hasdrubal Barca"},
            {"name": "Ben Kingsley", "character": "Hamilcar Barca"},
            {"name": "Riz Ahmed", "character": "Maharbal"}
        ]
    },
    {
        "id": 10040,
        "title": "Sovereignty: Pax Romana",
        "tagline": "Victory demands the ultimate sacrifice.",
        "overview": "Following the battle of Zama, Scipio Africanus confronts the Roman Senate while Hannibal seeks asylum in eastern kingdoms to mount one final resistance.",
        "genres": [{"id": 18, "name": "Drama"}, {"id": 36, "name": "History"}, {"id": 10752, "name": "War"}],
        "keywords": [{"id": 113, "name": "ancient rome"}, {"id": 114, "name": "hannibal"}, {"id": 16, "name": "political intrigue"}, {"id": 117, "name": "roman senate"}],
        "release_date": "2023-04-28",
        "runtime": 158,
        "popularity": 81.3,
        "vote_average": 8.1,
        "vote_count": 2800,
        "director": "Harrison Blake",
        "cast": [
            {"name": "Christian Bale", "character": "Scipio Africanus"},
            {"name": "Oscar Isaac", "character": "Hannibal Barca"},
            {"name": "Charles Dance", "character": "Senator Cato"},
            {"name": "Pedro Pascal", "character": "Hasdrubal Barca"},
            {"name": "Tom Hiddleston", "character": "Consul Tiberius"}
        ]
    }
]

def generate():
    movies_rows = []
    credits_rows = []
    
    for m in SYNTHETIC_MOVIES:
        # Movies row format
        movie_row = {
            "budget": 100000000,
            "genres": json.dumps(m["genres"]),
            "homepage": f"https://cinepulse.example.com/movies/{m['id']}",
            "id": m["id"],
            "keywords": json.dumps(m["keywords"]),
            "original_language": "en",
            "original_title": m["title"],
            "overview": m["overview"],
            "popularity": m["popularity"],
            "production_companies": json.dumps([{"name": "CinePulse Studios", "id": 999}]),
            "production_countries": json.dumps([{"iso_3166_1": "US", "name": "United States of America"}]),
            "release_date": m["release_date"],
            "revenue": int(m["popularity"] * 4000000),
            "runtime": m["runtime"],
            "spoken_languages": json.dumps([{"iso_639_1": "en", "name": "English"}]),
            "status": "Released",
            "tagline": m["tagline"],
            "title": m["title"],
            "vote_average": m["vote_average"],
            "vote_count": m["vote_count"]
        }
        movies_rows.append(movie_row)
        
        # Credits row format
        cast_list = []
        for idx, actor in enumerate(m["cast"]):
            cast_list.append({
                "cast_id": idx + 1,
                "character": actor["character"],
                "credit_id": f"c_{m['id']}_{idx+1}",
                "gender": 2 if idx % 2 == 0 else 1,
                "id": 50000 + idx,
                "name": actor["name"],
                "order": idx
            })
            
        crew_list = [
            {
                "credit_id": f"cr_{m['id']}_dir",
                "department": "Directing",
                "gender": 2,
                "id": 40000,
                "job": "Director",
                "name": m["director"]
            },
            {
                "credit_id": f"cr_{m['id']}_wri",
                "department": "Writing",
                "gender": 2,
                "id": 40001,
                "job": "Writer",
                "name": m["director"]
            }
        ]
        
        credits_row = {
            "movie_id": m["id"],
            "title": m["title"],
            "cast": json.dumps(cast_list),
            "crew": json.dumps(crew_list)
        }
        credits_rows.append(credits_row)

    movies_path = FIXTURES_DIR / "synthetic_tmdb_movies.csv"
    credits_path = FIXTURES_DIR / "synthetic_tmdb_credits.csv"
    
    # Write movies CSV
    movie_fieldnames = list(movies_rows[0].keys())
    with open(movies_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=movie_fieldnames)
        writer.writeheader()
        writer.writerows(movies_rows)
        
    # Write credits CSV
    credits_fieldnames = list(credits_rows[0].keys())
    with open(credits_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=credits_fieldnames)
        writer.writeheader()
        writer.writerows(credits_rows)
        
    print(f"Successfully generated {len(movies_rows)} synthetic movies fixture:")
    print(f" -> {movies_path}")
    print(f" -> {credits_path}")

if __name__ == "__main__":
    generate()
