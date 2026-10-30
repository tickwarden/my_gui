tag @a remove bazaar.open
tag @a remove bazaar.welcomed
kill @e[type=minecraft:chest_minecart,tag=bazaar.cart]
scoreboard objectives remove bazaar
scoreboard objectives remove bazaar.id
scoreboard objectives remove bazaar.page
scoreboard objectives remove bazaar.back
scoreboard objectives remove bazaar.grace
scoreboard objectives remove bazaar.tmp
scoreboard objectives remove bazaar.dead
scoreboard objectives remove bazaar.use
scoreboard objectives remove bazaar.bank
scoreboard objectives remove bazaar.day
data remove storage bazaar:config
data remove storage bazaar:rt
data remove storage bazaar:live
data remove storage bazaar:tmp
data remove storage bazaar:macro
data remove storage bazaar:shop
data remove storage bazaar:defaults
data remove storage bazaar:dest
tellraw @a {"text":"Zümrüt Çarşı kaldırıldı. Ardından datapack klasörünü sil.","color":"red"}
