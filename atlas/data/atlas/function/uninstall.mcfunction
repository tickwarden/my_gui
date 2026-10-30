tag @a remove atlas.open
tag @a remove atlas.welcomed
kill @e[type=minecraft:chest_minecart,tag=atlas.cart]
scoreboard objectives remove atlas
scoreboard objectives remove atlas.id
scoreboard objectives remove atlas.page
scoreboard objectives remove atlas.back
scoreboard objectives remove atlas.grace
scoreboard objectives remove atlas.tmp
scoreboard objectives remove atlas.dead
scoreboard objectives remove atlas.use
scoreboard objectives remove atlas.cd
scoreboard objectives remove atlas.mode
scoreboard objectives remove atlas.sel
scoreboard objectives remove atlas.timer
data remove storage atlas:config
data remove storage atlas:rt
data remove storage atlas:live
data remove storage atlas:tmp
data remove storage atlas:macro
data remove storage atlas:shop
data remove storage atlas:defaults
data remove storage atlas:dest
tellraw @a {"text":"Yol Atlası kaldırıldı. Ardından datapack klasörünü sil.","color":"red"}
