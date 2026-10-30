tag @e[type=minecraft:chest_minecart,tag=atlas.this] remove atlas.this
execute anchored eyes positioned ^ ^ ^1.15 run summon minecraft:chest_minecart ~ ~ ~ {Invulnerable:1b,Silent:1b,NoGravity:1b,CustomDisplayTile:1b,DisplayState:{Name:"minecraft:chest"},DisplayOffset:0,Tags:["atlas.cart","atlas.this"],CustomNameVisible:0b,CustomName:'{"text":"Yol Atlası","italic":false,"color":"aqua"}',Items:[]}
scoreboard players operation @e[type=minecraft:chest_minecart,tag=atlas.this,limit=1] atlas.id = @s atlas.id
scoreboard players set @e[type=minecraft:chest_minecart,tag=atlas.this,limit=1] atlas.page 0
