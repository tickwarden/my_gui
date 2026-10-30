$execute store result score #now reliquary.tmp run time query gametime
scoreboard players set #cd reliquary.tmp 0
$execute store result score #cd reliquary.tmp run data get storage reliquary:rt p$(pid).cd.$(class)
execute if score #cd reliquary.tmp > #now reliquary.tmp run scoreboard players operation #left reliquary.tmp = #cd reliquary.tmp
execute if score #cd reliquary.tmp > #now reliquary.tmp run scoreboard players operation #left reliquary.tmp -= #now reliquary.tmp
$execute if score #cd reliquary.tmp > #now reliquary.tmp run return run function reliquary:act/fail_cd
scoreboard players set #ok reliquary.tmp 1
