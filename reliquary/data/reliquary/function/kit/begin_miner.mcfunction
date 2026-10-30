scoreboard players set #ok reliquary.tmp 0
$function reliquary:kit/gate {pid:$(pid),class:"miner"}
execute unless score #ok reliquary.tmp matches 1 run return 0
function reliquary:kit/give_miner
$function reliquary:kit/stamp {pid:$(pid),class:"miner"}
$function reliquary:kit/join {team:"rel.miner"}
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.7 1
tellraw @s {"text":"Kit verildi.","color":"green"}
function reliquary:gui/render
