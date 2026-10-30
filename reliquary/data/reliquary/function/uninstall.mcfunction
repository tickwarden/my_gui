tag @a remove reliquary.open
tag @a remove reliquary.welcomed
kill @e[type=minecraft:chest_minecart,tag=reliquary.cart]
scoreboard objectives remove reliquary
scoreboard objectives remove reliquary.id
scoreboard objectives remove reliquary.page
scoreboard objectives remove reliquary.back
scoreboard objectives remove reliquary.grace
scoreboard objectives remove reliquary.tmp
scoreboard objectives remove reliquary.dead
scoreboard objectives remove reliquary.use
data remove storage reliquary:config
data remove storage reliquary:rt
data remove storage reliquary:live
data remove storage reliquary:tmp
data remove storage reliquary:macro
data remove storage reliquary:shop
data remove storage reliquary:defaults
data remove storage reliquary:dest
tellraw @a {"text":"Sınıf Emaneti kaldırıldı. Ardından datapack klasörünü sil.","color":"red"}

team empty rel.knight
team empty rel.archer
team empty rel.farmer
team empty rel.miner
team empty rel.alch
team empty rel.expl
