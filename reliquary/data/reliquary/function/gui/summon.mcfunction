tag @e[type=minecraft:chest_minecart,tag=reliquary.this] remove reliquary.this
execute anchored eyes positioned ^ ^ ^1.15 run summon minecraft:chest_minecart ~ ~ ~ {Invulnerable:1b,Silent:1b,NoGravity:1b,CustomDisplayTile:1b,DisplayState:{Name:"minecraft:chest"},DisplayOffset:0,Tags:["reliquary.cart","reliquary.this"],CustomNameVisible:0b,CustomName:'{"text":"Sınıf Emaneti","italic":false,"color":"light_purple"}',Items:[]}
scoreboard players operation @e[type=minecraft:chest_minecart,tag=reliquary.this,limit=1] reliquary.id = @s reliquary.id
scoreboard players set @e[type=minecraft:chest_minecart,tag=reliquary.this,limit=1] reliquary.page 0
