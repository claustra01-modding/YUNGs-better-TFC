#!/usr/bin/env python3
"""依存元1.21.1のloot tableからTFC互換上書きを再生成する。"""

from __future__ import annotations

import argparse
import copy
import json
import shutil
import zipfile
from pathlib import Path


MOD_ID = "yungsbettertfc"
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src/main/resources/data"
JARS = {
    "betterdungeons": "YungsBetterDungeons-1.21.1-NeoForge-5.1.4.jar",
    "betterfortresses": "YungsBetterNetherFortresses-1.21.1-NeoForge-3.1.5.jar",
    "betteroceanmonuments": "YungsBetterOceanMonuments-1.21.1-NeoForge-4.1.2.jar",
    "betterstrongholds": "YungsBetterStrongholds-1.21.1-NeoForge-5.1.3.jar",
}
PROFILE_BY_TABLE = {
    "minecraft:chests/end_city_treasure": "lategame",
    "minecraft:chests/nether_bridge": "dangerous",
}
MATERIALS = {
    "ordinary": ("copper", "bronze", "bismuth_bronze", "black_bronze"),
    "dangerous": ("wrought_iron",),
    "lategame": ("steel",),
}
INGOTS = {
    "ordinary": ("copper", "bronze", "bismuth_bronze", "black_bronze", "wrought_iron"),
    "dangerous": ("wrought_iron", "steel"),
    "lategame": ("steel", "black_steel"),
}
FAMILIES = {
    "pickaxe": (("pickaxe_head", "propick_head"), ("pickaxe", "propick")),
    "axe": (("axe_head", "saw_blade"), ("axe", "saw")),
    "hoe": (("hoe_head", "scythe_blade"), ("hoe", "scythe")),
    "sword": (("sword_blade", "javelin_head", "mace_head"), ("sword", "javelin", "mace")),
    "shovel": (("shovel_head",), ("shovel",)),
    "knife": (("knife_blade",), ("knife",)),
    "shears": ((), ("shears",)),
    "shield": ((), ("shield",)),
    "helmet": (("unfinished_helmet",), ("helmet",)),
    "chestplate": (("unfinished_chestplate",), ("chestplate",)),
    "leggings": (("unfinished_greaves",), ("greaves",)),
    "boots": (("unfinished_boots",), ("boots",)),
}
GEMS = {"diamond", "emerald", "lapis_lazuli", "amethyst_shard"}
PRODUCE = {"apple", "bread", "carrot", "potato", "glow_berries", "wheat", "beetroot", "melon_slice"}
SEEDS = {"beetroot_seeds", "melon_seeds", "pumpkin_seeds", "wheat_seeds"}
UTILITY = {"obsidian", "crying_obsidian", "quartz", "glowstone_dust"}


def dump(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def item(name: str, weight: int | None = None, functions: list | None = None) -> dict:
    value = {"type": "minecraft:item", "name": name}
    if weight is not None:
        value["weight"] = weight
    if functions:
        value["functions"] = functions
    return value


def table(name: str, source: dict, functions: list | None = None) -> dict:
    value = {key: copy.deepcopy(val) for key, val in source.items() if key not in {"type", "name", "functions"}}
    value.update({"type": "minecraft:loot_table", "value": name})
    if functions:
        value["functions"] = copy.deepcopy(functions)
    return value


def one_pool(entries: list[dict]) -> dict:
    return {"type": "minecraft:generic", "pools": [{"rolls": 1, "entries": entries}]}


def profile(namespace: str, logical_path: str) -> str:
    key = f"{namespace}:{logical_path}"
    if key in PROFILE_BY_TABLE:
        return PROFILE_BY_TABLE[key]
    if namespace in {"betterfortresses", "betterstrongholds"}:
        return "dangerous"
    if namespace == "betterdungeons" and logical_path.startswith("small_nether_dungeon/"):
        return "dangerous"
    return "ordinary"


def equipment_family(path: str) -> str | None:
    if path.endswith("horse_armor"):
        return "horse_armor"
    families = ("chestplate", "leggings", "helmet", "boots", "pickaxe", "shovel", "shears", "shield", "crossbow", "knife", "sword", "hoe", "axe", "bow")
    for family in families:
        if path == family or path.endswith("_" + family):
            return family
    return None


def equipment_table(current_profile: str, family: str, completion_functions: list[dict] | None = None) -> dict:
    if family in {"bow", "crossbow"}:
        return one_pool([item(f"minecraft:{family}", functions=completion_functions)])
    if family == "horse_armor":
        return one_pool([item(f"tfc:metal/horse_armor/{metal}") for metal in MATERIALS[current_profile]])
    parts, completed = FAMILIES[family]
    entries = []
    for metal in MATERIALS[current_profile]:
        entries.extend(item(f"tfc:metal/{part}/{metal}", weight=2) for part in parts)
        entries.extend(item(f"tfc:metal/{tool}/{metal}", weight=1, functions=completion_functions) for tool in completed)
    return one_pool(entries)


def transform_entry(entry: dict, current_profile: str, source_path: str) -> dict:
    value = copy.deepcopy(entry)
    if value.get("type") != "minecraft:item":
        return value
    name = value.get("name", "")
    namespace, _, path = name.partition(":")
    if namespace != "minecraft":
        return value
    functions = [
        copy.deepcopy(function)
        for function in value.get("functions", [])
        if function.get("function") != "minecraft:set_damage"
    ]
    if functions:
        value["functions"] = functions
    else:
        value.pop("functions", None)
    if source_path == "betterstrongholds/chests/cmd_yung" and path == "diamond_sword":
        value["name"] = "tfc:metal/sword/wrought_iron"
        return value
    if path in GEMS:
        return table(f"{MOD_ID}:shared/gems", value, functions)
    if path in {"iron_ingot", "gold_ingot"}:
        return table(f"{MOD_ID}:shared/ingots/{current_profile}", value, functions)
    if path == "iron_nugget":
        return table(f"{MOD_ID}:shared/small_ores/iron", value, functions)
    if path in {"gold_nugget", "raw_gold"}:
        value["name"] = "tfc:ore/small_native_gold"
        return value
    if path in {"coal", "charcoal"}:
        return table(f"{MOD_ID}:shared/coal_like", value, functions)
    if path == "torch":
        value["name"] = "tfc:torch"
        return value
    if path in PRODUCE:
        return table(f"{MOD_ID}:shared/produce", value, functions)
    if path in SEEDS:
        return table(f"{MOD_ID}:shared/seeds", value, functions)
    if path == "bone_meal":
        return table(f"{MOD_ID}:shared/fertilizers", value, functions)
    if path in UTILITY:
        return table(f"{MOD_ID}:shared/utility", value, functions)
    family = equipment_family(path)
    if family is None:
        return value
    if family in {"bow", "crossbow", "horse_armor"}:
        return table(f"{MOD_ID}:shared/equipment/{current_profile}/{family}", value, functions)
    target = f"{MOD_ID}:shared/equipment/{current_profile}/{family}"
    return table(target, value, functions)


def transform_node(value, current_profile: str, source_path: str):
    if isinstance(value, list):
        return [transform_node(child, current_profile, source_path) for child in value]
    if not isinstance(value, dict):
        return value
    if value.get("type") == "minecraft:item":
        return transform_entry(value, current_profile, source_path)
    return {key: transform_node(child, current_profile, source_path) for key, child in value.items()}


def shared_tables() -> dict[str, dict]:
    result = {
        "shared/gems": one_pool([item(f"tfc:gem/{gem}") for gem in ("amethyst", "diamond", "emerald", "lapis_lazuli", "opal", "pyrite", "ruby", "sapphire", "topaz")]),
        "shared/coal_like": one_pool([item(name) for name in ("minecraft:charcoal", "tfc:bituminous_coal", "tfc:lignite", "tfc:ore/graphite")]),
        "shared/utility": one_pool([item(name) for name in ("tfc:powder/flux", "minecraft:glass", "minecraft:glass_pane", "tfc:kaolin_clay", "tfc:powder/wood_ash", "tfc:powder/saltpeter", "tfc:powder/sylvite")]),
        "shared/produce": one_pool([{"type": "minecraft:tag", "name": f"{MOD_ID}:loot/produce", "expand": True}]),
        "shared/seeds": one_pool([{"type": "minecraft:tag", "name": f"{MOD_ID}:loot/seeds", "expand": True}]),
        "shared/fertilizers": one_pool([{"type": "minecraft:tag", "name": f"{MOD_ID}:loot/fertilizers", "expand": True}]),
        "shared/small_ores/iron": one_pool([item(f"tfc:ore/small_{ore}") for ore in ("hematite", "magnetite", "limonite")]),
    }
    for current_profile, metals in INGOTS.items():
        result[f"shared/ingots/{current_profile}"] = one_pool([item(f"tfc:metal/ingot/{metal}") for metal in metals])
        for family in tuple(FAMILIES) + ("bow", "crossbow", "horse_armor"):
            result[f"shared/equipment/{current_profile}/{family}"] = equipment_table(current_profile, family)
    return result


def source_for(namespace: str, mods_dir: Path, minecraft_jar: Path) -> Path:
    return minecraft_jar if namespace == "minecraft" else mods_dir / JARS[namespace]


def validate_tfc_item_ids(tfc_jar: Path) -> None:
    ids: set[str] = set()

    def collect(value) -> None:
        if isinstance(value, dict):
            if value.get("type") == "minecraft:item" and value.get("name", "").startswith("tfc:"):
                ids.add(value["name"].removeprefix("tfc:"))
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)

    for path in DATA.rglob("loot_table/**/*.json"):
        collect(json.loads(path.read_text(encoding="utf-8")))
    for path in (DATA / MOD_ID / "tags/item/loot").rglob("*.json"):
        tag = json.loads(path.read_text(encoding="utf-8"))
        ids.update(value.removeprefix("tfc:") for value in tag.get("values", []) if value.startswith("tfc:"))
    with zipfile.ZipFile(tfc_jar) as archive:
        resources = set(archive.namelist())
    missing = [item_id for item_id in sorted(ids) if f"assets/tfc/models/item/{item_id}.json" not in resources]
    if missing:
        raise ValueError("TFC 4.2.5に存在しないitem id: " + ", ".join(f"tfc:{item_id}" for item_id in missing))
    print(f"TFC item id検証: {len(ids)}件すべて存在")


def regenerate(minecraft_jar: Path, mods_dir: Path) -> None:
    targets = []
    for namespace in ("minecraft", *JARS):
        base = DATA / namespace / "loot_table"
        targets.extend((namespace, path, path.relative_to(base).with_suffix("").as_posix()) for path in base.rglob("*.json"))
    archives: dict[Path, zipfile.ZipFile] = {}
    try:
        for namespace, target, logical_path in targets:
            archive_path = source_for(namespace, mods_dir, minecraft_jar)
            archives.setdefault(archive_path, zipfile.ZipFile(archive_path))
            source_name = f"data/{namespace}/loot_table/{logical_path}.json"
            source = json.loads(archives[archive_path].read(source_name))
            transformed = transform_node(source, profile(namespace, logical_path), f"{namespace}/{logical_path}")
            dump(target, transformed)
    finally:
        for archive in archives.values():
            archive.close()
    shared_root = DATA / MOD_ID / "loot_table/shared"
    if shared_root.exists():
        shutil.rmtree(shared_root)
    for logical_path, value in shared_tables().items():
        dump(DATA / MOD_ID / "loot_table" / f"{logical_path}.json", value)
    tag_root = DATA / MOD_ID / "tags/item/loot"
    for obsolete in ("equipment", "horse_armor", "metals_ingot", "metals_rod", "metals_sheet"):
        shutil.rmtree(tag_root / obsolete, ignore_errors=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--minecraft-jar", type=Path, required=True)
    parser.add_argument("--mods-dir", type=Path, required=True)
    parser.add_argument("--tfc-jar", type=Path, required=True)
    args = parser.parse_args()
    regenerate(args.minecraft_jar, args.mods_dir)
    validate_tfc_item_ids(args.tfc_jar)


if __name__ == "__main__":
    main()
