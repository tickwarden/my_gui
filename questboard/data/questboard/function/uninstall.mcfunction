tag @a remove questboard.open
tag @a remove questboard.welcomed
kill @e[type=minecraft:chest_minecart,tag=questboard.cart]
scoreboard objectives remove questboard
scoreboard objectives remove questboard.id
scoreboard objectives remove questboard.page
scoreboard objectives remove questboard.back
scoreboard objectives remove questboard.grace
scoreboard objectives remove questboard.tmp
scoreboard objectives remove questboard.dead
scoreboard objectives remove questboard.use
data remove storage questboard:config
data remove storage questboard:rt
data remove storage questboard:live
data remove storage questboard:tmp
data remove storage questboard:macro
data remove storage questboard:shop
data remove storage questboard:defaults
data remove storage questboard:dest
tellraw @a {"text":"Görev Tahtası kaldırıldı. Ardından datapack klasörünü sil.","color":"red"}
