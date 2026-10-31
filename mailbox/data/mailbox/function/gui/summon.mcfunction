tag @e[type=minecraft:chest_minecart,tag=mailbox.this] remove mailbox.this
execute anchored eyes positioned ^ ^ ^1.15 run summon minecraft:chest_minecart ~ ~ ~ {Invulnerable:1b,Silent:1b,NoGravity:1b,CustomDisplayTile:1b,DisplayState:{Name:"minecraft:chest"},DisplayOffset:0,Tags:["mailbox.cart","mailbox.this"],CustomNameVisible:0b,CustomName:'{"text":"Posta Kutusu","italic":false,"color":"white"}',Items:[]}
scoreboard players operation @e[type=minecraft:chest_minecart,tag=mailbox.this,limit=1] mailbox.id = @s mailbox.id
scoreboard players set @e[type=minecraft:chest_minecart,tag=mailbox.this,limit=1] mailbox.page 0
