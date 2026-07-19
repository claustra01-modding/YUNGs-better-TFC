# YUNG's Better TFC 仕様

このリポジトリは Minecraft 1.21.1 / NeoForge 向けの TerraFirmaCraft
互換 mod である。目的は、YUNG's Better Series の構造物を TFC の地形に
生成できるようにし、構造物内のバニラブロック、装備、戦利品を TFC 相当に
置換すること。

今後の変更では、このファイルを仕様として扱う。ここに書かれた互換挙動は、
ユーザーが明示的に変更を求めた場合を除いて維持する。

## 共通開発ルール

- 仕様ファイル名は `AGENTS.md` とする。
- 小文字の `agents.md` は使わない。
- 本書は作業規約と実装仕様を兼ねる。正確な数値、ID、条件、fallback、例外、優先順位は残し、同一規則の全registry entry転記は共通式へ畳む。
- READMEは利用者向けの短い概要、配布先、build入口に絞り、詳細仕様を重複掲載しない。
- 挙動、対応版、依存、対象構造物、置換規則、worldgen、loot、検証手順を変更した場合は同じ変更で本書も更新する。
- 対象版の実JAR・公式ソースで確認し、公開済みID、client/server境界、optional依存なしのclass loadingを守る。
- 依存JAR、展開物、解析・生成scriptは `.tmp/` に置いてGit管理外にする。仕様と生成済みresourceを正本とし、JSONはBOMなしUTF-8とする。
- 無関係な差分、依存・version更新、format変更を混ぜない。

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
- フルブロックの `tfc:rock/raw/<rock>`, `tfc:rock/cobble/<rock>`,
  `tfc:rock/mossy_cobble/<rock>` は、配置座標の真下が air の場合だけ
  `tfc:rock/hardened/<rock>` に置換する。全対象構造物のテンプレート配置と
  Java `StructurePiece` 直接配置の両方へ適用する。stairs、slab、wall は対象外とする。
- block entity NBT の `final_state` にバニラ ore block id がある場合、そこも TFC ore に置換する。
- `furnace` を `tfc:firepit` に置換する場合:
  - furnace/campfire 由来の block entity NBT は破棄する。
  - horizontal facing から firepit の axis を可能な範囲で設定する。
- `tall_seagrass` の upper half は `minecraft:water` に置換する。

## 実行時ブロック置換マップ

具体的なregistry entryの正本は `TfcBlockReplacementProcessor` とする。変更時は以下の変換規則、fallback順、scopeを同時に保つ。

### 設備・鉱石

- `furnace`、`smoker`、`blast_furnace`、`campfire`、`soul_campfire` はTFC firepitへ置換し、互換性のないblock entity NBTを破棄する。
- Vanilla oreはTFC鉱石候補を優先順で解決し、配置地点のrock種を使う。対象gradeがないgem・coal系は非品位鉱石を使う。
- Deepslate oreも同じTFC oreへ統合し、Vanillaのstone/deepslate差をTFC側へ持ち込まない。
- ore候補がregistryに存在しない場合は次候補へ進み、全候補がない場合は元blockを維持する。

### 岩石・砂岩・土壌

`<rock>` は周辺から検出したTFC rock、未検出時は既定rock。各Vanilla形状を次のTFC familyへ対応させる。

| Vanilla family | TFC family |
| --- | --- |
| stone / stone bricks | raw / bricks |
| cobblestone | cobble |
| polished stone | smooth |
| chiseled stone | chiseled |
| cracked / mossy bricks | cracked_bricks / mossy_bricks |
| slab / stairs / wall / button / pressure plate | 同じfamilyの対応形状 |
| stonecutter | `tfc:rock/loose/<rock>` |

- Andesite、diorite、granite、deepslate、blackstone、tuff等も、構造物内では検出rockの同等familyへ統合する。
- Yellow/Red sandstoneは色を維持し、raw/cut/smoothと各slab/stairs/wallへ対応させる。
- `<soil>` は検出したTFC soil、未検出時は `mollisol`。dirt、coarse dirt、grass、grass path、rooted dirt、farmlandは同soilのTFC blockへ置換する。
- sandはyellow、red sandはredのTFC sandへ置換する。

### 木材

`<wood>` はtemplate内のVanilla wood hintをTFC woodへ正規化した値とする。

- 直接対応: oak、spruce、birch、acacia、mangrove。
- `dark_oak`、`cherry`、`bamboo`、`crimson`、`warped` はoakへ、`jungle` はacaciaへ正規化する。
- log/wood/stripped系、planks、slab、stairs、fence、fence gate、door、trapdoor、button、pressure plate、signは同じTFC wood familyへ置換する。
- chest、trapped chest、lectern、crafting tableはそれぞれTFC chest、trapped chest、lectern、workbenchへ置換する。
- utility-only scopeでは木材建材を置換せず、chest、trapped chest、lectern、crafting tableだけを対象にする。
- utility-only scopeではcoal blockも `tfc:bituminous_coal` へ置換する。

### 金属・装飾・容器・灯り

- iron bars、chain、iron trapdoor等の鉄製構造物部品はTFC wrought iron相当へ置換する。
- flower pot、植木、grass、fern、vine等は、TFCに明確な相当品があるものだけ置換する。植物の設置stateとNBTを壊さない。
- torch、wall torch、lantern、candleはTFC相当品へ置換し、wall/facing等の共有propertyを引き継ぐ。
- barrel、cauldron、composter等はTFC設備に1対1互換がある場合だけ置換し、block entity NBT互換がない場合は破棄する。
- 対応先が存在しない装飾blockはVanillaのまま維持し、推測で近似blockへ置換しない。

### Beneath連携

- NetherかつBeneathの対象registry entryが存在する場合だけ、Netherrack、Nether brick、soul soil系、fungus wood、ore、utility blockをBeneath/TFC相当へ置換する。
- Beneath未導入時はBeneath classを参照せず、registry lookup失敗を元block維持へfallbackする。
- Better FortressesとBeneath templateではutility-only scopeを基本とし、Nether固有地形をOverworld rock/soilへ変換しない。

## エンティティ装備置換

- `minecraft:` entity だけを処理する。
- `item_frame` と `glow_item_frame` は `Item` stack を置換する。
- `armor_stand` は `ArmorItems` と `HandItems` の stack を置換する。
- 対象テンプレートの名前空間にかかわらず `wrought_iron` を使う。
  Better Strongholdsも例外にしない。
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
`small_nether_dungeon` の prop NBT に含まれる `minecraft:coal_block` は、
utility-only scope の共通置換で `tfc:bituminous_coal` に置換する。

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

## TFC biome tag仕様

biomeの実値は `src/main/resources/data/yungsbettertfc/tags/worldgen/biome` を正本とする。ここでは選定規則とtag間制約を仕様とし、同じbiome IDを全件転記しない。

| Tag | 選定規則 |
| --- | --- |
| `tfc_mineshaft_oak_biomes` | 温帯の森林・平地・低地。特殊砂漠、海洋、極寒、高山を除外 |
| `tfc_mineshaft_desert_biomes` | yellow sand主体の乾燥地形 |
| `tfc_mineshaft_red_desert_biomes` | red sand主体の乾燥地形 |
| `tfc_mineshaft_mesa_biomes` | badlands/mesa相当の地形 |
| `tfc_mineshaft_ice_biomes` | 氷河・極寒地形 |
| `tfc_mineshaft_spruce_snowy_biomes` | 積雪森林・寒冷山地 |
| `tfc_coastal_biomes` | 海岸・沿岸遷移地形 |
| `tfc_deep_ocean_biomes` | 深海地形だけ |
| `tfc_land_biomes` | YUNG陸上構造物を許可するTFC陸地。ocean、deep ocean、shore専用地形を除外 |

- Mineshaft variant tagは重複を避け、1 biomeが複数variantへ同時分類されないようにする。
- coastalとdeep oceanを混同しない。Ocean Monumentはdeep ocean、沿岸構造物はcoastalを使う。
- TFC biome IDは気候そのものではなく地形分類である。温度・降水条件が必要な場合はbiome名の推測ではなくTFC climate placementを使う。
- TFC側でbiomeが追加・改名された場合は、全tagの包含、重複、未分類を機械的に監査する。
- tag JSONは `replace: false` を維持し、他data packの追加を不必要に消さない。

## 戦利品仕様

戦利品置換は [TFC互換loot table 共通再設計仕様](https://gist.github.com/claustra01/0b96699ab853bc17da8384426c6ffe5b)
を正本とする。依存元JARおよびMinecraft 1.21.1の同名loot tableから
上書きJSONと本節の変換仕様を正本とする。ローカル再生成にはGit管理外の
`.tmp/scripts/regenerate_loot_tables.py` を使用できるが、既存の上書きJSONを入力にしてはならない。

### 必ず保持する元仕様

- pool数、pool順、`rolls`、`bonus_rolls`
- entry数、entry順、`weight`、`quality`
- `conditions` とcount provider
- 元の `set_count` の範囲および個数
- エンチャント、damage、nameなど、完成品に適用可能な元function
- YUNG系mod固有itemおよび置換対象外のバニラitem
- 元itemのカテゴリ、装備slot、tool family、資源形態
- 同条件entryを合算せず、元entryを一対一で残す

### 構造物profile

- `ordinary`: abandoned mineshaft、simple dungeon、Better Dungeonsの通常dungeon
- `dangerous`: small nether dungeon、Better Fortresses、Better Strongholds、
  vanilla nether bridge
- `lategame`: End City
- Better Ocean Monumentsは、該当する置換対象がない限り依存元をそのまま保持する。

### 金属tier

- `ordinary` generic ingot: copper、bronze、bismuth bronze、black bronze、wrought iron
- `ordinary` equipment: copper、bronze、bismuth bronze、black bronze
- `dangerous` generic ingot: wrought iron、steel
- `dangerous` equipment: wrought iron
- `lategame` generic ingot: steel、black steel
- `lategame` equipment: steel
- red steelとblue steelはgeneric lootに含めない。
- black steelは`lategame`のingot候補だけに含め、部品、装備、horse armorには使わない。

### 資源カテゴリ

- diamond、emerald、lapis lazuli、amethyst shardは
  `yungsbettertfc:shared/gems`へ置換する。
- iron ingotとgold ingotはprofile別の
  `yungsbettertfc:shared/ingots/<profile>`へ置換する。
- iron nuggetは`yungsbettertfc:shared/small_ores/iron`へ置換し、hematite、magnetite、
  limoniteのsmall oreから選ぶ。
- gold nuggetとraw goldは`tfc:ore/small_native_gold`へ置換する。
- nuggetをingotへ、ingotをrodやsheetへ変えてはならない。
- generic ingot候補にrodやsheetを混在させてはならない。

### coal_like

`yungsbettertfc:shared/coal_like`は次の4候補だけを含む。

- `minecraft:charcoal`
- `tfc:ore/bituminous_coal`
- `tfc:ore/lignite`
- `tfc:ore/graphite`

minecraft coalとcharcoalをこのtableへ置換する。全候補はblock itemではなく通常itemとする。`tfc:powder/graphite`は使用しない。
graphiteは`coal_like`以外のshared tableへ入れない。

### utility

obsidian、crying obsidian、quartz、glowstone dustは
`yungsbettertfc:shared/utility`へ置換する。候補は次の7種類とする。

- `tfc:powder/flux`
- `minecraft:glass`
- `minecraft:glass_pane`
- `tfc:kaolin_clay`
- `tfc:powder/wood_ash`
- `tfc:powder/saltpeter`
- `tfc:powder/sylvite`

utilityにはcoal、charcoal、lignite、bituminous coal、graphiteを含めない。
utility用の新規poolは追加せず、依存元のgeneric material/resource entryを置換する。

### 食料、種、肥料、torch

- apple、bread、carrot、potato、glow berries、wheat、beetroot、melon sliceは
  `yungsbettertfc:shared/produce`へ置換する。
- beetroot seeds、melon seeds、pumpkin seeds、wheat seedsは
  `yungsbettertfc:shared/seeds`へ置換する。
- bone mealは`yungsbettertfc:shared/fertilizers`へ置換する。
- `minecraft:torch`は`tfc:torch`へ置換する。

### 装備family

元装備のfamilyとarmor slotを維持し、次の候補だけを使用する。

- pickaxe -> pickaxe head、propick head、pickaxe、propick
- axe -> axe head、saw blade、axe、saw
- hoe -> hoe head、scythe blade、hoe、scythe
- sword -> sword blade、javelin head、mace head、sword、javelin、mace
- shovel -> shovel head、shovel
- knife -> knife blade、knife
- shears -> shears
- shield -> shield
- bow -> vanilla bow
- crossbow -> vanilla crossbow
- helmet -> unfinished helmet、helmet
- chestplate -> unfinished chestplate、chestplate
- leggings -> unfinished greaves、greaves
- boots -> unfinished boots、boots
- horse armor -> profileの完成済みhorse armor

metal toolおよびarmorは、各部品候補のweightを2、各完成品候補のweightを1とし、
部品:完成品の合計weightを2:1にする。未完成品が存在しないshears、shield、horse armor、
bow、crossbowは完成品だけを候補にする。

### function適用

- `set_count`は元entry側に一度だけ残し、元のcount providerを変更しない。
- 元lootに含まれる`minecraft:set_damage`は削除し、置換後itemへ適用しない。
- `minecraft:set_name`は削除せず元entry側に保持する。このための個別shared tableは作成しない。
- `enchant_with_levels`と`enchant_randomly`は元entry側に保持する。TFC 4.2.5の
  金属部品とunfinished armorはenchantabilityを持たないため、生成結果は完成品だけが
  enchantされる。
- Better Strongholdsの`chests/cmd_yung`にある元のdiamond swordは特例とする。
  shared equipment tableを参照せず、`tfc:metal/sword/wrought_iron`を100%生成し、
  元のlevel 30 enchant、`set_name`、weight 1を維持する。
- End Cityを含め、依存元にenchantがある完成装備はそのenchantを維持する。

### shared table配置

- `shared/gems`
- `shared/ingots/ordinary`
- `shared/ingots/dangerous`
- `shared/ingots/lategame`
- `shared/small_ores/iron`
- `shared/coal_like`
- `shared/utility`
- `shared/produce`
- `shared/seeds`
- `shared/fertilizers`
- `shared/equipment/<profile>/<family>`

旧`metals_*`、`equipment_*`、`horse_armor_*`、`ranged_weapon` shared tableと、
それら専用のitem tagは使用しない。

### 検証

loot変更時は少なくとも次を確認する。

- 全JSONをparseできる。
- 依存元とのpool数、rolls、bonus rolls、entry数、weight、condition、countが一致する。
- YUNG系mod固有itemが変化していない。
- profileごとのtier上限を超えない。
- red steelとblue steelが存在しない。
- black steelがlategame ingot以外に存在しない。
- ingot tableにingot以外、small ore tableにsmall ore以外が存在しない。
- graphiteは`coal_like`内の`tfc:ore/graphite`だけである。
- utilityにcoal_like資源が存在しない。
- tool familyとarmor slotが一致する。
- 部品:完成品のweightが2:1である。
- 部品とunfinished armorの生成結果にenchantmentが付かない。
- `set_count`が同じentryへ重複していない。
- `--tfc-jar`で指定した実TFC JARのdatagen済みitem modelと全`tfc:` item idを照合し、欠落がない。
- `./gradlew build`が成功する。Minecraftクライアントは検証のために起動しない。
