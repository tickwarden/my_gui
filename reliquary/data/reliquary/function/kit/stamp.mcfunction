execute store result score #now reliquary.tmp run time query gametime
execute store result score #wait reliquary.tmp run data get storage reliquary:config cooldown
execute unless score #wait reliquary.tmp matches 1.. run scoreboard players set #wait reliquary.tmp 12000
scoreboard players operation #cd reliquary.tmp = #now reliquary.tmp
scoreboard players operation #cd reliquary.tmp += #wait reliquary.tmp
$execute store result storage reliquary:rt p$(pid).cd.$(class) int 1 run scoreboard players get #cd reliquary.tmp
scoreboard players set #n reliquary.tmp 0
$execute store result score #n reliquary.tmp run data get storage reliquary:rt p$(pid).master.$(class)
scoreboard players add #n reliquary.tmp 1
$execute store result storage reliquary:rt p$(pid).master.$(class) int 1 run scoreboard players get #n reliquary.tmp
execute if score #n reliquary.tmp matches 3 run function reliquary:kit/mastery
