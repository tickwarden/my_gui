item replace entity @e[type=minecraft:chest_minecart,tag=bazaar.this,limit=1] container.8 with minecraft:emerald_block[custom_name='{"text":"Stok yönetimi","italic":false,"color":"green","bold":true}',lore=['{"text":"Sınırlı stokları sıfırla","italic":false,"color":"gray"}','{"text":"Yalnız yöneticide görünür","italic":false,"color":"dark_gray"}'],custom_data={gui:1b,pack:"bazaar"},max_stack_size=1,enchantment_glint_override=true]
execute store result storage bazaar:macro pid int 1 run scoreboard players get @s bazaar.id
function bazaar:page/admin_act with storage bazaar:macro
