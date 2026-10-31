playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.5 1.3
tellraw @s {"text":"Görev kabul edildi: Buğday Biç","color":"green"}
title @s actionbar {"text":"Buğday Biç aktif.","color":"yellow"}
function questboard:gui/render
