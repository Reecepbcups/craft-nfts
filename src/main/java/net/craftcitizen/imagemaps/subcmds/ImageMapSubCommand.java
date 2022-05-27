package net.craftcitizen.imagemaps.subcmds;

import de.craftlancer.core.command.SubCommand;
import net.craftcitizen.imagemaps.ImageMaps;

public abstract class ImageMapSubCommand extends SubCommand {

    public ImageMapSubCommand(String permission, ImageMaps plugin, boolean console) {
        super(permission, plugin, console);
    }

    @Override
    public ImageMaps getPlugin() {
        return (ImageMaps) super.getPlugin();
    }
}
