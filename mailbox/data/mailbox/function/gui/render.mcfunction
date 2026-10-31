execute if score @s mailbox.page matches 0 run function mailbox:page/main
execute if score @s mailbox.page matches 1 run function mailbox:page/inbox
execute if score @s mailbox.page matches 2 run function mailbox:page/compose
execute if score @s mailbox.page matches 3 run function mailbox:page/help
title @s actionbar {"text":"Posta  •  gelen kutusunu kontrol et","color":"white"}
