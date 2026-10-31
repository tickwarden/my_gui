playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.5 1.3
tellraw @s {"text":"Görev kabul edildi: Odun Topla","color":"green"}
title @s actionbar {"text":"Odun Topla aktif.","color":"yellow"}
function questboard:gui/render
