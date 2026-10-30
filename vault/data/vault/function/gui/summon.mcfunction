tag @e[type=minecraft:chest_minecart,tag=vault.this] remove vault.this
execute anchored eyes positioned ^ ^ ^1.15 run summon minecraft:chest_minecart ~ ~ ~ {Invulnerable:1b,Silent:1b,NoGravity:1b,CustomDisplayTile:1b,DisplayState:{Name:"minecraft:chest"},DisplayOffset:0,Tags:["vault.cart","vault.this"],CustomNameVisible:0b,CustomName:'{"text":"Kutsal Kasa","italic":false,"color":"dark_aqua"}',Items:[]}
scoreboard players operation @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] vault.id = @s vault.id
scoreboard players set @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] vault.page 0
