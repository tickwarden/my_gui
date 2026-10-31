playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.5 1.3
tellraw @s {"text":"Görev kabul edildi: Taş Kır","color":"green"}
title @s actionbar {"text":"Taş Kır aktif.","color":"yellow"}
function questboard:gui/render
