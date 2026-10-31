scoreboard objectives add mailbox trigger
scoreboard objectives add mailbox.id dummy
scoreboard objectives add mailbox.page dummy
scoreboard objectives add mailbox.back dummy
scoreboard objectives add mailbox.grace dummy
scoreboard objectives add mailbox.tmp dummy
scoreboard objectives add mailbox.dead deathCount
scoreboard objectives add mailbox.use minecraft.used:minecraft.writable_book
execute unless data storage mailbox:config ready run function mailbox:init
kill @e[type=minecraft:chest_minecart,tag=mailbox.cart]
tag @a remove mailbox.open
tellraw @a [{"text":"[Posta Kutusu] ","color":"white","bold":true},{"text":"yüklendi. ","color":"gray"},{"text":"/trigger mailbox","color":"aqua","underlined":true,"clickEvent":{"action":"run_command","value":"/trigger mailbox"},"hoverEvent":{"action":"show_text","contents":{"text":"Menüyü aç","color":"yellow"}}}]
