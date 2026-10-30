scoreboard objectives add vault trigger
scoreboard objectives add vault.id dummy
scoreboard objectives add vault.page dummy
scoreboard objectives add vault.back dummy
scoreboard objectives add vault.grace dummy
scoreboard objectives add vault.tmp dummy
scoreboard objectives add vault.dead deathCount
scoreboard objectives add vault.use minecraft.used:minecraft.warped_fungus_on_a_stick
scoreboard objectives add vault.used dummy
execute unless data storage vault:config ready run function vault:init
kill @e[type=minecraft:chest_minecart,tag=vault.cart]
tag @a remove vault.open
tellraw @a [{"text":"[Kutsal Kasa] ","color":"dark_aqua","bold":true},{"text":"yüklendi. ","color":"gray"},{"text":"/trigger vault","color":"aqua","underlined":true,"clickEvent":{"action":"run_command","value":"/trigger vault"},"hoverEvent":{"action":"show_text","contents":{"text":"Menüyü aç","color":"yellow"}}}]
