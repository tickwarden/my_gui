scoreboard objectives add atelier trigger
scoreboard objectives add atelier.id dummy
scoreboard objectives add atelier.page dummy
scoreboard objectives add atelier.back dummy
scoreboard objectives add atelier.grace dummy
scoreboard objectives add atelier.tmp dummy
scoreboard objectives add atelier.dead deathCount
scoreboard objectives add atelier.use minecraft.used:minecraft.enchanted_book
execute unless data storage atelier:config ready run function atelier:init
kill @e[type=minecraft:chest_minecart,tag=atelier.cart]
tag @a remove atelier.open
tellraw @a [{"text":"[Büyü Atölyesi] ","color":"light_purple","bold":true},{"text":"yüklendi. ","color":"gray"},{"text":"/trigger atelier","color":"aqua","underlined":true,"clickEvent":{"action":"run_command","value":"/trigger atelier"},"hoverEvent":{"action":"show_text","contents":{"text":"Menüyü aç","color":"yellow"}}}]
