tag @a remove mailbox.open
tag @a remove mailbox.welcomed
kill @e[type=minecraft:chest_minecart,tag=mailbox.cart]
scoreboard objectives remove mailbox
scoreboard objectives remove mailbox.id
scoreboard objectives remove mailbox.page
scoreboard objectives remove mailbox.back
scoreboard objectives remove mailbox.grace
scoreboard objectives remove mailbox.tmp
scoreboard objectives remove mailbox.dead
scoreboard objectives remove mailbox.use
data remove storage mailbox:config
data remove storage mailbox:rt
data remove storage mailbox:live
data remove storage mailbox:tmp
data remove storage mailbox:macro
data remove storage mailbox:shop
data remove storage mailbox:defaults
data remove storage mailbox:dest
tellraw @a {"text":"Posta Kutusu kaldırıldı. Ardından datapack klasörünü sil.","color":"red"}
