tag @a remove atelier.open
tag @a remove atelier.welcomed
kill @e[type=minecraft:chest_minecart,tag=atelier.cart]
scoreboard objectives remove atelier
scoreboard objectives remove atelier.id
scoreboard objectives remove atelier.page
scoreboard objectives remove atelier.back
scoreboard objectives remove atelier.grace
scoreboard objectives remove atelier.tmp
scoreboard objectives remove atelier.dead
scoreboard objectives remove atelier.use
data remove storage atelier:config
data remove storage atelier:rt
data remove storage atelier:live
data remove storage atelier:tmp
data remove storage atelier:macro
data remove storage atelier:shop
data remove storage atelier:defaults
data remove storage atelier:dest
tellraw @a {"text":"Büyü Atölyesi kaldırıldı. Ardından datapack klasörünü sil.","color":"red"}
