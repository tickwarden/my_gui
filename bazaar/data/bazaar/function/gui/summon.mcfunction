tag @e[type=minecraft:chest_minecart,tag=bazaar.this] remove bazaar.this
execute anchored eyes positioned ^ ^ ^1.15 run summon minecraft:chest_minecart ~ ~ ~ {Invulnerable:1b,Silent:1b,NoGravity:1b,CustomDisplayTile:1b,DisplayState:{Name:"minecraft:chest"},DisplayOffset:0,Tags:["bazaar.cart","bazaar.this"],CustomNameVisible:0b,CustomName:'{"text":"Zümrüt Çarşı","italic":false,"color":"gold"}',Items:[]}
scoreboard players operation @e[type=minecraft:chest_minecart,tag=bazaar.this,limit=1] bazaar.id = @s bazaar.id
scoreboard players set @e[type=minecraft:chest_minecart,tag=bazaar.this,limit=1] bazaar.page 0
