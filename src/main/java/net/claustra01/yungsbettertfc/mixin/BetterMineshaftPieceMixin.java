package net.claustra01.yungsbettertfc.mixin;

import net.claustra01.yungsbettertfc.world.processor.TfcBlockReplacementProcessor;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.state.BlockState;
import org.spongepowered.asm.mixin.Dynamic;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Pseudo;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

@Pseudo
@Mixin(
        targets = "com.yungnickyoung.minecraft.bettermineshafts.world.generator.pieces.BetterMineshaftPiece",
        remap = false)
public abstract class BetterMineshaftPieceMixin {
    @Unique
    private static final String BETTER_MINESHAFT_PIECE =
            "com.yungnickyoung.minecraft.bettermineshafts.world.generator.pieces.BetterMineshaftPiece";
    @Unique
    private static final String SET_BLOCK_TARGET =
            "Lnet/minecraft/world/level/WorldGenLevel;setBlock("
                    + "Lnet/minecraft/core/BlockPos;"
                    + "Lnet/minecraft/world/level/block/state/BlockState;"
                    + "I)Z";
    @Unique
    private static final String GENERATE_LEG_OR_CHAIN_METHOD =
            "generateLegOrChain("
                    + "Lnet/minecraft/world/level/WorldGenLevel;"
                    + "Lnet/minecraft/util/RandomSource;"
                    + "Lnet/minecraft/world/level/levelgen/structure/BoundingBox;"
                    + "II"
                    + "Lcom/yungnickyoung/minecraft/yungsapi/api/world/randomize/BlockStateRandomizer;"
                    + ")Z";
    @Unique
    private static final String GENERATE_PILLAR_DOWN_OR_CHAIN_UP_METHOD =
            "generatePillarDownOrChainUp("
                    + "Lnet/minecraft/world/level/WorldGenLevel;"
                    + "Lnet/minecraft/util/RandomSource;"
                    + "Lnet/minecraft/world/level/levelgen/structure/BoundingBox;"
                    + "IIII"
                    + "Lnet/minecraft/world/level/block/state/BlockState;"
                    + ")V";
    @Unique
    private static final String FILL_COLUMN_BLOCKSTATE_METHOD =
            "fillColumnBetween("
                    + "Lnet/minecraft/world/level/WorldGenLevel;"
                    + "Lnet/minecraft/world/level/block/state/BlockState;"
                    + "Lnet/minecraft/core/BlockPos$MutableBlockPos;"
                    + "II"
                    + ")V";
    @Unique
    private static final String FILL_COLUMN_RANDOMIZER_METHOD =
            "fillColumnBetween("
                    + "Lnet/minecraft/world/level/WorldGenLevel;"
                    + "Lnet/minecraft/util/RandomSource;"
                    + "Lcom/yungnickyoung/minecraft/yungsapi/api/world/randomize/BlockStateRandomizer;"
                    + "Lnet/minecraft/core/BlockPos$MutableBlockPos;"
                    + "II"
                    + ")V";

    @Dynamic("Better Mineshafts optional piece method")
    @Redirect(
            method = GENERATE_LEG_OR_CHAIN_METHOD,
            at = @At(value = "INVOKE", target = SET_BLOCK_TARGET),
            remap = false)
    private boolean yungsbettertfc$replaceGenerateLegOrChainBlock(
            WorldGenLevel level, BlockPos pos, BlockState state, int flags) {
        return level.setBlock(pos, yungsbettertfc$replaceBetterMineshaftState(level, pos, state), flags);
    }

    @Dynamic("Better Mineshafts optional piece method")
    @Redirect(
            method = GENERATE_PILLAR_DOWN_OR_CHAIN_UP_METHOD,
            at = @At(value = "INVOKE", target = SET_BLOCK_TARGET),
            remap = false)
    private boolean yungsbettertfc$replaceGeneratePillarDownOrChainUpBlock(
            WorldGenLevel level, BlockPos pos, BlockState state, int flags) {
        return level.setBlock(pos, yungsbettertfc$replaceBetterMineshaftState(level, pos, state), flags);
    }

    @Dynamic("Better Mineshafts optional static column helper")
    @Redirect(
            method = FILL_COLUMN_BLOCKSTATE_METHOD,
            at = @At(value = "INVOKE", target = SET_BLOCK_TARGET),
            remap = false)
    private static boolean yungsbettertfc$replaceFillColumnBlock(
            WorldGenLevel level, BlockPos pos, BlockState state, int flags) {
        return level.setBlock(pos, yungsbettertfc$replaceBetterMineshaftState(level, pos, state), flags);
    }

    @Dynamic("Better Mineshafts optional static column helper")
    @Redirect(
            method = FILL_COLUMN_RANDOMIZER_METHOD,
            at = @At(value = "INVOKE", target = SET_BLOCK_TARGET),
            remap = false)
    private static boolean yungsbettertfc$replaceFillColumnRandomizerBlock(
            WorldGenLevel level, BlockPos pos, BlockState state, int flags) {
        return level.setBlock(pos, yungsbettertfc$replaceBetterMineshaftState(level, pos, state), flags);
    }

    @Unique
    private static BlockState yungsbettertfc$replaceBetterMineshaftState(
            WorldGenLevel level, BlockPos pos, BlockState state) {
        return TfcBlockReplacementProcessor.replaceGeneratedBlock(level, pos, state, BETTER_MINESHAFT_PIECE);
    }
}
