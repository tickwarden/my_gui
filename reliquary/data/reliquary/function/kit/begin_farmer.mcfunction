scoreboard players set #ok reliquary.tmp 0
$function reliquary:kit/gate {pid:$(pid),class:"farmer"}
execute unless score #ok reliquary.tmp matches 1 run return 0
function reliquary:kit/give_farmer
$function reliquary:kit/stamp {pid:$(pid),class:"farmer"}
$function reliquary:kit/join {team:"rel.farmer"}
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.7 1
tellraw @s {"text":"Kit verildi.","color":"green"}
function reliquary:gui/render
