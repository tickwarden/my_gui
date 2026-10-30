summon minecraft:item ~ ~0.2 ~ {PickupDelay:0s,Tags:["vault.return"],Item:{id:"minecraft:stone",count:1}}
data modify entity @e[type=minecraft:item,tag=vault.return,limit=1,sort=nearest] Item set from storage vault:live Items[{Slot:22b}]
execute if data entity @e[type=minecraft:item,tag=vault.return,limit=1,sort=nearest] Item.components."minecraft:custom_data"{gui:1b} run kill @e[type=minecraft:item,tag=vault.return,limit=1,sort=nearest]
data remove entity @e[type=minecraft:item,tag=vault.return,limit=1,sort=nearest] Item.Slot
tag @e[type=minecraft:item,tag=vault.return] remove vault.return
