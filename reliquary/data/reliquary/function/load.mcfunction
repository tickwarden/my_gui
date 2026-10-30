scoreboard objectives add reliquary trigger
scoreboard objectives add reliquary.id dummy
scoreboard objectives add reliquary.page dummy
scoreboard objectives add reliquary.back dummy
scoreboard objectives add reliquary.grace dummy
scoreboard objectives add reliquary.tmp dummy
scoreboard objectives add reliquary.dead deathCount
scoreboard objectives add reliquary.use minecraft.used:minecraft.carrot_on_a_stick
execute unless data storage reliquary:config ready run function reliquary:init
kill @e[type=minecraft:chest_minecart,tag=reliquary.cart]
tag @a remove reliquary.open
tellraw @a [{"text":"[Sınıf Emaneti] ","color":"light_purple","bold":true},{"text":"yüklendi. ","color":"gray"},{"text":"/trigger reliquary","color":"aqua","underlined":true,"clickEvent":{"action":"run_command","value":"/trigger reliquary"},"hoverEvent":{"action":"show_text","contents":{"text":"Menüyü aç","color":"yellow"}}}]
