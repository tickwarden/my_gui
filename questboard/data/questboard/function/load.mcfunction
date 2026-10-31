scoreboard objectives add questboard trigger
scoreboard objectives add questboard.id dummy
scoreboard objectives add questboard.page dummy
scoreboard objectives add questboard.back dummy
scoreboard objectives add questboard.grace dummy
scoreboard objectives add questboard.tmp dummy
scoreboard objectives add questboard.dead deathCount
scoreboard objectives add questboard.use minecraft.used:minecraft.filled_map
execute unless data storage questboard:config ready run function questboard:init
kill @e[type=minecraft:chest_minecart,tag=questboard.cart]
tag @a remove questboard.open
tellraw @a [{"text":"[Görev Tahtası] ","color":"gold","bold":true},{"text":"yüklendi. ","color":"gray"},{"text":"/trigger questboard","color":"aqua","underlined":true,"clickEvent":{"action":"run_command","value":"/trigger questboard"},"hoverEvent":{"action":"show_text","contents":{"text":"Menüyü aç","color":"yellow"}}}]
