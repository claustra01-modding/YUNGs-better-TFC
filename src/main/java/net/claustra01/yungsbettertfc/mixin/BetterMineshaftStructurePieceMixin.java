package net.claustra01.yungsbettertfc.mixin;

import net.claustra01.yungsbettertfc.world.processor.TfcBlockReplacementProcessor;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.structure.StructurePiece;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

@Mixin(StructurePiece.class)
public abstract class BetterMineshaftStructurePieceMixin {
    @Unique
    private static final String BETTER_MINESHAFT_PIECE_PACKAGE =
            "com.yungnickyoung.minecraft.bettermineshafts.world.generator.pieces.";
    @Unique
    private static final String PLACE_BLOCK_METHOD =
            "placeBlock(Lnet/minecraft/world/level/WorldGenLevel;"
                    + "Lnet/minecraft/world/level/block/state/BlockState;"
                    + "IIILnet/minecraft/world/level/levelgen/structure/BoundingBox;)V";
    @Unique
    private static final String CREATE_CHEST_METHOD =
            "createChest(Lnet/minecraft/world/level/ServerLevelAccessor;"
                    + "Lnet/minecraft/world/level/levelgen/structure/BoundingBox;"
                    + "Lnet/minecraft/util/RandomSource;"
                    + "Lnet/minecraft/core/BlockPos;"
                    + "Lnet/minecraft/resources/ResourceKey;"
                    + "Lnet/minecraft/world/level/block/state/BlockState;)Z";

    @Redirect(
            method = PLACE_BLOCK_METHOD,
            at = @At(
                    value = "INVOKE",
                    target = "Lnet/minecraft/world/level/WorldGenLevel;setBlock(Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/level/block/state/BlockState;I)Z"),
            remap = false)
    private boolean yungsbettertfc$replaceBetterMineshaftPlacedBlock(
            WorldGenLevel level, BlockPos pos, BlockState state, int flags) {
        return level.setBlock(pos, this.yungsbettertfc$replaceBetterMineshaftState(level, pos, state), flags);
    }

    @Redirect(
            method = CREATE_CHEST_METHOD,
            at = @At(
                    value = "INVOKE",
                    target = "Lnet/minecraft/world/level/ServerLevelAccessor;setBlock(Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/level/block/state/BlockState;I)Z"),
            remap = false)
    private boolean yungsbettertfc$replaceBetterMineshaftChestBlock(
            ServerLevelAccessor level, BlockPos pos, BlockState state, int flags) {
        return level.setBlock(pos, this.yungsbettertfc$replaceBetterMineshaftState(level, pos, state), flags);
    }

    @Unique
    private BlockState yungsbettertfc$replaceBetterMineshaftState(
            ServerLevelAccessor level, BlockPos pos, BlockState state) {
        String source = ((Object) this).getClass().getName();
        if (!source.startsWith(BETTER_MINESHAFT_PIECE_PACKAGE)) {
            return state;
        }
        return TfcBlockReplacementProcessor.replaceGeneratedBlock(level, pos, state, source);
    }
}
