scoreboard objectives add atlas trigger
scoreboard objectives add atlas.id dummy
scoreboard objectives add atlas.page dummy
scoreboard objectives add atlas.back dummy
scoreboard objectives add atlas.grace dummy
scoreboard objectives add atlas.tmp dummy
scoreboard objectives add atlas.dead deathCount
scoreboard objectives add atlas.use minecraft.used:minecraft.carrot_on_a_stick
scoreboard objectives add atlas.cd dummy
scoreboard objectives add atlas.mode dummy
scoreboard objectives add atlas.sel dummy
scoreboard objectives add atlas.timer dummy
execute unless data storage atlas:config ready run function atlas:init
kill @e[type=minecraft:chest_minecart,tag=atlas.cart]
tag @a remove atlas.open
tellraw @a [{"text":"[Yol Atlası] ","color":"aqua","bold":true},{"text":"yüklendi. ","color":"gray"},{"text":"/trigger atlas","color":"aqua","underlined":true,"clickEvent":{"action":"run_command","value":"/trigger atlas"},"hoverEvent":{"action":"show_text","contents":{"text":"Menüyü aç","color":"yellow"}}}]
