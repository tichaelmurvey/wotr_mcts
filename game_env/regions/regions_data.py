from collections import namedtuple
from game_env.game_env_enums import Nation
from game_env.regions.region import Region, RegionFeature
from game_env.regions_enum import R


N = Nation


def f(*args):
    return set(args)


test = namedtuple("test", ["aaax", "dfdfdfdf"])

regions_init = (
    # === ELVES ===
    Region(
        R.GREY_HAVENS,
        "Grey Havens",
        nation=N.ELVES,
        adj_regions=f(R.TOWER_HILLS, R.FORLINDON, R.HARLINDON, R.ERED_LUIN),
        features=f(RegionFeature.STRONGHOLD, RegionFeature.COASTAL),
    ),
    Region(
        R.RIVENDELL,
        "Rivendell",
        nation=N.ELVES,
        adj_regions=f(R.TROLLSHAWS, R.FORDS_OF_BRUINEN),
        features=f(RegionFeature.STRONGHOLD),
    ),
    Region(
        R.WOODLAND_REALM,
        "Woodland Realm",
        nation=N.ELVES,
        adj_regions=f(
            R.NORTHERN_MIRKWOOD,
            R.DALE,
            R.OLD_FOREST_ROAD,
            R.WESTERN_MIRKWOOD,
            R.WITHERED_HEATH,
        ),
        features=f(RegionFeature.STRONGHOLD),
    ),
    Region(
        R.LORIEN,
        "Lorien",
        adj_regions=f(R.DIMRILL_DALE, R.PARTH_CELEBRANT),
        nation=N.ELVES,
        features=f(RegionFeature.STRONGHOLD),
    ),
    # === NORTH  ===
    Region(
        R.THE_SHIRE,
        "The Shire",
        nation=N.NORTH,
        adj_regions=f(
            R.TOWER_HILLS, R.BUCKLAND, R.OLD_FOREST, R.SOUTH_ERED_LUIN, R.EVENDIM
        ),
        features=f(RegionFeature.CITY),
    ),
    Region(
        R.BUCKLAND,
        "Buckland",
        nation=N.NORTH,
        adj_regions=f(
            R.THE_SHIRE,
            R.OLD_FOREST,
            R.SOUTH_DOWNS,
            R.BREE,
            R.NORTH_DOWNS,
            R.EVENDIM,
            R.CARDOLAN,
        ),
    ),
    Region(
        R.BREE,
        "Bree",
        nation=N.NORTH,
        adj_regions=f(R.NORTH_DOWNS, R.SOUTH_DOWNS, R.WEATHER_HILLS, R.BUCKLAND),
        features=f(RegionFeature.TOWN),
    ),
    Region(
        R.OLD_FOREST_ROAD,
        "Old Forest Road",
        nation=N.NORTH,
        adj_regions=f(
            R.WOODLAND_REALM,
            R.EASTERN_MIRKWOOD,
            R.WESTERN_MIRKWOOD,
            R.NARROWS_OF_THE_FOREST,
            R.RHOSGOBEL,
            R.DALE,
            R.NORTHERN_RHOVANION,
            R.CARROCK,
        ),
    ),
    Region(
        R.NORTH_DOWNS,
        "North Downs",
        adj_regions=f(
            R.EVENDIM, R.ARNOR, R.ETTENMOORS, R.WEATHER_HILLS, R.BREE, R.BUCKLAND
        ),
    ),
    Region(
        R.CARROCK,
        "Carrock",
        adj_regions=f(
            R.EAGLES_EYRIE,
            R.OLD_FORD,
            R.RHOSGOBEL,
            R.NORTHERN_MIRKWOOD,
            R.WESTERN_MIRKWOOD,
            R.OLD_FOREST_ROAD,
        ),
        features=f(RegionFeature.TOWN),
    ),
    Region(
        R.RHOSGOBEL,
        "Rhosgobel",
        adj_regions=f(
            R.CARROCK,
            R.NORTH_ANDUIN_VALE,
            R.OLD_FORD,
            R.NARROWS_OF_THE_FOREST,
            R.GLADDEN_FIELDS,
            R.OLD_FOREST_ROAD,
        ),
    ),
    Region(
        R.DALE,
        "Dale",
        nation=N.NORTH,
        adj_regions=f(
            R.EREBOR,
            R.WOODLAND_REALM,
            R.NORTHERN_RHOVANION,
            R.VALE_OF_THE_CARNEN,
            R.IRON_HILLS,
            R.WITHERED_HEATH,
            R.OLD_FOREST_ROAD,
        ),
        features=f(RegionFeature.CITY),
    ),
    # === DWARVES (brown border) ===
    Region(
        R.IRON_HILLS,
        "Iron Hills",
        nation=N.DWARVES,
        adj_regions=f(R.EREBOR, R.VALE_OF_THE_CARNEN, R.EAST_RHUN, R.DALE),
        features=f(RegionFeature.TOWN, RegionFeature.EASTERN),
    ),
    Region(
        R.EREBOR,
        "Erebor",
        nation=N.DWARVES,
        adj_regions=f(R.IRON_HILLS, R.DALE, R.WITHERED_HEATH),
        features=f(RegionFeature.STRONGHOLD),
    ),
    Region(
        R.ERED_LUIN,
        "Ered Luin",
        nation=N.DWARVES,
        adj_regions=f(R.NORTH_ERED_LUIN, R.GREY_HAVENS, R.TOWER_HILLS, R.EVENDIM),
        features=f(RegionFeature.TOWN),
    ),
    Region(
        R.NORTH_ERED_LUIN,
        "North Ered Luin",
        nation=N.DWARVES,
        adj_regions=f(R.ERED_LUIN, R.EVENDIM),
        features=f(RegionFeature.COASTAL),
    ),
    # === GONDOR (dark blue border) ===
    Region(
        R.ANFALAS,
        "Anfalas",
        nation=N.GONDOR,
        adj_regions=f(R.ANDRAST, R.ERECH, R.DOL_AMROTH),
        features=f(RegionFeature.COASTAL),
    ),
    Region(
        R.ERECH,
        "Erech",
        nation=N.GONDOR,
        adj_regions=f(R.ANFALAS, R.DOL_AMROTH, R.LAMEDON),
    ),
    Region(
        R.DOL_AMROTH,
        "Dol Amroth",
        nation=N.GONDOR,
        adj_regions=f(R.ANFALAS, R.ERECH, R.LAMEDON),
        features=f(RegionFeature.STRONGHOLD, RegionFeature.COASTAL),
    ),
    Region(
        R.LAMEDON,
        "Lamedon",
        nation=N.GONDOR,
        adj_regions=f(R.ERECH, R.DOL_AMROTH, R.PELARGIR),
        features=f(RegionFeature.TOWN, RegionFeature.COASTAL),
    ),
    Region(
        R.PELARGIR,
        "Pelargir",
        nation=N.GONDOR,
        adj_regions=f(R.LAMEDON, R.LOSSARNACH, R.WEST_HARONDOR, R.OSGILIATH),
        features=f(RegionFeature.CITY, RegionFeature.COASTAL),
    ),
    Region(
        R.MINAS_TIRITH,
        "Minas Tirith",
        nation=N.GONDOR,
        adj_regions=f(R.DRUADAN_FOREST, R.OSGILIATH, R.LOSSARNACH),
        features=f(RegionFeature.STRONGHOLD),
    ),
    Region(
        R.DRUADAN_FOREST,
        "Druadan Forest",
        nation=N.GONDOR,
        adj_regions=f(
            R.MINAS_TIRITH,
            R.OSGILIATH,
            R.WESTERN_EMYN_MUIL,
            R.FOLDE,
            R.DEAD_MARSHES,
            R.EASTEMNET,
        ),
    ),
    Region(
        R.LOSSARNACH,
        "Lossarnach",
        nation=N.GONDOR,
        adj_regions=f(R.MINAS_TIRITH, R.PELARGIR, R.PELARGIR),
        features=f(RegionFeature.TOWN),
    ),
    # === ROHAN (dark green border) ===
    Region(
        R.FORDS_OF_ISEN,
        "Fords of Isen",
        nation=N.ROHAN,
        adj_regions=f(
            R.GAP_OF_ROHAN,
            R.HELMS_DEEP,
            R.WESTEMNET,
            R.DRUWAITH_IAUR,
            R.ORTHANC,
            R.FANGORN,
        ),
        features=f(RegionFeature.FORT),
    ),
    Region(
        R.HELMS_DEEP,
        "Helm's Deep",
        nation=N.ROHAN,
        adj_regions=f(R.FORDS_OF_ISEN, R.WESTEMNET),
        features=f(RegionFeature.STRONGHOLD),
    ),
    Region(
        R.WESTEMNET,
        "Westemnet",
        nation=N.ROHAN,
        adj_regions=f(
            R.FORDS_OF_ISEN, R.HELMS_DEEP, R.EDORAS, R.FANGORN, R.EASTEMNET, R.FOLDE
        ),
        features=f(RegionFeature.TOWN),
    ),
    Region(
        R.EDORAS,
        "Edoras",
        nation=N.ROHAN,
        adj_regions=f(R.WESTEMNET, R.FOLDE),
        features=f(RegionFeature.CITY),
    ),
    Region(
        R.FOLDE,
        "Folde",
        nation=N.ROHAN,
        adj_regions=f(R.EDORAS, R.DRUADAN_FOREST, R.EASTEMNET, R.WESTEMNET),
        features=f(RegionFeature.TOWN),
    ),
    Region(
        R.EASTEMNET,
        "Eastemnet",
        nation=N.ROHAN,
        adj_regions=f(
            R.DRUADAN_FOREST,
            R.FANGORN,
            R.PARTH_CELEBRANT,
            R.FOLDE,
            R.WESTERN_EMYN_MUIL,
            R.WESTEMNET,
            R.WESTERN_BROWN_LANDS,
        ),
    ),
    # SOUTHRONS AND EASTERLINGS
    Region(
        R.UMBAR,
        "Umbar",
        nation=N.ELINGS,
        adj_regions=f(R.WEST_HARONDOR, R.NEAR_HARAD),
        features=f(RegionFeature.STRONGHOLD, RegionFeature.COASTAL),
    ),
    Region(
        R.NEAR_HARAD,
        "Near Harad",
        nation=N.ELINGS,
        adj_regions=f(R.UMBAR, R.EAST_HARONDOR, R.FAR_HARAD, R.WEST_HARONDOR, R.KHAND),
        features=f(RegionFeature.TOWN),
    ),
    Region(
        R.FAR_HARAD,
        "Far Harad",
        nation=N.ELINGS,
        adj_regions=f(R.NEAR_HARAD, R.KHAND),
        features=f(RegionFeature.CITY, RegionFeature.EASTERN),
    ),
    Region(
        R.KHAND,
        "Khand",
        nation=N.ELINGS,
        adj_regions=f(R.NEAR_HARAD, R.FAR_HARAD),
        features=f(RegionFeature.EASTERN),
    ),
    Region(
        R.SOUTH_RHUN,
        "South Rhun",
        nation=N.ELINGS,
        adj_regions=f(R.ASH_MOUNTAINS, R.SOUTHERN_DORWINION, R.EAST_RHUN),
        features=f(RegionFeature.TOWN, RegionFeature.EASTERN),
    ),
    Region(
        R.NORTH_RHUN,
        "North Rhun",
        nation=N.ELINGS,
        adj_regions=f(
            R.EAST_RHUN,
            R.NORTHERN_DORWINION,
            R.VALE_OF_THE_CARNEN,
            R.VALE_OF_THE_CELDUIN,
        ),
        features=f(RegionFeature.TOWN),
    ),
    Region(
        R.EAST_RHUN,
        "East Rhun",
        nation=N.ELINGS,
        adj_regions=f(R.IRON_HILLS, R.NORTH_RHUN, R.SOUTH_RHUN, R.VALE_OF_THE_CARNEN),
        features=f(RegionFeature.EASTERN),
    ),
    # === MORDOR ===
    Region(
        R.MORIA,
        "Moria",
        nation=N.MORDOR,
        adj_regions=f(R.DIMRILL_DALE, R.HOLLIN, R.NORTH_DUNLAND),
        features=f(RegionFeature.STRONGHOLD),
    ),
    Region(
        R.MORANNON,
        "Morannon",
        nation=N.MORDOR,
        adj_regions=f(R.DAGORLAD, R.GORGOROTH),
        features=f(RegionFeature.STRONGHOLD),
    ),
    Region(
        R.MINAS_MORGUL,
        "Minas Morgul",
        nation=N.MORDOR,
        adj_regions=f(R.NORTH_ITHILIEN, R.GORGOROTH, R.SOUTH_ITHILIEN),
        features=f(RegionFeature.STRONGHOLD),
    ),
    Region(
        R.GORGOROTH,
        "Gorgoroth",
        nation=N.MORDOR,
        adj_regions=f(R.MINAS_MORGUL, R.BARAD_DUR, R.NURN, R.MORANNON),
        features=f(RegionFeature.EASTERN),
    ),
    Region(
        R.BARAD_DUR,
        "Barad-dur",
        nation=N.MORDOR,
        adj_regions=f(R.GORGOROTH),
        features=f(RegionFeature.STRONGHOLD),
    ),
    Region(
        R.MOUNT_GUNDABAD,
        "Mount Gundabad",
        nation=N.MORDOR,
        adj_regions=f(R.MOUNT_GRAM, R.EAGLES_EYRIE),
        features=f(RegionFeature.STRONGHOLD),
    ),
    Region(
        R.MOUNT_GRAM,
        "Mount Gram",
        nation=N.MORDOR,
        adj_regions=f(R.ANGMAR, R.ETTENMOORS, R.MOUNT_GUNDABAD),
    ),
    Region(R.NURN, "Nurn", nation=N.MORDOR, adj_regions=f(R.GORGOROTH)),
    Region(
        R.ANGMAR,
        "Angmar",
        nation=N.MORDOR,
        adj_regions=f(R.MOUNT_GRAM, R.ETTENMOORS, R.ARNOR),
        features=f(RegionFeature.CITY),
    ),
    Region(
        R.DOL_GULDUR,
        "Dol Guldur",
        nation=N.MORDOR,
        adj_regions=f(
            R.SOUTHERN_MIRKWOOD,
            R.NARROWS_OF_THE_FOREST,
            R.EASTERN_BROWN_LANDS,
            R.EASTERN_MIRKWOOD,
            R.SOUTH_ANDUIN_VALE,
            R.WESTERN_BROWN_LANDS,
            R.NORTH_ANDUIN_VALE,
        ),
        features=f(RegionFeature.STRONGHOLD),
    ),
    # === NEUTRAL ===
    Region(
        R.ARNOR,
        "Arnor",
        adj_regions=f(R.EVENDIM, R.NORTH_DOWNS, R.ETTENMOORS, R.ANGMAR),
        features=f(RegionFeature.COASTAL),
    ),
    Region(
        R.ETTENMOORS,
        "Ettenmoors",
        adj_regions=f(
            R.ARNOR,
            R.NORTH_DOWNS,
            R.MOUNT_GRAM,
            R.WEATHER_HILLS,
            R.TROLLSHAWS,
            R.ANGMAR,
        ),
    ),
    Region(
        R.TOWER_HILLS,
        "Tower Hills",
        adj_regions=f(
            R.GREY_HAVENS, R.THE_SHIRE, R.ERED_LUIN, R.EVENDIM, R.SOUTH_ERED_LUIN
        ),
    ),
    Region(
        R.FORLINDON,
        "Forlindon",
        adj_regions=f(
            R.GREY_HAVENS,
        ),
        features=f(RegionFeature.COASTAL),
    ),
    Region(
        R.HARLINDON,
        "Harlindon",
        adj_regions=f(R.GREY_HAVENS, R.SOUTH_ERED_LUIN),
        features=f(RegionFeature.COASTAL),
    ),
    Region(
        R.FORDS_OF_BRUINEN,
        "Fords of Bruinen",
        adj_regions=f(R.RIVENDELL, R.TROLLSHAWS, R.HIGH_PASS, R.HOLLIN),
    ),
    Region(
        R.NORTHERN_MIRKWOOD,
        "Northern Mirkwood",
        adj_regions=f(
            R.WOODLAND_REALM,
            R.WESTERN_MIRKWOOD,
            R.WITHERED_HEATH,
            R.CARROCK,
        ),
    ),
    Region(
        R.WESTERN_MIRKWOOD,
        "Western Mirkwood",
        adj_regions=f(
            R.NORTHERN_MIRKWOOD,
            R.CARROCK,
            R.OLD_FOREST_ROAD,
            R.WOODLAND_REALM,
        ),
    ),
    Region(
        R.EVENDIM,
        "Evendim",
        adj_regions=f(
            R.NORTH_ERED_LUIN,
            R.ERED_LUIN,
            R.NORTH_DOWNS,
            R.THE_SHIRE,
            R.ARNOR,
            R.TOWER_HILLS,
            R.BUCKLAND,
        ),
        features=f(RegionFeature.COASTAL),
    ),
    Region(
        R.SOUTH_ERED_LUIN,
        "South Ered Luin",
        adj_regions=f(
            R.TOWER_HILLS,
            R.THE_SHIRE,
            R.HARLINDON,
            R.OLD_FOREST,
            R.MINHIRIATH,
            R.CARDOLAN,
        ),
        features=f(RegionFeature.COASTAL),
    ),
    Region(
        R.CARDOLAN,
        "Cardolan",
        adj_regions=f(
            R.MINHIRIATH,
            R.THARBAD,
            R.SOUTH_DOWNS,
            R.OLD_FOREST,
            R.BUCKLAND,
            R.NORTH_DUNLAND,
            R.SOUTH_ERED_LUIN,
        ),
    ),
    Region(
        R.MINHIRIATH,
        "Minhiriath",
        adj_regions=f(R.SOUTH_ERED_LUIN, R.CARDOLAN, R.THARBAD, R.ENEDWAITH),
        features=f(RegionFeature.COASTAL),
    ),
    Region(
        R.THARBAD,
        "Tharbad",
        adj_regions=f(
            R.CARDOLAN, R.MINHIRIATH, R.ENEDWAITH, R.NORTH_DUNLAND, R.SOUTH_DUNLAND
        ),
    ),
    Region(
        R.SOUTH_DOWNS,
        "South Downs",
        adj_regions=f(
            R.BREE,
            R.BUCKLAND,
            R.CARDOLAN,
            R.WEATHER_HILLS,
            R.TROLLSHAWS,
            R.NORTH_DUNLAND,
            R.HOLLIN,
        ),
    ),
    Region(
        R.OLD_FOREST,
        "Old Forest",
        adj_regions=f(R.BUCKLAND, R.THE_SHIRE, R.SOUTH_ERED_LUIN, R.CARDOLAN),
    ),
    Region(
        R.WEATHER_HILLS,
        "Weather Hills",
        adj_regions=f(R.NORTH_DOWNS, R.BREE, R.TROLLSHAWS, R.ETTENMOORS, R.SOUTH_DOWNS),
    ),
    Region(
        R.TROLLSHAWS,
        "Trollshaws",
        adj_regions=f(
            R.WEATHER_HILLS,
            R.RIVENDELL,
            R.FORDS_OF_BRUINEN,
            R.ETTENMOORS,
            R.HOLLIN,
            R.SOUTH_DOWNS,
        ),
    ),
    Region(
        R.HOLLIN,
        "Hollin",
        adj_regions=f(
            R.FORDS_OF_BRUINEN, R.MORIA, R.SOUTH_DOWNS, R.TROLLSHAWS, R.NORTH_DUNLAND
        ),
    ),
    Region(
        R.EAGLES_EYRIE,
        "Eagle's Eyrie",
        adj_regions=f(R.CARROCK, R.OLD_FORD, R.MOUNT_GUNDABAD),
    ),
    Region(
        R.OLD_FORD,
        "Old Ford",
        adj_regions=f(
            R.CARROCK, R.RHOSGOBEL, R.GLADDEN_FIELDS, R.EAGLES_EYRIE, R.GOBLINS_GATE
        ),
    ),
    Region(
        R.GLADDEN_FIELDS,
        "Gladden Fields",
        adj_regions=f(R.OLD_FORD, R.NORTH_ANDUIN_VALE, R.DIMRILL_DALE, R.RHOSGOBEL),
    ),
    Region(
        R.DIMRILL_DALE,
        "Dimrill Dale",
        adj_regions=f(
            R.GLADDEN_FIELDS,
            R.LORIEN,
            R.MORIA,
            R.NORTH_ANDUIN_VALE,
            R.SOUTH_ANDUIN_VALE,
            R.PARTH_CELEBRANT,
        ),
    ),
    Region(
        R.NORTH_ANDUIN_VALE,
        "North Anduin Vale",
        adj_regions=f(
            R.GLADDEN_FIELDS,
            R.DIMRILL_DALE,
            R.SOUTH_ANDUIN_VALE,
            R.NARROWS_OF_THE_FOREST,
            R.DOL_GULDUR,
            R.RHOSGOBEL,
        ),
    ),
    Region(
        R.SOUTH_ANDUIN_VALE,
        "South Anduin Vale",
        adj_regions=f(
            R.DOL_GULDUR,
            R.WESTERN_BROWN_LANDS,
            R.NORTH_ANDUIN_VALE,
            R.PARTH_CELEBRANT,
            R.DIMRILL_DALE,
        ),
    ),
    Region(
        R.HIGH_PASS,
        "High Pass",
        adj_regions=f(R.FORDS_OF_BRUINEN, R.GOBLINS_GATE),
    ),
    Region(
        R.WITHERED_HEATH,
        "Withered Heath",
        adj_regions=f(R.EREBOR, R.NORTHERN_MIRKWOOD, R.DALE, R.WOODLAND_REALM),
    ),
    Region(
        R.ENEDWAITH,
        "Enedwaith",
        adj_regions=f(
            R.GAP_OF_ROHAN, R.THARBAD, R.DRUWAITH_IAUR, R.MINHIRIATH, R.SOUTH_DUNLAND
        ),
        features=f(RegionFeature.COASTAL),
    ),
    Region(
        R.DRUWAITH_IAUR,
        "Druwaith Iaur",
        adj_regions=f(R.ENEDWAITH, R.ANDRAST, R.FORDS_OF_ISEN, R.GAP_OF_ROHAN),
        features=f(RegionFeature.COASTAL),
    ),
    Region(
        R.ANDRAST,
        "Andrast",
        adj_regions=f(R.ANFALAS, R.DRUWAITH_IAUR),
        features=f(RegionFeature.COASTAL),
    ),
    Region(
        R.FANGORN,
        "Fangorn",
        adj_regions=f(R.WESTEMNET, R.EASTEMNET, R.PARTH_CELEBRANT, R.FORDS_OF_ISEN),
    ),
    Region(
        R.PARTH_CELEBRANT,
        "Parth Celebrant",
        adj_regions=f(
            R.LORIEN,
            R.FANGORN,
            R.EASTEMNET,
            R.WESTERN_BROWN_LANDS,
            R.SOUTH_ANDUIN_VALE,
            R.DIMRILL_DALE,
        ),
    ),
    Region(
        R.OSGILIATH,
        "Osgiliath",
        adj_regions=f(
            R.MINAS_TIRITH,
            R.DRUADAN_FOREST,
            R.SOUTH_ITHILIEN,
            R.DEAD_MARSHES,
            R.NORTH_ITHILIEN,
            R.SOUTH_ITHILIEN,
            R.WEST_HARONDOR,
            R.PELARGIR,
        ),
        features=f(RegionFeature.FORT),
    ),
    Region(
        R.NORTH_ITHILIEN,
        "North Ithilien",
        adj_regions=f(
            R.SOUTH_ITHILIEN,
            R.MINAS_MORGUL,
            R.DEAD_MARSHES,
            R.EASTERN_EMYN_MUIL,
            R.DAGORLAD,
            R.OSGILIATH,
        ),
    ),
    Region(
        R.SOUTH_ITHILIEN,
        "South Ithilien",
        adj_regions=f(
            R.OSGILIATH,
            R.NORTH_ITHILIEN,
            R.WEST_HARONDOR,
            R.EAST_HARONDOR,
            R.MINAS_MORGUL,
        ),
    ),
    Region(
        R.WEST_HARONDOR,
        "West Harondor",
        adj_regions=f(
            R.PELARGIR,
            R.EAST_HARONDOR,
            R.SOUTH_ITHILIEN,
            R.OSGILIATH,
            R.UMBAR,
            R.NEAR_HARAD,
        ),
        features=f(RegionFeature.COASTAL),
    ),
    Region(
        R.EAST_HARONDOR,
        "East Harondor",
        adj_regions=f(R.WEST_HARONDOR, R.SOUTH_ITHILIEN, R.NEAR_HARAD),
    ),
    # === ISENGARD (yellow border) ===
    Region(
        R.ORTHANC,
        "Orthanc",
        nation=N.ISENGARD,
        adj_regions=f(R.GAP_OF_ROHAN, R.FORDS_OF_ISEN),
        features=f(RegionFeature.STRONGHOLD),
    ),
    Region(
        R.GAP_OF_ROHAN,
        "Gap of Rohan",
        adj_regions=f(
            R.ORTHANC, R.FORDS_OF_ISEN, R.ENEDWAITH, R.SOUTH_DUNLAND, R.DRUWAITH_IAUR
        ),
    ),
    Region(
        R.NORTH_DUNLAND,
        "North Dunland",
        nation=N.ISENGARD,
        adj_regions=f(
            R.SOUTH_DUNLAND, R.THARBAD, R.HOLLIN, R.CARDOLAN, R.SOUTH_DOWNS, R.MORIA
        ),
        features=f(RegionFeature.TOWN),
    ),
    Region(
        R.SOUTH_DUNLAND,
        "South Dunland",
        nation=N.ISENGARD,
        adj_regions=f(R.NORTH_DUNLAND, R.THARBAD, R.GAP_OF_ROHAN, R.ENEDWAITH),
        features=f(RegionFeature.TOWN),
    ),
    Region(
        R.DEAD_MARSHES,
        "Dead Marshes",
        adj_regions=f(
            R.NORTH_ITHILIEN,
            R.NORTH_ITHILIEN,
            R.DRUADAN_FOREST,
            R.OSGILIATH,
            R.EASTERN_EMYN_MUIL,
            R.WESTERN_EMYN_MUIL,
        ),
    ),
    Region(
        R.DAGORLAD,
        "Dagorlad",
        adj_regions=f(
            R.MORANNON,
            R.ASH_MOUNTAINS,
            R.EASTERN_EMYN_MUIL,
            R.NOMAN_LANDS,
            R.NORTH_ITHILIEN,
        ),
    ),
    Region(
        R.ASH_MOUNTAINS,
        "Ash Mountains",
        adj_regions=f(R.DAGORLAD, R.SOUTH_RHUN, R.NOMAN_LANDS, R.SOUTHERN_DORWINION),
    ),
    Region(
        R.SOUTHERN_DORWINION,
        "Southern Dorwinion",
        adj_regions=f(
            R.ASH_MOUNTAINS,
            R.SOUTH_RHUN,
            R.NOMAN_LANDS,
            R.NORTHERN_DORWINION,
            R.SOUTHERN_RHOVANION,
        ),
    ),
    Region(
        R.NORTHERN_DORWINION,
        "Northern Dorwinion",
        adj_regions=f(
            R.VALE_OF_THE_CELDUIN,
            R.NORTH_RHUN,
            R.SOUTHERN_DORWINION,
            R.SOUTHERN_RHOVANION,
        ),
    ),
    Region(
        R.GOBLINS_GATE,
        "Goblin's Gate",
        adj_regions=f(R.HIGH_PASS, R.OLD_FORD),
        features=f(RegionFeature.TOWN),
    ),
    Region(
        R.VALE_OF_THE_CELDUIN,
        "Vale of the Celduin",
        nation=N.ELINGS,
        adj_regions=f(
            R.NORTHERN_DORWINION,
            R.VALE_OF_THE_CARNEN,
            R.NORTHERN_RHOVANION,
            R.SOUTHERN_RHOVANION,
            R.NORTH_RHUN,
        ),
    ),
    Region(
        R.VALE_OF_THE_CARNEN,
        "Vale of the Carnen",
        adj_regions=f(
            R.IRON_HILLS,
            R.VALE_OF_THE_CELDUIN,
            R.EAST_RHUN,
            R.NORTH_RHUN,
            R.DALE,
            R.NORTHERN_RHOVANION,
        ),
    ),
    Region(
        R.EASTERN_MIRKWOOD,
        "Eastern Mirkwood",
        f(
            R.NARROWS_OF_THE_FOREST,
            R.OLD_FOREST_ROAD,
            R.NORTHERN_RHOVANION,
            R.OLD_FOREST_ROAD,
            R.DOL_GULDUR,
            R.SOUTHERN_MIRKWOOD,
        ),
    ),
    Region(
        R.NARROWS_OF_THE_FOREST,
        "Narrows of the Forest",
        f(
            R.DOL_GULDUR,
            R.EASTERN_MIRKWOOD,
            R.OLD_FOREST_ROAD,
            R.RHOSGOBEL,
            R.NORTH_ANDUIN_VALE,
        ),
    ),
    Region(
        R.SOUTHERN_MIRKWOOD,
        "Southern Mirkwood",
        adj_regions=f(
            R.DOL_GULDUR,
            R.EASTERN_MIRKWOOD,
            R.NORTHERN_RHOVANION,
            R.SOUTHERN_RHOVANION,
            R.EASTERN_BROWN_LANDS,
        ),
    ),
    Region(
        R.SOUTHERN_RHOVANION,
        "Southern Rhovanion",
        adj_regions=f(
            R.SOUTHERN_MIRKWOOD,
            R.NORTHERN_RHOVANION,
            R.NOMAN_LANDS,
            R.VALE_OF_THE_CELDUIN,
            R.NORTHERN_DORWINION,
            R.SOUTHERN_DORWINION,
            R.EASTERN_BROWN_LANDS,
        ),
    ),
    Region(
        R.NORTHERN_RHOVANION,
        "Northern Rhovanion",
        f(
            R.SOUTHERN_RHOVANION,
            R.VALE_OF_THE_CELDUIN,
            R.VALE_OF_THE_CARNEN,
            R.DALE,
            R.OLD_FOREST_ROAD,
            R.SOUTHERN_MIRKWOOD,
            R.EASTERN_MIRKWOOD,
        ),
    ),
    Region(
        R.NOMAN_LANDS,
        "Noman-lands",
        f(
            R.EASTERN_BROWN_LANDS,
            R.SOUTHERN_RHOVANION,
            R.EASTERN_EMYN_MUIL,
            R.DAGORLAD,
            R.ASH_MOUNTAINS,
            R.SOUTHERN_DORWINION,
        ),
    ),
    Region(
        R.WESTERN_BROWN_LANDS,
        "Western Brown Lands",
        f(
            R.EASTERN_BROWN_LANDS,
            R.PARTH_CELEBRANT,
            R.SOUTH_ANDUIN_VALE,
            R.WESTERN_EMYN_MUIL,
            R.DOL_GULDUR,
            R.EASTEMNET,
        ),
    ),
    Region(
        R.EASTERN_BROWN_LANDS,
        "Eastern Brown Lands",
        f(
            R.DOL_GULDUR,
            R.NOMAN_LANDS,
            R.WESTERN_BROWN_LANDS,
            R.SOUTHERN_RHOVANION,
            R.EASTERN_EMYN_MUIL,
            R.SOUTHERN_MIRKWOOD,
            R.WESTERN_EMYN_MUIL,
        ),
    ),
    Region(
        R.WESTERN_EMYN_MUIL,
        "Western Emyn Muil",
        f(
            R.EASTERN_EMYN_MUIL,
            R.EASTEMNET,
            R.DRUADAN_FOREST,
            R.WESTERN_BROWN_LANDS,
            R.DEAD_MARSHES,
            R.EASTERN_BROWN_LANDS,
            R.WESTERN_BROWN_LANDS,
        ),
    ),
    Region(
        R.EASTERN_EMYN_MUIL,
        "Eastern Emyn Muil",
        f(
            R.DEAD_MARSHES,
            R.WESTERN_EMYN_MUIL,
            R.NOMAN_LANDS,
            R.NORTH_ITHILIEN,
            R.DAGORLAD,
            R.EASTERN_BROWN_LANDS,
        ),
    ),
)
