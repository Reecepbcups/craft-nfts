package net.craftcitizen.imagemaps.adelete_later;

import de.craftlancer.core.Utils;
import de.craftlancer.core.util.MessageLevel;
import de.craftlancer.core.util.MessageUtil;
import net.craftcitizen.imagemaps.ImageMaps;
import net.craftcitizen.imagemaps.subcmds.ImageMapSubCommand;

import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;

import java.io.File;
import java.util.Collections;
import java.util.List;

public class ImageMapReloadCommand extends ImageMapSubCommand {

    // TODO I dont think we even need this class since IPFS images never change.

    public ImageMapReloadCommand(ImageMaps plugin) {
        super("craftnfts.reload", plugin, true);
    }

    @Override
    protected String execute(CommandSender sender, Command cmd, String label, String[] args) {
        if (!checkSender(sender)) {
            MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.WARNING, "You can't run this command.");
            return null;
        }

        if (args.length < 2) {
            MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.WARNING, "You must specify a file name.");
            return null;
        }

        String nftName = args[1];

        if (nftName.contains("/") || nftName.contains("\\") || nftName.contains(":")) {
            MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.WARNING, "NFTName contains illegal character.");
            return null;
        }

        System.out.println("ReloadImage in ImagemapReloadCommand is commented out!");
        // if (getPlugin().reloadImage(nftName))
        //     MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.NORMAL, "NFT Image reloaded.");
        // else
        //     MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.NORMAL, "NFT Iamge couldn't be reloaded (does it exist?).");

        return null;
    }

    @Override
    public void help(CommandSender sender) {
        MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.NORMAL, "Reloads an image from database, to be used when the file changed.");
        MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.NORMAL, "Avoid resolution changes, since they won't be scaled.");
        MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.INFO, "Usage: /imagemap reload <nftName>");
    }

    @Override
    protected List<String> onTabComplete(CommandSender sender, String[] args) {
        if (args.length == 2)
            return Utils.getMatches(args[1], new File(plugin.getDataFolder(), "images").list());

        return Collections.emptyList();
    }

}
