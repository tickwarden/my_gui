tag @a remove vault.open
tag @a remove vault.welcomed
kill @e[type=minecraft:chest_minecart,tag=vault.cart]
scoreboard objectives remove vault
scoreboard objectives remove vault.id
scoreboard objectives remove vault.page
scoreboard objectives remove vault.back
scoreboard objectives remove vault.grace
scoreboard objectives remove vault.tmp
scoreboard objectives remove vault.dead
scoreboard objectives remove vault.use
scoreboard objectives remove vault.used
data remove storage vault:config
data remove storage vault:rt
data remove storage vault:live
data remove storage vault:tmp
data remove storage vault:macro
data remove storage vault:shop
data remove storage vault:defaults
data remove storage vault:dest
tellraw @a {"text":"Kutsal Kasa kaldırıldı. Ardından datapack klasörünü sil.","color":"red"}
