# YUNG's Better TFC 仕様

このリポジトリは Minecraft 1.21.1 / NeoForge 向けの TerraFirmaCraft
互換 mod である。目的は、YUNG's Better Series の構造物を TFC の地形に
生成できるようにし、構造物内のバニラブロック、装備、戦利品を TFC 相当に
置換すること。

今後の変更では、このファイルを仕様として扱う。ここに書かれた互換挙動は、
ユーザーが明示的に変更を求めた場合を除いて維持する。

## ファイル名

- 仕様ファイル名は `AGENTS.md` とする。
- 小文字の `agents.md` は使わない。

## バージョンと依存関係

- Minecraft: `1.21.1`
- NeoForge: `21.1.219`
- Java: `21`
- mod id: `yungsbettertfc`
- 必須実行時 mod:
  - `tfc`
  - `yungsapi`
- 任意実行時 mod:
  - `beneath`
  - `betterdungeons`
  - `betterfortresses`
  - `bettermineshafts`
  - `betteroceanmonuments`
  - `betterstrongholds`
- 任意 YUNG 系 dependency は `optional` のままにする。
- `tfc` と `yungsapi` は `required` のままにする。
- `beneath` と YUNG 系 optional dependency は `ordering="AFTER"` のままにする。
- `build.gradle` の実装依存は NeoForge userdev のみでよい。TFC と YUNG 系 mod
  との実行時関係は `META-INF/neoforge.mods.toml` で表現する。

## 依存元実装の比較基準

YUNG 系 mod と比較する場合は、Minecraft 1.21.1 に合わせて以下の依存元を
基準にする。

- `YUNG-GANG/YUNGs-Better-Dungeons`, branch `1.21.1`
- `YUNG-GANG/YUNGs-Better-Strongholds`, branch `1.21.1`
- `YUNG-GANG/YUNGs-Better-Fortresses`, branch `1.21.1`
- `YUNG-GANG/YUNGs-Better-Mineshafts`, branch `1.21.1`
- `YUNG-GANG/YUNGs-Better-Ocean-Monuments`, branch `1.21.1`

`minecraft:` 名前空間の戦利品テーブル上書きは Minecraft バニラ `1.21.1` の
data を基準に比較する。

## 構造物プロセッサ注入仕様

- `yungsbettertfc:tfc_block_replacement` という構造物プロセッサ type を登録する。
- `StructureTemplateManager#getOrCreate` の戻り値に、読み込まれたテンプレート id を保存する。
- `StructureTemplate#placeInWorld` の先頭で、対象テンプレートに
  `TfcBlockReplacementProcessor.INSTANCE` を追加する。
- 対象テンプレート名前空間:
  - `betterstrongholds`
  - `betterdungeons`
  - `betteroceanmonuments`
  - `betterfortresses`
  - `beneath`
- バニラ名前空間は全体を対象にせず、`minecraft:end_city/*` のテンプレートだけを
  追加対象にする。
- プロセッサは構造物側の既存プロセッサの後に実行されるよう、末尾へ追加する。
- 同じ `StructurePlaceSettings` に同一プロセッサ instance を重複追加しない。

## 実行時ブロック置換の共通仕様

- 置換対象は `minecraft:` 名前空間のブロックだけ。
- air は即時スキップする。
- `infested_` で始まる path は、接頭辞を外して通常ブロックとして扱う。
- Overworld では全置換 scope を使う。
- Overworld 以外では utility-only scope を使う。
- ただし furnace/firepit 置換と ore 置換は、dimension に関係なく常に処理する。
- 既定値:
  - Overworld rock: `granite`
  - Nether rock: `basalt`
  - End rock: `granite`
  - soil: `mollisol`
  - wood: `oak`
- 全置換 scope では、cache origin から下方向へ最大 64 block 調べ、TFC rock/soil を検出する。
- rock、soil、wood hint はテンプレートでは配置 origin ごと、Better Mineshafts の
  `StructurePiece` 生成では piece bounding box の最小座標ごとに cache する。
- 置換先 block が同名 property と同じ値を持てる場合、置換元 block state の property を引き継ぐ。
- block entity NBT の `final_state` にバニラ ore block id がある場合、そこも TFC ore に置換する。
- `furnace` を `tfc:firepit` に置換する場合:
  - furnace/campfire 由来の block entity NBT は破棄する。
  - horizontal facing から firepit の axis を可能な範囲で設定する。
- `tall_seagrass` の upper half は `minecraft:water` に置換する。

## 実行時ブロック置換マップ

### 火と調理

- `minecraft:furnace` -> `tfc:firepit`
- `minecraft:blast_furnace` -> `tfc:firepit`

### 鉱石

候補が複数ある場合は、registry に存在する最初の TFC block を使う。

- `minecraft:coal_ore`, `minecraft:deepslate_coal_ore` ->
  `tfc:lignite`, fallback は `tfc:bituminous_coal`
- `minecraft:iron_ore`, `minecraft:deepslate_iron_ore` ->
  `tfc:ore/normal_hematite/<rock>`, fallback は `tfc:ore/normal_magnetite/<rock>`,
  さらに fallback は `tfc:ore/normal_limonite/<rock>`
- `minecraft:copper_ore`, `minecraft:deepslate_copper_ore` ->
  `tfc:ore/normal_native_copper/<rock>`
- `minecraft:gold_ore`, `minecraft:deepslate_gold_ore` ->
  `tfc:ore/normal_native_gold/<rock>`
- `minecraft:nether_gold_ore` ->
  `tfc:ore/normal_native_gold/<rock>`
- `minecraft:lapis_ore`, `minecraft:deepslate_lapis_ore` ->
  `tfc:ore/lapis_lazuli/<rock>`
- `minecraft:diamond_ore`, `minecraft:deepslate_diamond_ore` ->
  `tfc:ore/diamond/<rock>`
- `minecraft:emerald_ore`, `minecraft:deepslate_emerald_ore` ->
  `tfc:ore/emerald/<rock>`
- `minecraft:redstone_ore`, `minecraft:deepslate_redstone_ore` ->
  `tfc:ore/cinnabar/<rock>`
- `minecraft:nether_quartz_ore` -> `tfc:ore/quartz/<rock>`。ただし TFC block が存在する場合だけ。

### 石材と rock 種

`<rock>` は検出した TFC rock、検出できない場合は dimension 既定 rock。

- `stone_bricks` -> `tfc:rock/bricks/<rock>`
- `mossy_stone_bricks` -> `tfc:rock/mossy_bricks/<rock>`
- `cracked_stone_bricks` -> `tfc:rock/cracked_bricks/<rock>`
- `chiseled_stone_bricks` -> `tfc:rock/chiseled/<rock>`
- `stone_brick_stairs` -> `tfc:rock/bricks/<rock>_stairs`
- `stone_brick_slab` -> `tfc:rock/bricks/<rock>_slab`
- `stone_brick_wall` -> `tfc:rock/bricks/<rock>_wall`
- `mossy_stone_brick_stairs` -> `tfc:rock/mossy_bricks/<rock>_stairs`
- `mossy_stone_brick_slab` -> `tfc:rock/mossy_bricks/<rock>_slab`
- `mossy_stone_brick_wall` -> `tfc:rock/mossy_bricks/<rock>_wall`
- `cobblestone` -> `tfc:rock/cobble/<rock>`
- `mossy_cobblestone` -> `tfc:rock/mossy_cobble/<rock>`
- `cobblestone_stairs` -> `tfc:rock/cobble/<rock>_stairs`
- `cobblestone_slab` -> `tfc:rock/cobble/<rock>_slab`
- `cobblestone_wall` -> `tfc:rock/cobble/<rock>_wall`
- `mossy_cobblestone_stairs` -> `tfc:rock/mossy_cobble/<rock>_stairs`
- `mossy_cobblestone_slab` -> `tfc:rock/mossy_cobble/<rock>_slab`
- `mossy_cobblestone_wall` -> `tfc:rock/mossy_cobble/<rock>_wall`
- `stone` -> `tfc:rock/raw/<rock>`
- `stone_stairs` -> `tfc:rock/raw/<rock>_stairs`
- `stone_slab` -> `tfc:rock/raw/<rock>_slab`
- `smooth_stone` -> `tfc:rock/smooth/<rock>`
- `smooth_stone_slab` -> `tfc:rock/smooth/<rock>_slab`
- `gravel` -> `tfc:rock/gravel/<rock>`
- `andesite` -> `tfc:rock/raw/<rock>`
- `andesite_stairs` -> `tfc:rock/raw/<rock>_stairs`
- `andesite_slab` -> `tfc:rock/raw/<rock>_slab`
- `andesite_wall` -> `tfc:rock/raw/<rock>_wall`
- `polished_andesite` -> `tfc:rock/smooth/<rock>`
- `polished_andesite_stairs` -> `tfc:rock/smooth/<rock>_stairs`
- `polished_andesite_slab` -> `tfc:rock/smooth/<rock>_slab`
- `stone_button` -> `tfc:rock/button/<rock>`
- `stone_pressure_plate` -> `tfc:rock/pressure_plate/<rock>`

### 砂岩

- `sandstone` -> `tfc:raw_sandstone/yellow`
- `sandstone_stairs` -> `tfc:raw_sandstone/yellow_stairs`
- `sandstone_slab` -> `tfc:raw_sandstone/yellow_slab`
- `sandstone_wall` -> `tfc:raw_sandstone/yellow_wall`
- `chiseled_sandstone`, `cut_sandstone` -> `tfc:cut_sandstone/yellow`
- `cut_sandstone_slab` -> `tfc:cut_sandstone/yellow_slab`
- `smooth_sandstone` -> `tfc:smooth_sandstone/yellow`
- `smooth_sandstone_stairs` -> `tfc:smooth_sandstone/yellow_stairs`
- `smooth_sandstone_slab` -> `tfc:smooth_sandstone/yellow_slab`
- `red_sandstone` -> `tfc:raw_sandstone/red`
- `red_sandstone_stairs` -> `tfc:raw_sandstone/red_stairs`
- `red_sandstone_slab` -> `tfc:raw_sandstone/red_slab`
- `red_sandstone_wall` -> `tfc:raw_sandstone/red_wall`
- `chiseled_red_sandstone`, `cut_red_sandstone` -> `tfc:cut_sandstone/red`
- `cut_red_sandstone_slab` -> `tfc:cut_sandstone/red_slab`
- `smooth_red_sandstone` -> `tfc:smooth_sandstone/red`
- `smooth_red_sandstone_stairs` -> `tfc:smooth_sandstone/red_stairs`
- `smooth_red_sandstone_slab` -> `tfc:smooth_sandstone/red_slab`

### 土壌

`<soil>` は検出した TFC soil、検出できない場合は `mollisol`。

- `dirt` -> `tfc:dirt/<soil>`
- `coarse_dirt` -> `tfc:coarse_dirt/<soil>`
- `grass_block` -> `tfc:grass/<soil>`
- `grass_path` -> `tfc:grass_path/<soil>`
- `rooted_dirt` -> `tfc:rooted_dirt/<soil>`
- `farmland` -> `tfc:farmland/<soil>`
- `sand` -> `tfc:sand/yellow`
- `red_sand` -> `tfc:sand/red`

### 木材

バニラ wood hint として扱う値:

- `oak`
- `spruce`
- `birch`
- `jungle`
- `acacia`
- `dark_oak`
- `mangrove`
- `cherry`
- `bamboo`

TFC に存在しない wood は以下へ normalize する。

- `dark_oak` -> `oak`
- `jungle` -> `acacia`
- `cherry` -> `oak`
- `bamboo` -> `oak`
- `crimson` -> `oak`
- `warped` -> `oak`

木材置換:

- `chest` -> `tfc:wood/chest/<wood>`
- `trapped_chest` -> `tfc:wood/trapped_chest/<wood>`
- `lectern` -> `tfc:wood/lectern/<wood>`
- `crafting_table` -> `tfc:wood/workbench/<wood>`
- `<wood>_planks` -> `tfc:wood/planks/<wood>`
- `<wood>_stairs` -> `tfc:wood/planks/<wood>_stairs`
- `<wood>_slab` -> `tfc:wood/planks/<wood>_slab`
- `stripped_<wood>_log` -> `tfc:wood/stripped_log/<wood>`
- `stripped_<wood>_wood` -> `tfc:wood/stripped_wood/<wood>`
- `<wood>_log` -> `tfc:wood/log/<wood>`
- `<wood>_wood` -> `tfc:wood/wood/<wood>`
- `<wood>_fence_gate` -> `tfc:wood/fence_gate/<wood>`
- `<wood>_fence` -> `tfc:wood/fence/<wood>`
- `<wood>_door` -> `tfc:wood/door/<wood>`
- `<wood>_trapdoor` -> `tfc:wood/trapdoor/<wood>`
- `<wood>_pressure_plate` -> `tfc:wood/pressure_plate/<wood>`
- `<wood>_button` -> `tfc:wood/button/<wood>`
- `<wood>_wall_sign` -> `tfc:wood/wall_sign/<wood>`
- `<wood>_sign` -> `tfc:wood/sign/<wood>`

utility-only scope では、木材系は以下だけ置換する。

- `chest`
- `trapped_chest`
- `lectern`
- `crafting_table`

### 金属ブロック

- `iron_bars` -> `tfc:metal/bars/wrought_iron`
- `chain` -> `tfc:metal/chain/wrought_iron`
- `iron_block` -> `tfc:metal/block/wrought_iron`
- `iron_trapdoor` -> `tfc:metal/trapdoor/wrought_iron`
- `gold_block`, `raw_gold_block` -> `tfc:metal/block/gold`
- `copper_block`, `cut_copper` -> `tfc:metal/block/copper`
- `cut_copper_slab` -> `tfc:metal/block/copper_slab`
- `cut_copper_stairs` -> `tfc:metal/block/copper_stairs`
- `exposed_copper`, `exposed_cut_copper` -> `tfc:metal/exposed_block/copper`
- `exposed_cut_copper_slab` -> `tfc:metal/exposed_block/copper_slab`
- `exposed_cut_copper_stairs` -> `tfc:metal/exposed_block/copper_stairs`
- `weathered_copper`, `weathered_cut_copper` -> `tfc:metal/weathered_block/copper`
- `weathered_cut_copper_slab` -> `tfc:metal/weathered_block/copper_slab`
- `weathered_cut_copper_stairs` -> `tfc:metal/weathered_block/copper_stairs`
- `oxidized_copper`, `oxidized_cut_copper`, `waxed_oxidized_cut_copper` ->
  `tfc:metal/oxidized_block/copper`
- `oxidized_cut_copper_slab`, `waxed_oxidized_cut_copper_slab` ->
  `tfc:metal/oxidized_block/copper_slab`
- `oxidized_cut_copper_stairs`, `waxed_oxidized_cut_copper_stairs` ->
  `tfc:metal/oxidized_block/copper_stairs`

anvil 系置換は意図的に無効化されている。

### 植物、装飾、容器、灯り

- `kelp`, `kelp_plant` -> `minecraft:water`
- `seagrass`, `tall_seagrass` -> `tfc:plant/eel_grass`
- `tall_seagrass` upper half -> `minecraft:water`
- `sea_pickle` -> `tfc:sea_pickle`
- `vine` -> `tfc:plant/ivy`
- `cactus` の最下段 -> `tfc:plant/silken_pincushion_cactus`
- `cactus` のうち、下方向に空気だけを挟んで `minecraft:cactus` または
  `tfc:plant/silken_pincushion_cactus` がある上段 -> `minecraft:air`
- `dead_bush` -> `tfc:plant/dead_bush`
- `potted_<plant>` -> `tfc:plant/potted/<plant>`。ただし TFC block が存在する場合だけ。
- `candle` -> `tfc:candle`
- `<color>_candle` -> `tfc:candle/<color>`。ただし TFC block が存在する場合だけ。
- `candle_cake` -> `tfc:candle_cake`
- `<color>_candle_cake` -> `tfc:candle_cake/<color>`。ただし TFC block が存在する場合だけ。
- `cauldron`, `water_cauldron`, `lava_cauldron`, `powder_snow_cauldron` ->
  `tfc:ceramic/large_vessel`
- `torch` -> `tfc:torch`
- `wall_torch` -> `tfc:wall_torch`

### Beneath Nether 連携

Nether かつ Beneath の対象 block が registry に存在する場合だけ置換する。

- `crimson_planks` -> `beneath:wood/planks/crimson`
- `crimson_slab` -> `beneath:wood/planks/crimson_slab`
- `crimson_stairs` -> `beneath:wood/planks/crimson_stairs`
- `crimson_door` -> `beneath:wood/door/crimson`
- `crimson_trapdoor` -> `beneath:wood/trapdoor/crimson`
- `crimson_button` -> `beneath:wood/button/crimson`
- `crimson_pressure_plate` -> `beneath:wood/pressure_plate/crimson`
- `crimson_fence` -> `beneath:wood/fence/crimson`
- `crimson_fence_gate` -> `beneath:wood/fence_gate/crimson`
- `crimson_stem` -> `beneath:wood/log/crimson`
- `crimson_hyphae` -> `beneath:wood/wood/crimson`
- `stripped_crimson_stem` -> `beneath:wood/stripped_log/crimson`
- `stripped_crimson_hyphae` -> `beneath:wood/stripped_wood/crimson`
- `warped_planks` -> `beneath:wood/planks/warped`
- `warped_slab` -> `beneath:wood/planks/warped_slab`
- `warped_stairs` -> `beneath:wood/planks/warped_stairs`
- `warped_door` -> `beneath:wood/door/warped`
- `warped_trapdoor` -> `beneath:wood/trapdoor/warped`
- `warped_button` -> `beneath:wood/button/warped`
- `warped_pressure_plate` -> `beneath:wood/pressure_plate/warped`
- `warped_fence` -> `beneath:wood/fence/warped`
- `warped_fence_gate` -> `beneath:wood/fence_gate/warped`
- `warped_stem` -> `beneath:wood/log/warped`
- `warped_hyphae` -> `beneath:wood/wood/warped`
- `stripped_warped_stem` -> `beneath:wood/stripped_log/warped`
- `stripped_warped_hyphae` -> `beneath:wood/stripped_wood/warped`
- `nether_gold_ore` -> `beneath:ore/normal_nether_gold`

## エンティティ装備置換

- `minecraft:` entity だけを処理する。
- `item_frame` と `glow_item_frame` は `Item` stack を置換する。
- `armor_stand` は `ArmorItems` と `HandItems` の stack を置換する。
- `betterstrongholds` 名前空間のテンプレートは `black_steel` を使う。
- それ以外のテンプレートは `wrought_iron` を使う。
- item id 置換:
  - `*_sword` -> `tfc:metal/sword/<metal>`
  - `*_axe` -> `tfc:metal/axe/<metal>`
  - `*_pickaxe` -> `tfc:metal/pickaxe/<metal>`
  - `*_shovel` -> `tfc:metal/shovel/<metal>`
  - `*_hoe` -> `tfc:metal/hoe/<metal>`
  - `*_helmet` -> `tfc:metal/helmet/<metal>`
  - `*_chestplate` -> `tfc:metal/chestplate/<metal>`
  - `*_leggings` -> `tfc:metal/greaves/<metal>`
  - `*_boots` -> `tfc:metal/boots/<metal>`
  - `shield` -> `tfc:metal/shield/<metal>`
  - `bow`, `crossbow`, `trident` -> `tfc:metal/javelin/<metal>`
  - `mace` -> `tfc:metal/mace/<metal>`
- stack id 置換後は、元 stack の `components`, `tag`, `Damage`, `damage` を削除する。

## ワールド生成差分

YUNG 側の `worldgen/structure/*.json` は `biomes` で
`#<mod>:has_structure/...` を参照する。この mod は同じ tag path を追加提供し、
TFC biome tag を足す。全て `replace:false` なので、依存元のバニラ/forge/c tag は
消さずに追加する。

### Better Dungeons

以下の依存元 tag に `#yungsbettertfc:tfc_land_biomes` と
`#yungsbettertfc:tfc_coastal_biomes` を追加する。

- `data/betterdungeons/tags/worldgen/biome/has_structure/skeleton_dungeon.json`
- `data/betterdungeons/tags/worldgen/biome/has_structure/small_dungeon.json`
- `data/betterdungeons/tags/worldgen/biome/has_structure/spider_dungeon.json`
- `data/betterdungeons/tags/worldgen/biome/has_structure/zombie_dungeon.json`

`small_nether_dungeon` は上書きしない。依存元通り Nether 構造物のままにする。

Spider Dungeon は template pool / NBT ではなく
`com.yungnickyoung.minecraft.betterdungeons.world.structure.spider_dungeon.piece.`
配下の Java `StructurePiece` 実装で主な洞窟形状を生成する。`SpiderDungeonNestPiece`,
`SpiderDungeonSmallTunnelPiece`, `SpiderDungeonBigTunnelPiece`, `SpiderDungeonEggRoomPiece`
はいずれも `Blocks.COBBLESTONE` などを vanilla `StructurePiece#placeBlock` 経由で配置するため、
Better Mineshafts と同じ `WorldGenLevel#setBlock` redirect で
`TfcBlockReplacementProcessor` の共通ブロック置換を適用する。

### Better Strongholds

- `data/betterstrongholds/tags/worldgen/biome/has_structure/better_stronghold.json`
  に `#yungsbettertfc:tfc_land_biomes` と
  `#yungsbettertfc:tfc_coastal_biomes` を追加する。

### Better Ocean Monuments

- `data/betteroceanmonuments/tags/worldgen/biome/has_structure/better_ocean_monument.json`
  に `#yungsbettertfc:tfc_deep_ocean_biomes` を追加する。

### Better Mineshafts

TFC Overworld へ生成させる variant は以下の 6 種だけにする。

- `oak`
- `desert`
- `red_desert`
- `mesa`
- `ice`
- `spruce_snowy`

`overgrown` は現時点では採用しない。`acacia`, `dripstone`, `jungle`, `lush`,
`mushroom`, `spruce`, `overgrown` の TFC biome tag override は追加しない。

以下の依存元 tag に、それぞれ対応する `yungsbettertfc` 側の TFC 専用 biome tag を
追加する。全て `replace:false` とし、依存元の vanilla/forge/c tag は消さない。

- `data/bettermineshafts/tags/worldgen/biome/has_structure/better_mineshaft_oak.json`
  に `#yungsbettertfc:tfc_mineshaft_oak_biomes` を追加する。
- `data/bettermineshafts/tags/worldgen/biome/has_structure/better_mineshaft_desert.json`
  に `#yungsbettertfc:tfc_mineshaft_desert_biomes` を追加する。
- `data/bettermineshafts/tags/worldgen/biome/has_structure/better_mineshaft_red_desert.json`
  に `#yungsbettertfc:tfc_mineshaft_red_desert_biomes` を追加する。
- `data/bettermineshafts/tags/worldgen/biome/has_structure/better_mineshaft_mesa.json`
  に `#yungsbettertfc:tfc_mineshaft_mesa_biomes` を追加する。
- `data/bettermineshafts/tags/worldgen/biome/has_structure/better_mineshaft_ice.json`
  に `#yungsbettertfc:tfc_mineshaft_ice_biomes` を追加する。
- `data/bettermineshafts/tags/worldgen/biome/has_structure/better_mineshaft_spruce_snowy.json`
  に `#yungsbettertfc:tfc_mineshaft_spruce_snowy_biomes` を追加する。

Better Mineshafts は template pool / NBT ではなく Java の `StructurePiece` 実装で
主なブロックを生成するため、`StructureTemplateMixin` の processor 注入だけでは
ブロック置換が効かない。Better Mineshafts の各 piece は木材、石材、作業台などの
大半を vanilla `StructurePiece#placeBlock` 経由で配置するため、このメソッドの
`WorldGenLevel#setBlock` 呼び出しを mixin で redirect する。実行時の piece class 名が
`com.yungnickyoung.minecraft.bettermineshafts.world.generator.pieces.` で始まる場合だけ、
既存の `TfcBlockReplacementProcessor` と同じブロック置換を適用する。

Better Mineshafts の dungeon chest は vanilla `StructurePiece#createChest` 経由で
配置されるため、この chest 設置も同じ条件で redirect する。TFC chest block entity は
vanilla `ChestBlockEntity` を継承するため、依存元の loot table 設定は維持される。

依存元 `BetterMineshaftPiece` では、空洞/溶岩上の脚生成だけ
`StructurePiece#placeBlock` を経由せず、`generateLegOrChain`,
`generatePillarDownOrChainUp`, `fillColumnBetween` から直接 `WorldGenLevel#setBlock`
する。この直接配置も `@Pseudo` mixin で redirect し、支柱 log/planks と chain に
同じ置換を適用する。

依存元 `OreDeposit` piece は構造 JSON の block state ではなく、Java enum の
`Blocks.COAL_ORE`, `Blocks.IRON_ORE`, `Blocks.REDSTONE_ORE`, `Blocks.GOLD_ORE`,
`Blocks.LAPIS_ORE`, `Blocks.EMERALD_ORE`, `Blocks.DIAMOND_ORE` を
`chanceReplaceSolid` で配置する。この配置は `StructurePiece#placeBlock` 経由なので、
Better Mineshafts の piece class 条件により既存の ore 置換 map を適用する。TFC の ore
block id は `tfc:ore/<ore>/<rock>` 形式なので、検出 rock を suffix に含める。

Better Mineshafts 専用のブロック置換マップは追加しない。必要な置換は共通の
`TfcBlockReplacementProcessor` に追加し、`StructureTemplateMixin` 経由の構造物にも
同じ挙動を適用する。`barrel`, `rail`, `lantern`, `bed`, `anvil`, `smithing_table`
など、既存マップにないブロックはこの段階では変換しない。

Better Mineshafts の chest minecart、barrel、dungeon chest は全て vanilla
`minecraft:chests/abandoned_mineshaft` を参照する。`bettermineshafts:` 名前空間の
専用 loot table は依存元に存在しないため追加しない。loot 置換は
`data/minecraft/loot_table/chests/abandoned_mineshaft.json` の上書きで行い、既存の
overworld dungeon 互換と同じ方針が明確な item だけを shared loot table へ置換する。

`structure_set` 上書きは行わない。

### Better Fortresses

- biome tag override は存在しない。依存元通り Nether 構造物のままにする。

## TFC biome tag 内容

### `yungsbettertfc:tfc_mineshaft_oak_biomes`

- `tfc:active_shield_volcano`
- `tfc:ancient_shield_volcano`
- `tfc:burren_plains`
- `tfc:burren_roche_moutonee`
- `tfc:cenote_canyons`
- `tfc:cenote_highlands`
- `tfc:cenote_hills`
- `tfc:cenote_plains`
- `tfc:cenote_plateau`
- `tfc:cenote_rolling_hills`
- `tfc:doline_canyons`
- `tfc:doline_highlands`
- `tfc:doline_hills`
- `tfc:doline_plains`
- `tfc:doline_plateau`
- `tfc:doline_rolling_hills`
- `tfc:dormant_shield_volcano`
- `tfc:drumlins`
- `tfc:extinct_shield_volcano`
- `tfc:extreme_doline_mountains`
- `tfc:extreme_doline_plateau`
- `tfc:guano_island`
- `tfc:highlands`
- `tfc:hills`
- `tfc:inverted_patterned_ground`
- `tfc:knob_and_kettle`
- `tfc:lowlands`
- `tfc:mountains`
- `tfc:oceanic_mountains`
- `tfc:old_mountains`
- `tfc:patterned_ground`
- `tfc:plains`
- `tfc:plateau`
- `tfc:plateau_wide`
- `tfc:rolling_hills`
- `tfc:salt_marsh`
- `tfc:shilin_canyons`
- `tfc:shilin_highlands`
- `tfc:shilin_hills`
- `tfc:shilin_plains`
- `tfc:shilin_plateau`
- `tfc:stone_circles`
- `tfc:sunken_shield_volcano`
- `tfc:tower_karst_bay`
- `tfc:tower_karst_canyons`
- `tfc:tower_karst_highlands`
- `tfc:tower_karst_hills`
- `tfc:tower_karst_plains`
- `tfc:volcanic_mountains`
- `tfc:volcanic_oceanic_mountains`
- `tfc:lake`
- `tfc:mountain_lake`
- `tfc:old_mountain_lake`
- `tfc:oceanic_mountain_lake`
- `tfc:plateau_lake`
- `tfc:river`
- `tfc:tower_karst_lake`
- `tfc:volcanic_mountain_lake`
- `tfc:volcanic_oceanic_mountain_lake`
- `tfc:shore`
- `tfc:rocky_shores`
- `tfc:setback_cliffs`
- `tfc:terrace_upper`
- `tfc:terrace_lower`
- `tfc:embayments`
- `tfc:tidal_flats`
- `tfc:sea_stacks`
- `tfc:shield_volcano_shore`
- `tfc:old_shield_volcano_shore`

### `yungsbettertfc:tfc_mineshaft_desert_biomes`

- `tfc:dune_sea`
- `tfc:grassy_dunes`
- `tfc:salt_flats`
- `tfc:mud_flats`
- `tfc:coastal_dunes`

### `yungsbettertfc:tfc_mineshaft_red_desert_biomes`

- `tfc:badlands`
- `tfc:burren_badlands`
- `tfc:burren_badlands_tall`
- `tfc:canyons`
- `tfc:low_canyons`
- `tfc:stair_step_canyons`
- `tfc:whorled_canyons`

### `yungsbettertfc:tfc_mineshaft_mesa_biomes`

- `tfc:mesas`
- `tfc:buttes`
- `tfc:hoodoos`
- `tfc:rocky_plateau`
- `tfc:burren_plateau`

### `yungsbettertfc:tfc_mineshaft_ice_biomes`

- `#tfc:is_ice_sheet`

### `yungsbettertfc:tfc_mineshaft_spruce_snowy_biomes`

- `#tfc:is_glaciated`
- `tfc:glacially_carved_mountains`
- `tfc:glacially_carved_oceanic_mountains`
- `tfc:tuyas`
- `tfc:meltwater_lake`

### `yungsbettertfc:tfc_coastal_biomes`

- `tfc:shore`
- `tfc:rocky_shores`
- `tfc:coastal_dunes`
- `tfc:setback_cliffs`
- `tfc:terrace_upper`
- `tfc:terrace_lower`
- `tfc:embayments`
- `tfc:tidal_flats`
- `tfc:sea_stacks`
- `tfc:shield_volcano_shore`
- `tfc:old_shield_volcano_shore`
- `tfc:ice_sheet_shore`

### `yungsbettertfc:tfc_deep_ocean_biomes`

- `tfc:deep_ocean`
- `tfc:deep_ocean_trench`
- `tfc:ice_sheet_oceanic`
- `tfc:ocean`
- `tfc:ocean_reef`

### `yungsbettertfc:tfc_land_biomes`

- `tfc:active_shield_volcano`
- `tfc:ancient_shield_volcano`
- `tfc:badlands`
- `tfc:burren_badlands`
- `tfc:burren_badlands_tall`
- `tfc:burren_plains`
- `tfc:burren_plateau`
- `tfc:burren_roche_moutonee`
- `tfc:buttes`
- `tfc:canyons`
- `tfc:cenote_canyons`
- `tfc:cenote_highlands`
- `tfc:cenote_hills`
- `tfc:cenote_plains`
- `tfc:cenote_plateau`
- `tfc:cenote_rolling_hills`
- `tfc:doline_canyons`
- `tfc:doline_highlands`
- `tfc:doline_hills`
- `tfc:doline_plains`
- `tfc:doline_plateau`
- `tfc:doline_rolling_hills`
- `tfc:dormant_shield_volcano`
- `tfc:drumlins`
- `tfc:dune_sea`
- `tfc:extinct_shield_volcano`
- `tfc:extreme_doline_mountains`
- `tfc:extreme_doline_plateau`
- `tfc:glacially_carved_mountains`
- `tfc:glacially_carved_oceanic_mountains`
- `tfc:glaciated_mountains`
- `tfc:glaciated_oceanic_mountains`
- `tfc:glaciated_shield_volcano`
- `tfc:grassy_dunes`
- `tfc:guano_island`
- `tfc:highlands`
- `tfc:hills`
- `tfc:hoodoos`
- `tfc:ice_sheet`
- `tfc:ice_sheet_edge`
- `tfc:ice_sheet_mountains`
- `tfc:ice_sheet_mountains_edge`
- `tfc:ice_sheet_oceanic_mountains`
- `tfc:ice_sheet_oceanic_mountains_edge`
- `tfc:ice_sheet_shield_volcano`
- `tfc:ice_sheet_tuyas`
- `tfc:ice_sheet_tuyas_edge`
- `tfc:inverted_patterned_ground`
- `tfc:knob_and_kettle`
- `tfc:low_canyons`
- `tfc:lowlands`
- `tfc:mesas`
- `tfc:mountains`
- `tfc:mud_flats`
- `tfc:oceanic_mountains`
- `tfc:old_mountains`
- `tfc:patterned_ground`
- `tfc:plains`
- `tfc:plateau`
- `tfc:plateau_wide`
- `tfc:rocky_plateau`
- `tfc:rolling_hills`
- `tfc:salt_flats`
- `tfc:salt_marsh`
- `tfc:shilin_canyons`
- `tfc:shilin_highlands`
- `tfc:shilin_hills`
- `tfc:shilin_plains`
- `tfc:shilin_plateau`
- `tfc:stair_step_canyons`
- `tfc:stone_circles`
- `tfc:sunken_shield_volcano`
- `tfc:tower_karst_bay`
- `tfc:tower_karst_canyons`
- `tfc:tower_karst_highlands`
- `tfc:tower_karst_hills`
- `tfc:tower_karst_plains`
- `tfc:tuyas`
- `tfc:volcanic_mountains`
- `tfc:volcanic_oceanic_mountains`
- `tfc:whorled_canyons`
- `tfc:lake`
- `tfc:meltwater_lake`
- `tfc:mountain_lake`
- `tfc:old_mountain_lake`
- `tfc:oceanic_mountain_lake`
- `tfc:plateau_lake`
- `tfc:river`
- `tfc:subglacial_lake`
- `tfc:tower_karst_lake`
- `tfc:volcanic_mountain_lake`
- `tfc:volcanic_oceanic_mountain_lake`

## 戦利品仕様

戦利品テーブル上書きはファイル単位で依存元/バニラの同名 table を置き換える。
この節では、依存元との差分として「削除した参照」と「追加した参照」を全件列挙する。
`xN` は同じ参照が N 回存在することを表す。

保持されるバニラ参照は、この節で削除として記載されていない限り維持する。
例: 本、地図、鞍、music disc、redstone、potion、string、bone、rotten flesh、
nether wart、trim template など。

### End City 戦利品差分

End City の `minecraft:end_city/*` テンプレートには共通ブロック置換を適用する。
End dimension の utility-only scope により、テンプレート内の `minecraft:chest` は
既定 wood の `tfc:wood/chest/oak` へ置換する。`EndCityPieces#handleDataMarker` は
配置後の chest block entity に `minecraft:chests/end_city_treasure` を設定するため、
TFC chest でもこの節の戦利品テーブルを維持する。

#### `data/minecraft/loot_table/chests/end_city_treasure.json`

- 元の pool 1 の rolls `2～6`、全 entry の weight、set_count の個数範囲を維持する。
- 元の pool 2 と `spire_armor_trim_smithing_template` の出現率 `1/15` を維持する。
- 置換後の装備には、元 entry と同じ `minecraft:enchant_with_levels` を適用する。
  level は一様分布 `20～39`、options は `#minecraft:on_random_loot` とする。
- 同じ shared table に置換される同条件 entry は weight を合算してよい。
  装備14 entry は各 weight 3 なので、`equipment_end_city` 1 entry の weight 42 とする。
- 削除:
  - `item:minecraft:diamond`
  - `item:minecraft:iron_ingot`
  - `item:minecraft:gold_ingot`
  - `item:minecraft:emerald`
  - `item:minecraft:beetroot_seeds`
  - `item:minecraft:iron_horse_armor`
  - `item:minecraft:golden_horse_armor`
  - `item:minecraft:diamond_horse_armor`
  - `item:minecraft:diamond_sword`
  - `item:minecraft:diamond_boots`
  - `item:minecraft:diamond_chestplate`
  - `item:minecraft:diamond_leggings`
  - `item:minecraft:diamond_helmet`
  - `item:minecraft:diamond_pickaxe`
  - `item:minecraft:diamond_shovel`
  - `item:minecraft:iron_sword`
  - `item:minecraft:iron_boots`
  - `item:minecraft:iron_chestplate`
  - `item:minecraft:iron_leggings`
  - `item:minecraft:iron_helmet`
  - `item:minecraft:iron_pickaxe`
  - `item:minecraft:iron_shovel`
- 追加:
  - `loot_table:yungsbettertfc:shared/gemsx2`
  - `loot_table:yungsbettertfc:shared/metals_end_cityx2`
  - `loot_table:yungsbettertfc:shared/seeds`
  - `loot_table:yungsbettertfc:shared/horse_armor_end_city`
    （元の3 entry分を合算した weight 3）
  - `loot_table:yungsbettertfc:shared/equipment_end_city`
    （元の14 entry分を合算した weight 42）

### Better Dungeons 戦利品差分

#### `data/betterdungeons/loot_table/skeleton_dungeon/chests/common.json`

- 削除:
  - `item:minecraft:bow`
  - `item:minecraft:iron_ingot`
  - `item:minecraft:gold_ingot`
  - `item:minecraft:bone_meal`
- 追加:
  - `loot_table:yungsbettertfc:shared/ranged_weapon`
  - `loot_table:yungsbettertfc:shared/metals_overworldx2`
  - `loot_table:yungsbettertfc:shared/fertilizers`

#### `data/betterdungeons/loot_table/skeleton_dungeon/chests/middle.json`

- 削除:
  - `item:minecraft:coal`
  - `item:minecraft:diamond`
- 追加:
  - `loot_table:yungsbettertfc:shared/coal_like`
  - `loot_table:yungsbettertfc:shared/gems`

#### `data/betterdungeons/loot_table/small_dungeon/chests/loot_piles.json`

- 依存元と完全一致。
- 参照差分なし。

#### `data/betterdungeons/loot_table/small_nether_dungeon/chests/common.json`

- 削除:
  - `item:minecraft:coalx2`
  - `item:minecraft:iron_ingot`
  - `item:minecraft:gold_ingotx2`
  - `item:minecraft:gold_nugget`
  - `item:minecraft:golden_horse_armor`
  - `item:minecraft:golden_sword`
  - `item:minecraft:golden_boots`
  - `item:minecraft:golden_chestplate`
  - `item:minecraft:golden_leggings`
  - `item:minecraft:golden_helmet`
  - `item:minecraft:iron_sword`
  - `item:minecraft:chainmail_boots`
  - `item:minecraft:chainmail_chestplate`
  - `item:minecraft:chainmail_leggings`
  - `item:minecraft:chainmail_helmet`
- 追加:
  - `loot_table:yungsbettertfc:shared/coal_likex2`
  - `loot_table:yungsbettertfc:shared/metals_small_netherx4`
  - `loot_table:yungsbettertfc:shared/horse_armor_small_nether`
  - `loot_table:yungsbettertfc:shared/equipment_small_netherx10`

#### `data/betterdungeons/loot_table/spider_dungeon/chests/egg_room.json`

- 削除:
  - `item:minecraft:diamond`
  - `item:minecraft:coal`
  - `item:minecraft:beetroot_seeds`
  - `item:minecraft:pumpkin_seeds`
  - `item:minecraft:melon_seeds`
- 追加:
  - `loot_table:yungsbettertfc:shared/gems`
  - `loot_table:yungsbettertfc:shared/coal_like`
  - `loot_table:yungsbettertfc:shared/seedsx3`

#### `data/betterdungeons/loot_table/zombie_dungeon/chests/common.json`

- 削除:
  - `item:minecraft:stone_sword`
  - `item:minecraft:stone_axe`
  - `item:minecraft:stone_shovel`
  - `item:minecraft:iron_sword`
  - `item:minecraft:iron_axe`
  - `item:minecraft:iron_shovel`
  - `item:minecraft:iron_helmet`
  - `item:minecraft:iron_chestplate`
  - `item:minecraft:iron_leggings`
  - `item:minecraft:iron_boots`
  - `item:minecraft:iron_ingot`
  - `item:minecraft:gold_ingot`
  - `item:minecraft:diamond_sword`
  - `item:minecraft:diamond_axe`
  - `item:minecraft:diamond_shovel`
  - `item:minecraft:apple`
  - `item:minecraft:coal`
  - `item:minecraft:beetroot_seeds`
  - `item:minecraft:wheat_seeds`
  - `item:minecraft:carrot`
  - `item:minecraft:potato`
- 追加:
  - `loot_table:yungsbettertfc:shared/equipment_overworldx13`
  - `loot_table:yungsbettertfc:shared/metals_overworldx2`
  - `loot_table:yungsbettertfc:shared/producex3`
  - `loot_table:yungsbettertfc:shared/coal_like`
  - `loot_table:yungsbettertfc:shared/seedsx2`

#### `data/betterdungeons/loot_table/zombie_dungeon/chests/special.json`

- 削除:
  - `item:minecraft:stone_sword`
  - `item:minecraft:stone_axe`
  - `item:minecraft:stone_shovel`
  - `item:minecraft:iron_sword`
  - `item:minecraft:iron_axe`
  - `item:minecraft:iron_shovel`
  - `item:minecraft:iron_helmet`
  - `item:minecraft:iron_chestplate`
  - `item:minecraft:iron_leggings`
  - `item:minecraft:iron_boots`
  - `item:minecraft:iron_ingot`
  - `item:minecraft:gold_ingot`
  - `item:minecraft:diamond_sword`
  - `item:minecraft:diamond_axe`
  - `item:minecraft:diamond_shovel`
  - `item:minecraft:apple`
  - `item:minecraft:coal`
  - `item:minecraft:beetroot_seeds`
  - `item:minecraft:wheat_seeds`
  - `item:minecraft:carrot`
  - `item:minecraft:potato`
- 追加:
  - `loot_table:yungsbettertfc:shared/equipment_overworldx13`
  - `loot_table:yungsbettertfc:shared/metals_overworldx2`
  - `loot_table:yungsbettertfc:shared/producex3`
  - `loot_table:yungsbettertfc:shared/coal_like`
  - `loot_table:yungsbettertfc:shared/seedsx2`

#### `data/betterdungeons/loot_table/zombie_dungeon/chests/tombstone.json`

- 削除:
  - `item:minecraft:bone_meal`
  - `item:minecraft:emerald`
  - `item:minecraft:diamond`
  - `item:minecraft:diamond_sword`
- 追加:
  - `loot_table:yungsbettertfc:shared/fertilizers`
  - `loot_table:yungsbettertfc:shared/gemsx2`
  - `loot_table:yungsbettertfc:shared/equipment_overworld`

### Better Fortresses 戦利品差分

#### `data/betterfortresses/loot_table/chests/beacon.json`

- 削除:
  - `item:minecraft:bowx3`
- 追加:
  - `loot_table:yungsbettertfc:shared/ranged_weaponx3`

#### `data/betterfortresses/loot_table/chests/extra.json`

- 削除:
  - `item:minecraft:iron_nugget`
  - `item:minecraft:gold_nugget`
  - `item:minecraft:iron_ingot`
  - `item:minecraft:gold_ingot`
- 追加:
  - `loot_table:yungsbettertfc:shared/metals_nether_fortressx4`

#### `data/betterfortresses/loot_table/chests/hall.json`

- 削除:
  - `item:minecraft:iron_nugget`
  - `item:minecraft:gold_nugget`
  - `item:minecraft:iron_ingot`
  - `item:minecraft:gold_ingot`
- 追加:
  - `loot_table:yungsbettertfc:shared/metals_nether_fortressx4`

#### `data/betterfortresses/loot_table/chests/keep.json`

- 削除:
  - `item:minecraft:coal`
  - `item:minecraft:iron_horse_armor`
  - `item:minecraft:golden_horse_armor`
  - `item:minecraft:diamond_horse_armor`
  - `item:minecraft:stone_swordx2`
  - `item:minecraft:iron_swordx2`
  - `item:minecraft:golden_swordx2`
  - `item:minecraft:leather_helmetx2`
  - `item:minecraft:chainmail_helmetx2`
  - `item:minecraft:golden_helmetx2`
  - `item:minecraft:leather_chestplatex2`
  - `item:minecraft:chainmail_chestplatex2`
  - `item:minecraft:golden_chestplatex2`
  - `item:minecraft:leather_leggingsx2`
  - `item:minecraft:chainmail_leggingsx2`
  - `item:minecraft:golden_leggingsx2`
  - `item:minecraft:leather_bootsx2`
  - `item:minecraft:chainmail_bootsx2`
  - `item:minecraft:golden_bootsx2`
- 追加:
  - `loot_table:yungsbettertfc:shared/coal_like`
  - `loot_table:yungsbettertfc:shared/horse_armor_nether_fortressx3`
  - `loot_table:yungsbettertfc:shared/equipment_nether_fortressx30`

#### `data/betterfortresses/loot_table/chests/obsidian.json`

- 削除:
  - `item:minecraft:diamond`
- 追加:
  - `loot_table:yungsbettertfc:shared/gems`

#### `data/betterfortresses/loot_table/chests/puzzle.json`

- 削除:
  - `item:minecraft:iron_nugget`
  - `item:minecraft:gold_nugget`
  - `item:minecraft:iron_ingot`
  - `item:minecraft:gold_ingot`
  - `item:minecraft:diamond`
- 追加:
  - `loot_table:yungsbettertfc:shared/metals_nether_fortressx4`
  - `loot_table:yungsbettertfc:shared/gems`

#### `data/betterfortresses/loot_table/chests/quarters.json`

- 削除:
  - `item:minecraft:iron_nugget`
  - `item:minecraft:gold_nugget`
  - `item:minecraft:iron_ingot`
  - `item:minecraft:gold_ingot`
  - `item:minecraft:diamond`
- 追加:
  - `loot_table:yungsbettertfc:shared/metals_nether_fortressx4`
  - `loot_table:yungsbettertfc:shared/gems`

#### `data/betterfortresses/loot_table/chests/storage.json`

- 削除:
  - `item:minecraft:iron_nugget`
  - `item:minecraft:gold_nugget`
  - `item:minecraft:gold_ingot`
  - `item:minecraft:diamond`
- 追加:
  - `loot_table:yungsbettertfc:shared/metals_nether_fortressx3`
  - `loot_table:yungsbettertfc:shared/gems`

#### `data/betterfortresses/loot_table/chests/worship.json`

- 削除:
  - `item:minecraft:iron_nugget`
  - `item:minecraft:gold_nugget`
  - `item:minecraft:iron_ingot`
  - `item:minecraft:gold_ingot`
  - `item:minecraft:diamond`
- 追加:
  - `loot_table:yungsbettertfc:shared/metals_nether_fortressx4`
  - `loot_table:yungsbettertfc:shared/gems`

### Better Ocean Monuments 戦利品差分

#### `data/betteroceanmonuments/loot_table/chests/upper_side_chamber.json`

- 依存元と完全一致。
- 参照差分なし。

### Better Strongholds 戦利品差分

#### `data/betterstrongholds/loot_table/chests/armoury.json`

- 削除:
  - `item:minecraft:wooden_swordx2`
  - `item:minecraft:iron_swordx2`
  - `item:minecraft:diamond_swordx2`
  - `item:minecraft:leather_helmet`
  - `item:minecraft:leather_chestplate`
  - `item:minecraft:leather_leggings`
  - `item:minecraft:leather_boots`
  - `item:minecraft:chainmail_helmet`
  - `item:minecraft:chainmail_chestplate`
  - `item:minecraft:chainmail_leggings`
  - `item:minecraft:chainmail_boots`
  - `item:minecraft:iron_helmetx2`
  - `item:minecraft:iron_chestplatex2`
  - `item:minecraft:iron_leggingsx2`
  - `item:minecraft:iron_bootsx2`
  - `item:minecraft:diamond_helmetx2`
  - `item:minecraft:diamond_chestplatex2`
  - `item:minecraft:diamond_leggingsx2`
  - `item:minecraft:diamond_bootsx2`
  - `item:minecraft:shield`
  - `item:minecraft:bowx2`
  - `item:minecraft:coal`
- 追加:
  - `loot_table:yungsbettertfc:shared/equipment_strongholdx31`
  - `loot_table:yungsbettertfc:shared/ranged_weaponx2`
  - `loot_table:yungsbettertfc:shared/coal_like`

#### `data/betterstrongholds/loot_table/chests/cmd_yung.json`

- 削除:
  - `item:minecraft:diamond_sword`
- 追加:
  - `loot_table:yungsbettertfc:shared/equipment_stronghold`

#### `data/betterstrongholds/loot_table/chests/common.json`

- 削除:
  - `item:minecraft:iron_ingot`
  - `item:minecraft:gold_ingot`
  - `item:minecraft:coal`
  - `item:minecraft:bread`
  - `item:minecraft:potato`
  - `item:minecraft:apple`
  - `item:minecraft:iron_pickaxe`
  - `item:minecraft:wooden_pickaxe`
  - `item:minecraft:iron_horse_armor`
  - `item:minecraft:golden_horse_armor`
  - `item:minecraft:diamond_horse_armor`
- 追加:
  - `loot_table:yungsbettertfc:shared/metals_strongholdx2`
  - `loot_table:yungsbettertfc:shared/coal_like`
  - `loot_table:yungsbettertfc:shared/producex3`
  - `loot_table:yungsbettertfc:shared/equipment_strongholdx2`
  - `loot_table:yungsbettertfc:shared/horse_armor_strongholdx3`

#### `data/betterstrongholds/loot_table/chests/crypt.json`

- 削除:
  - `item:minecraft:bone_meal`
  - `item:minecraft:diamond`
  - `item:minecraft:iron_sword`
- 追加:
  - `loot_table:yungsbettertfc:shared/fertilizers`
  - `loot_table:yungsbettertfc:shared/gems`
  - `loot_table:yungsbettertfc:shared/equipment_stronghold`

#### `data/betterstrongholds/loot_table/chests/grand_library.json`

- 依存元と完全一致。
- 参照差分なし。

#### `data/betterstrongholds/loot_table/chests/library_md.json`

- 依存元と完全一致。
- 参照差分なし。

#### `data/betterstrongholds/loot_table/chests/mess.json`

- 削除:
  - `item:minecraft:bread`
  - `item:minecraft:apple`
  - `item:minecraft:potato`
  - `item:minecraft:beetroot`
  - `item:minecraft:melon_slice`
- 追加:
  - `loot_table:yungsbettertfc:shared/producex5`

#### `data/betterstrongholds/loot_table/chests/prison_lg.json`

- 削除:
  - `item:minecraft:coal`
  - `item:minecraft:diamond`
  - `item:minecraft:emerald`
- 追加:
  - `loot_table:yungsbettertfc:shared/coal_like`
  - `loot_table:yungsbettertfc:shared/gemsx2`

#### `data/betterstrongholds/loot_table/chests/trap.json`

- 削除:
  - `item:minecraft:iron_ingot`
  - `item:minecraft:gold_ingot`
  - `item:minecraft:diamond`
  - `item:minecraft:emerald`
- 追加:
  - `loot_table:yungsbettertfc:shared/metals_strongholdx2`
  - `loot_table:yungsbettertfc:shared/gemsx2`

#### `data/betterstrongholds/loot_table/chests/treasure.json`

- 削除:
  - `item:minecraft:iron_ingot`
  - `item:minecraft:iron_nugget`
  - `item:minecraft:gold_ingot`
  - `item:minecraft:gold_nugget`
  - `item:minecraft:diamond`
  - `item:minecraft:emerald`
  - `item:minecraft:lapis_lazuli`
- 追加:
  - `loot_table:yungsbettertfc:shared/metals_strongholdx4`
  - `loot_table:yungsbettertfc:shared/gemsx3`

### バニラ Minecraft 戦利品差分

#### `data/minecraft/loot_table/chests/abandoned_mineshaft.json`

Better Mineshafts の全 loot コンテナもこの vanilla table を参照する。

- 削除:
  - `item:minecraft:iron_pickaxe`
  - `item:minecraft:iron_ingot`
  - `item:minecraft:gold_ingot`
  - `item:minecraft:lapis_lazuli`
  - `item:minecraft:diamond`
  - `item:minecraft:coal`
  - `item:minecraft:bread`
  - `item:minecraft:glow_berries`
  - `item:minecraft:melon_seeds`
  - `item:minecraft:pumpkin_seeds`
  - `item:minecraft:beetroot_seeds`
- 追加:
  - `item:tfc:metal/pickaxe/wrought_iron`
  - `loot_table:yungsbettertfc:shared/metals_overworldx2`
  - `loot_table:yungsbettertfc:shared/gemsx2`
  - `loot_table:yungsbettertfc:shared/coal_like`
  - `loot_table:yungsbettertfc:shared/producex2`
  - `loot_table:yungsbettertfc:shared/seedsx3`
- 方針保留で未置換:
  - `item:minecraft:rail`
  - `item:minecraft:powered_rail`
  - `item:minecraft:detector_rail`
  - `item:minecraft:activator_rail`

#### `data/minecraft/loot_table/chests/nether_bridge.json`

- 削除:
  - `item:minecraft:diamond`
  - `item:minecraft:iron_ingot`
  - `item:minecraft:gold_ingot`
  - `item:minecraft:golden_sword`
  - `item:minecraft:golden_chestplate`
  - `item:minecraft:golden_horse_armor`
  - `item:minecraft:iron_horse_armor`
  - `item:minecraft:diamond_horse_armor`
- 追加:
  - `loot_table:yungsbettertfc:shared/gems`
  - `loot_table:yungsbettertfc:shared/metals_nether_fortressx2`
  - `loot_table:yungsbettertfc:shared/equipment_nether_fortressx2`
  - `loot_table:yungsbettertfc:shared/horse_armor_nether_fortressx3`

#### `data/minecraft/loot_table/chests/simple_dungeon.json`

- 削除:
  - `item:minecraft:golden_horse_armor`
  - `item:minecraft:iron_horse_armor`
  - `item:minecraft:diamond_horse_armor`
  - `item:minecraft:iron_ingot`
  - `item:minecraft:gold_ingot`
  - `item:minecraft:bread`
  - `item:minecraft:wheat`
  - `item:minecraft:coal`
  - `item:minecraft:melon_seeds`
  - `item:minecraft:pumpkin_seeds`
  - `item:minecraft:beetroot_seeds`
- 追加:
  - `loot_table:yungsbettertfc:shared/horse_armor_overworldx3`
  - `loot_table:yungsbettertfc:shared/metals_overworldx2`
  - `loot_table:yungsbettertfc:shared/producex2`
  - `loot_table:yungsbettertfc:shared/coal_like`
  - `loot_table:yungsbettertfc:shared/seedsx3`

#### `data/minecraft/loot_table/chests/stronghold_corridor.json`

- 削除:
  - `item:minecraft:diamond`
  - `item:minecraft:iron_ingot`
  - `item:minecraft:gold_ingot`
  - `item:minecraft:bread`
  - `item:minecraft:apple`
  - `item:minecraft:iron_pickaxe`
  - `item:minecraft:iron_sword`
  - `item:minecraft:iron_chestplate`
  - `item:minecraft:iron_helmet`
  - `item:minecraft:iron_leggings`
  - `item:minecraft:iron_boots`
  - `item:minecraft:iron_horse_armor`
  - `item:minecraft:golden_horse_armor`
  - `item:minecraft:diamond_horse_armor`
- 追加:
  - `loot_table:yungsbettertfc:shared/gems`
  - `loot_table:yungsbettertfc:shared/metals_strongholdx2`
  - `loot_table:yungsbettertfc:shared/producex2`
  - `loot_table:yungsbettertfc:shared/equipment_strongholdx6`
  - `loot_table:yungsbettertfc:shared/horse_armor_strongholdx3`

#### `data/minecraft/loot_table/chests/stronghold_crossing.json`

- 削除:
  - `item:minecraft:iron_ingot`
  - `item:minecraft:gold_ingot`
  - `item:minecraft:coal`
  - `item:minecraft:bread`
  - `item:minecraft:apple`
  - `item:minecraft:iron_pickaxe`
- 追加:
  - `loot_table:yungsbettertfc:shared/metals_strongholdx2`
  - `loot_table:yungsbettertfc:shared/coal_like`
  - `loot_table:yungsbettertfc:shared/producex2`
  - `loot_table:yungsbettertfc:shared/equipment_stronghold`

#### `data/minecraft/loot_table/chests/stronghold_library.json`

- バニラと完全一致。
- 参照差分なし。

## 新規 shared 戦利品テーブル

### `data/yungsbettertfc/loot_table/shared/coal_like.json`

- `item:minecraft:coal`
- `item:tfc:powder/graphite`
- `item:tfc:kaolin_clay`

### `data/yungsbettertfc/loot_table/shared/ranged_weapon.json`

- `item:minecraft:crossbow`
- `item:minecraft:bow`

### `data/yungsbettertfc/loot_table/shared/gems.json`

- `tag:yungsbettertfc:loot/gems`

### `data/yungsbettertfc/loot_table/shared/fertilizers.json`

- `tag:yungsbettertfc:loot/fertilizers`

### `data/yungsbettertfc/loot_table/shared/produce.json`

- `tag:yungsbettertfc:loot/produce`

### `data/yungsbettertfc/loot_table/shared/seeds.json`

- `tag:yungsbettertfc:loot/seeds`

### `data/yungsbettertfc/loot_table/shared/equipment_overworld.json`

- `tag:yungsbettertfc:loot/equipment/overworld_rare`
- `tag:yungsbettertfc:loot/equipment/overworld_common`

### `data/yungsbettertfc/loot_table/shared/equipment_small_nether.json`

- `tag:yungsbettertfc:loot/equipment/small_nether`

### `data/yungsbettertfc/loot_table/shared/equipment_nether_fortress.json`

- `tag:yungsbettertfc:loot/equipment/nether_fortress_rare`
- `tag:yungsbettertfc:loot/equipment/nether_fortress_common`

### `data/yungsbettertfc/loot_table/shared/equipment_stronghold.json`

- `tag:yungsbettertfc:loot/equipment/stronghold`

### `data/yungsbettertfc/loot_table/shared/equipment_end_city.json`

- `tag:yungsbettertfc:loot/equipment/end_city`

### `data/yungsbettertfc/loot_table/shared/horse_armor_overworld.json`

- `tag:yungsbettertfc:loot/horse_armor/overworld_rare`
- `tag:yungsbettertfc:loot/horse_armor/overworld_common`

### `data/yungsbettertfc/loot_table/shared/horse_armor_small_nether.json`

- `tag:yungsbettertfc:loot/horse_armor/small_nether`

### `data/yungsbettertfc/loot_table/shared/horse_armor_nether_fortress.json`

- `tag:yungsbettertfc:loot/horse_armor/nether_fortress_rare`
- `tag:yungsbettertfc:loot/horse_armor/nether_fortress_common`

### `data/yungsbettertfc/loot_table/shared/horse_armor_stronghold.json`

- `tag:yungsbettertfc:loot/horse_armor/stronghold`

### `data/yungsbettertfc/loot_table/shared/horse_armor_end_city.json`

- `tag:yungsbettertfc:loot/horse_armor/end_city`

### `data/yungsbettertfc/loot_table/shared/metals_overworld.json`

- `tag:yungsbettertfc:loot/metals_sheet/overworld_rare`
- `tag:yungsbettertfc:loot/metals_rod/overworld_rare`
- `tag:yungsbettertfc:loot/metals_ingot/overworld_rare`
- `tag:yungsbettertfc:loot/metals_sheet/overworld_common`
- `tag:yungsbettertfc:loot/metals_rod/overworld_common`
- `tag:yungsbettertfc:loot/metals_ingot/overworld_common`

### `data/yungsbettertfc/loot_table/shared/metals_small_nether.json`

- `tag:yungsbettertfc:loot/metals_sheet/small_nether`
- `tag:yungsbettertfc:loot/metals_rod/small_nether`
- `tag:yungsbettertfc:loot/metals_ingot/small_nether`

### `data/yungsbettertfc/loot_table/shared/metals_nether_fortress.json`

- `tag:yungsbettertfc:loot/metals_sheet/nether_fortress_rare`
- `tag:yungsbettertfc:loot/metals_rod/nether_fortress_rare`
- `tag:yungsbettertfc:loot/metals_ingot/nether_fortress_rare`
- `tag:yungsbettertfc:loot/metals_sheet/nether_fortress_common`
- `tag:yungsbettertfc:loot/metals_rod/nether_fortress_common`
- `tag:yungsbettertfc:loot/metals_ingot/nether_fortress_common`

### `data/yungsbettertfc/loot_table/shared/metals_stronghold.json`

- `tag:yungsbettertfc:loot/metals_sheet/stronghold`
- `tag:yungsbettertfc:loot/metals_rod/stronghold`
- `tag:yungsbettertfc:loot/metals_ingot/stronghold`

### `data/yungsbettertfc/loot_table/shared/metals_end_city.json`

- `tag:yungsbettertfc:loot/metals_sheet/end_city`
- `tag:yungsbettertfc:loot/metals_rod/end_city`
- `tag:yungsbettertfc:loot/metals_ingot/end_city`

## 戦利品 item tag 内容

### 金属 item tag の段階

`metals_ingot`, `metals_rod`, `metals_sheet` は、suffix だけが違い、material
集合は同じ。

- `overworld_common`:
  - `copper`
  - `bronze`
  - `bismuth_bronze`
  - `wrought_iron`
  - `bismuth`
  - `tin`
  - `zinc`
  - `brass`
- `overworld_rare`:
  - `black_bronze`
  - `steel`
- `small_nether`:
  - `wrought_iron`
  - `steel`
  - `gold`
  - `silver`
  - `nickel`
- `nether_fortress_common`:
  - `wrought_iron`
  - `steel`
  - `gold`
  - `silver`
  - `nickel`
- `nether_fortress_rare`:
  - `black_steel`
- `stronghold`:
  - `steel`
  - `black_steel`
- `end_city`:
  - `black_steel`
  - `red_steel`
  - `blue_steel`

実際の item id は以下の形にする。

- ingot: `tfc:metal/ingot/<material>`
- rod: `tfc:metal/rod/<material>`
- sheet: `tfc:metal/sheet/<material>`

### 装備 item tag の段階

各 material について、以下の equipment id を全て含める。

- `sword`
- `mace`
- `javelin`
- `axe`
- `shovel`
- `pickaxe`
- `hoe`
- `knife`
- `scythe`
- `propick`
- `chisel`
- `hammer`
- `saw`
- `shears`
- `helmet`
- `chestplate`
- `greaves`
- `boots`
- `shield`

material 集合:

- `overworld_common`: `bronze`, `bismuth_bronze`, `wrought_iron`
- `overworld_rare`: `black_bronze`, `steel`
- `small_nether`: `wrought_iron`, `steel`
- `nether_fortress_common`: `wrought_iron`, `steel`
- `nether_fortress_rare`: `black_steel`
- `stronghold`: `steel`, `black_steel`
- `end_city`: `black_steel`, `red_steel`, `blue_steel`

実際の item id は `tfc:metal/<equipment>/<material>` の形にする。

### 馬鎧 item tag

- `overworld_common`:
  - `tfc:metal/horse_armor/bronze`
  - `tfc:metal/horse_armor/bismuth_bronze`
  - `tfc:metal/horse_armor/wrought_iron`
- `overworld_rare`:
  - `tfc:metal/horse_armor/black_bronze`
  - `tfc:metal/horse_armor/steel`
- `small_nether`:
  - `tfc:metal/horse_armor/wrought_iron`
  - `tfc:metal/horse_armor/steel`
- `nether_fortress_common`:
  - `tfc:metal/horse_armor/wrought_iron`
  - `tfc:metal/horse_armor/steel`
- `nether_fortress_rare`:
  - `tfc:metal/horse_armor/black_steel`
- `stronghold`:
  - `tfc:metal/horse_armor/steel`
  - `tfc:metal/horse_armor/black_steel`
- `end_city`:
  - `tfc:metal/horse_armor/black_steel`
  - `tfc:metal/horse_armor/red_steel`
  - `tfc:metal/horse_armor/blue_steel`

### 宝石

- `tfc:gem/amethyst`
- `tfc:gem/diamond`
- `tfc:gem/emerald`
- `tfc:gem/lapis_lazuli`
- `tfc:gem/opal`
- `tfc:gem/pyrite`
- `tfc:gem/ruby`
- `tfc:gem/sapphire`
- `tfc:gem/topaz`

### 肥料

- `tfc:compost`
- `tfc:rotten_compost`
- `tfc:powder/wood_ash`
- `tfc:powder/saltpeter`
- `tfc:powder/sylvite`
- `tfc:groundcover/guano`

### 農作物と食料

- `tfc:food/blackberry`
- `tfc:food/blueberry`
- `tfc:food/bunchberry`
- `tfc:food/cranberry`
- `tfc:food/elderberry`
- `tfc:food/gooseberry`
- `tfc:food/cloudberry`
- `tfc:food/raspberry`
- `tfc:food/snowberry`
- `tfc:food/strawberry`
- `tfc:food/wintergreen_berry`
- `tfc:food/red_apple`
- `tfc:food/green_apple`
- `tfc:food/plum`
- `tfc:food/beet`
- `tfc:food/cabbage`
- `tfc:food/carrot`
- `tfc:food/cassava`
- `tfc:food/garlic`
- `tfc:food/green_bean`
- `tfc:food/lentil`
- `tfc:food/maize`
- `tfc:food/melon_slice`
- `tfc:food/oat`
- `tfc:food/onion`
- `tfc:food/peanut`
- `tfc:food/potato`
- `tfc:food/pumpkin_chunks`
- `tfc:food/rice`
- `tfc:food/rye`
- `tfc:food/soybean`
- `tfc:food/squash`
- `tfc:food/sugarcane`
- `tfc:food/taro_root`
- `tfc:food/tomato`
- `tfc:food/wheat`
- `tfc:food/barley`
- `tfc:food/red_bell_pepper`
- `tfc:food/yellow_bell_pepper`

### 種

- `tfc:seeds/alfalfa`
- `tfc:seeds/barley`
- `tfc:seeds/beet`
- `tfc:seeds/cabbage`
- `tfc:seeds/canola`
- `tfc:seeds/carrot`
- `tfc:seeds/cassava`
- `tfc:seeds/garlic`
- `tfc:seeds/green_bean`
- `tfc:seeds/jute`
- `tfc:seeds/lentil`
- `tfc:seeds/maize`
- `tfc:seeds/melon`
- `tfc:seeds/oat`
- `tfc:seeds/onion`
- `tfc:seeds/papyrus`
- `tfc:seeds/peanut`
- `tfc:seeds/potato`
- `tfc:seeds/pumpkin`
- `tfc:seeds/radish`
- `tfc:seeds/red_bell_pepper`
- `tfc:seeds/rice`
- `tfc:seeds/rye`
- `tfc:seeds/squash`
- `tfc:seeds/soybean`
- `tfc:seeds/sugarcane`
- `tfc:seeds/tomato`
- `tfc:seeds/wheat`
- `tfc:seeds/yellow_bell_pepper`
