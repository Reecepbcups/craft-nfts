package net.craftcitizen.imagemaps.subcmds;

import de.craftlancer.core.Utils;
import de.craftlancer.core.util.MessageLevel;
import de.craftlancer.core.util.MessageUtil;
import de.craftlancer.core.util.Tuple;
import net.craftcitizen.imagemaps.ImageMaps;
import net.craftcitizen.imagemaps.db.ImageThings;
import net.craftcitizen.imagemaps.db.NFTCache;
import net.craftcitizen.imagemaps.images.PlacementData;

import org.bukkit.GameMode;
import org.bukkit.Warning.WarningState;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.metadata.FixedMetadataValue;

import java.awt.image.BufferedImage;
import java.util.Collections;
import java.util.List;

public class ImageMapPlaceCommand extends ImageMapSubCommand {

    // What I want:
    // - /imagemap place rat 1x1 false
    // TODO WIP

    public ImageMapPlaceCommand(ImageMaps plugin) {
        super("craftnfts.place", plugin, false);
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

        String nftName = args[1]; // make sure to replace " " with "_"
        boolean isInvisible = true;
        boolean isFixed = false; // means user can not break in survival
        boolean isGlowing = false;
        Tuple<Integer, Integer> scale = args.length >= 3 ? parseScale(args[2]) : new Tuple<>(-1, -1);

        // if (getPlugin().isInvisibilitySupported()) {
        //     // isInvisible = args.length >= 3 && Boolean.parseBoolean(args[2]);
        //     // isFixed = args.length >= 4 && Boolean.parseBoolean(args[3]);
        //     if (getPlugin().isGlowingSupported()) {
        //         isGlowing = args.length >= 5 && Boolean.parseBoolean(args[4]);
        //         scale = args.length >= 6 ? parseScale(args[5]) : new Tuple<>(-1, -1);
        //     } else {
        //         scale = args.length >= 5 ? parseScale(args[4]) : new Tuple<>(-1, -1);
        //     }
        // } else {
        //     scale = args.length >= 3 ? parseScale(args[2]) : new Tuple<>(-1, -1);
        // }

        if (nftName.contains("/") || nftName.contains("\\") || nftName.contains(":")) {
            MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.WARNING, "NFTName contains illegal character.");
            return null;
        }

        if(nftName.contains("_")) {            
            nftName = nftName.replace("_", " ");
            System.out.println("NFT name contained underscores! moved them to be spaces>> " + nftName);
        }


        // If user owns NFT, continue
        ImageThings iT = new ImageThings(ImageMaps.MY_ADDRESS);

        // TODO
        // if(!iT.getMyNFTNames().contains(nftName)) {
        //     System.out.println(iT.getMyNFTNames());
        //     MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.WARNING, "You don't own this NFT." + ImageMaps.MY_ADDRESS + " -> " + nftName);
        //     return null;
        // }

        
        // Get cached version, if none, get from MongoDB
        BufferedImage image = null;

        // System.out.println("TESTING 18923893");
        // System.out.println(ImageThings.getAllSavedNFTFilenames() + "");
        // System.out.println(ImageThings.getAllSavedNFTFilenames().contains(nftName));

        if(!ImageThings.getAllSavedNFTFilenames().contains(nftName)) {
            System.out.println("NFT is not in the database, we need to upload it & cache!");

            String link = iT.getIPFSLink(nftName); // This will return null if we try to change the name of the NFT before getting it (ex. lowercase, or _)
            if(link == null) { // HOW?
                MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.WARNING, "Error, " + nftName + " could not download from link");
                return null;
            }

            image = ImageThings.downloadNFT(link);
            if(image == null) {
                MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.WARNING, "Could not download NFT, " + nftName);
                return null;
            }

            // add to cache first since the upload is async
            // NFTCache.addImage(nftName, image); // done in ImageThings.uploadAsyncToMongo

            // adds to cache, then upload it to MongoDB async
            ImageThings.uploadAsyncToMongo(nftName, image); 
            System.out.println(nftName + " was added to the cache & uploaded to MongoDB!");
        }
                    
       
        if(image == null) {
            // get image from cache, if its not there it gets from MongoDB
            image = NFTCache.getImage(nftName);
        }
        
        if(image == null) {
            MessageUtil.sendMessage(plugin, sender, MessageLevel.WARNING, "This NFT was not in cache nor in the database. Make sure you synced.");
            return null;
        }

        System.out.println("Loaded image in ImageMapPlaceCommand.java");

        Player player = (Player) sender;
        if(player.getGameMode().equals(GameMode.CREATIVE)) {
            MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.INFO, "Since you placed this in creative, users in survival can not break.");
            isFixed = true; // so users can not break it in survival
        }
        player.setMetadata(ImageMaps.PLACEMENT_METADATA, new FixedMetadataValue(getPlugin(), new PlacementData(nftName, image, isInvisible, isFixed, isGlowing, scale)));

        Tuple<Integer, Integer> size = getPlugin().getImageSize(image, scale);
        MessageUtil.sendMessage(getPlugin(),
                sender,
                MessageLevel.NORMAL,
                String.format("Started placing of %s. It needs a %d by %d area.", args[1], size.getKey(), size.getValue()));
        MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.NORMAL, "Right click on the block, that should be the upper left corner.");
        return null;
    }

    // Just use underscores
    // public static String argsToSingleString(final int startPoint, final String[] args) {
	// 	final StringBuilder str = new StringBuilder();
	// 	for (int i = startPoint; i < args.length; i++) {
	// 		if (i+1 < args.length) {
	// 			str.append(args[i]).append(" ");
	// 		} else {
	// 			str.append(args[i]);
	// 		}
	// 	}
	// 	return str.toString();
	// }

    @Override
    public void help(CommandSender sender) {
        MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.NORMAL, "Starts placing an image.");

        if (getPlugin().isGlowingSupported()) {
            MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.INFO, "Usage: /imagemap place <filename> [frameInvisible] [frameFixed] [frameGlowing] [size]");
        } else if (getPlugin().isInvisibilitySupported()) {
            MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.INFO, "Usage: /imagemap place <filename> [frameInvisible] [frameFixed] [size]");
        } else {
            MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.INFO, "Usage: /imagemap place <filename> [size]");
        }

        MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.NORMAL, "Size format: XxY -> 5x2, use -1 for default");
        MessageUtil.sendMessage(getPlugin(),
                sender,
                MessageLevel.NORMAL,
                "The plugin will scale the map to not be larger than the given size while maintaining the aspect ratio.");
        MessageUtil.sendMessage(getPlugin(),
                sender,
                MessageLevel.NORMAL,
                "It's recommended to avoid the size function in favor of using properly sized source images.");
    }

    private static Tuple<Integer, Integer> parseScale(String string) {
        String[] tmp = string.split("x");

        if (tmp.length < 2)
            return new Tuple<>(-1, -1);

        return new Tuple<>(Utils.parseIntegerOrDefault(tmp[0], -1), Utils.parseIntegerOrDefault(tmp[1], -1));
    }

    @Override
    protected List<String> onTabComplete(CommandSender sender, String[] args) {
        if (args.length > 2 && !getPlugin().isInvisibilitySupported()
                || args.length > 4 && !getPlugin().isGlowingSupported()) {
            return Collections.emptyList();
        }

        switch (args.length) {
            case 2:
                // return Utils.getMatches(args[1], new File(plugin.getDataFolder(), "images").list());
                // System.out.println("In the future change this to mongodb list of placed/downloaded images (ImageMapPlaceCommand)");
                return Collections.emptyList();
            case 3:
                // return Utils.getMatches(args[2], Arrays.asList("true", "false"));
                return Collections.emptyList();
            case 4:
                // return Utils.getMatches(args[3], Arrays.asList("true", "false"));
                return Collections.emptyList();
            case 5:
                // return Utils.getMatches(args[4], Arrays.asList("true", "false"));
                return Collections.emptyList();
            default:
                return Collections.emptyList();
        }
    }
}
