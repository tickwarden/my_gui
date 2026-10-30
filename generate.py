#!/usr/bin/env python3
"""Generate four Minecraft 1.21.3 chest-GUI datapacks for tickwarden/my_gui."""
from __future__ import annotations

import json
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK_FORMAT = 57

def jtext(text: str, color: str | None = None, bold: bool = False) -> str:
    obj: dict = {"text": text, "italic": False}
    if color:
        obj["color"] = color
    if bold:
        obj["bold"] = True
    return "'" + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "'"

def lore_snbt(lines: list[tuple[str, str]]) -> str:
    return "[" + ",".join(jtext(t, c) for t, c in lines) + "]"

def snbt_item(slot: int, item_id: str, name: str | None, lore: list[tuple[str, str]], pack: str, glint: bool = False, count: int = 1, hide: bool = False, color: str | None = None) -> str:
    comps = [f'"minecraft:custom_data":{{gui:1b,pack:"{pack}"}}', '"minecraft:max_stack_size":1']
    if hide:
        comps.append('"minecraft:hide_tooltip":{}')
    else:
        if name is not None:
            comps.append(f'"minecraft:custom_name":{jtext(name, color, bold=True)}')
        if lore:
            comps.append(f'"minecraft:lore":{lore_snbt(lore)}')
    if glint:
        comps.append('"minecraft:enchantment_glint_override":true')
    return f'{{Slot:{slot}b,id:"{item_id}",count:{count},components:{{{",".join(comps)}}}}}'

def filler(slot: int, pack: str) -> str:
    return snbt_item(slot, "minecraft:gray_stained_glass_pane", None, [], pack, hide=True)

def actions_snbt(actions: list[str]) -> str:
    return "{" + ",".join(f's{i}:"{a}"' for i, a in enumerate(actions)) + "}"

def png(path: Path, rgb: tuple[int, int, int], mark: tuple[int, int, int]) -> None:
    w = h = 64
    rows = []
    for y in range(h):
        row = []
        for x in range(w):
            border = x < 4 or y < 4 or x >= 60 or y >= 60
            lid = 14 <= y <= 28 and 10 <= x <= 54
            latch = 24 <= y <= 34 and 28 <= x <= 36
            if latch:
                row.extend(mark)
            elif lid or border:
                row.extend(tuple(max(0, c - 40) for c in rgb))
            else:
                row.extend(rgb)
        rows.append(bytes(row))
    raw = b"".join(b"\x00" + r for r in rows)

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))

def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")

def mcmeta(folder: Path, title: str, color: str, blurb: str) -> None:
    data = {
        "pack": {
            "pack_format": PACK_FORMAT,
            "supported_formats": [PACK_FORMAT, PACK_FORMAT],
            "description": [
                {"text": title + "\n", "color": color, "bold": True},
                {"text": blurb, "color": "gray"},
            ],
        }
    }
    write(folder / "pack.mcmeta", json.dumps(data, ensure_ascii=False, indent=2))

def tags(folder: Path, ns: str) -> None:
    write(folder / "data/minecraft/tags/function/load.json", json.dumps({"values": [f"{ns}:load"]}, indent=2))
    write(folder / "data/minecraft/tags/function/tick.json", json.dumps({"values": [f"{ns}:tick"]}, indent=2))
    write(
        folder / f"data/{ns}/tags/block/passable.json",
        json.dumps(
            {
                "values": [
                    "minecraft:air",
                    "minecraft:cave_air",
                    "minecraft:void_air",
                    "minecraft:short_grass",
                    "minecraft:fern",
                    "minecraft:snow",
                    "minecraft:vine",
                    "minecraft:light",
                ]
            },
            indent=2,
        ),
    )
    write(
        folder / f"data/{ns}/predicate/sneaking.json",
        json.dumps(
            {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"flags": {"is_sneaking": True}}},
            indent=2,
        ),
    )

def engine(folder: Path, ns: str, title: str, title_color: str, use_item: str, vault: bool) -> None:
    """Shared chest-minecart GUI engine. Vault replaces scan with its own sync."""
    P = folder / "data" / ns / "function"
    obj = [
        f"scoreboard objectives add {ns} trigger",
        f"scoreboard objectives add {ns}.id dummy",
        f"scoreboard objectives add {ns}.page dummy",
        f"scoreboard objectives add {ns}.back dummy",
        f"scoreboard objectives add {ns}.grace dummy",
        f"scoreboard objectives add {ns}.tmp dummy",
        f"scoreboard objectives add {ns}.dead deathCount",
        f"scoreboard objectives add {ns}.use minecraft.used:{use_item.replace(':', '.', 1)}",
    ]
    extra_obj = []
    if ns == "bazaar":
        extra_obj = ["scoreboard objectives add bazaar.bank dummy", "scoreboard objectives add bazaar.day dummy"]
    if ns == "atlas":
        extra_obj = [
            "scoreboard objectives add atlas.cd dummy",
            "scoreboard objectives add atlas.mode dummy",
            "scoreboard objectives add atlas.sel dummy",
            "scoreboard objectives add atlas.timer dummy",
        ]
    if ns == "vault":
        extra_obj = ["scoreboard objectives add vault.used dummy"]
    write(
        P / "load.mcfunction",
        "\n".join(obj + extra_obj)
        + f"""
execute unless data storage {ns}:config ready run function {ns}:init
kill @e[type=minecraft:chest_minecart,tag={ns}.cart]
tag @a remove {ns}.open
tellraw @a [{{"text":"[{title}] ","color":"{title_color}","bold":true}},{{"text":"yüklendi. ","color":"gray"}},{{"text":"/trigger {ns}","color":"aqua","underlined":true,"clickEvent":{{"action":"run_command","value":"/trigger {ns}"}},"hoverEvent":{{"action":"show_text","contents":{{"text":"Menüyü aç","color":"yellow"}}}}}}]
""",
    )
    scan_line = f"function {ns}:gui/scan" if not vault else f"function {ns}:gui/vault_tick"
    write(
        P / "tick.mcfunction",
        f"""
execute as @a[tag=!{ns}.welcomed] run function {ns}:welcome
scoreboard players enable @a {ns}
execute as @a[scores={{{ns}=1..}}] at @s run function {ns}:gui/open
scoreboard players set @a {ns} 0
execute as @a[scores={{{ns}.use=1..}}] at @s if items entity @s weapon.mainhand *[minecraft:custom_data={{key:1b,pack:"{ns}"}}] run function {ns}:gui/open
execute as @a[scores={{{ns}.use=1..}}] at @s if items entity @s weapon.offhand *[minecraft:custom_data={{key:1b,pack:"{ns}"}}] run function {ns}:gui/open
scoreboard players set @a {ns}.use 0
execute as @a[scores={{{ns}.dead=1..}},tag={ns}.open] run function {ns}:gui/close
scoreboard players set @a {ns}.dead 0
execute as @a[tag={ns}.open] at @s run function {ns}:gui/tick_player
kill @e[type=minecraft:item,nbt={{Item:{{components:{{"minecraft:custom_data":{{gui:1b,pack:"{ns}"}}}}}}}}]
clear @a *[minecraft:custom_data={{gui:1b,pack:"{ns}"}}]
execute as @e[type=minecraft:hopper_minecart] if data entity @s Items[{{components:{{"minecraft:custom_data":{{gui:1b,pack:"{ns}"}}}}}}] run data remove entity @s Items[{{components:{{"minecraft:custom_data":{{gui:1b,pack:"{ns}"}}}}}}]
execute as @e[type=minecraft:chest_minecart,tag={ns}.cart] at @s unless entity @a[tag={ns}.open,distance=..8] run function {ns}:gui/orphan
""",
    )
    write(
        P / "gui/tick_player.mcfunction",
        f"""
tag @e[type=minecraft:chest_minecart,tag={ns}.this] remove {ns}.this
scoreboard players operation #id {ns}.tmp = @s {ns}.id
execute as @e[type=minecraft:chest_minecart,tag={ns}.cart] if score @s {ns}.id = #id {ns}.tmp run tag @s add {ns}.this
execute unless entity @e[type=minecraft:chest_minecart,tag={ns}.this,limit=1] run return run function {ns}:gui/lost
execute if score @s {ns}.grace matches 1.. run scoreboard players remove @s {ns}.grace 1
execute if score @s {ns}.grace matches 0 if predicate {ns}:sneaking run return run function {ns}:gui/close
execute unless entity @e[type=minecraft:chest_minecart,tag={ns}.this,distance=..7,limit=1] run return run function {ns}:gui/close
execute at @e[type=minecraft:chest_minecart,tag={ns}.this,limit=1] if block ~ ~ ~ minecraft:nether_portal run return run function {ns}:gui/close
execute at @e[type=minecraft:chest_minecart,tag={ns}.this,limit=1] if block ~ ~-1 ~ minecraft:hopper run return run function {ns}:gui/anti_hopper
{scan_line}
execute as @e[type=minecraft:chest_minecart,tag={ns}.this,limit=1] run data merge entity @s {{Motion:[0.0d,0.0d,0.0d]}}
tag @e[type=minecraft:chest_minecart,tag={ns}.this] remove {ns}.this
""",
    )
    write(
        P / "gui/anti_hopper.mcfunction",
        f"""
data remove block ~ ~-1 ~ Items[{{components:{{"minecraft:custom_data":{{gui:1b,pack:"{ns}"}}}}}}]
{"function vault:gui/close" if vault else f"function {ns}:gui/render"}
title @s actionbar {{"text":"Huni menünün altındaydı. Menü yenilendi.","color":"red"}}
""",
    )
    write(
        P / "gui/open.mcfunction",
        f"""
execute if entity @s[gamemode=spectator] run return run title @s actionbar {{"text":"İzleyici modunda açılamaz.","color":"red"}}
execute if entity @s[tag={ns}.open] run return run title @s actionbar {{"text":"Menü zaten açık. Sağ tıkla.","color":"yellow"}}
execute unless score @s {ns}.id matches 1.. run function {ns}:assign_id
function {ns}:gui/summon
execute unless entity @e[type=minecraft:chest_minecart,tag={ns}.this,limit=1] run return run title @s actionbar {{"text":"Menü oluşturulamadı.","color":"red"}}
scoreboard players set @s {ns}.page 0
scoreboard players set @s {ns}.grace 25
tag @s add {ns}.open
function {ns}:gui/render
playsound minecraft:block.chest.open player @s ~ ~ ~ 0.7 1.1
title @s actionbar {{"text":"Sandığa sağ tıkla  •  eğilerek kapat","color":"{title_color}"}}
tag @e[type=minecraft:chest_minecart,tag={ns}.this] remove {ns}.this
""",
    )
    write(
        P / "gui/summon.mcfunction",
        f"""
tag @e[type=minecraft:chest_minecart,tag={ns}.this] remove {ns}.this
execute anchored eyes positioned ^ ^ ^1.15 run summon minecraft:chest_minecart ~ ~ ~ {{Invulnerable:1b,Silent:1b,NoGravity:1b,CustomDisplayTile:1b,DisplayState:{{Name:"minecraft:chest"}},DisplayOffset:0,Tags:["{ns}.cart","{ns}.this"],CustomNameVisible:0b,CustomName:{jtext(title, title_color)},Items:[]}}
scoreboard players operation @e[type=minecraft:chest_minecart,tag={ns}.this,limit=1] {ns}.id = @s {ns}.id
scoreboard players set @e[type=minecraft:chest_minecart,tag={ns}.this,limit=1] {ns}.page 0
""",
    )
    if vault:
        save_line = (
            f"tag @e[type=minecraft:chest_minecart,tag={ns}.this] remove {ns}.this\n"
            f"scoreboard players operation #id {ns}.tmp = @s {ns}.id\n"
            f"execute as @e[type=minecraft:chest_minecart,tag={ns}.cart] if score @s {ns}.id = #id {ns}.tmp run tag @s add {ns}.this\n"
            f"execute if entity @e[type=minecraft:chest_minecart,tag={ns}.this,limit=1] run function {ns}:gui/save"
        )
    else:
        save_line = "execute if entity @s"
    write(
        P / "gui/close.mcfunction",
        f"""
execute unless entity @s[tag={ns}.open] run return 0
{save_line}
tag @s remove {ns}.open
scoreboard players operation #id {ns}.tmp = @s {ns}.id
execute as @e[type=minecraft:chest_minecart,tag={ns}.cart] if score @s {ns}.id = #id {ns}.tmp run kill @s
clear @s *[minecraft:custom_data={{gui:1b,pack:"{ns}"}}]
playsound minecraft:block.chest.close player @s ~ ~ ~ 0.55 1
scoreboard players set @s {ns}.grace 0
""",
    )
    write(
        P / "gui/lost.mcfunction",
        f"""
tag @s remove {ns}.open
scoreboard players set @s {ns}.grace 0
clear @s *[minecraft:custom_data={{gui:1b,pack:"{ns}"}}]
title @s actionbar {{"text":"Menü kapandı.","color":"gray"}}
""",
    )
    if vault:
        write(
            P / "gui/orphan.mcfunction",
            f"""
scoreboard players operation #id {ns}.tmp = @s {ns}.id
execute store result storage {ns}:macro pid int 1 run scoreboard players get #id {ns}.tmp
execute if score @s {ns}.page matches 0 run function {ns}:vault/sync_orphan_a with storage {ns}:macro
execute if score @s {ns}.page matches 1 run function {ns}:vault/sync_orphan_b with storage {ns}:macro
execute if score @s {ns}.page matches 2 run function {ns}:vault/sync_orphan_c with storage {ns}:macro
kill @s
""",
        )
    else:
        write(P / "gui/orphan.mcfunction", "kill @s")
    write(
        P / "gui/scan.mcfunction",
        f"""
data modify storage {ns}:live Items set from entity @e[type=minecraft:chest_minecart,tag={ns}.this,limit=1] Items
scoreboard players set #dirty {ns}.tmp 0
execute store result storage {ns}:macro pid int 1 run scoreboard players get @s {ns}.id
scoreboard players set #slot {ns}.tmp 0
function {ns}:gui/scan_loop
execute if score #dirty {ns}.tmp matches 1.. run function {ns}:gui/render
function {ns}:gui/dispatch
""",
    )
    write(
        P / "gui/scan_loop.mcfunction",
        f"""
execute if score #slot {ns}.tmp matches 27.. run return 0
execute store result storage {ns}:macro slot int 1 run scoreboard players get #slot {ns}.tmp
function {ns}:gui/scan_slot with storage {ns}:macro
scoreboard players add #slot {ns}.tmp 1
function {ns}:gui/scan_loop
""",
    )
    write(
        P / "gui/scan_slot.mcfunction",
        f"""
$execute unless data storage {ns}:live Items[{{Slot:$(slot)b,components:{{"minecraft:custom_data":{{gui:1b,pack:"{ns}"}}}}}}] run function {ns}:gui/slot_bad with storage {ns}:macro
""",
    )
    write(
        P / "gui/slot_bad.mcfunction",
        f"""
$execute if data storage {ns}:live Items[{{Slot:$(slot)b}}] run function {ns}:gui/return_item with storage {ns}:macro
function {ns}:gui/queue_slot with storage {ns}:macro
scoreboard players set #dirty {ns}.tmp 1
""",
    )
    write(
        P / "gui/return_item.mcfunction",
        f"""
summon minecraft:item ~ ~0.2 ~ {{PickupDelay:0s,Tags:["{ns}.return"],Item:{{id:"minecraft:stone",count:1}}}}
$data modify entity @e[type=minecraft:item,tag={ns}.return,limit=1,sort=nearest] Item set from storage {ns}:live Items[{{Slot:$(slot)b}}]
data remove entity @e[type=minecraft:item,tag={ns}.return,limit=1,sort=nearest] Item.Slot
tag @e[type=minecraft:item,tag={ns}.return,limit=1,sort=nearest] remove {ns}.return
playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.4 1.2
""",
    )
    write(
        P / "gui/queue_slot.mcfunction",
        f"""
$execute unless data storage {ns}:rt p$(pid).actions.s$(slot) run return 0
$data modify storage {ns}:tmp act set from storage {ns}:rt p$(pid).actions.s$(slot)
execute if data storage {ns}:tmp {{act:"none"}} run return 0
$execute if data storage {ns}:rt p$(pid).queue run return 0
$data modify storage {ns}:rt p$(pid).queue set from storage {ns}:tmp act
""",
    )
    write(
        P / "gui/dispatch.mcfunction",
        f"""
execute store result storage {ns}:macro pid int 1 run scoreboard players get @s {ns}.id
function {ns}:gui/dispatch_m with storage {ns}:macro
""",
    )
    write(
        P / "gui/dispatch_m.mcfunction",
        f"""
$execute unless data storage {ns}:rt p$(pid).queue run return 0
$data modify storage {ns}:macro action set from storage {ns}:rt p$(pid).queue
$data remove storage {ns}:rt p$(pid).queue
function {ns}:gui/dispatch_call with storage {ns}:macro
""",
    )
    write(
        P / "gui/dispatch_call.mcfunction",
        f"$function {ns}:act/$(action)",
    )
    write(
        P / "assign_id.mcfunction",
        f"""
scoreboard players add #next {ns}.id 1
scoreboard players operation @s {ns}.id = #next {ns}.id
execute store result storage {ns}:macro pid int 1 run scoreboard players get @s {ns}.id
function {ns}:assign_store with storage {ns}:macro
""",
    )
    if vault:
        write(
            P / "assign_store.mcfunction",
            f'$execute unless data storage {ns}:rt p$(pid) run data modify storage {ns}:rt p$(pid) set value {{A:{{}},B:{{}},C:{{}}}}',
        )
    else:
        write(P / "assign_store.mcfunction", f"$execute unless data storage {ns}:rt p$(pid) run data modify storage {ns}:rt p$(pid) set value {{}}")
    objs_remove = [
        ns,
        f"{ns}.id",
        f"{ns}.page",
        f"{ns}.back",
        f"{ns}.grace",
        f"{ns}.tmp",
        f"{ns}.dead",
        f"{ns}.use",
    ]
    if ns == "bazaar":
        objs_remove += ["bazaar.bank", "bazaar.day"]
    if ns == "atlas":
        objs_remove += ["atlas.cd", "atlas.mode", "atlas.sel", "atlas.timer"]
    if ns == "vault":
        objs_remove += ["vault.used"]
    removes = "\n".join(f"scoreboard objectives remove {o}" for o in objs_remove)
    storages = " ".join(f"{ns}:{s}" for s in ["config", "rt", "live", "tmp", "macro", "shop", "defaults", "dest"])
    write(
        P / "uninstall.mcfunction",
        f"""
tag @a remove {ns}.open
tag @a remove {ns}.welcomed
kill @e[type=minecraft:chest_minecart,tag={ns}.cart]
{removes}
data remove storage {ns}:config
data remove storage {ns}:rt
data remove storage {ns}:live
data remove storage {ns}:tmp
data remove storage {ns}:macro
data remove storage {ns}:shop
data remove storage {ns}:defaults
data remove storage {ns}:dest
tellraw @a {{"text":"{title} kaldırıldı. Ardından datapack klasörünü sil.","color":"red"}}
""",
    )
    # silence unused
    del storages

def page(folder: Path, ns: str, name: str, title: str, color: str, slots: list[dict | None], pack_actions_ok: bool = True) -> None:
    actions: list[str] = []
    items: list[str] = []
    for i, slot in enumerate(slots):
        if slot is None:
            items.append(filler(i, ns))
            actions.append("none")
        else:
            items.append(
                snbt_item(
                    i,
                    slot["id"],
                    slot["name"],
                    slot.get("lore", []),
                    ns,
                    glint=slot.get("glint", False),
                    count=slot.get("count", 1),
                    color=slot.get("color"),
                )
            )
            actions.append(slot.get("action", "none"))
    P = folder / "data" / ns / "function"
    write(
        P / f"page/{name}.mcfunction",
        f"""
data merge entity @e[type=minecraft:chest_minecart,tag={ns}.this,limit=1] {{CustomName:{jtext(title, color)},Items:[{",".join(items)}]}}
execute store result storage {ns}:macro pid int 1 run scoreboard players get @s {ns}.id
function {ns}:page/{name}_act with storage {ns}:macro
""",
    )
    write(
        P / f"page/{name}_act.mcfunction",
        f"$data modify storage {ns}:rt p$(pid).actions set value {actions_snbt(actions)}",
    )
    for action in actions:
        if action != "none":
            pack_actions_ok = pack_actions_ok
    return actions

def blank() -> list[None]:
    return [None] * 27

def put(slots: list, index: int, **kwargs) -> None:
    slots[index] = kwargs

# ---------- bazaar ----------
BUY = "buy"
SELL = "sell"

def shop_tuple(key, item, name, count, price, stock, mode):
    return {"key": key, "id": item, "name": name, "count": count, "price": price, "stock": stock, "mode": mode}

BLOCKS = [
    shop_tuple("stone", "minecraft:stone", "Tas", 64, 1, -1, BUY),
    shop_tuple("cobble", "minecraft:cobblestone", "Kiriktas", 64, 1, -1, BUY),
    shop_tuple("oak_log", "minecraft:oak_log", "Mese kutugu", 32, 2, -1, BUY),
    shop_tuple("glass", "minecraft:glass", "Cam", 32, 3, -1, BUY),
    shop_tuple("bricks", "minecraft:bricks", "Tugla", 32, 4, -1, BUY),
    shop_tuple("obsidian", "minecraft:obsidian", "Obsidyen", 8, 6, -1, BUY),
    shop_tuple("netherrack", "minecraft:netherrack", "Nether kayasi", 64, 2, -1, BUY),
    shop_tuple("end_stone", "minecraft:end_stone", "End tasi", 32, 4, -1, BUY),
    shop_tuple("deepslate", "minecraft:deepslate", "Derin kayrak", 64, 2, -1, BUY),
    shop_tuple("concrete", "minecraft:white_concrete", "Beyaz beton", 32, 3, -1, BUY),
    shop_tuple("lantern", "minecraft:lantern", "Fener", 8, 2, -1, BUY),
    shop_tuple("bookshelf", "minecraft:bookshelf", "Kitaplik", 4, 3, -1, BUY),
    shop_tuple("crying", "minecraft:crying_obsidian", "Aglayan obsidyen", 4, 8, 16, BUY),
    shop_tuple("debris", "minecraft:ancient_debris", "Antik kalinti", 1, 48, 2, BUY),
    shop_tuple("moss", "minecraft:moss_block", "Yosun blogu", 32, 2, -1, BUY),
    shop_tuple("mud", "minecraft:mud_bricks", "Camur tugla", 32, 2, -1, BUY),
    shop_tuple("amethyst", "minecraft:amethyst_block", "Ametist blogu", 4, 6, -1, BUY),
    shop_tuple("sponge", "minecraft:sponge", "Sunger", 1, 16, 4, BUY),
]
FOOD = [
    shop_tuple("bread", "minecraft:bread", "Ekmek", 16, 1, -1, BUY),
    shop_tuple("beef", "minecraft:cooked_beef", "Pismis biftek", 16, 3, -1, BUY),
    shop_tuple("gcarrot", "minecraft:golden_carrot", "Altin havuc", 8, 6, -1, BUY),
    shop_tuple("gapple", "minecraft:golden_apple", "Altin elma", 1, 16, 8, BUY),
    shop_tuple("egapple", "minecraft:enchanted_golden_apple", "Buyulu altin elma", 1, 64, 1, BUY),
    shop_tuple("cake", "minecraft:cake", "Pasta", 1, 4, -1, BUY),
    shop_tuple("pie", "minecraft:pumpkin_pie", "Balkabagi turtasi", 8, 2, -1, BUY),
    shop_tuple("cod", "minecraft:cooked_cod", "Pismis morina", 16, 2, -1, BUY),
    shop_tuple("honey", "minecraft:honey_bottle", "Bal sisesi", 4, 4, -1, BUY),
    shop_tuple("berries", "minecraft:sweet_berries", "Tatli yemis", 16, 1, -1, BUY),
    shop_tuple("beet", "minecraft:beetroot_soup", "Pancar corbasi", 4, 2, -1, BUY),
    shop_tuple("stew", "minecraft:mushroom_stew", "Mantar yahnisi", 4, 2, -1, BUY),
    shop_tuple("cookie", "minecraft:cookie", "Kurabiye", 16, 1, -1, BUY),
    shop_tuple("kelp", "minecraft:dried_kelp", "Kurutulmus yosun", 32, 1, -1, BUY),
    shop_tuple("rabbit", "minecraft:rabbit_stew", "Tavsan yahnisi", 2, 4, -1, BUY),
    shop_tuple("potato", "minecraft:baked_potato", "Firinlanmis patates", 16, 1, -1, BUY),
    shop_tuple("chorus", "minecraft:chorus_fruit", "Koro meyvesi", 8, 5, -1, BUY),
    shop_tuple("apple", "minecraft:apple", "Elma", 16, 1, -1, BUY),
]
COMBAT = [
    shop_tuple("sword", "minecraft:iron_sword", "Demir kilic", 1, 8, -1, BUY),
    shop_tuple("bow", "minecraft:bow", "Yay", 1, 6, -1, BUY),
    shop_tuple("arrow", "minecraft:arrow", "Ok", 32, 2, -1, BUY),
    shop_tuple("shield", "minecraft:shield", "Kalkan", 1, 6, -1, BUY),
    shop_tuple("ihelm", "minecraft:iron_helmet", "Demir migfer", 1, 8, -1, BUY),
    shop_tuple("ichest", "minecraft:iron_chestplate", "Demir zırh", 1, 12, -1, BUY),
    shop_tuple("ilegs", "minecraft:iron_leggings", "Demir pantolon", 1, 10, -1, BUY),
    shop_tuple("iboots", "minecraft:iron_boots", "Demir bot", 1, 8, -1, BUY),
    shop_tuple("crossbow", "minecraft:crossbow", "Arbalet", 1, 10, -1, BUY),
    shop_tuple("pearl", "minecraft:ender_pearl", "Ender incisi", 1, 6, -1, BUY),
    shop_tuple("wind", "minecraft:wind_charge", "Ruzgar yuku", 4, 4, -1, BUY),
    shop_tuple("web", "minecraft:cobweb", "Orumcek agi", 4, 3, -1, BUY),
    shop_tuple("totem", "minecraft:totem_of_undying", "Totem", 1, 48, 2, BUY),
    shop_tuple("turtle", "minecraft:turtle_helmet", "Kaplumbaga kabugu", 1, 16, -1, BUY),
    shop_tuple("trident", "minecraft:trident", "Uc disli mizrak", 1, 32, 2, BUY),
    shop_tuple("mace", "minecraft:mace", "Topuz", 1, 64, 1, BUY),
    shop_tuple("brod", "minecraft:breeze_rod", "Esinti cubugu", 4, 8, -1, BUY),
    shop_tuple("xpb", "minecraft:experience_bottle", "Deneyim sisesi", 8, 6, -1, BUY),
]
REDSTONE = [
    shop_tuple("redstone", "minecraft:redstone", "Kiziltas", 32, 4, -1, BUY),
    shop_tuple("repeater", "minecraft:repeater", "Tekrarlayici", 4, 3, -1, BUY),
    shop_tuple("comparator", "minecraft:comparator", "Karsilastirici", 2, 4, -1, BUY),
    shop_tuple("piston", "minecraft:piston", "Piston", 4, 4, -1, BUY),
    shop_tuple("sticky", "minecraft:sticky_piston", "Yapiskan piston", 2, 6, -1, BUY),
    shop_tuple("observer", "minecraft:observer", "Gozlemci", 2, 5, -1, BUY),
    shop_tuple("hopper", "minecraft:hopper", "Huni", 2, 8, -1, BUY),
    shop_tuple("dispenser", "minecraft:dispenser", "Firlatıcı", 2, 6, -1, BUY),
    shop_tuple("dropper", "minecraft:dropper", "Birakici", 4, 3, -1, BUY),
    shop_tuple("slime", "minecraft:slime_ball", "Balcik topu", 4, 4, -1, BUY),
    shop_tuple("note", "minecraft:note_block", "Nota bloğu", 2, 3, -1, BUY),
    shop_tuple("target", "minecraft:target", "Hedef", 1, 4, -1, BUY),
    shop_tuple("rod", "minecraft:lightning_rod", "Paratoner", 2, 3, -1, BUY),
    shop_tuple("lamp", "minecraft:redstone_lamp", "Kiziltas lambasi", 4, 4, -1, BUY),
    shop_tuple("tnt", "minecraft:tnt", "Dinamit", 4, 8, -1, BUY),
    shop_tuple("daylight", "minecraft:daylight_detector", "Gun isigi algilayici", 1, 3, -1, BUY),
    shop_tuple("lectern", "minecraft:lectern", "Kursu", 1, 3, -1, BUY),
    shop_tuple("crafter", "minecraft:crafter", "Uretici", 1, 12, 8, BUY),
]
RARE = [
    shop_tuple("ningot", "minecraft:netherite_ingot", "Netherite kulcesi", 1, 48, 3, BUY),
    shop_tuple("diamond", "minecraft:diamond", "Elmas", 1, 12, -1, BUY),
    shop_tuple("elytra", "minecraft:elytra", "Elitra", 1, 96, 1, BUY),
    shop_tuple("shulker", "minecraft:shulker_box", "Shulker kutusu", 1, 24, 4, BUY),
    shop_tuple("nametag", "minecraft:name_tag", "Isim etiketi", 1, 8, -1, BUY),
    shop_tuple("saddle", "minecraft:saddle", "Eyer", 1, 8, -1, BUY),
    shop_tuple("heart", "minecraft:heart_of_the_sea", "Deniz kalbi", 1, 32, 2, BUY),
    shop_tuple("beacon", "minecraft:beacon", "Isik feneri", 1, 72, 1, BUY),
    shop_tuple("conduit", "minecraft:conduit", "Kanal", 1, 48, 1, BUY),
    shop_tuple("rcompass", "minecraft:recovery_compass", "Kurtarma pusulası", 1, 16, -1, BUY),
    shop_tuple("lode", "minecraft:lodestone", "Miknatis tasi", 1, 10, -1, BUY),
    shop_tuple("crystal", "minecraft:end_crystal", "End kristalı", 1, 24, 4, BUY),
    shop_tuple("breath", "minecraft:dragon_breath", "Ejderha nefesi", 1, 12, -1, BUY),
    shop_tuple("spore", "minecraft:spore_blossom", "Spor çiçeği", 1, 8, -1, BUY),
    shop_tuple("sniffer", "minecraft:sniffer_egg", "Koklayici yumurtasi", 1, 40, 2, BUY),
    shop_tuple("star", "minecraft:nether_star", "Nether yildizi", 1, 64, 2, BUY),
    shop_tuple("echo", "minecraft:echo_shard", "Yankı parcasi", 1, 20, -1, BUY),
    shop_tuple("core", "minecraft:heavy_core", "Agir cekirdek", 1, 36, 2, BUY),
]
SELLS = [
    shop_tuple("sflesh", "minecraft:rotten_flesh", "Curuk et", 32, 1, -1, SELL),
    shop_tuple("sbone", "minecraft:bone", "Kemik", 32, 1, -1, SELL),
    shop_tuple("sstring", "minecraft:string", "Ip", 32, 1, -1, SELL),
    shop_tuple("sgun", "minecraft:gunpowder", "Barut", 16, 2, -1, SELL),
    shop_tuple("spearl", "minecraft:ender_pearl", "Ender incisi", 4, 4, -1, SELL),
    shop_tuple("sblaze", "minecraft:blaze_rod", "Blaze cubugu", 4, 6, -1, SELL),
    shop_tuple("sdia", "minecraft:diamond", "Elmas", 1, 8, -1, SELL),
    shop_tuple("sdebris", "minecraft:ancient_debris", "Antik kalinti", 1, 24, -1, SELL),
    shop_tuple("sscrap", "minecraft:netherite_scrap", "Netherite parcasi", 1, 20, -1, SELL),
    shop_tuple("scoal", "minecraft:coal", "Komur", 64, 1, -1, SELL),
    shop_tuple("siron", "minecraft:iron_ingot", "Demir kulcesi", 8, 2, -1, SELL),
    shop_tuple("sgold", "minecraft:gold_ingot", "Altin kulcesi", 8, 2, -1, SELL),
    shop_tuple("scopper", "minecraft:copper_ingot", "Bakir kulcesi", 32, 1, -1, SELL),
    shop_tuple("swheat", "minecraft:wheat", "Bugday", 64, 1, -1, SELL),
    shop_tuple("smem", "minecraft:phantom_membrane", "Hayalet zarı", 2, 3, -1, SELL),
    shop_tuple("sbrod", "minecraft:breeze_rod", "Esinti cubugu", 2, 4, -1, SELL),
    shop_tuple("seye", "minecraft:spider_eye", "Orumcek gozu", 16, 1, -1, SELL),
    shop_tuple("sleather", "minecraft:leather", "Deri", 16, 1, -1, SELL),
]

# Fix names that I stripped accents from - user is Turkish, use proper Turkish without apostrophes.
# I'll override names with proper unicode now.
NAME_FIX = {
    "Tas": "Taş",
    "Kiriktas": "Kırıktaş",
    "Mese kutugu": "Meşe kütüğü",
    "Tugla": "Tuğla",
    "Nether kayasi": "Nether kayası",
    "End tasi": "End taşı",
    "Kitaplik": "Kitaplık",
    "Aglayan obsidyen": "Ağlayan obsidyen",
    "Antik kalinti": "Antik kalıntı",
    "Yosun blogu": "Yosun bloğu",
    "Camur tugla": "Çamur tuğla",
    "Ametist blogu": "Ametist bloğu",
    "Sunger": "Sünger",
    "Pismis biftek": "Pişmiş biftek",
    "Altin havuc": "Altın havuç",
    "Altin elma": "Altın elma",
    "Buyulu altin elma": "Büyülü altın elma",
    "Balkabagi turtasi": "Balkabağı turtası",
    "Pismis morina": "Pişmiş morina",
    "Bal sisesi": "Bal şişesi",
    "Tatli yemis": "Tatlı yemiş",
    "Pancar corbasi": "Pancar çorbası",
    "Kurutulmus yosun": "Kurutulmuş yosun",
    "Tavsan yahnisi": "Tavşan yahnisi",
    "Firinlanmis patates": "Fırınlanmış patates",
    "Demir kilic": "Demir kılıç",
    "Demir migfer": "Demir miğfer",
    "Demir zırh": "Demir göğüslük",
    "Ruzgar yuku": "Rüzgar yükü",
    "Orumcek agi": "Örümcek ağı",
    "Kaplumbaga kabugu": "Kaplumbağa kabuğu",
    "Uc disli mizrak": "Üç dişli mızrak",
    "Esinti cubugu": "Esinti çubuğu",
    "Deneyim sisesi": "Deneyim şişesi",
    "Kiziltas": "Kızıltaş",
    "Tekrarlayici": "Tekrarlayıcı",
    "Karsilastirici": "Karşılaştırıcı",
    "Yapiskan piston": "Yapışkan piston",
    "Gozlemci": "Gözlemci",
    "Firlatıcı": "Fırlatıcı",
    "Birakici": "Bırakıcı",
    "Balcik topu": "Balçık topu",
    "Kiziltas lambasi": "Kızıltaş lambası",
    "Gun isigi algilayici": "Gün ışığı algılayıcı",
    "Kursu": "Kürsü",
    "Uretici": "Üretici",
    "Netherite kulcesi": "Netherite külçesi",
    "Isim etiketi": "İsim etiketi",
    "Isik feneri": "Işık feneri",
    "Miknatis tasi": "Mıknatıs taşı",
    "Koklayici yumurtasi": "Koklayıcı yumurtası",
    "Nether yildizi": "Nether yıldızı",
    "Yankı parcasi": "Yankı parçası",
    "Agir cekirdek": "Ağır çekirdek",
    "Curuk et": "Çürük et",
    "Ip": "İp",
    "Blaze cubugu": "Blaze çubuğu",
    "Netherite parcasi": "Netherite parçası",
    "Komur": "Kömür",
    "Demir kulcesi": "Demir külçesi",
    "Altin kulcesi": "Altın külçesi",
    "Bakir kulcesi": "Bakır külçesi",
    "Bugday": "Buğday",
    "Orumcek gozu": "Örümcek gözü",
}
for group in (BLOCKS, FOOD, COMBAT, REDSTONE, RARE, SELLS):
    for it in group:
        it["name"] = NAME_FIX.get(it["name"], it["name"])

def shop_snbt(items: list[dict]) -> str:
    parts = []
    for it in items:
        parts.append(
            f'{it["key"]}:{{id:"{it["id"]}",count:{it["count"]},price:{it["price"]},stock:{it["stock"]},name:"{it["name"]}",mode:"{it["mode"]}"}}'
        )
    return "{" + ",".join(parts) + "}"

def category_slots(items: list[dict], mode: str) -> list:
    slots = blank()
    verb = "Satın almak için tıkla" if mode == BUY else "Satmak için tıkla"
    for i, it in enumerate(items):
        stock = "Sınırsız stok" if it["stock"] < 0 else f"Stok sınırı {it['stock']}"
        price = f"{it['price']} zümrüt"
        put(
            slots,
            i,
            id=it["id"],
            name=it["name"],
            color="gold" if mode == BUY else "green",
            lore=[(price, "green"), (stock, "aqua"), (verb, "gray"), ("İşlem fiyatı depodan okunur", "dark_gray")],
            action=f'{"buy" if mode == BUY else "sell"}_{it["key"]}',
            glint=it["stock"] >= 0,
            count=1,
        )
    put(slots, 18, id="minecraft:arrow", name="Geri", color="yellow", lore=[("Ana sayfa", "gray")], action="page_main")
    put(slots, 22, id="minecraft:emerald", name="Bakiye", color="green", lore=[("Tam bakiye aksiyon çubuğunda", "gray"), ("Banka sayfasından yönet", "dark_gray")], action="page_bank")
    put(slots, 26, id="minecraft:barrier", name="Kapat", color="red", lore=[("Menüyü kapat", "gray")], action="close")
    return slots

def write_bazaar(folder: Path) -> None:
    ns = "bazaar"
    mcmeta(folder, "Zümrüt Çarşı", "gold", "Chest GUI dükkan • 1.21.3")
    png(folder / "pack.png", (184, 132, 46), (80, 200, 90))
    tags(folder, ns)
    engine(folder, ns, "Zümrüt Çarşı", "gold", "minecraft:warped_fungus_on_a_stick", vault=False)
    P = folder / "data" / ns / "function"
    write(
        P / "init.mcfunction",
        f"""
data modify storage bazaar:shop items set value {shop_snbt(BLOCKS + FOOD + COMBAT + REDSTONE + RARE + SELLS)}
data modify storage bazaar:defaults items set from storage bazaar:shop items
data modify storage bazaar:config set value {{ready:1b,daily:8}}
""",
    )
    write(
        P / "welcome.mcfunction",
        """
tag @s add bazaar.welcomed
execute unless score @s bazaar.id matches 1.. run function bazaar:assign_id
scoreboard players set @s bazaar.day -1
function bazaar:give_key
tellraw @s [{"text":"Çarşı asası verildi. ","color":"gold"},{"text":"Sağ tıkla","color":"yellow","bold":true},{"text":" veya ","color":"gray"},{"text":"/trigger bazaar","color":"aqua","underlined":true,"clickEvent":{"action":"run_command","value":"/trigger bazaar"}}]
""",
    )
    write(
        P / "give_key.mcfunction",
        f"""
give @s minecraft:warped_fungus_on_a_stick[custom_name={jtext("Çarşı Asası", "gold", bold=True)},lore={lore_snbt([("Sağ tık: çarşıyı aç", "gray"), ("/trigger bazaar", "dark_gray")])},custom_data={{key:1b,pack:"bazaar"}},max_stack_size=1,enchantment_glint_override=true] 1
""",
    )
    # pages
    main = blank()
    put(main, 0, id="minecraft:bricks", name="Bloklar", color="gold", lore=[("İnşaat malzemeleri", "gray")], action="page_blocks", glint=True)
    put(main, 1, id="minecraft:cooked_beef", name="Yiyecek", color="gold", lore=[("Yemek ve iksirlik", "gray")], action="page_food", glint=True)
    put(main, 2, id="minecraft:iron_sword", name="Savaş", color="red", lore=[("Silah ve zırh", "gray")], action="page_combat", glint=True)
    put(main, 3, id="minecraft:redstone", name="Kızıltaş", color="red", lore=[("Mekanizmalar", "gray")], action="page_redstone", glint=True)
    put(main, 4, id="minecraft:nether_star", name="Nadir", color="light_purple", lore=[("Sınırlı stoklar", "gray")], action="page_rare", glint=True)
    put(main, 5, id="minecraft:gold_ingot", name="Satış", color="green", lore=[("Eşya karşılığı zümrüt", "gray")], action="page_sell", glint=True)
    put(main, 6, id="minecraft:emerald", name="Banka", color="green", lore=[("Yatır, çek, bakiye", "gray")], action="page_bank")
    put(main, 7, id="minecraft:book", name="Yardım", color="aqua", lore=[("Nasıl kullanılır", "gray")], action="page_help")
    put(main, 13, id="minecraft:paper", name="Zümrüt Çarşı", color="gold", lore=[("Ödeme banka bakiyesinden", "gray"), ("Onay ekranı fiyatı esas alır", "yellow"), ("Yönetici: /tag @s add bazaar.admin", "dark_gray")], action="none")
    put(main, 22, id="minecraft:sunflower", name="Günlük ödül", color="yellow", lore=[("Her Minecraft günü 8 zümrüt", "gray")], action="daily", glint=True)
    put(main, 26, id="minecraft:barrier", name="Kapat", color="red", lore=[("Veya eğil", "gray")], action="close")
    page(folder, ns, "main", "Zümrüt Çarşı", "gold", main)
    # admin overlay appended
    text = (P / "page/main.mcfunction").read_text(encoding="utf-8")
    text += "\nexecute if entity @s[tag=bazaar.admin] run function bazaar:page/admin_button\n"
    write(P / "page/main.mcfunction", text)
    write(
        P / "page/admin_button.mcfunction",
        f"""
item replace entity @e[type=minecraft:chest_minecart,tag=bazaar.this,limit=1] container.8 with minecraft:emerald_block[custom_name={jtext("Stok yönetimi", "green", bold=True)},lore={lore_snbt([("Sınırlı stokları sıfırla", "gray"), ("Yalnız yöneticide görünür", "dark_gray")])},custom_data={{gui:1b,pack:"bazaar"}},max_stack_size=1,enchantment_glint_override=true]
execute store result storage bazaar:macro pid int 1 run scoreboard players get @s bazaar.id
function bazaar:page/admin_act with storage bazaar:macro
""",
    )
    write(P / "page/admin_act.mcfunction", '$data modify storage bazaar:rt p$(pid).actions.s8 set value "admin_page"')
    page(folder, ns, "blocks", "Çarşı • Bloklar", "gold", category_slots(BLOCKS, BUY))
    page(folder, ns, "food", "Çarşı • Yiyecek", "gold", category_slots(FOOD, BUY))
    page(folder, ns, "combat", "Çarşı • Savaş", "red", category_slots(COMBAT, BUY))
    page(folder, ns, "redstone", "Çarşı • Kızıltaş", "red", category_slots(REDSTONE, BUY))
    page(folder, ns, "rare", "Çarşı • Nadir", "light_purple", category_slots(RARE, BUY))
    page(folder, ns, "sell", "Çarşı • Satış", "green", category_slots(SELLS, SELL))
    bank = blank()
    put(bank, 4, id="minecraft:paper", name="Banka", color="green", lore=[("Zümrütler burada durur", "gray"), ("Alışveriş bakiyeden düşer", "gray"), ("Tam sayı aksiyon çubuğunda", "yellow")], action="none")
    put(bank, 11, id="minecraft:emerald", name="64 yatır", color="green", lore=[("Envanterden bankaya", "gray")], action="bank_deposit")
    put(bank, 13, id="minecraft:emerald_block", name="Hepsini yatır", color="green", lore=[("Tüm zümrütler", "gray")], action="bank_all", glint=True)
    put(bank, 15, id="minecraft:gold_ingot", name="64 çek", color="yellow", lore=[("Bankadan envantere", "gray")], action="bank_withdraw")
    put(bank, 18, id="minecraft:arrow", name="Geri", color="yellow", lore=[("Ana sayfa", "gray")], action="page_main")
    put(bank, 26, id="minecraft:barrier", name="Kapat", color="red", lore=[("Menüyü kapat", "gray")], action="close")
    page(folder, ns, "bank", "Çarşı • Banka", "green", bank)
    help_slots = blank()
    put(help_slots, 0, id="minecraft:warped_fungus_on_a_stick", name="Açılış", color="gold", lore=[("Asaya sağ tıkla", "gray"), ("veya /trigger bazaar", "aqua")], action="none")
    put(help_slots, 1, id="minecraft:emerald", name="Para", color="green", lore=[("Önce bankaya yatır", "gray"), ("Fiyat onayda görünür", "gray")], action="none")
    put(help_slots, 2, id="minecraft:chest", name="Tıklama", color="yellow", lore=[("Düğmeyi alman gerekmez", "gray"), ("Alan eşya iade edilir", "gray"), ("Menü eşyası silinir", "dark_gray")], action="none")
    put(help_slots, 3, id="minecraft:hopper", name="Güvenlik", color="red", lore=[("Huni altına koyma", "gray"), ("GUI eşyası temizlenir", "gray"), ("Yaratıcı orta tık da silinir", "dark_gray")], action="none")
    put(help_slots, 4, id="minecraft:command_block", name="Yönetici", color="light_purple", lore=[("/tag @s add bazaar.admin", "gray"), ("Stok sıfırlama düğmesi", "gray")], action="none", glint=True)
    put(help_slots, 18, id="minecraft:arrow", name="Geri", color="yellow", lore=[("Ana sayfa", "gray")], action="page_main")
    put(help_slots, 26, id="minecraft:barrier", name="Kapat", color="red", lore=[("Menüyü kapat", "gray")], action="close")
    # command block as icon is ok as a GUI display item with gui tag, cleared if taken. User cares about security - a command block icon could be taken for 1 tick before clear. That's a problem in creative. In survival command blocks can't be taken/placed without op... if they TAKE the item into inventory, clear removes it next tick. If they place it same tick... unlikely in survival because mining/placing command block needs op. The item existing 1 tick in survival inventory then cleared is OK. I'll still avoid command_block and use structure... no, use jukebox or lectern.
    help_slots[4]["id"] = "minecraft:lectern"
    page(folder, ns, "help", "Çarşı • Yardım", "aqua", help_slots)
    confirm = blank()
    put(confirm, 4, id="minecraft:paper", name="Onay", color="yellow", lore=[("Sohbet fiyatı gösterir", "gray"), ("Yeşil: onayla", "green"), ("Kırmızı: vazgeç", "red")], action="none")
    put(confirm, 11, id="minecraft:red_wool", name="Vazgeç", color="red", lore=[("İşlemi iptal et", "gray")], action="buy_no")
    put(confirm, 13, id="minecraft:paper", name="Ürün", color="white", lore=[("Yükleniyor", "gray")], action="none")
    put(confirm, 15, id="minecraft:lime_wool", name="Onayla", color="green", lore=[("Bakiyeyi kullan", "gray")], action="buy_yes", glint=True)
    put(confirm, 22, id="minecraft:arrow", name="Geri", color="yellow", lore=[("Kategoriye dön", "gray")], action="buy_no")
    put(confirm, 26, id="minecraft:barrier", name="Kapat", color="red", lore=[("Menüyü kapat", "gray")], action="close")
    page(folder, ns, "confirm", "Çarşı • Onay", "yellow", confirm)
    text = (P / "page/confirm.mcfunction").read_text(encoding="utf-8")
    text += "\nfunction bazaar:page/confirm_icon\n"
    write(P / "page/confirm.mcfunction", text)
    write(
        P / "page/confirm_icon.mcfunction",
        """
execute store result storage bazaar:macro pid int 1 run scoreboard players get @s bazaar.id
function bazaar:page/confirm_icon_m with storage bazaar:macro
""",
    )
    write(
        P / "page/confirm_icon_m.mcfunction",
        """
$data modify storage bazaar:tmp offer set from storage bazaar:rt p$(pid).offer
function bazaar:page/confirm_icon_put with storage bazaar:tmp offer
""",
    )
    write(
        P / "page/confirm_icon_put.mcfunction",
        f"""
$item replace entity @e[type=minecraft:chest_minecart,tag=bazaar.this,limit=1] container.13 with $(id) $(count)
data modify entity @e[type=minecraft:chest_minecart,tag=bazaar.this,limit=1] Items[{{Slot:13b}}].components."minecraft:custom_data" set value {{gui:1b,pack:"bazaar"}}
function bazaar:page/confirm_icon_name with storage bazaar:tmp offer
""",
    )
    write(
        P / "page/confirm_icon_name.mcfunction",
        f"""
$data modify entity @e[type=minecraft:chest_minecart,tag=bazaar.this,limit=1] Items[{{Slot:13b}}].components."minecraft:custom_name" set value {{{{jtext("PLACEHOLDER")}}}}
""".replace("'" + json.dumps({"text": "PLACEHOLDER", "italic": False}, separators=(",", ":")) + "'", "'{\"text\":\"$(name)\",\"italic\":false,\"color\":\"white\"}'"),
    )
    # The replace above is fragile. Write the function explicitly.
    write(
        P / "page/confirm_icon_name.mcfunction",
        """
$data modify entity @e[type=minecraft:chest_minecart,tag=bazaar.this,limit=1] Items[{Slot:13b}].components."minecraft:custom_name" set value '{"text":"$(name)","italic":false,"color":"white"}'
$data modify entity @e[type=minecraft:chest_minecart,tag=bazaar.this,limit=1] Items[{Slot:13b}].components."minecraft:lore" set value ['{"text":"Önizleme","italic":false,"color":"gray"}','{"text":"Bu eşya alınamaz","italic":false,"color":"dark_gray"}']
""",
    )
    write(
        P / "gui/render.mcfunction",
        """
execute if score @s bazaar.page matches 0 run function bazaar:page/main
execute if score @s bazaar.page matches 1 run function bazaar:page/blocks
execute if score @s bazaar.page matches 2 run function bazaar:page/food
execute if score @s bazaar.page matches 3 run function bazaar:page/combat
execute if score @s bazaar.page matches 4 run function bazaar:page/redstone
execute if score @s bazaar.page matches 5 run function bazaar:page/rare
execute if score @s bazaar.page matches 6 run function bazaar:page/sell
execute if score @s bazaar.page matches 7 run function bazaar:page/bank
execute if score @s bazaar.page matches 8 run function bazaar:page/help
execute if score @s bazaar.page matches 9 run function bazaar:page/confirm
execute if score @s bazaar.page matches 10 run function bazaar:page/admin
title @s actionbar [{"text":"Bakiye ","color":"gray"},{"score":{"name":"@s","objective":"bazaar.bank"},"color":"green"},{"text":" zümrüt","color":"dark_gray"}]
""",
    )
    admin = blank()
    put(admin, 11, id="minecraft:emerald_block", name="Stokları sıfırla", color="green", lore=[("Varsayılan stok ve fiyat", "gray"), ("Oyuncu bakiyesine dokunmaz", "yellow")], action="restock", glint=True)
    put(admin, 13, id="minecraft:paper", name="Düzen", color="aqua", lore=[("Fiyatlar storage bazaar:shop", "gray"), ("items.<anahtar>.price", "gray"), ("Onay ekranı canlı okur", "yellow")], action="none")
    put(admin, 15, id="minecraft:book", name="Anahtarlar", color="white", lore=[("Sınırlı ürünler glintli", "gray"), ("stock -1 sınırsız", "gray")], action="none")
    put(admin, 18, id="minecraft:arrow", name="Geri", color="yellow", lore=[("Ana sayfa", "gray")], action="page_main")
    put(admin, 26, id="minecraft:barrier", name="Kapat", color="red", lore=[("Menüyü kapat", "gray")], action="close")
    page(folder, ns, "admin", "Çarşı • Yönetici", "green", admin)

    def simple_page(action: str, body: str) -> None:
        write(P / f"act/{action}.mcfunction", body.strip() + "\n")

    for action, pg in [
        ("page_main", 0),
        ("page_blocks", 1),
        ("page_food", 2),
        ("page_combat", 3),
        ("page_redstone", 4),
        ("page_rare", 5),
        ("page_sell", 6),
        ("page_bank", 7),
        ("page_help", 8),
        ("admin_page", 10),
    ]:
        simple_page(
            action,
            f"""
scoreboard players set @s bazaar.page {pg}
function bazaar:gui/render
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.45 1.2
""",
        )
    simple_page("close", "function bazaar:gui/close")
    simple_page(
        "buy_no",
        """
scoreboard players operation @s bazaar.page = @s bazaar.back
function bazaar:gui/render
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.4 0.9
""",
    )
    simple_page(
        "daily",
        """
execute store result score #day bazaar.tmp run time query day
execute unless score @s bazaar.day < #day bazaar.tmp run return run function bazaar:act/fail_daily
scoreboard players operation @s bazaar.day = #day bazaar.tmp
execute store result score #gift bazaar.tmp run data get storage bazaar:config daily
execute unless score #gift bazaar.tmp matches 1.. run scoreboard players set #gift bazaar.tmp 8
scoreboard players operation @s bazaar.bank += #gift bazaar.tmp
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.4
tellraw @s [{"text":"Günlük ödül: ","color":"gold"},{"score":{"name":"#gift","objective":"bazaar.tmp"},"color":"green"},{"text":" zümrüt bankana eklendi.","color":"gray"}]
function bazaar:gui/render
""",
    )
    simple_page("fail_daily", 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.6 1\ntitle @s actionbar {"text":"Bugünün ödülü alındı.","color":"red"}')
    simple_page(
        "bank_deposit",
        """
execute store result score #moved bazaar.tmp run clear @s minecraft:emerald 64
execute if score #moved bazaar.tmp matches 0 run return run function bazaar:act/fail_noemerald
scoreboard players operation @s bazaar.bank += #moved bazaar.tmp
playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.6 1.3
tellraw @s [{"text":"Yatırıldı: ","color":"green"},{"score":{"name":"#moved","objective":"bazaar.tmp"},"color":"yellow"},{"text":" zümrüt","color":"gray"}]
function bazaar:gui/render
""",
    )
    simple_page(
        "bank_all",
        """
execute store result score #moved bazaar.tmp run clear @s minecraft:emerald 0
execute if score #moved bazaar.tmp matches 0 run return run function bazaar:act/fail_noemerald
clear @s minecraft:emerald
scoreboard players operation @s bazaar.bank += #moved bazaar.tmp
playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.7 1.1
tellraw @s [{"text":"Tümü yatırıldı: ","color":"green"},{"score":{"name":"#moved","objective":"bazaar.tmp"},"color":"yellow"}]
function bazaar:gui/render
""",
    )
    simple_page("fail_noemerald", 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.6 1\ntitle @s actionbar {"text":"Envanterde zümrüt yok.","color":"red"}')
    simple_page(
        "bank_withdraw",
        """
execute unless score @s bazaar.bank matches 1.. run return run function bazaar:act/fail_money
scoreboard players set #move bazaar.tmp 64
execute if score @s bazaar.bank < #move bazaar.tmp run scoreboard players operation #move bazaar.tmp = @s bazaar.bank
scoreboard players operation @s bazaar.bank -= #move bazaar.tmp
execute store result storage bazaar:macro n int 1 run scoreboard players get #move bazaar.tmp
function bazaar:act/give_emeralds with storage bazaar:macro
playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.6 1
tellraw @s [{"text":"Çekildi: ","color":"yellow"},{"score":{"name":"#move","objective":"bazaar.tmp"},"color":"green"},{"text":" zümrüt","color":"gray"}]
function bazaar:gui/render
""",
    )
    write(P / "act/give_emeralds.mcfunction", "$give @s minecraft:emerald $(n)\n")
    simple_page("fail_money", 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.7 1\ntitle @s actionbar {"text":"Bakiye yetmiyor.","color":"red"}')
    simple_page("fail_stock", 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.7 0.8\ntitle @s actionbar {"text":"Stok tükendi.","color":"red"}')
    simple_page("fail_items", 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.7 1\ntitle @s actionbar {"text":"Envanterde yeteri kadar yok.","color":"red"}')
    simple_page("fail_missing", 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.6 1\ntitle @s actionbar {"text":"Ürün kaydı yok.","color":"red"}')
    write(
        P / "act/prep_offer.mcfunction",
        """
scoreboard players operation @s bazaar.back = @s bazaar.page
$execute unless data storage bazaar:shop items.$(key) run return run function bazaar:act/fail_missing
$data modify storage bazaar:tmp offer set from storage bazaar:shop items.$(key)
$data modify storage bazaar:tmp offer.key set value "$(key)"
$data modify storage bazaar:tmp offer.mode set value "$(mode)"
execute store result storage bazaar:macro pid int 1 run scoreboard players get @s bazaar.id
function bazaar:act/store_offer with storage bazaar:macro
scoreboard players set @s bazaar.page 9
function bazaar:gui/render
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.5 1.15
function bazaar:act/announce_offer with storage bazaar:tmp offer
""",
    )
    write(P / "act/store_offer.mcfunction", "$data modify storage bazaar:rt p$(pid).offer set from storage bazaar:tmp offer\n")
    write(
        P / "act/announce_offer.mcfunction",
        """
$tellraw @s [{"text":"$(name)","color":"yellow","bold":true},{"text":"  x$(count)","color":"white"},{"text":"  •  ","color":"dark_gray"},{"text":"$(price) zümrüt","color":"green"},{"text":"  ($(mode))","color":"gray"}]
$scoreboard players set #stock bazaar.tmp $(stock)
execute if score #stock bazaar.tmp matches ..-1 run tellraw @s {"text":"Stok: sınırsız","color":"gray"}
execute if score #stock bazaar.tmp matches 0.. run tellraw @s [{"text":"Kalan stok: ","color":"gray"},{"score":{"name":"#stock","objective":"bazaar.tmp"},"color":"aqua"}]
execute if score #stock bazaar.tmp matches 0 run tellraw @s {"text":"Bu ürün tükendi.","color":"red"}
""",
    )
    write(
        P / "act/buy_yes.mcfunction",
        """
execute store result storage bazaar:macro pid int 1 run scoreboard players get @s bazaar.id
function bazaar:act/commit with storage bazaar:macro
""",
    )
    write(
        P / "act/commit.mcfunction",
        """
$execute unless data storage bazaar:rt p$(pid).offer.id run return run function bazaar:act/fail_missing
$function bazaar:act/commit2 with storage bazaar:rt p$(pid).offer
""",
    )
    write(
        P / "act/commit2.mcfunction",
        """
$scoreboard players set #price bazaar.tmp $(price)
$scoreboard players set #count bazaar.tmp $(count)
$scoreboard players set #stock bazaar.tmp $(stock)
$data modify storage bazaar:tmp id set value "$(id)"
$data modify storage bazaar:tmp key set value "$(key)"
$data modify storage bazaar:tmp mode set value "$(mode)"
$data modify storage bazaar:tmp name set value "$(name)"
execute store result storage bazaar:tmp count int 1 run scoreboard players get #count bazaar.tmp
execute if data storage bazaar:tmp {mode:"sell"} run return run function bazaar:act/commit_sell
function bazaar:act/commit_buy
""",
    )
    write(
        P / "act/commit_buy.mcfunction",
        """
execute if score #stock bazaar.tmp matches 0 run return run function bazaar:act/fail_stock
execute unless score @s bazaar.bank >= #price bazaar.tmp run return run function bazaar:act/fail_money
scoreboard players operation @s bazaar.bank -= #price bazaar.tmp
function bazaar:act/give_offer with storage bazaar:tmp
execute if score #stock bazaar.tmp matches 1.. run function bazaar:act/dec_stock
playsound minecraft:entity.villager.yes player @s ~ ~ ~ 0.8 1
playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.5 1.4
tellraw @s [{"text":"Satın alındı. ","color":"green"},{"text":"Kalan bakiye: ","color":"gray"},{"score":{"name":"@s","objective":"bazaar.bank"},"color":"yellow"}]
function bazaar:act/buy_no
""",
    )
    write(P / "act/give_offer.mcfunction", "$give @s $(id) $(count)\n")
    write(
        P / "act/dec_stock.mcfunction",
        """
scoreboard players remove #stock bazaar.tmp 1
function bazaar:act/dec_stock_m with storage bazaar:tmp
""",
    )
    write(
        P / "act/dec_stock_m.mcfunction",
        "$execute store result storage bazaar:shop items.$(key).stock int 1 run scoreboard players get #stock bazaar.tmp\n",
    )
    write(
        P / "act/commit_sell.mcfunction",
        """
function bazaar:act/count_item with storage bazaar:tmp
execute if score #have bazaar.tmp < #count bazaar.tmp run return run function bazaar:act/fail_items
function bazaar:act/clear_item with storage bazaar:tmp
scoreboard players operation @s bazaar.bank += #price bazaar.tmp
execute if score #stock bazaar.tmp matches 0.. run function bazaar:act/inc_stock
playsound minecraft:entity.villager.trade player @s ~ ~ ~ 0.8 1
tellraw @s [{"text":"Satıldı. Banka +","color":"green"},{"score":{"name":"#price","objective":"bazaar.tmp"},"color":"yellow"}]
function bazaar:act/buy_no
""",
    )
    write(P / "act/count_item.mcfunction", "$execute store result score #have bazaar.tmp run clear @s $(id) 0\n")
    write(P / "act/clear_item.mcfunction", "$clear @s $(id) $(count)\n")
    write(
        P / "act/inc_stock.mcfunction",
        """
scoreboard players add #stock bazaar.tmp 1
function bazaar:act/dec_stock_m with storage bazaar:tmp
""",
    )
    write(
        P / "act/restock.mcfunction",
        """
execute unless entity @s[tag=bazaar.admin] run return run function bazaar:act/fail_admin
data modify storage bazaar:shop items set from storage bazaar:defaults items
playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1
tellraw @s {"text":"Stok ve fiyatlar varsayılana döndü.","color":"green"}
function bazaar:gui/render
""",
    )
    simple_page("fail_admin", 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.7 1\ntitle @s actionbar {"text":"bazaar.admin etiketi gerekli.","color":"red"}')
    for it in BLOCKS + FOOD + COMBAT + REDSTONE + RARE:
        write(P / f"act/buy_{it['key']}.mcfunction", f'function bazaar:act/prep_offer {{key:"{it["key"]}",mode:"buy"}}\n')
    for it in SELLS:
        write(P / f"act/sell_{it['key']}.mcfunction", f'function bazaar:act/prep_offer {{key:"{it["key"]}",mode:"sell"}}\n')
    write(
        P / "admin/grant.mcfunction",
        """
scoreboard players add @s bazaar.bank 64
tellraw @s {"text":"+64 zümrüt (yönetici).","color":"green"}
""",
    )

def write_atlas(folder: Path) -> None:
    ns = "atlas"
    mcmeta(folder, "Yol Atlası", "aqua", "Chest GUI ışınlanma • 1.21.3")
    png(folder / "pack.png", (46, 120, 150), (230, 210, 120))
    tags(folder, ns)
    engine(folder, ns, "Yol Atlası", "aqua", "minecraft:carrot_on_a_stick", vault=False)
    P = folder / "data" / ns / "function"
    write(
        P / "init.mcfunction",
        """
data modify storage atlas:config set value {ready:1b,cooldown:160}
data modify storage atlas:dest spawn set value {set:0b,x:0,y:80,z:0,dim:0,name:"Dünya merkezi"}
data modify storage atlas:dest nether set value {set:0b,x:0,y:64,z:0,dim:1,name:"Nether kapısı"}
data modify storage atlas:dest end set value {set:1b,x:100,y:49,z:0,dim:2,name:"End adası"}
data modify storage atlas:dest s0 set value {set:0b,x:0,y:64,z:0,dim:0,name:"İşaret 1"}
data modify storage atlas:dest s1 set value {set:0b,x:0,y:64,z:0,dim:0,name:"İşaret 2"}
data modify storage atlas:dest s2 set value {set:0b,x:0,y:64,z:0,dim:0,name:"İşaret 3"}
data modify storage atlas:dest s3 set value {set:0b,x:0,y:64,z:0,dim:0,name:"İşaret 4"}
data modify storage atlas:dest s4 set value {set:0b,x:0,y:64,z:0,dim:0,name:"İşaret 5"}
data modify storage atlas:dest s5 set value {set:0b,x:0,y:64,z:0,dim:0,name:"İşaret 6"}
""",
    )
    write(
        P / "welcome.mcfunction",
        f"""
tag @s add atlas.welcomed
execute unless score @s atlas.id matches 1.. run function atlas:assign_id
function atlas:give_key
tellraw @s [{{"text":"Atlas değneği verildi. ","color":"aqua"}},{{"text":"/trigger atlas","color":"yellow","underlined":true,"clickEvent":{{"action":"run_command","value":"/trigger atlas"}}}}]
""",
    )
    write(
        P / "give_key.mcfunction",
        f"""
give @s minecraft:carrot_on_a_stick[custom_name={jtext("Atlas Değneği", "aqua", bold=True)},lore={lore_snbt([("Sağ tık: atlası aç", "gray"), ("/trigger atlas", "dark_gray")])},custom_data={{key:1b,pack:"atlas"}},max_stack_size=1,enchantment_glint_override=true] 1
""",
    )
    # tick extra: safe position. Append to tick file.
    tick = (P / "tick.mcfunction").read_text(encoding="utf-8")
    tick += """
scoreboard players add @a atlas.timer 1
execute as @a[scores={atlas.timer=100..}] at @s run function atlas:safe/try
scoreboard players set @a[scores={atlas.timer=100..}] atlas.timer 0
"""
    write(P / "tick.mcfunction", tick)
    write(
        P / "safe/try.mcfunction",
        """
execute unless score @s atlas.id matches 1.. run return 0
execute unless data entity @s {OnGround:1b} run return 0
execute if block ~ ~ ~ minecraft:lava run return 0
execute if block ~ ~-1 ~ minecraft:lava run return 0
execute unless block ~ ~-1 ~ #minecraft:solid run return 0
execute unless block ~ ~ ~ #atlas:passable run return 0
execute unless block ~ ~1 ~ #atlas:passable run return 0
function atlas:safe/save
""",
    )
    write(
        P / "safe/save.mcfunction",
        """
execute store result score #x atlas.tmp run data get entity @s Pos[0]
execute store result score #y atlas.tmp run data get entity @s Pos[1]
execute store result score #z atlas.tmp run data get entity @s Pos[2]
scoreboard players set #dim atlas.tmp -1
execute if entity @s[nbt={Dimension:"minecraft:overworld"}] run scoreboard players set #dim atlas.tmp 0
execute if entity @s[nbt={Dimension:"minecraft:the_nether"}] run scoreboard players set #dim atlas.tmp 1
execute if entity @s[nbt={Dimension:"minecraft:the_end"}] run scoreboard players set #dim atlas.tmp 2
execute unless score #dim atlas.tmp matches 0..2 run return 0
execute store result storage atlas:macro pid int 1 run scoreboard players get @s atlas.id
execute store result storage atlas:macro x int 1 run scoreboard players get #x atlas.tmp
execute store result storage atlas:macro y int 1 run scoreboard players get #y atlas.tmp
execute store result storage atlas:macro z int 1 run scoreboard players get #z atlas.tmp
execute store result storage atlas:macro dim int 1 run scoreboard players get #dim atlas.tmp
function atlas:safe/write with storage atlas:macro
""",
    )
    write(
        P / "safe/write.mcfunction",
        """
$data modify storage atlas:rt p$(pid).safe set value {set:1b,x:$(x),y:$(y),z:$(z),dim:$(dim),name:"Son güvenli yer"}
""",
    )
    main = blank()
    put(main, 1, id="minecraft:compass", name="Dünya merkezi", color="gold", lore=[("Yönetici kaydeder", "gray"), ("Tıkla: ayrıntı", "yellow")], action="open_spawn", glint=True)
    put(main, 3, id="minecraft:netherrack", name="Nether kapısı", color="red", lore=[("Yönetici kaydeder", "gray")], action="open_nether", glint=True)
    put(main, 5, id="minecraft:end_stone", name="End adası", color="light_purple", lore=[("Varsayılan 100 49 0", "gray"), ("Üstüne yazılabilir", "dark_gray")], action="open_end", glint=True)
    put(main, 7, id="minecraft:recovery_compass", name="Son güvenli yer", color="aqua", lore=[("5 saniyede bir kaydolur", "gray"), ("Lav ve boşluk sayılmaz", "dark_gray")], action="open_safe")
    put(main, 11, id="minecraft:red_bed", name="Evler", color="red", lore=[("3 kişisel işaret", "gray")], action="page_homes")
    put(main, 13, id="minecraft:lodestone", name="Sunucu işaretleri", color="gold", lore=[("6 ortak işaret", "gray"), ("Kayıt: atlas.admin", "yellow")], action="page_warps", glint=True)
    put(main, 15, id="minecraft:book", name="Yardım", color="aqua", lore=[("Bekleme ve güvenlik", "gray")], action="page_help")
    put(main, 26, id="minecraft:barrier", name="Kapat", color="red", lore=[("Veya eğil", "gray")], action="close")
    page(folder, ns, "main", "Yol Atlası", "aqua", main)
    homes = blank()
    for i, nm in enumerate(("Ev 1", "Ev 2", "Ev 3")):
        put(homes, i, id="minecraft:red_bed", name=nm, color="red", lore=[("Ayrıntı, kaydet, ışınlan", "gray")], action=f"open_home{i}")
    put(homes, 18, id="minecraft:arrow", name="Geri", color="yellow", lore=[("Ana sayfa", "gray")], action="page_main")
    put(homes, 26, id="minecraft:barrier", name="Kapat", color="red", lore=[("Menüyü kapat", "gray")], action="close")
    page(folder, ns, "homes", "Atlas • Evler", "red", homes)
    warps = blank()
    for i in range(6):
        put(warps, i, id="minecraft:lodestone", name=f"İşaret {i+1}", color="gold", lore=[("Sunucu işareti", "gray")], action=f"open_warp{i}", glint=True)
    put(warps, 18, id="minecraft:arrow", name="Geri", color="yellow", lore=[("Ana sayfa", "gray")], action="page_main")
    put(warps, 26, id="minecraft:barrier", name="Kapat", color="red", lore=[("Menüyü kapat", "gray")], action="close")
    page(folder, ns, "warps", "Atlas • İşaretler", "gold", warps)
    detail = blank()
    put(detail, 4, id="minecraft:paper", name="Seçilen yer", color="white", lore=[("Işınlanmadan önce bak", "gray")], action="none")
    put(detail, 11, id="minecraft:lime_wool", name="Işınlan", color="green", lore=[("Bekleme süresi uygulanır", "gray"), ("Düşüşe karşı yavaş düşüş", "aqua")], action="detail_tp", glint=True)
    put(detail, 13, id="minecraft:yellow_wool", name="Burayı kaydet", color="yellow", lore=[("Bulunduğun yeri yazar", "gray"), ("Sabit yerler yönetici ister", "dark_gray")], action="detail_save")
    put(detail, 15, id="minecraft:red_wool", name="Sil", color="red", lore=[("Kaydı temizler", "gray")], action="detail_del")
    put(detail, 18, id="minecraft:arrow", name="Geri", color="yellow", lore=[("Önceki sayfa", "gray")], action="go_back")
    put(detail, 22, id="minecraft:clock", name="Bekleme", color="gold", lore=[("Varsayılan 8 saniye", "gray"), ("storage atlas:config cooldown", "dark_gray")], action="none")
    put(detail, 26, id="minecraft:barrier", name="Kapat", color="red", lore=[("Menüyü kapat", "gray")], action="close")
    page(folder, ns, "detail", "Atlas • Ayrıntı", "yellow", detail)
    help_slots = blank()
    put(help_slots, 0, id="minecraft:carrot_on_a_stick", name="Açılış", color="aqua", lore=[("Değneğe sağ tık", "gray"), ("/trigger atlas", "yellow")], action="none")
    put(help_slots, 1, id="minecraft:recovery_compass", name="Güvenli yer", color="green", lore=[("Yerdeyken 5 sn'de bir", "gray"), ("Lavda kaydetmez", "red")], action="none")
    put(help_slots, 2, id="minecraft:name_tag", name="Yönetici", color="gold", lore=[("/tag @s add atlas.admin", "gray"), ("Merkez, nether, işaret", "gray")], action="none")
    put(help_slots, 3, id="minecraft:feather", name="Güvenli iniş", color="white", lore=[("Katı zemin aranır", "gray"), ("Direnç ve yavaş düşüş", "aqua")], action="none")
    put(help_slots, 18, id="minecraft:arrow", name="Geri", color="yellow", lore=[("Ana sayfa", "gray")], action="page_main")
    put(help_slots, 26, id="minecraft:barrier", name="Kapat", color="red", lore=[("Menüyü kapat", "gray")], action="close")
    page(folder, ns, "help", "Atlas • Yardım", "aqua", help_slots)
    write(
        P / "gui/render.mcfunction",
        """
execute if score @s atlas.page matches 0 run function atlas:page/main
execute if score @s atlas.page matches 1 run function atlas:page/homes
execute if score @s atlas.page matches 2 run function atlas:page/warps
execute if score @s atlas.page matches 3 run function atlas:page/detail
execute if score @s atlas.page matches 4 run function atlas:page/help
function atlas:gui/bar
""",
    )
    write(
        P / "gui/bar.mcfunction",
        """
execute store result score #now atlas.tmp run time query gametime
scoreboard players set #left atlas.tmp 0
execute if score @s atlas.cd > #now atlas.tmp run scoreboard players operation #left atlas.tmp = @s atlas.cd
execute if score @s atlas.cd > #now atlas.tmp run scoreboard players operation #left atlas.tmp -= #now atlas.tmp
scoreboard players set #20 atlas.tmp 20
execute if score #left atlas.tmp matches 1.. run scoreboard players operation #left atlas.tmp /= #20 atlas.tmp
title @s actionbar [{"text":"Atlas","color":"aqua"},{"text":"  •  bekleme ","color":"gray"},{"score":{"name":"#left","objective":"atlas.tmp"},"color":"yellow"},{"text":" sn","color":"dark_gray"}]
""",
    )

    def act(name: str, body: str) -> None:
        write(P / f"act/{name}.mcfunction", body.strip() + "\n")

    act("close", "function atlas:gui/close")
    act(
        "page_main",
        """
scoreboard players set @s atlas.page 0
function atlas:gui/render
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.4 1.2
""",
    )
    act(
        "page_homes",
        """
scoreboard players set @s atlas.page 1
function atlas:gui/render
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.4 1.2
""",
    )
    act(
        "page_warps",
        """
scoreboard players set @s atlas.page 2
function atlas:gui/render
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.4 1.2
""",
    )
    act(
        "page_help",
        """
scoreboard players set @s atlas.page 4
function atlas:gui/render
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.4 1.2
""",
    )
    act(
        "go_back",
        """
scoreboard players operation @s atlas.page = @s atlas.back
function atlas:gui/render
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.4 1
""",
    )

    def opener(name: str, mode: int, sel: int) -> None:
        act(
            name,
            f"""
scoreboard players operation @s atlas.back = @s atlas.page
scoreboard players set @s atlas.mode {mode}
scoreboard players set @s atlas.sel {sel}
scoreboard players set @s atlas.page 3
function atlas:gui/render
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.45 1.3
""",
        )

    opener("open_spawn", 1, 0)
    opener("open_nether", 2, 0)
    opener("open_end", 3, 0)
    opener("open_safe", 4, 0)
    for i in range(3):
        opener(f"open_home{i}", 5, i)
    for i in range(6):
        opener(f"open_warp{i}", 6, i)

    act("fail_admin", 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.7 1\ntitle @s actionbar {"text":"atlas.admin etiketi gerekli.","color":"red"}')
    act("fail_unset", 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.7 1\ntitle @s actionbar {"text":"Bu yer henüz kaydedilmedi.","color":"red"}')
    act(
        "fail_cd",
        """
execute store result score #now atlas.tmp run time query gametime
scoreboard players operation #left atlas.tmp = @s atlas.cd
scoreboard players operation #left atlas.tmp -= #now atlas.tmp
scoreboard players set #20 atlas.tmp 20
scoreboard players operation #left atlas.tmp /= #20 atlas.tmp
playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.6 0.7
title @s actionbar [{"text":"Bekleme: ","color":"red"},{"score":{"name":"#left","objective":"atlas.tmp"},"color":"yellow"},{"text":" sn","color":"gray"}]
""",
    )
    act(
        "detail_tp",
        """
execute if score @s atlas.mode matches 1 run return run function atlas:tp/from_spawn
execute if score @s atlas.mode matches 2 run return run function atlas:tp/from_nether
execute if score @s atlas.mode matches 3 run return run function atlas:tp/from_end
execute if score @s atlas.mode matches 4 run return run function atlas:tp/from_safe
execute if score @s atlas.mode matches 5 run return run function atlas:tp/from_home
execute if score @s atlas.mode matches 6 run return run function atlas:tp/from_server
""",
    )
    for key, fn in [("spawn", "from_spawn"), ("nether", "from_nether"), ("end", "from_end")]:
        write(
            P / f"tp/{fn}.mcfunction",
            f"""
execute unless data storage atlas:dest {key}{{set:1b}} run return run function atlas:act/fail_unset
execute store result score #x atlas.tmp run data get storage atlas:dest {key}.x
execute store result score #y atlas.tmp run data get storage atlas:dest {key}.y
execute store result score #z atlas.tmp run data get storage atlas:dest {key}.z
execute store result score #dim atlas.tmp run data get storage atlas:dest {key}.dim
function atlas:tp/go
""",
        )
    write(
        P / "tp/from_safe.mcfunction",
        """
execute store result storage atlas:macro pid int 1 run scoreboard players get @s atlas.id
function atlas:tp/from_safe_m with storage atlas:macro
""",
    )
    write(
        P / "tp/from_safe_m.mcfunction",
        """
$execute unless data storage atlas:rt p$(pid).safe{set:1b} run return run function atlas:act/fail_unset
$execute store result score #x atlas.tmp run data get storage atlas:rt p$(pid).safe.x
$execute store result score #y atlas.tmp run data get storage atlas:rt p$(pid).safe.y
$execute store result score #z atlas.tmp run data get storage atlas:rt p$(pid).safe.z
$execute store result score #dim atlas.tmp run data get storage atlas:rt p$(pid).safe.dim
function atlas:tp/go
""",
    )
    write(
        P / "tp/from_home.mcfunction",
        """
execute store result storage atlas:macro pid int 1 run scoreboard players get @s atlas.id
execute store result storage atlas:macro sel int 1 run scoreboard players get @s atlas.sel
function atlas:tp/from_home_m with storage atlas:macro
""",
    )
    write(
        P / "tp/from_home_m.mcfunction",
        """
$execute unless data storage atlas:rt p$(pid).h$(sel){set:1b} run return run function atlas:act/fail_unset
$execute store result score #x atlas.tmp run data get storage atlas:rt p$(pid).h$(sel).x
$execute store result score #y atlas.tmp run data get storage atlas:rt p$(pid).h$(sel).y
$execute store result score #z atlas.tmp run data get storage atlas:rt p$(pid).h$(sel).z
$execute store result score #dim atlas.tmp run data get storage atlas:rt p$(pid).h$(sel).dim
function atlas:tp/go
""",
    )
    write(
        P / "tp/from_server.mcfunction",
        """
execute if score @s atlas.sel matches 0 run function atlas:tp/server0
execute if score @s atlas.sel matches 1 run function atlas:tp/server1
execute if score @s atlas.sel matches 2 run function atlas:tp/server2
execute if score @s atlas.sel matches 3 run function atlas:tp/server3
execute if score @s atlas.sel matches 4 run function atlas:tp/server4
execute if score @s atlas.sel matches 5 run function atlas:tp/server5
""",
    )
    for i in range(6):
        write(
            P / f"tp/server{i}.mcfunction",
            f"""
execute unless data storage atlas:dest s{i}{{set:1b}} run return run function atlas:act/fail_unset
execute store result score #x atlas.tmp run data get storage atlas:dest s{i}.x
execute store result score #y atlas.tmp run data get storage atlas:dest s{i}.y
execute store result score #z atlas.tmp run data get storage atlas:dest s{i}.z
execute store result score #dim atlas.tmp run data get storage atlas:dest s{i}.dim
function atlas:tp/go
""",
        )
    write(
        P / "tp/go.mcfunction",
        """
execute store result score #now atlas.tmp run time query gametime
execute if score @s atlas.cd > #now atlas.tmp run return run function atlas:act/fail_cd
execute store result score #wait atlas.tmp run data get storage atlas:config cooldown
execute unless score #wait atlas.tmp matches 1.. run scoreboard players set #wait atlas.tmp 160
scoreboard players operation #cd atlas.tmp = #now atlas.tmp
scoreboard players operation #cd atlas.tmp += #wait atlas.tmp
scoreboard players operation @s atlas.cd = #cd atlas.tmp
execute store result storage atlas:macro x int 1 run scoreboard players get #x atlas.tmp
execute store result storage atlas:macro y int 1 run scoreboard players get #y atlas.tmp
execute store result storage atlas:macro z int 1 run scoreboard players get #z atlas.tmp
execute if score #dim atlas.tmp matches 0 run function atlas:tp/go_ow with storage atlas:macro
execute if score #dim atlas.tmp matches 1 run function atlas:tp/go_nether with storage atlas:macro
execute if score #dim atlas.tmp matches 2 run function atlas:tp/go_end with storage atlas:macro
function atlas:gui/close
execute at @s run function atlas:tp/safety
playsound minecraft:entity.enderman.teleport player @s ~ ~ ~ 1 1
playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.35 1.4
title @s title {"text":"Işınlandın","color":"aqua"}
title @s subtitle {"text":"Zemin kontrol edildi","color":"gray"}
""",
    )
    write(P / "tp/go_ow.mcfunction", "$execute in minecraft:overworld run tp @s $(x).5 $(y) $(z).5\n")
    write(P / "tp/go_nether.mcfunction", "$execute in minecraft:the_nether run tp @s $(x).5 $(y) $(z).5\n")
    write(P / "tp/go_end.mcfunction", "$execute in minecraft:the_end run tp @s $(x).5 $(y) $(z).5\n")
    write(
        P / "tp/safety.mcfunction",
        """
scoreboard players set #lift atlas.tmp 0
function atlas:tp/lift
scoreboard players set #drop atlas.tmp 0
function atlas:tp/drop
effect give @s minecraft:resistance 5 4 true
effect give @s minecraft:slow_falling 6 0 true
""",
    )
    write(
        P / "tp/lift.mcfunction",
        """
execute if score #lift atlas.tmp matches 20.. run return 0
execute if block ~ ~ ~ #atlas:passable if block ~ ~1 ~ #atlas:passable run return 0
tp @s ~ ~1 ~
scoreboard players add #lift atlas.tmp 1
function atlas:tp/lift
""",
    )
    write(
        P / "tp/drop.mcfunction",
        """
execute if score #drop atlas.tmp matches 32.. run return 0
execute store result score #py atlas.tmp run data get entity @s Pos[1]
execute if score #py atlas.tmp matches ..-60 run return 0
execute unless block ~ ~-1 ~ #atlas:passable run return 0
execute if block ~ ~-1 ~ minecraft:lava run return 0
tp @s ~ ~-1 ~
scoreboard players add #drop atlas.tmp 1
function atlas:tp/drop
""",
    )
    act(
        "detail_save",
        """
execute if score @s atlas.mode matches 1 unless entity @s[tag=atlas.admin] run return run function atlas:act/fail_admin
execute if score @s atlas.mode matches 2 unless entity @s[tag=atlas.admin] run return run function atlas:act/fail_admin
execute if score @s atlas.mode matches 3 unless entity @s[tag=atlas.admin] run return run function atlas:act/fail_admin
execute if score @s atlas.mode matches 6 unless entity @s[tag=atlas.admin] run return run function atlas:act/fail_admin
function atlas:save/capture
execute if score @s atlas.mode matches 1 run function atlas:save/spawn
execute if score @s atlas.mode matches 2 run function atlas:save/nether
execute if score @s atlas.mode matches 3 run function atlas:save/end
execute if score @s atlas.mode matches 4 run function atlas:save/safe
execute if score @s atlas.mode matches 5 run function atlas:save/home
execute if score @s atlas.mode matches 6 run function atlas:save/server
playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.2
title @s actionbar {"text":"Konum kaydedildi.","color":"green"}
""",
    )
    write(
        P / "save/capture.mcfunction",
        """
execute store result score #x atlas.tmp run data get entity @s Pos[0]
execute store result score #y atlas.tmp run data get entity @s Pos[1]
execute store result score #z atlas.tmp run data get entity @s Pos[2]
scoreboard players set #dim atlas.tmp -1
execute if entity @s[nbt={Dimension:"minecraft:overworld"}] run scoreboard players set #dim atlas.tmp 0
execute if entity @s[nbt={Dimension:"minecraft:the_nether"}] run scoreboard players set #dim atlas.tmp 1
execute if entity @s[nbt={Dimension:"minecraft:the_end"}] run scoreboard players set #dim atlas.tmp 2
execute if score #dim atlas.tmp matches -1 run scoreboard players set #dim atlas.tmp 0
execute store result storage atlas:macro x int 1 run scoreboard players get #x atlas.tmp
execute store result storage atlas:macro y int 1 run scoreboard players get #y atlas.tmp
execute store result storage atlas:macro z int 1 run scoreboard players get #z atlas.tmp
execute store result storage atlas:macro dim int 1 run scoreboard players get #dim atlas.tmp
execute store result storage atlas:macro pid int 1 run scoreboard players get @s atlas.id
execute store result storage atlas:macro sel int 1 run scoreboard players get @s atlas.sel
""",
    )
    for key in ("spawn", "nether", "end"):
        write(
            P / f"save/{key}.mcfunction",
            f"""
function atlas:save/fixed with storage atlas:macro
$data modify storage atlas:dest {key}.name set value "{key}"
""",
        )
    # fixed uses $(key) - do it properly per file without broken macro mix
    for key, label in (("spawn", "Dünya merkezi"), ("nether", "Nether kapısı"), ("end", "End adası")):
        write(
            P / f"save/{key}.mcfunction",
            f"""
$execute store result storage atlas:dest {key}.x int 1 run scoreboard players get #x atlas.tmp
$execute store result storage atlas:dest {key}.y int 1 run scoreboard players get #y atlas.tmp
$execute store result storage atlas:dest {key}.z int 1 run scoreboard players get #z atlas.tmp
$execute store result storage atlas:dest {key}.dim int 1 run scoreboard players get #dim atlas.tmp
data modify storage atlas:dest {key}.set set value 1b
data modify storage atlas:dest {key}.name set value "{label}"
""",
        )
    # Those files have $ but don't need args if scores are global. A function with $ must be called with args.
    # Remove $ from lines that don't need macros.
    for key, label in (("spawn", "Dünya merkezi"), ("nether", "Nether kapısı"), ("end", "End adası")):
        write(
            P / f"save/{key}.mcfunction",
            f"""
execute store result storage atlas:dest {key}.x int 1 run scoreboard players get #x atlas.tmp
execute store result storage atlas:dest {key}.y int 1 run scoreboard players get #y atlas.tmp
execute store result storage atlas:dest {key}.z int 1 run scoreboard players get #z atlas.tmp
execute store result storage atlas:dest {key}.dim int 1 run scoreboard players get #dim atlas.tmp
data modify storage atlas:dest {key}.set set value 1b
data modify storage atlas:dest {key}.name set value "{label}"
""",
        )
    write(
        P / "save/safe.mcfunction",
        """
function atlas:save/safe_m with storage atlas:macro
""",
    )
    write(
        P / "save/safe_m.mcfunction",
        """
$data modify storage atlas:rt p$(pid).safe set value {set:1b,x:$(x),y:$(y),z:$(z),dim:$(dim),name:"Son güvenli yer"}
""",
    )
    write(P / "save/home.mcfunction", "function atlas:save/home_m with storage atlas:macro\n")
    write(
        P / "save/home_m.mcfunction",
        """
$data modify storage atlas:rt p$(pid).h$(sel) set value {set:1b,x:$(x),y:$(y),z:$(z),dim:$(dim),name:"Ev"}
""",
    )
    write(
        P / "save/server.mcfunction",
        """
execute if score @s atlas.sel matches 0 run function atlas:save/s0
execute if score @s atlas.sel matches 1 run function atlas:save/s1
execute if score @s atlas.sel matches 2 run function atlas:save/s2
execute if score @s atlas.sel matches 3 run function atlas:save/s3
execute if score @s atlas.sel matches 4 run function atlas:save/s4
execute if score @s atlas.sel matches 5 run function atlas:save/s5
""",
    )
    for i in range(6):
        write(
            P / f"save/s{i}.mcfunction",
            f"""
execute store result storage atlas:dest s{i}.x int 1 run scoreboard players get #x atlas.tmp
execute store result storage atlas:dest s{i}.y int 1 run scoreboard players get #y atlas.tmp
execute store result storage atlas:dest s{i}.z int 1 run scoreboard players get #z atlas.tmp
execute store result storage atlas:dest s{i}.dim int 1 run scoreboard players get #dim atlas.tmp
data modify storage atlas:dest s{i}.set set value 1b
data modify storage atlas:dest s{i}.name set value "İşaret {i+1}"
""",
        )
    act(
        "detail_del",
        """
execute if score @s atlas.mode matches 1 unless entity @s[tag=atlas.admin] run return run function atlas:act/fail_admin
execute if score @s atlas.mode matches 2 unless entity @s[tag=atlas.admin] run return run function atlas:act/fail_admin
execute if score @s atlas.mode matches 3 unless entity @s[tag=atlas.admin] run return run function atlas:act/fail_admin
execute if score @s atlas.mode matches 6 unless entity @s[tag=atlas.admin] run return run function atlas:act/fail_admin
execute if score @s atlas.mode matches 1 run data modify storage atlas:dest spawn.set set value 0b
execute if score @s atlas.mode matches 2 run data modify storage atlas:dest nether.set set value 0b
execute if score @s atlas.mode matches 3 run data modify storage atlas:dest end.set set value 0b
execute if score @s atlas.mode matches 4 run function atlas:save/del_safe
execute if score @s atlas.mode matches 5 run function atlas:save/del_home
execute if score @s atlas.mode matches 6 run function atlas:save/del_server
playsound minecraft:block.fire.extinguish player @s ~ ~ ~ 0.4 1.4
title @s actionbar {"text":"Kayıt silindi.","color":"red"}
""",
    )
    write(
        P / "save/del_safe.mcfunction",
        """
execute store result storage atlas:macro pid int 1 run scoreboard players get @s atlas.id
function atlas:save/del_safe_m with storage atlas:macro
""",
    )
    write(P / "save/del_safe_m.mcfunction", "$data remove storage atlas:rt p$(pid).safe\n")
    write(
        P / "save/del_home.mcfunction",
        """
execute store result storage atlas:macro pid int 1 run scoreboard players get @s atlas.id
execute store result storage atlas:macro sel int 1 run scoreboard players get @s atlas.sel
function atlas:save/del_home_m with storage atlas:macro
""",
    )
    write(P / "save/del_home_m.mcfunction", "$data remove storage atlas:rt p$(pid).h$(sel)\n")
    write(
        P / "save/del_server.mcfunction",
        """
execute if score @s atlas.sel matches 0 run data modify storage atlas:dest s0.set set value 0b
execute if score @s atlas.sel matches 1 run data modify storage atlas:dest s1.set set value 0b
execute if score @s atlas.sel matches 2 run data modify storage atlas:dest s2.set set value 0b
execute if score @s atlas.sel matches 3 run data modify storage atlas:dest s3.set set value 0b
execute if score @s atlas.sel matches 4 run data modify storage atlas:dest s4.set set value 0b
execute if score @s atlas.sel matches 5 run data modify storage atlas:dest s5.set set value 0b
""",
    )

def write_reliquary(folder: Path) -> None:
    ns = "reliquary"
    mcmeta(folder, "Sınıf Emaneti", "light_purple", "Chest GUI sınıf kiti • 1.21.3")
    png(folder / "pack.png", (110, 70, 150), (230, 190, 90))
    tags(folder, ns)
    engine(folder, ns, "Sınıf Emaneti", "light_purple", "minecraft:carrot_on_a_stick", vault=False)
    P = folder / "data" / ns / "function"
    write(
        P / "init.mcfunction",
        """
data modify storage reliquary:config set value {ready:1b,cooldown:12000,teams:1b}
team add rel.knight
team modify rel.knight color red
team modify rel.knight friendlyFire true
team modify rel.knight collisionRule always
team modify rel.knight prefix {"text":"[Şövalye] ","color":"red"}
team add rel.archer
team modify rel.archer color green
team modify rel.archer friendlyFire true
team modify rel.archer collisionRule always
team modify rel.archer prefix {"text":"[Nişancı] ","color":"green"}
team add rel.farmer
team modify rel.farmer color yellow
team modify rel.farmer friendlyFire true
team modify rel.farmer collisionRule always
team modify rel.farmer prefix {"text":"[Çiftçi] ","color":"yellow"}
team add rel.miner
team modify rel.miner color gray
team modify rel.miner friendlyFire true
team modify rel.miner collisionRule always
team modify rel.miner prefix {"text":"[Madenci] ","color":"gray"}
team add rel.alch
team modify rel.alch color light_purple
team modify rel.alch friendlyFire true
team modify rel.alch collisionRule always
team modify rel.alch prefix {"text":"[Simyacı] ","color":"light_purple"}
team add rel.expl
team modify rel.expl color aqua
team modify rel.expl friendlyFire true
team modify rel.expl collisionRule always
team modify rel.expl prefix {"text":"[Kaşif] ","color":"aqua"}
""",
    )
    # uninstall should empty teams too
    uni = (P / "uninstall.mcfunction").read_text(encoding="utf-8")
    uni += """
team empty rel.knight
team empty rel.archer
team empty rel.farmer
team empty rel.miner
team empty rel.alch
team empty rel.expl
"""
    write(P / "uninstall.mcfunction", uni)
    write(
        P / "welcome.mcfunction",
        """
tag @s add reliquary.welcomed
execute unless score @s reliquary.id matches 1.. run function reliquary:assign_id
function reliquary:give_key
tellraw @s [{"text":"Emanet asası verildi. ","color":"light_purple"},{"text":"/trigger reliquary","color":"aqua","underlined":true,"clickEvent":{"action":"run_command","value":"/trigger reliquary"}}]
""",
    )
    write(
        P / "give_key.mcfunction",
        f"""
give @s minecraft:carrot_on_a_stick[custom_name={jtext("Emanet Asası", "light_purple", bold=True)},lore={lore_snbt([("Sağ tık: sınıf salonu", "gray"), ("/trigger reliquary", "dark_gray")])},custom_data={{key:1b,pack:"reliquary"}},max_stack_size=1,enchantment_glint_override=true] 1
""",
    )
    main = blank()
    classes = [
        (0, "minecraft:iron_sword", "Şövalye", "red", "Herkese açık", "page_knight"),
        (1, "minecraft:bow", "Nişancı", "green", "Bir ok fırlat", "page_archer"),
        (2, "minecraft:wheat", "Çiftçi", "yellow", "Bir tohum ek", "page_farmer"),
        (3, "minecraft:iron_pickaxe", "Madenci", "gray", "Demir erit", "page_miner"),
        (4, "minecraft:potion", "Simyacı", "light_purple", "Bir iksir damıt", "page_alchemist"),
        (5, "minecraft:compass", "Kaşif", "aqua", "Yatakta uyu", "page_explorer"),
    ]
    for i, (idx, iid, name, col, req, actn) in enumerate(classes):
        put(main, i, id=iid, name=name, color=col, lore=[(req, "gray"), ("10 dk bekleme", "dark_gray"), ("3. alışta ustalık", "yellow")], action=actn, glint=True)
    put(main, 13, id="minecraft:book", name="Salon", color="light_purple", lore=[("Önizlemeyi alma", "gray"), ("Kiti al düğmesini kullan", "yellow"), ("Takım öneki isteğe bağlı", "dark_gray")], action="none")
    put(main, 22, id="minecraft:paper", name="Yardım", color="aqua", lore=[("Kilitler ve bekleme", "gray")], action="page_help")
    put(main, 26, id="minecraft:barrier", name="Kapat", color="red", lore=[("Veya eğil", "gray")], action="close")
    page(folder, ns, "main", "Sınıf Emaneti", "light_purple", main)

    def class_page(name, title, color, icon, req_lines, claim, previews):
        slots = blank()
        put(slots, 4, id=icon, name=title, color=color, lore=req_lines, action="none", glint=True)
        for i, prev in enumerate(previews[:7]):
            put(
                slots,
                10 + i,
                id=prev[0],
                name=prev[1],
                color="white",
                lore=[("Önizleme, alınamaz", "dark_gray")],
                action="none",
            )
        put(slots, 18, id="minecraft:arrow", name="Geri", color="yellow", lore=[("Salona dön", "gray")], action="page_main")
        put(slots, 22, id="minecraft:lime_wool", name="Kiti al", color="green", lore=[("Bekleme ve kilit kontrol", "gray"), ("Gerçek eşyalar verilir", "yellow")], action=claim, glint=True)
        put(slots, 26, id="minecraft:barrier", name="Kapat", color="red", lore=[("Menüyü kapat", "gray")], action="close")
        page(folder, ns, name, f"Emanet • {title}", color, slots)

    class_page(
        "knight",
        "Şövalye",
        "red",
        "minecraft:iron_sword",
        [("Şart yok", "green"), ("Demir set ve kalkan", "gray")],
        "claim_knight",
        [
            ("minecraft:iron_sword", "Keskinlik I"),
            ("minecraft:shield", "Kalkan"),
            ("minecraft:iron_helmet", "Miğfer"),
            ("minecraft:iron_chestplate", "Göğüslük"),
            ("minecraft:iron_leggings", "Pantolon"),
            ("minecraft:iron_boots", "Bot"),
            ("minecraft:cooked_beef", "Biftek x16"),
        ],
    )
    class_page(
        "archer",
        "Nişancı",
        "green",
        "minecraft:bow",
        [("Bir ok fırlat", "yellow"), ("Güç I yay, 48 ok", "gray")],
        "claim_archer",
        [
            ("minecraft:bow", "Güç I"),
            ("minecraft:arrow", "Ok x48"),
            ("minecraft:leather_helmet", "Yeşil deri"),
            ("minecraft:leather_chestplate", "Yeşil deri"),
            ("minecraft:leather_leggings", "Yeşil deri"),
            ("minecraft:leather_boots", "Yeşil deri"),
            ("minecraft:cooked_beef", "Biftek x12"),
        ],
    )
    class_page(
        "farmer",
        "Çiftçi",
        "yellow",
        "minecraft:wheat",
        [("Bir tohum ek", "yellow"), ("Tohum, kemik unu, kova", "gray")],
        "claim_farmer",
        [
            ("minecraft:iron_hoe", "Demir çapa"),
            ("minecraft:wheat_seeds", "Tohum x16"),
            ("minecraft:carrot", "Havuç x8"),
            ("minecraft:potato", "Patates x8"),
            ("minecraft:bone_meal", "Kemik unu x16"),
            ("minecraft:bread", "Ekmek x12"),
            ("minecraft:water_bucket", "Su kovası"),
        ],
    )
    class_page(
        "miner",
        "Madenci",
        "gray",
        "minecraft:iron_pickaxe",
        [("Demir erit", "yellow"), ("Verim II kazma", "gray")],
        "claim_miner",
        [
            ("minecraft:iron_pickaxe", "Verim II"),
            ("minecraft:torch", "Meşale x64"),
            ("minecraft:coal", "Kömür x32"),
            ("minecraft:bread", "Ekmek x16"),
            ("minecraft:iron_helmet", "Miğfer"),
            ("minecraft:bucket", "Kova"),
        ],
    )
    class_page(
        "alchemist",
        "Simyacı",
        "light_purple",
        "minecraft:brewing_stand",
        [("Bir iksir damıt", "yellow"), ("Sehpa ve temel iksirler", "gray")],
        "claim_alchemist",
        [
            ("minecraft:brewing_stand", "İksir sehpası"),
            ("minecraft:nether_wart", "Nether siğili x8"),
            ("minecraft:blaze_powder", "Blaze tozu x4"),
            ("minecraft:glass_bottle", "Şişe x8"),
            ("minecraft:potion", "İyileştirme"),
            ("minecraft:potion", "Ateş direnci"),
            ("minecraft:golden_carrot", "Altın havuç x6"),
        ],
    )
    class_page(
        "explorer",
        "Kaşif",
        "aqua",
        "minecraft:compass",
        [("Yatakta uyu", "yellow"), ("Pusula, yatak, bot", "gray")],
        "claim_explorer",
        [
            ("minecraft:compass", "Pusula"),
            ("minecraft:clock", "Saat"),
            ("minecraft:oak_boat", "Meşe sandal"),
            ("minecraft:white_bed", "Yatak"),
            ("minecraft:spyglass", "Dürbün"),
            ("minecraft:cooked_cod", "Morina x16"),
            ("minecraft:leather_boots", "Derinlik adımı"),
        ],
    )
    help_slots = blank()
    put(help_slots, 0, id="minecraft:carrot_on_a_stick", name="Açılış", color="light_purple", lore=[("Asaya sağ tık", "gray"), ("/trigger reliquary", "aqua")], action="none")
    put(help_slots, 1, id="minecraft:clock", name="Bekleme", color="gold", lore=[("Varsayılan 10 dakika", "gray"), ("storage reliquary:config cooldown", "dark_gray")], action="none")
    put(help_slots, 2, id="minecraft:name_tag", name="Takım öneki", color="yellow", lore=[("PvP kapanmaz", "green"), ("friendlyFire açık kalır", "gray"), ("Kapat: teams_off", "dark_gray")], action="none")
    put(help_slots, 3, id="minecraft:golden_apple", name="Ustalık", color="gold", lore=[("Aynı sınıfı 3. kez alınca", "gray"), ("Bir altın elma", "yellow")], action="none", glint=True)
    put(help_slots, 18, id="minecraft:arrow", name="Geri", color="yellow", lore=[("Salon", "gray")], action="page_main")
    put(help_slots, 26, id="minecraft:barrier", name="Kapat", color="red", lore=[("Menüyü kapat", "gray")], action="close")
    page(folder, ns, "help", "Emanet • Yardım", "aqua", help_slots)
    write(
        P / "gui/render.mcfunction",
        """
execute if score @s reliquary.page matches 0 run function reliquary:page/main
execute if score @s reliquary.page matches 1 run function reliquary:page/knight
execute if score @s reliquary.page matches 2 run function reliquary:page/archer
execute if score @s reliquary.page matches 3 run function reliquary:page/farmer
execute if score @s reliquary.page matches 4 run function reliquary:page/miner
execute if score @s reliquary.page matches 5 run function reliquary:page/alchemist
execute if score @s reliquary.page matches 6 run function reliquary:page/explorer
execute if score @s reliquary.page matches 7 run function reliquary:page/help
title @s actionbar {"text":"Önizleme alınamaz  •  Kiti al gerçek eşya verir","color":"light_purple"}
""",
    )

    def act(name: str, body: str) -> None:
        write(P / f"act/{name}.mcfunction", body.strip() + "\n")

    act("close", "function reliquary:gui/close")
    for action, pg in [
        ("page_main", 0),
        ("page_knight", 1),
        ("page_archer", 2),
        ("page_farmer", 3),
        ("page_miner", 4),
        ("page_alchemist", 5),
        ("page_explorer", 6),
        ("page_help", 7),
    ]:
        act(
            action,
            f"""
scoreboard players set @s reliquary.page {pg}
function reliquary:gui/render
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.45 1.25
""",
        )
    act("fail_lock", 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.7 1\ntitle @s actionbar {"text":"Bu sınıf henüz kilitli.","color":"red"}')
    act(
        "fail_cd",
        """
scoreboard players set #20 reliquary.tmp 20
scoreboard players operation #left reliquary.tmp /= #20 reliquary.tmp
playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.6 0.8
title @s actionbar [{"text":"Bekleme: ","color":"red"},{"score":{"name":"#left","objective":"reliquary.tmp"},"color":"yellow"},{"text":" sn","color":"gray"}]
""",
    )
    write(
        P / "kit/gate.mcfunction",
        """
$execute store result score #now reliquary.tmp run time query gametime
scoreboard players set #cd reliquary.tmp 0
$execute store result score #cd reliquary.tmp run data get storage reliquary:rt p$(pid).cd.$(class)
execute if score #cd reliquary.tmp > #now reliquary.tmp run scoreboard players operation #left reliquary.tmp = #cd reliquary.tmp
execute if score #cd reliquary.tmp > #now reliquary.tmp run scoreboard players operation #left reliquary.tmp -= #now reliquary.tmp
$execute if score #cd reliquary.tmp > #now reliquary.tmp run return run function reliquary:act/fail_cd
scoreboard players set #ok reliquary.tmp 1
""",
    )
    # gate uses $(pid) and $(class) so caller passes both. Also #left must be set before fail_cd divides it.
    # Bug: fail_cd divides #left by 20 but #left is ticks. Good if we set #left before call.
    # Bug: first line has $ on a command that doesn't need class. That's ok if whole function is macro.
    write(
        P / "kit/stamp.mcfunction",
        """
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
""",
    )
    write(
        P / "kit/mastery.mcfunction",
        """
give @s minecraft:golden_apple 1
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 1
tellraw @s {"text":"Ustalık: altın elma.","color":"gold"}
""",
    )
    write(
        P / "kit/join.mcfunction",
        """
$execute unless data storage reliquary:config {teams:1b} run return 0
$team join $(team) @s
""",
    )

    claims = {
        "knight": ("", "rel.knight"),
        "archer": ("execute unless entity @s[advancements={minecraft:adventure/shoot_arrow=true}] run return run function reliquary:act/fail_lock", "rel.archer"),
        "farmer": ("execute unless entity @s[advancements={minecraft:husbandry/plant_seed=true}] run return run function reliquary:act/fail_lock", "rel.farmer"),
        "miner": ("execute unless entity @s[advancements={minecraft:story/smelt_iron=true}] run return run function reliquary:act/fail_lock", "rel.miner"),
        "alchemist": ("execute unless entity @s[advancements={minecraft:nether/brew_potion=true}] run return run function reliquary:act/fail_lock", "rel.alch"),
        "explorer": ("execute unless entity @s[advancements={minecraft:adventure/sleep_in_bed=true}] run return run function reliquary:act/fail_lock", "rel.expl"),
    }
    gives = {
        "knight": """
give @s minecraft:iron_sword[enchantments={levels:{"minecraft:sharpness":1,"minecraft:unbreaking":1}}] 1
give @s minecraft:shield 1
give @s minecraft:iron_helmet 1
give @s minecraft:iron_chestplate 1
give @s minecraft:iron_leggings 1
give @s minecraft:iron_boots 1
give @s minecraft:cooked_beef 16
""",
        "archer": """
give @s minecraft:bow[enchantments={levels:{"minecraft:power":1}}] 1
give @s minecraft:arrow 48
give @s minecraft:leather_helmet[dyed_color={rgb:3897898,show_in_tooltip:1b}] 1
give @s minecraft:leather_chestplate[dyed_color={rgb:3897898,show_in_tooltip:1b}] 1
give @s minecraft:leather_leggings[dyed_color={rgb:3897898,show_in_tooltip:1b}] 1
give @s minecraft:leather_boots[dyed_color={rgb:3897898,show_in_tooltip:1b}] 1
give @s minecraft:cooked_beef 12
""",
        "farmer": """
give @s minecraft:iron_hoe 1
give @s minecraft:wheat_seeds 16
give @s minecraft:carrot 8
give @s minecraft:potato 8
give @s minecraft:bone_meal 16
give @s minecraft:bread 12
give @s minecraft:water_bucket 1
give @s minecraft:leather_helmet[dyed_color={rgb:14859204,show_in_tooltip:1b}] 1
""",
        "miner": """
give @s minecraft:iron_pickaxe[enchantments={levels:{"minecraft:efficiency":2,"minecraft:unbreaking":1}}] 1
give @s minecraft:torch 64
give @s minecraft:coal 32
give @s minecraft:bread 16
give @s minecraft:iron_helmet 1
give @s minecraft:bucket 1
""",
        "alchemist": """
give @s minecraft:brewing_stand 1
give @s minecraft:glass_bottle 8
give @s minecraft:nether_wart 8
give @s minecraft:blaze_powder 4
give @s minecraft:golden_carrot 6
give @s minecraft:potion[potion_contents={potion:"minecraft:strong_healing"}] 2
give @s minecraft:potion[potion_contents={potion:"minecraft:fire_resistance"}] 1
give @s minecraft:potion[potion_contents={potion:"minecraft:swiftness"}] 1
""",
        "explorer": """
give @s minecraft:compass 1
give @s minecraft:clock 1
give @s minecraft:oak_boat 1
give @s minecraft:white_bed 1
give @s minecraft:spyglass 1
give @s minecraft:torch 32
give @s minecraft:cooked_cod 16
give @s minecraft:leather_boots[enchantments={levels:{"minecraft:depth_strider":1}},dyed_color={rgb:5978646,show_in_tooltip:1b}] 1
""",
    }
    for cls, (lock, team) in claims.items():
        lock_line = (lock + "\n") if lock else ""
        write(
            P / f"act/claim_{cls}.mcfunction",
            f"""
{lock_line}execute store result storage reliquary:macro pid int 1 run scoreboard players get @s reliquary.id
function reliquary:kit/begin_{cls} with storage reliquary:macro
""",
        )
        write(
            P / f"kit/begin_{cls}.mcfunction",
            f"""
scoreboard players set #ok reliquary.tmp 0
$function reliquary:kit/gate {{pid:$(pid),class:"{cls}"}}
execute unless score #ok reliquary.tmp matches 1 run return 0
function reliquary:kit/give_{cls}
$function reliquary:kit/stamp {{pid:$(pid),class:"{cls}"}}
$function reliquary:kit/join {{team:"{team}"}}
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.7 1
tellraw @s {{"text":"Kit verildi.","color":"green"}}
function reliquary:gui/render
""",
        )
        write(P / f"kit/give_{cls}.mcfunction", gives[cls].strip() + "\n")
    write(
        P / "admin/teams_off.mcfunction",
        """
data modify storage reliquary:config teams set value 0b
tellraw @s {"text":"Yeni kitler takıma katılmaz. Mevcut önekler durur.","color":"yellow"}
""",
    )
    write(
        P / "admin/teams_on.mcfunction",
        """
data modify storage reliquary:config teams set value 1b
tellraw @s {"text":"Takım önekleri tekrar açık.","color":"green"}
""",
    )
    write(
        P / "admin/clear_teams.mcfunction",
        """
team empty rel.knight
team empty rel.archer
team empty rel.farmer
team empty rel.miner
team empty rel.alch
team empty rel.expl
tellraw @s {"text":"Emanet takımları boşaltıldı.","color":"gold"}
""",
    )

def write_vault(folder: Path) -> None:
    ns = "vault"
    mcmeta(folder, "Kutsal Kasa", "dark_aqua", "Chest GUI kişisel depo • 1.21.3")
    png(folder / "pack.png", (30, 110, 110), (220, 180, 70))
    tags(folder, ns)
    engine(folder, ns, "Kutsal Kasa", "dark_aqua", "minecraft:warped_fungus_on_a_stick", vault=True)
    P = folder / "data" / ns / "function"
    write(P / "init.mcfunction", "data modify storage vault:config set value {ready:1b}\n")
    write(
        P / "welcome.mcfunction",
        f"""
tag @s add vault.welcomed
execute unless score @s vault.id matches 1.. run function vault:assign_id
function vault:give_key
tellraw @s [{{"text":"Kasa anahtarı verildi. ","color":"dark_aqua"}},{{"text":"/trigger vault","color":"aqua","underlined":true,"clickEvent":{{"action":"run_command","value":"/trigger vault"}}}}]
""",
    )
    write(
        P / "give_key.mcfunction",
        f"""
give @s minecraft:warped_fungus_on_a_stick[custom_name={jtext("Kasa Anahtarı", "dark_aqua", bold=True)},lore={lore_snbt([("Sağ tık: kasayı aç", "gray"), ("/trigger vault", "dark_gray"), ("3 sayfa, 54 göz", "yellow")])},custom_data={{key:1b,pack:"vault"}},max_stack_size=1,enchantment_glint_override=true] 1
""",
    )
    write(P / "gui/save.mcfunction", "function vault:sync/current\n")
    write(
        P / "gui/render.mcfunction",
        """
function vault:load/current
""",
    )
    write(
        P / "gui/vault_tick.mcfunction",
        """
function vault:sync/current
function vault:ctrl/check
execute if score #dirty vault.tmp matches 1.. run function vault:ctrl/paint
function vault:gui/dispatch
function vault:ctrl/bar
""",
    )
    # Fix vault tick: dispatch for vault uses same gui/dispatch which calls vault:act/
    # But queue is set by ctrl/check into storage. gui/dispatch reads p$(pid).queue. Good.
    # ctrl/check must set #dirty and queue. It should NOT use button scan of all 27.
    write(
        P / "sync/current.mcfunction",
        """
execute store result storage vault:macro pid int 1 run scoreboard players get @s vault.id
execute if score @s vault.page matches 0 run function vault:sync/page_a with storage vault:macro
execute if score @s vault.page matches 1 run function vault:sync/page_b with storage vault:macro
execute if score @s vault.page matches 2 run function vault:sync/page_c with storage vault:macro
scoreboard players operation @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] vault.page = @s vault.page
scoreboard players operation @s vault.used = #used vault.tmp
""",
    )
    def sync_page(letter: str, key: str) -> str:
        lines = ["scoreboard players set #used vault.tmp 0"]
        for s in range(18):
            lines.append(f"function vault:sync/slot with storage vault:macro {{slot:{s},page:\"{key}\"}}".replace("{slot:", "").replace("}") )
        # I'll just unroll explicitly without nested macro confusion
        lines = ["scoreboard players set #used vault.tmp 0"]
        for s in range(18):
            lines.append(f"$function vault:sync/one {{pid:$(pid),slot:{s},page:\"{key}\"}}")
        return "\n".join(lines) + "\n"
    # Calling with extra args AND storage: `function x with storage` uses storage only.
    # Use inline only:
    for letter, key in (("a", "A"), ("b", "B"), ("c", "C")):
        lines = ["scoreboard players set #used vault.tmp 0"]
        for s in range(18):
            lines.append(f'$function vault:sync/one {{pid:$(pid),slot:{s},page:"{key}"}}')
        write(P / f"sync/page_{letter}.mcfunction", "\n".join(lines) + "\n")
        write(
            P / f"vault/sync_orphan_{letter}.mcfunction",
            "\n".join([f'$function vault:sync/one_orphan {{pid:$(pid),slot:{s},page:"{key}"}}' for s in range(18)]) + "\n",
        )
    write(
        P / "sync/one.mcfunction",
        """
$execute if data entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items[{Slot:$(slot)b,components:{"minecraft:custom_data":{gui:1b}}}] run data remove entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items[{Slot:$(slot)b}]
$execute if data entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items[{Slot:$(slot)b}] run function vault:sync/save with storage vault:macro
$execute unless data entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items[{Slot:$(slot)b}] run function vault:sync/clear with storage vault:macro
""",
    )
    # BUG: save/clear called with storage vault:macro which may not include slot/page from the outer macro.
    # The outer function has pid, slot, page as arguments. Inner `with storage vault:macro` only has pid.
    # Fix: call save using the same macro args by not switching storage.
    write(
        P / "sync/one.mcfunction",
        """
$execute unless entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] run return 0
$execute if data entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items[{Slot:$(slot)b,components:{"minecraft:custom_data":{gui:1b}}}] run data remove entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items[{Slot:$(slot)b}]
$execute if data entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items[{Slot:$(slot)b}] run function vault:sync/save {pid:$(pid),slot:$(slot),page:"$(page)"}
$execute unless data entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items[{Slot:$(slot)b}] run function vault:sync/clear {pid:$(pid),slot:$(slot),page:"$(page)"}
""",
    )
    write(
        P / "sync/save.mcfunction",
        """
data remove storage vault:tmp one
$data modify storage vault:tmp one set from entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items[{Slot:$(slot)b}]
data remove storage vault:tmp one.Slot
$data modify storage vault:rt p$(pid).$(page).s$(slot) set from storage vault:tmp one
scoreboard players add #used vault.tmp 1
""",
    )
    write(
        P / "sync/clear.mcfunction",
        """
$data remove storage vault:rt p$(pid).$(page).s$(slot)
""",
    )
    write(
        P / "sync/one_orphan.mcfunction",
        """
$execute if data entity @s Items[{Slot:$(slot)b,components:{"minecraft:custom_data":{gui:1b}}}] run data remove entity @s Items[{Slot:$(slot)b}]
$execute if data entity @s Items[{Slot:$(slot)b}] run function vault:sync/save_self {pid:$(pid),slot:$(slot),page:"$(page)"}
$execute unless data entity @s Items[{Slot:$(slot)b}] run function vault:sync/clear {pid:$(pid),slot:$(slot),page:"$(page)"}
""",
    )
    write(
        P / "sync/save_self.mcfunction",
        """
data remove storage vault:tmp one
$data modify storage vault:tmp one set from entity @s Items[{Slot:$(slot)b}]
data remove storage vault:tmp one.Slot
$data modify storage vault:rt p$(pid).$(page).s$(slot) set from storage vault:tmp one
""",
    )
    # orphan runs as the cart, and sync_orphan is `function ... with storage` as the cart (@s).
    # engine orphan:
    # execute as cart run function vault/sync_orphan_a with storage
    # But sync_orphan_a calls one_orphan which expects @s to be the cart. Good if we don't change executor.
    # one_orphan is called as function from cart, @s remains cart. Good.

    write(
        P / "load/current.mcfunction",
        """
execute store result storage vault:macro pid int 1 run scoreboard players get @s vault.id
data merge entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] {Items:[]}
execute if score @s vault.page matches 0 run function vault:load/page_a with storage vault:macro
execute if score @s vault.page matches 1 run function vault:load/page_b with storage vault:macro
execute if score @s vault.page matches 2 run function vault:load/page_c with storage vault:macro
function vault:ctrl/paint
scoreboard players operation @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] vault.page = @s vault.page
""",
    )
    for letter, key, title in (("a", "A", "Kasa • A"), ("b", "B", "Kasa • B"), ("c", "C", "Kasa • C")):
        lines = [f"data merge entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] {{CustomName:{jtext(title, 'dark_aqua')}}}"]
        for s in range(18):
            lines.append(f'$function vault:load/one {{pid:$(pid),slot:{s},page:"{key}"}}')
        write(P / f"load/page_{letter}.mcfunction", "\n".join(lines) + "\n")
    write(
        P / "load/one.mcfunction",
        """
$execute unless data storage vault:rt p$(pid).$(page).s$(slot) run return 0
data remove storage vault:tmp one
$data modify storage vault:tmp one set from storage vault:rt p$(pid).$(page).s$(slot)
$data modify storage vault:tmp one.Slot set value $(slot)b
data modify entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items append from storage vault:tmp one
""",
    )
    # Controls
    controls = {
        18: ("minecraft:arrow", "Önceki sayfa", "yellow", "page_prev"),
        19: ("minecraft:lime_dye", "Sayfa", "green", "none"),
        20: ("minecraft:hopper", "Sıkıştır", "gold", "compact"),
        22: ("minecraft:book", "Nasıl", "aqua", "none"),
        25: ("minecraft:barrier", "Kapat", "red", "close"),
        26: ("minecraft:arrow", "Sonraki sayfa", "yellow", "page_next"),
    }
    lore_ctrl = {
        18: [("A B C arasında", "gray")],
        19: [("Üst 18 göz senin", "gray"), ("Alt şerit düğme", "dark_gray")],
        20: [("Boşlukları sola toplar", "gray")],
        22: [("Eşyayı koy veya al", "gray"), ("Eğilerek de kapanır", "dark_gray"), ("Huni altına koyma", "red")],
        25: [("Kasayı kapatır ve kaydeder", "gray")],
        26: [("Sonraki sayfa", "gray")],
    }
    paint = []
    for slot, (iid, name, col, _act) in controls.items():
        paint.append(
            f"item replace entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] container.{slot} with {iid}[custom_name={jtext(name, col, bold=True)},lore={lore_snbt(lore_ctrl[slot])},custom_data={{gui:1b,pack:\"vault\"}},max_stack_size=1]"
        )
    for slot in (21, 23, 24):
        paint.append(
            f"item replace entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] container.{slot} with minecraft:gray_stained_glass_pane[hide_tooltip={{}},custom_data={{gui:1b,pack:\"vault\"}},max_stack_size=1]"
        )
    write(P / "ctrl/paint.mcfunction", "\n".join(paint) + "\n")
    # check controls 18-26
    checks = ["scoreboard players set #dirty vault.tmp 0", "data modify storage vault:live Items set from entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items", "execute store result storage vault:macro pid int 1 run scoreboard players get @s vault.id"]
    for slot, action in [(18, "page_prev"), (20, "compact"), (25, "close"), (26, "page_next")]:
        checks.append(f"execute unless data storage vault:live Items[{{Slot:{slot}b,components:{{\"minecraft:custom_data\":{{gui:1b,pack:\"vault\"}}}}}}] run function vault:ctrl/bad_{slot}")
    # also fillers 19,21,22,23,24 should be restored if missing but not queue a second action if already queued
    for slot in (19, 21, 22, 23, 24):
        checks.append(f"execute unless data storage vault:live Items[{{Slot:{slot}b,components:{{\"minecraft:custom_data\":{{gui:1b,pack:\"vault\"}}}}}}] run function vault:ctrl/bad_fill_{slot}")
    write(P / "ctrl/check.mcfunction", "\n".join(checks) + "\n")
    for slot, action in [(18, "page_prev"), (20, "compact"), (25, "close"), (26, "page_next")]:
        write(
            P / f"ctrl/bad_{slot}.mcfunction",
            f"""
execute if data storage vault:live Items[{{Slot:{slot}b}}] run function vault:ctrl/return_{slot}
execute store result storage vault:macro pid int 1 run scoreboard players get @s vault.id
function vault:ctrl/queue_{action} with storage vault:macro
scoreboard players set #dirty vault.tmp 1
""",
        )
        write(
            P / f"ctrl/return_{slot}.mcfunction",
            f"""
summon minecraft:item ~ ~0.2 ~ {{PickupDelay:0s,Tags:["vault.return"],Item:{{id:"minecraft:stone",count:1}}}}
data modify entity @e[type=minecraft:item,tag=vault.return,limit=1,sort=nearest] Item set from storage vault:live Items[{{Slot:{slot}b}}]
data remove entity @e[type=minecraft:item,tag=vault.return,limit=1,sort=nearest] Item.Slot
tag @e[type=minecraft:item,tag=vault.return,limit=1,sort=nearest] remove vault.return
""",
        )
        write(
            P / f"ctrl/queue_{action}.mcfunction",
            f"""
$execute if data storage vault:rt p$(pid).queue run return 0
$data modify storage vault:rt p$(pid).queue set value "{action}"
""",
        )
    for slot in (19, 21, 22, 23, 24):
        write(
            P / f"ctrl/bad_fill_{slot}.mcfunction",
            f"""
execute if data storage vault:live Items[{{Slot:{slot}b}}] unless data storage vault:live Items[{{Slot:{slot}b,components:{{"minecraft:custom_data":{{gui:1b}}}}}}] run function vault:ctrl/return_{slot}
scoreboard players set #dirty vault.tmp 1
""",
        )
        write(
            P / f"ctrl/return_{slot}.mcfunction",
            f"""
summon minecraft:item ~ ~0.2 ~ {{PickupDelay:0s,Tags:["vault.return"],Item:{{id:"minecraft:stone",count:1}}}}
data modify entity @e[type=minecraft:item,tag=vault.return,limit=1,sort=nearest] Item set from storage vault:live Items[{{Slot:{slot}b}}]
execute if data entity @e[type=minecraft:item,tag=vault.return,limit=1,sort=nearest] Item.components."minecraft:custom_data"{{gui:1b}} run kill @e[type=minecraft:item,tag=vault.return,limit=1,sort=nearest]
data remove entity @e[type=minecraft:item,tag=vault.return,limit=1,sort=nearest] Item.Slot
tag @e[type=minecraft:item,tag=vault.return] remove vault.return
""",
        )
    write(
        P / "ctrl/bar.mcfunction",
        """
execute if score @s vault.page matches 0 run title @s actionbar [{"text":"Sayfa A","color":"green"},{"text":"  ","color":"gray"},{"score":{"name":"@s","objective":"vault.used"},"color":"white"},{"text":"/18","color":"dark_gray"}]
execute if score @s vault.page matches 1 run title @s actionbar [{"text":"Sayfa B","color":"yellow"},{"text":"  ","color":"gray"},{"score":{"name":"@s","objective":"vault.used"},"color":"white"},{"text":"/18","color":"dark_gray"}]
execute if score @s vault.page matches 2 run title @s actionbar [{"text":"Sayfa C","color":"aqua"},{"text":"  ","color":"gray"},{"score":{"name":"@s","objective":"vault.used"},"color":"white"},{"text":"/18","color":"dark_gray"}]
""",
    )
    write(
        P / "act/close.mcfunction",
        "function vault:gui/close\n",
    )
    write(
        P / "act/page_next.mcfunction",
        """
function vault:sync/current
scoreboard players operation #p vault.tmp = @s vault.page
execute if score #p vault.tmp matches 0 run scoreboard players set @s vault.page 1
execute if score #p vault.tmp matches 1 run scoreboard players set @s vault.page 2
execute if score #p vault.tmp matches 2 run scoreboard players set @s vault.page 0
function vault:load/current
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.4 1.3
""",
    )
    write(
        P / "act/page_prev.mcfunction",
        """
function vault:sync/current
scoreboard players operation #p vault.tmp = @s vault.page
execute if score #p vault.tmp matches 0 run scoreboard players set @s vault.page 2
execute if score #p vault.tmp matches 1 run scoreboard players set @s vault.page 0
execute if score #p vault.tmp matches 2 run scoreboard players set @s vault.page 1
function vault:load/current
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.4 1.1
""",
    )
    write(
        P / "act/compact.mcfunction",
        """
function vault:sync/current
execute store result storage vault:macro pid int 1 run scoreboard players get @s vault.id
execute if score @s vault.page matches 0 run function vault:compact/run {pid:0,page:"A"}
execute if score @s vault.page matches 0 run function vault:compact/go_a with storage vault:macro
execute if score @s vault.page matches 1 run function vault:compact/go_b with storage vault:macro
execute if score @s vault.page matches 2 run function vault:compact/go_c with storage vault:macro
function vault:load/current
playsound minecraft:block.chest.close player @s ~ ~ ~ 0.4 1.4
title @s actionbar {"text":"Sayfa sıkıştırıldı.","color":"gold"}
""",
    )
    # remove the bogus line
    write(
        P / "act/compact.mcfunction",
        """
function vault:sync/current
execute store result storage vault:macro pid int 1 run scoreboard players get @s vault.id
execute if score @s vault.page matches 0 run function vault:compact/go_a with storage vault:macro
execute if score @s vault.page matches 1 run function vault:compact/go_b with storage vault:macro
execute if score @s vault.page matches 2 run function vault:compact/go_c with storage vault:macro
function vault:load/current
playsound minecraft:block.chest.close player @s ~ ~ ~ 0.4 1.4
title @s actionbar {"text":"Sayfa sıkıştırıldı.","color":"gold"}
""",
    )
    for letter, key in (("a", "A"), ("b", "B"), ("c", "C")):
        lines = [
            "data modify storage vault:tmp list set value []",
        ]
        for s in range(18):
            lines.append(f"$execute if data storage vault:rt p$(pid).{key}.s{s}.id run data modify storage vault:tmp list append from storage vault:rt p$(pid).{key}.s{s}")
        lines.append(f"$data remove storage vault:rt p$(pid).{key}")
        lines.append(f"$data modify storage vault:rt p$(pid).{key} set value {{}}")
        for s in range(18):
            lines.append(f"$execute if data storage vault:tmp list[{s}] run data modify storage vault:rt p$(pid).{key}.s{s} set from storage vault:tmp list[{s}]")
        write(P / f"compact/go_{letter}.mcfunction", "\n".join(lines) + "\n")
    # Vault dispatch_call expects act functions. page_prev etc exist.
    # gui/scan.mcfunction exists but vault tick doesn't call it. That's ok.
    # Dummy act/none not needed.
    # queue actions: page_prev, page_next, compact, close. All exist.
    # Provide a no-op act used nowhere.
    write(P / "act/none.mcfunction", "execute if entity @s\n")

def readme() -> str:
    return '''# my_gui

Minecraft **Java 1.21.3** için dört bağımsız chest GUI datapack'i. `pack_format` **57**. Diyalog komutu yok; menü, oyuncunun önüne çağrılan görünmez hitbox'lı sandık vagonudur ve başlığı sandık arayüzünde görünür.

Kurulum: bir klasörü dünyanın `datapacks/` dizinine kopyala, `/reload`. Dört paket birlikte durabilir; anahtarlar `custom_data.pack` ile ayrılır.

| Paket | Klasör | Açılış | Ne işe yarar |
|---|---|---|---|
| Zümrüt Çarşı | `bazaar` | `/trigger bazaar` veya Çarşı Asası | Çok sayfalı alış, satış, banka, günlük ödül, sınırlı stok |
| Yol Atlası | `atlas` | `/trigger atlas` veya Atlas Değneği | Ev, sunucu işareti, son güvenli yer, merkez / nether / end |
| Sınıf Emaneti | `reliquary` | `/trigger reliquary` veya Emanet Asası | Kilitli sınıflar, 10 dk kit, ustalık, takım öneki |
| Kutsal Kasa | `vault` | `/trigger vault` veya Kasa Anahtarı | Kişiye özel 3×18 gerçek eşya deposu |

## Ortak kullanım

- Sandık görünen vagona **sağ tık**.
- Kapatmak için **eğil** ya da bariyer. Açılıştan sonra kısa bir süre eğilme yok sayılır.
- Menü eşyası envantere geçerse aynı tick içinde silinir. Yanlışlıkla konan eşya yere iade edilir.
- Huni ve huni vagonu GUI eşyasını çekemez; kasa gerçek eşyada huni altına açılırsa bir tick içinde depoya yazılır, yine de huninin üstünde açmayın.
- İzleyici modu açamaz. Uzaklaşınca veya ölünce kapanır.

## Zümrüt Çarşı

Para, envanterdeki zümrüt değil **banka bakiyesi** (`bazaar.bank`). Banka sayfasından yatırılır ve çekilir. Günlük ödül Minecraft günü başına bir kez, varsayılan 8.

Fiyat ve stok `storage bazaar:shop items.<anahtar>` içindedir. Onay ekranı burayı okur. `stock` değeri `-1` sınırsızdır. Yönetici:

```
/tag @s add bazaar.admin
/function bazaar:admin/grant
```

Yönetici düğmesi stokları `bazaar:defaults` kopyasına döndürür, bakiyeye dokunmaz.

## Yol Atlası

- End adası ilk yüklemede `100 49 0` olarak hazırdır. Dünya merkezi ve nether boştur.
- Kişisel ev (3) herkese açıktır. Merkez, nether, end üstüne yazma ve 6 sunucu işareti için:

```
/tag @s add atlas.admin
```

- Son güvenli yer, yerdeyken ve lavda değilken yaklaşık 5 saniyede bir yazılır.
- Işınlanma varsayılan 8 saniye bekletir (`storage atlas:config cooldown`, tick). Hedefte zemin aranır; Direnç IV (5 sn) ve Yavaş Düşüş verilir.
- Yalnız `overworld`, `the_nether`, `the_end`.

## Sınıf Emaneti

| Sınıf | Kilit |
|---|---|
| Şövalye | yok |
| Nişancı | `adventure/shoot_arrow` |
| Çiftçi | `husbandry/plant_seed` |
| Madenci | `story/smelt_iron` |
| Simyacı | `nether/brew_potion` |
| Kaşif | `adventure/sleep_in_bed` |

Bekleme varsayılan 12000 tick (10 dk): `storage reliquary:config cooldown`. Aynı sınıfın üçüncü verilişinde bir altın elma düşer. Takım yalnız prefix değiştirir; `friendlyFire true` ve `collisionRule always` olduğu için PvP kapanmaz.

```
/function reliquary:admin/teams_off
/function reliquary:admin/teams_on
/function reliquary:admin/clear_teams
```

## Kutsal Kasa

Üst 18 göz gerçek depodur (sayfa A/B/C, toplam 54). Alt şerit düğmedir. Eşya sandığa konunca depoya yazılır, alınca depodan düşer. Kapanırken, oyuncu uzaklaşınca veya sandık vagonu sahipsiz kalınca tekrar yazılır, sonra vagon silinir. Sıkıştır boş gözleri sola toplar.

`/function vault:uninstall` **kasadaki eşyaların veri kopyasını da siler.**

Yaratıcı modda orta tık ile kopyalamak kasayı yanıltabilir. Hayatta kalma için tasarlandı.

## Kaldırma

```
/function bazaar:uninstall
/function atlas:uninstall
/function reliquary:uninstall
/function vault:uninstall
```

Sonra klasörü `datapacks` içinden silip `/reload`.

## Güvenlik

- Tıklama eylemi sandıktaki NBT'den değil, sunucunun sayfa tablosundan seçilir.
- `give` yalnız çarşı deposundaki `minecraft:` kimliğine gider. Sohbet girdisi komut üretmez.
- Menü eşyasında `custom_data.gui` vardır; envanter, yer eşyası ve huni vagonundan temizlenir.
- Op, komut bloğu veya `execute run op` yok. Yönetici yetkisi düz etikettir.
- `team` PvP'yi kapatmaz.

## Sürüm

Yalnızca **1.21.2–1.21.3**, veri paketi formatı **57**. 1.21.4 `custom_model_data`, 1.21.5 metin bileşeni ve 1.21.6 `/dialog` bu paketlerde kullanılmaz. Kaynak dosyalar UTF-8 `mcfunction`dır. `tools/generate.py` paketleri yeniden üretir; elle düzeltme yaptıysan betiği çalıştırma.

Lisans: MIT.
'''

def license_text() -> str:
    return """MIT License

Copyright (c) 2026 tickwarden

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

def validate(root: Path) -> None:
    errors: list[str] = []
    fn_re_files = {}
    for mc in root.glob("*"):
        if not mc.is_dir() or mc.name == "tools":
            continue
        meta = json.loads((mc / "pack.mcmeta").read_text(encoding="utf-8"))
        if meta["pack"]["pack_format"] != 57:
            errors.append(f"{mc.name} pack_format")
        for path in mc.rglob("*"):
            if path.suffix == ".json":
                json.loads(path.read_text(encoding="utf-8"))
            if path.suffix == ".mcfunction":
                text = path.read_text(encoding="utf-8")
                if "\t" in text:
                    errors.append(f"tab {path}")
                rel = path.relative_to(mc / "data")
                parts = rel.parts
                if len(parts) < 3 or parts[1] != "function":
                    continue
                ns = parts[0]
                sub = "/".join(parts[2:]).removesuffix(".mcfunction")
                fn_re_files[f"{ns}:{sub}"] = path
                for line in text.splitlines():
                    raw = line.strip()
                    if raw.startswith("$") and "$( " in raw:
                        errors.append(f"macro space {path}")
    # objectives
    import re
    obj_re = re.compile(r"scoreboard objectives add ([^\s]+)")
    call_re = re.compile(r"function ([a-z0-9_]+:[a-z0-9_./]+)")
    for path in root.glob("*/*"):
        pass
    for path in root.rglob("*.mcfunction"):
        text = path.read_text(encoding="utf-8")
        for m in obj_re.finditer(text):
            if len(m.group(1)) > 16:
                errors.append(f"obj {m.group(1)} in {path}")
        for line in text.splitlines():
            if "$(" in line:
                continue
            for m in call_re.finditer(line):
                name = m.group(1)
                if name not in fn_re_files:
                    errors.append(f"missing {name} from {path.relative_to(root)}")
        if "click_event" in text or "min_format" in text:
            errors.append(f"new syntax {path}")
    if errors:
        raise SystemExit("VALIDATION FAILED\n" + "\n".join(errors[:80]))
    print(f"ok functions={len(fn_re_files)}")

def main() -> None:
    bazaar = ROOT / "bazaar"
    atlas = ROOT / "atlas"
    reliquary = ROOT / "reliquary"
    vault = ROOT / "vault"
    for p in (bazaar, atlas, reliquary, vault):
        if p.exists():
            import shutil
            shutil.rmtree(p)
    write_bazaar(bazaar)
    write_atlas(atlas)
    write_reliquary(reliquary)
    write_vault(vault)
    write(ROOT / "README.md", readme())
    write(ROOT / "LICENSE", license_text())
    validate(ROOT)

if __name__ == "__main__":
    main()
