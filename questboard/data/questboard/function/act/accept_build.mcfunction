playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.5 1.3
tellraw @s {"text":"Görev kabul edildi: İnşaat Ustası","color":"green"}
title @s actionbar {"text":"İnşaat Ustası aktif.","color":"yellow"}
function questboard:gui/render
