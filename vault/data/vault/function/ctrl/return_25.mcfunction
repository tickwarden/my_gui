summon minecraft:item ~ ~0.2 ~ {PickupDelay:0s,Tags:["vault.return"],Item:{id:"minecraft:stone",count:1}}
data modify entity @e[type=minecraft:item,tag=vault.return,limit=1,sort=nearest] Item set from storage vault:live Items[{Slot:25b}]
data remove entity @e[type=minecraft:item,tag=vault.return,limit=1,sort=nearest] Item.Slot
tag @e[type=minecraft:item,tag=vault.return,limit=1,sort=nearest] remove vault.return
