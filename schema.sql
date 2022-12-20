create table if not exists players(
    PlayerId integer primary key autoincrement,
    Nickname text, 
    Level integer, 
    Hp integer, 
    CurHp integer, 
    Money integer, 
    Attack integer, 
    MagicAttack integer, 
    Xp integer, 
    Armour integer, 
    MagicArmour integer,
    LocationID integer
);

create table if not exists mobs(
    MobId integer primary key autoincrement,
    Hp integer, 
    Xp integer, 
    ReqLevel integer, 
    AttackType text,
    Attack integer,
    Armour integer,
    MagicArmour integer
);

create table if not exists locations(
    LocationID integer primary key autoincrement,
    XCoord integer, 
    YCoord integer, 
    LocationType text not null
);

create table if not exists items(
    ItemId integer primary key autoincrement,
    Cost integer, 
    CostToSale integer, 
    ItemType text, 
    Hp integer, 
    Mana integer, 
    Attack integer, 
    MagicAttack integer, 
    Armour integer, 
    MagicArmour integer, 
    ReqLevel integer
);

