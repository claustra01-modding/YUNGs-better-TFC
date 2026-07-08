# YUNG's Better Mineshafts 13 種 variant 調査メモ

調査対象は `YUNG-GANG/YUNGs-Better-Mineshafts` の `1.21.1` ブランチ、確認時点の commit `78e4655440bc32a5c42b39198fcc64741fa08b5e`。mod id は `bettermineshafts`、mod version は `5.1.1`。

この mod の廃坑は template pool / NBT ではなく、`BetterMineshaftStructure` と `StructurePiece` 系クラスによる Java 実装で生成される。したがって、既存の `StructureTemplate` 系 mixin だけでは主な構成ブロックは置換できない。

## 共通仕様

- 構造物 type: `bettermineshafts:mineshaft`
- Y 範囲の初期値: `minY = -55`, `maxY = 30`
- vanilla mineshaft 無効化設定の初期値: `disableVanillaMineshafts = true`
- 入口 piece: `VerticalEntrance`
- 主な piece: `BigTunnel`, `SmallTunnel`, `SmallTunnelStairs`, `SmallTunnelTurn`, `LayeredIntersection4`, `LayeredIntersection5`, `SideRoom`, `SideRoomDungeon`, `OreDeposit`, `ZombieVillagerRoom`
- ore deposit の初期出現率:
  - cobblestone: `50`
  - coal ore: `20`
  - iron ore: `9`
  - redstone ore: `7`
  - gold ore: `7`
  - lapis ore: `3`
  - emerald ore: `3`
  - diamond ore: `1`
- 装飾・特殊配置の初期出現率:
  - lantern: `0.0067`
  - torch: `0.02`
  - workstation: `0.025`
  - workstation dungeon: `0.25`
  - small shaft: `0.07`
  - cobweb: `0.15`
  - small tunnel chest minecart: `0.00125`
  - small tunnel TNT minecart: `0.0025`
  - main tunnel chest minecart: `0.01`
  - main tunnel TNT minecart: `0.0025`
  - zombie villager room: `2`
  - small shaft chain length: `9`

## 共通 loot

Better Mineshafts 独自の loot table はなく、全て vanilla の `BuiltInLootTables.ABANDONED_MINESHAFT`、つまり `minecraft:chests/abandoned_mineshaft` を参照する。

参照箇所:

- `BigTunnel`: chest minecart
- `SmallTunnel`: chest minecart
- `SideRoom`: barrel
- `SideRoomDungeon`: chest
- `ZombieVillagerRoom`: barrel

`minecraft:chests/abandoned_mineshaft` の vanilla 内容:

- pool 1、rolls `1`
  - golden apple: weight `20`
  - enchanted golden apple: weight `1`
  - name tag: weight `30`
  - enchanted book: weight `10`
  - iron pickaxe: weight `5`
  - empty: weight `5`
- pool 2、rolls `2..4`
  - iron ingot: weight `10`, count `1..5`
  - gold ingot: weight `5`, count `1..3`
  - redstone: weight `5`, count `4..9`
  - lapis lazuli: weight `5`, count `4..9`
  - diamond: weight `3`, count `1..2`
  - coal: weight `10`, count `3..8`
  - bread: weight `15`, count `1..3`
  - glow berries: weight `15`, count `3..6`
  - melon seeds: weight `10`, count `2..4`
  - pumpkin seeds: weight `10`, count `2..4`
  - beetroot seeds: weight `10`, count `2..4`
- pool 3、rolls `3`
  - rail: weight `20`, count `4..8`
  - powered rail: weight `5`, count `1..4`
  - detector rail: weight `5`, count `1..4`
  - activator rail: weight `5`, count `1..4`
  - torch: weight `15`, count `1..16`
- Trade Rebalance 有効時の追加 pool
  - empty: weight `4`
  - Efficiency の enchanted book: weight `1`

TFC 対応では、この loot table を差し替えるだけで Better Mineshafts 内の chest minecart / barrel / chest の loot 全体に効く。

## Java 直置きされる主な vanilla ブロック

variant 設定とは別に piece 実装から直接置かれるブロックがある。TFC 対応では、template 置換ではなく Better Mineshafts の piece 生成を捕まえるか、設置時の block state を変換する必要がある。

- 交通・鉱山設備: `rail`, `powered_rail`, `chest_minecart`, `tnt_minecart`
- 光源: `wall_torch`, `lantern`, `redstone_torch`
- 鉱山らしい装飾: `cobweb`, `chain`, `ladder`, `iron_bars`, `iron_door`
- container / workstation: `barrel`, `chest`, `furnace`, `crafting_table`, `smithing_table`, `blast_furnace`, `anvil`
- dungeon / 部屋: `spawner`, `black_bed`, `stone_button`
- 自然物: `vine`, `snow`, `cactus`, `dead_bush`, `brown_mushroom`, `red_mushroom`, `moss_carpet`
- ore deposit: `coal_ore`, `iron_ore`, `redstone_ore`, `gold_ore`, `lapis_ore`, `emerald_ore`, `diamond_ore`

## 13 種 variant 詳細

### 1. acacia

- 置換率: `0.6`
- leg variant: `edge`
- 装飾:
  - vine chance: `0.1`
  - gravel pile chance: `0.1`
- 固定 block state:
  - main block: `minecraft:acacia_planks`
  - support block: `minecraft:acacia_fence`
  - slab block: `minecraft:acacia_slab`
  - gravel block: `minecraft:gravel`
  - stone wall block: `minecraft:stone_brick_wall`
  - stone slab block: `minecraft:stone_brick_slab`
  - trapdoor block: `minecraft:acacia_trapdoor`
  - small leg block: `minecraft:stripped_acacia_log`
- ランダム block state 候補:
  - `minecraft:acacia_planks`
  - `minecraft:cobblestone`
  - `minecraft:stone_bricks`
  - `minecraft:mossy_stone_bricks`
  - `minecraft:cracked_stone_bricks`
  - `minecraft:cave_air`
  - `minecraft:stripped_acacia_log`
- 元 mod の生成バイオーム:
  - `minecraft:savanna`
  - `minecraft:savanna_plateau`
  - optional `#forge:is_savanna`
  - optional `#c:savanna`
  - optional `terralith:arid_highlands`
  - optional `terralith:hot_shrubland`
  - optional `terralith:sakura_grove`
  - optional `terralith:sakura_valley`
  - optional `projectvibrantjourneys:baobab_fields`
- loot: 共通の `minecraft:chests/abandoned_mineshaft`

### 2. desert

- 置換率: `0.6`
- leg variant: `edge`
- 装飾:
  - cactus chance: `0.1`
  - dead bush chance: `0.1`
  - gravel pile chance: `0.2`
- 固定 block state:
  - main block: `minecraft:sandstone`
  - support block: `minecraft:sandstone_wall`
  - slab block: `minecraft:sandstone_slab`
  - gravel block: `minecraft:sand`
  - stone wall block: `minecraft:sandstone_wall`
  - stone slab block: `minecraft:sandstone_slab`
  - trapdoor block: `minecraft:oak_trapdoor`
  - small leg block: `minecraft:smooth_sandstone`
- ランダム block state 候補:
  - `minecraft:sandstone`
  - `minecraft:cut_sandstone`
  - `minecraft:chiseled_sandstone`
  - `minecraft:smooth_sandstone`
  - `minecraft:sand`
  - `minecraft:stone_bricks`
  - `minecraft:cracked_stone_bricks`
  - `minecraft:cave_air`
- 元 mod の生成バイオーム:
  - `minecraft:desert`
  - optional `#forge:is_desert`
  - optional `#c:desert`
  - optional `terralith:lush_desert`
  - optional `biomesoplenty:lush_desert`
  - optional `projectvibrantjourneys:desert_shrubland`
  - optional `projectvibrantjourneys:verdant_sands`
- loot: 共通の `minecraft:chests/abandoned_mineshaft`

### 3. dripstone

- 置換率: `0.6`
- leg variant: `edge`
- 装飾:
  - vine chance: `0.1`
  - gravel pile chance: `0.1`
  - dripstone decorations: `true`
- 固定 block state:
  - main block: `minecraft:oak_planks`
  - support block: `minecraft:oak_fence`
  - slab block: `minecraft:oak_slab`
  - gravel block: `minecraft:gravel`
  - stone wall block: `minecraft:stone_brick_wall`
  - stone slab block: `minecraft:stone_brick_slab`
  - trapdoor block: `minecraft:oak_trapdoor`
  - small leg block: `minecraft:stripped_oak_log`
- ランダム block state 候補:
  - `minecraft:oak_planks`
  - `minecraft:cobblestone`
  - `minecraft:stone_bricks`
  - `minecraft:mossy_stone_bricks`
  - `minecraft:cracked_stone_bricks`
  - `minecraft:cave_air`
- 元 mod の生成バイオーム:
  - `minecraft:dripstone_caves`
- loot: 共通の `minecraft:chests/abandoned_mineshaft`

### 4. ice

- 置換率: `0.95`
- leg variant: `inner`
- 装飾:
  - gravel pile chance: `0.1`
- 固定 block state:
  - main block: `minecraft:packed_ice`
  - support block: `minecraft:packed_ice`
  - slab block: `minecraft:packed_ice`
  - gravel block: `minecraft:snow_block`
  - stone wall block: `minecraft:packed_ice`
  - stone slab block: `minecraft:packed_ice`
  - trapdoor block: `minecraft:spruce_trapdoor`
  - small leg block: `minecraft:packed_ice`
- ランダム block state 候補:
  - `minecraft:packed_ice`
  - `minecraft:blue_ice`
  - `minecraft:snow_block`
  - `minecraft:cave_air`
- 元 mod の生成バイオーム:
  - `minecraft:ice_spikes`
  - `minecraft:frozen_peaks`
  - optional `#byg:is_icy`
  - optional `#forge:is_icy`
  - optional `#c:icy`
- loot: 共通の `minecraft:chests/abandoned_mineshaft`

### 5. jungle

- 置換率: `0.6`
- leg variant: `edge`
- 装飾:
  - vine chance: `0.5`
  - gravel pile chance: `0.1`
- 固定 block state:
  - main block: `minecraft:jungle_planks`
  - support block: `minecraft:jungle_fence`
  - slab block: `minecraft:jungle_slab`
  - gravel block: `minecraft:gravel`
  - stone wall block: `minecraft:cobblestone_wall`
  - stone slab block: `minecraft:cobblestone_slab`
  - trapdoor block: `minecraft:jungle_trapdoor`
  - small leg block: `minecraft:stripped_jungle_log`
- ランダム block state 候補:
  - `minecraft:jungle_planks`
  - `minecraft:mossy_cobblestone`
  - `minecraft:stone_bricks`
  - `minecraft:chiseled_stone_bricks`
  - `minecraft:mossy_stone_bricks`
  - `minecraft:cracked_stone_bricks`
  - `minecraft:cave_air`
  - `minecraft:stripped_jungle_log`
- 元 mod の生成バイオーム:
  - `#minecraft:is_jungle`
  - optional `#forge:is_jungle`
  - optional `#c:in_jungle`
- loot: 共通の `minecraft:chests/abandoned_mineshaft`

### 6. lush

- 置換率: `0.95`
- leg variant: `edge`
- 装飾:
  - gravel pile chance: `0.1`
  - lush decorations: `true`
- 固定 block state:
  - main block: `minecraft:oak_planks`
  - support block: `minecraft:oak_fence`
  - slab block: `minecraft:oak_slab`
  - gravel block: `minecraft:gravel`
  - stone wall block: `minecraft:mossy_cobblestone_wall`
  - stone slab block: `minecraft:mossy_cobblestone_slab`
  - trapdoor block: `minecraft:oak_trapdoor`
  - small leg block: `minecraft:stripped_oak_log`
- ランダム block state 候補:
  - `minecraft:oak_planks`
  - `minecraft:moss_block`
  - `minecraft:stone_bricks`
  - `minecraft:mossy_stone_bricks`
  - `minecraft:cracked_stone_bricks`
  - `minecraft:cave_air`
- 元 mod の生成バイオーム:
  - `minecraft:lush_caves`
- loot: 共通の `minecraft:chests/abandoned_mineshaft`

### 7. mesa

- 置換率: `0.9`
- leg variant: `edge`
- 装飾:
  - vine chance: `0.1`
  - dead bush chance: `0.1`
  - gravel pile chance: `0.1`
- 固定 block state:
  - main block: `minecraft:dark_oak_planks`
  - support block: `minecraft:dark_oak_fence`
  - slab block: `minecraft:dark_oak_slab`
  - gravel block: `minecraft:gravel`
  - stone wall block: `minecraft:cobblestone_wall`
  - stone slab block: `minecraft:cobblestone_slab`
  - trapdoor block: `minecraft:dark_oak_trapdoor`
  - small leg block: `minecraft:stripped_dark_oak_log`
- ランダム block state 候補:
  - `minecraft:dark_oak_planks`
  - `minecraft:white_terracotta`
  - `minecraft:orange_terracotta`
  - `minecraft:yellow_terracotta`
  - `minecraft:brown_terracotta`
  - `minecraft:stone_bricks`
  - `minecraft:mossy_stone_bricks`
  - `minecraft:cracked_stone_bricks`
  - `minecraft:cave_air`
- 元 mod の生成バイオーム:
  - `#minecraft:is_badlands`
  - optional `#forge:is_mesa`
  - optional `#c:in_mesa`
  - optional `#forge:is_badlands`
  - optional `#c:badlands`
- loot: 共通の `minecraft:chests/abandoned_mineshaft`

### 8. mushroom

- 置換率: `0.95`
- leg variant: `inner`
- 装飾:
  - vine chance: `0.1`
  - mushroom chance: `0.4`
  - gravel pile chance: `0.1`
- 固定 block state:
  - main block: `minecraft:red_mushroom_block`
  - support block: `minecraft:mushroom_stem`
  - slab block: `minecraft:brown_mushroom_block`
  - gravel block: `minecraft:gravel`
  - stone wall block: `minecraft:mushroom_stem`
  - stone slab block: `minecraft:red_mushroom_block`
  - trapdoor block: `minecraft:oak_trapdoor`
  - small leg block: `minecraft:brown_mushroom_block`
- ランダム block state 候補:
  - `minecraft:red_mushroom_block`
  - `minecraft:brown_mushroom_block`
  - `minecraft:mushroom_stem`
  - `minecraft:mycelium`
- 元 mod の生成バイオーム:
  - `minecraft:mushroom_fields`
  - optional `#forge:is_mushroom`
  - optional `#c:mushroom`
  - optional `biomesoplenty:fungal_jungle`
- loot: 共通の `minecraft:chests/abandoned_mineshaft`

### 9. oak

- 置換率: `0.6`
- leg variant: `edge`
- 装飾:
  - vine chance: `0.1`
  - gravel pile chance: `0.1`
- 固定 block state:
  - main block: `minecraft:oak_planks`
  - support block: `minecraft:oak_fence`
  - slab block: `minecraft:oak_slab`
  - gravel block: `minecraft:gravel`
  - stone wall block: `minecraft:stone_brick_wall`
  - stone slab block: `minecraft:stone_brick_slab`
  - trapdoor block: `minecraft:oak_trapdoor`
  - small leg block: `minecraft:stripped_oak_log`
- ランダム block state 候補:
  - `minecraft:oak_planks`
  - `minecraft:cobblestone`
  - `minecraft:stone_bricks`
  - `minecraft:mossy_stone_bricks`
  - `minecraft:cracked_stone_bricks`
  - `minecraft:cave_air`
- 元 mod の生成バイオーム:
  - `minecraft:plains`
  - `minecraft:sunflower_plains`
  - `minecraft:swamp`
  - `minecraft:meadow`
  - optional `terralith:brushland`
  - optional `projectvibrantjourneys:prairie`
  - optional `#c:plains`
- loot: 共通の `minecraft:chests/abandoned_mineshaft`

### 10. overgrown

- 置換率: `0.95`
- leg variant: `edge`
- 装飾:
  - vine chance: `0.5`
  - gravel pile chance: `0.8`
- 固定 block state:
  - main block: `minecraft:spruce_planks`
  - support block: `minecraft:spruce_fence`
  - slab block: `minecraft:spruce_slab`
  - gravel block: `minecraft:spruce_leaves`
  - stone wall block: `minecraft:mossy_cobblestone_wall`
  - stone slab block: `minecraft:mossy_cobblestone_slab`
  - trapdoor block: `minecraft:oak_trapdoor`
  - small leg block: `minecraft:oak_log`
- ランダム block state 候補:
  - `minecraft:spruce_planks`
  - `minecraft:spruce_leaves`
  - `minecraft:oak_log`
  - `minecraft:cobblestone`
  - `minecraft:mossy_cobblestone`
- 元 mod の生成バイオーム:
  - `#minecraft:is_forest`
  - optional `#forge:is_forest`
  - optional `#c:forest`
  - optional `byg:red_oak_forest`
  - optional `byg:temperate_rainforest`
  - optional `byg:orchard`
  - optional `byg:autumnal_forest`
  - optional `byg:cherry_blossom_forest`
  - optional `biomesoplenty:cherry_blossom_grove`
  - optional `biomesoplenty:orchard`
  - optional `biomesoplenty:seasonal_forest`
  - optional `biomesoplenty:woodland`
  - optional `biomesoplenty:old_growth_woodland`
  - optional `magicalforest:magical_forest`
- loot: 共通の `minecraft:chests/abandoned_mineshaft`

### 11. red_desert

- 置換率: `0.6`
- leg variant: `edge`
- 装飾:
  - cactus chance: `0.1`
  - dead bush chance: `0.1`
  - gravel pile chance: `0.2`
- 固定 block state:
  - main block: `minecraft:red_sandstone`
  - support block: `minecraft:red_sandstone_wall`
  - slab block: `minecraft:red_sandstone_slab`
  - gravel block: `minecraft:red_sand`
  - stone wall block: `minecraft:red_sandstone_wall`
  - stone slab block: `minecraft:red_sandstone_slab`
  - trapdoor block: `minecraft:dark_oak_trapdoor`
  - small leg block: `minecraft:smooth_red_sandstone`
- ランダム block state 候補:
  - `minecraft:red_sandstone`
  - `minecraft:cut_red_sandstone`
  - `minecraft:chiseled_red_sandstone`
  - `minecraft:smooth_red_sandstone`
  - `minecraft:red_sand`
  - `minecraft:stone_bricks`
  - `minecraft:cracked_stone_bricks`
  - `minecraft:cave_air`
- 元 mod の生成バイオーム:
  - `#minecraft:is_badlands`
  - optional `#forge:is_badlands`
  - optional `#c:badlands`
- loot: 共通の `minecraft:chests/abandoned_mineshaft`

### 12. spruce

- 置換率: `0.6`
- leg variant: `edge`
- 装飾:
  - vine chance: `0.05`
  - gravel pile chance: `0.1`
- 固定 block state:
  - main block: `minecraft:spruce_planks`
  - support block: `minecraft:spruce_fence`
  - slab block: `minecraft:spruce_slab`
  - gravel block: `minecraft:gravel`
  - stone wall block: `minecraft:stone_brick_wall`
  - stone slab block: `minecraft:stone_brick_slab`
  - trapdoor block: `minecraft:spruce_trapdoor`
  - small leg block: `minecraft:stripped_spruce_log`
- ランダム block state 候補:
  - `minecraft:spruce_planks`
  - `minecraft:cobblestone`
  - `minecraft:stone_bricks`
  - `minecraft:mossy_stone_bricks`
  - `minecraft:cracked_stone_bricks`
  - `minecraft:cave_air`
- 元 mod の生成バイオーム:
  - `#minecraft:is_taiga`
  - optional `terralith:cloud_forest`
  - optional `terralith:forested_highlands`
  - optional `terralith:lavender_forest`
  - optional `terralith:lavender_valley`
  - optional `terralith:moonlight_grove`
  - optional `terralith:moonlight_valley`
  - optional `terralith:shrubland`
  - optional `biomesoplenty:jade_cliffs`
  - optional `biomesoplenty:mediterranean_taiga`
  - optional `biomesoplenty:dead_forest`
  - optional `biomesoplenty:old_growth_dead_forest`
  - optional `byg:autumnal_taiga`
  - optional `byg:canadian_shield`
  - optional `byg:maple_taiga`
  - optional `projectvibrantjourneys:boreal_forest`
  - optional `projectvibrantjourneys:crystal_lakes`
- loot: 共通の `minecraft:chests/abandoned_mineshaft`

### 13. spruce_snowy

- 置換率: `0.9`
- leg variant: `edge`
- 装飾:
  - snow chance: `1.0`
  - gravel pile chance: `0.1`
- 固定 block state:
  - main block: `minecraft:spruce_planks`
  - support block: `minecraft:spruce_fence`
  - slab block: `minecraft:spruce_slab`
  - gravel block: `minecraft:snow_block`
  - stone wall block: `minecraft:stone_brick_wall`
  - stone slab block: `minecraft:stone_brick_slab`
  - trapdoor block: `minecraft:spruce_trapdoor`
  - small leg block: `minecraft:stripped_spruce_log`
- ランダム block state 候補:
  - `minecraft:spruce_planks`
  - `minecraft:snow_block`
  - `minecraft:packed_ice`
  - `minecraft:cobblestone`
  - `minecraft:stone_bricks`
  - `minecraft:mossy_stone_bricks`
  - `minecraft:cracked_stone_bricks`
  - `minecraft:cave_air`
- 元 mod の生成バイオーム:
  - `minecraft:snowy_taiga`
  - `minecraft:snowy_plains`
  - `minecraft:snowy_slopes`
  - `minecraft:jagged_peaks`
  - optional `terralith:cold_shrubland`
  - optional `terralith:rocky_shrubland`
  - optional `terralith:wintry_forest`
- loot: 共通の `minecraft:chests/abandoned_mineshaft`
