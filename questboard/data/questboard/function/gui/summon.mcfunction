tag @e[type=minecraft:chest_minecart,tag=questboard.this] remove questboard.this
execute anchored eyes positioned ^ ^ ^1.15 run summon minecraft:chest_minecart ~ ~ ~ {Invulnerable:1b,Silent:1b,NoGravity:1b,CustomDisplayTile:1b,DisplayState:{Name:"minecraft:chest"},DisplayOffset:0,Tags:["questboard.cart","questboard.this"],CustomNameVisible:0b,CustomName:'{"text":"Görev Tahtası","italic":false,"color":"gold"}',Items:[]}
scoreboard players operation @e[type=minecraft:chest_minecart,tag=questboard.this,limit=1] questboard.id = @s questboard.id
scoreboard players set @e[type=minecraft:chest_minecart,tag=questboard.this,limit=1] questboard.page 0
