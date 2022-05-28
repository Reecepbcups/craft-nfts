package net.craftcitizen.imagemaps.handlers;

import de.craftlancer.core.command.CommandHandler;
import net.craftcitizen.imagemaps.ImageMaps;
import net.craftcitizen.imagemaps.a_done.ImageMapHelpCommand;
import net.craftcitizen.imagemaps.a_done.ImageMapListCommand;
import net.craftcitizen.imagemaps.adelete_later.ImageMapDeleteCommand;
import net.craftcitizen.imagemaps.adelete_later.ImageMapDownloadCommand;
import net.craftcitizen.imagemaps.adelete_later.ImageMapInfoCommand;
import net.craftcitizen.imagemaps.adelete_later.ImageMapReloadCommand;
import net.craftcitizen.imagemaps.subcmds.ImageMapPlaceCommand;

public class ImageMapCommandHandler extends CommandHandler {
    public ImageMapCommandHandler(ImageMaps plugin) {
        super(plugin);
        registerSubCommand("download", new ImageMapDownloadCommand(plugin));
        registerSubCommand("delete", new ImageMapDeleteCommand(plugin));
        registerSubCommand("place", new ImageMapPlaceCommand(plugin));
        registerSubCommand("info", new ImageMapInfoCommand(plugin));
        registerSubCommand("list", new ImageMapListCommand(plugin));
        registerSubCommand("reload", new ImageMapReloadCommand(plugin));
        registerSubCommand("help", new ImageMapHelpCommand(plugin, getCommands()), "?");
    }
}
