scoreboard players set #ok reliquary.tmp 0
$function reliquary:kit/gate {pid:$(pid),class:"archer"}
execute unless score #ok reliquary.tmp matches 1 run return 0
function reliquary:kit/give_archer
$function reliquary:kit/stamp {pid:$(pid),class:"archer"}
$function reliquary:kit/join {team:"rel.archer"}
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.7 1
tellraw @s {"text":"Kit verildi.","color":"green"}
function reliquary:gui/render
