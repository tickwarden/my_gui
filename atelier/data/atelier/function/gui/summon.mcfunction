tag @e[type=minecraft:chest_minecart,tag=atelier.this] remove atelier.this
execute anchored eyes positioned ^ ^ ^1.15 run summon minecraft:chest_minecart ~ ~ ~ {Invulnerable:1b,Silent:1b,NoGravity:1b,CustomDisplayTile:1b,DisplayState:{Name:"minecraft:chest"},DisplayOffset:0,Tags:["atelier.cart","atelier.this"],CustomNameVisible:0b,CustomName:'{"text":"Büyü Atölyesi","italic":false,"color":"light_purple"}',Items:[]}
scoreboard players operation @e[type=minecraft:chest_minecart,tag=atelier.this,limit=1] atelier.id = @s atelier.id
scoreboard players set @e[type=minecraft:chest_minecart,tag=atelier.this,limit=1] atelier.page 0
