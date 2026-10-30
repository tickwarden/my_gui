scoreboard players set #ok reliquary.tmp 0
$function reliquary:kit/gate {pid:$(pid),class:"alchemist"}
execute unless score #ok reliquary.tmp matches 1 run return 0
function reliquary:kit/give_alchemist
$function reliquary:kit/stamp {pid:$(pid),class:"alchemist"}
$function reliquary:kit/join {team:"rel.alch"}
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.7 1
tellraw @s {"text":"Kit verildi.","color":"green"}
function reliquary:gui/render
