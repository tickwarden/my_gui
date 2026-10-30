scoreboard objectives add bazaar trigger
scoreboard objectives add bazaar.id dummy
scoreboard objectives add bazaar.page dummy
scoreboard objectives add bazaar.back dummy
scoreboard objectives add bazaar.grace dummy
scoreboard objectives add bazaar.tmp dummy
scoreboard objectives add bazaar.dead deathCount
scoreboard objectives add bazaar.use minecraft.used:minecraft.warped_fungus_on_a_stick
scoreboard objectives add bazaar.bank dummy
scoreboard objectives add bazaar.day dummy
execute unless data storage bazaar:config ready run function bazaar:init
kill @e[type=minecraft:chest_minecart,tag=bazaar.cart]
tag @a remove bazaar.open
tellraw @a [{"text":"[Zümrüt Çarşı] ","color":"gold","bold":true},{"text":"yüklendi. ","color":"gray"},{"text":"/trigger bazaar","color":"aqua","underlined":true,"clickEvent":{"action":"run_command","value":"/trigger bazaar"},"hoverEvent":{"action":"show_text","contents":{"text":"Menüyü aç","color":"yellow"}}}]
