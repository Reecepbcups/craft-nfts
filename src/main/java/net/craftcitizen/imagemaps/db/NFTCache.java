package net.craftcitizen.imagemaps.db;

import java.awt.image.BufferedImage;
import java.util.HashMap;
import java.util.Map;

import org.bukkit.Bukkit;

import net.craftcitizen.imagemaps.rendering.ImageMap;
import net.craftcitizen.imagemaps.rendering.ImageMapRenderer;



public class NFTCache {
    // hasImage
    // getImage

    private static Map<String, BufferedImage> imageCache = new HashMap<>();
    private static Map<ImageMap, Integer> maps = new HashMap<>();

    public static Map<ImageMap, Integer> getMaps() {
        return maps;
    }
    public static void addMap(ImageMap im, Integer id) {
        maps.put(im, id);
    }

    public boolean hasImage(String nftName) {
        if (imageCache.containsKey(nftName.toLowerCase())) {
            return true;
        }
            
        return getImage(nftName) != null;
    }

    public BufferedImage getImage(String NFTName) {
        // Gets image or adds it to cache

        // gets already placed images. 
        if (imageCache.containsKey(NFTName.toLowerCase()))
            return imageCache.get(NFTName.toLowerCase());

        // we should prob do this before hand?
        ImageThings iT = new ImageThings("craft178n8r8wmkjy2e3ark3c2dhp4jma0r6zwce9z7k");

        BufferedImage image = iT.loadImageFromMongDB(NFTName);

        // BufferedImage image = iT.toBufferedImage(byteArray);
        System.out.println("Loaded image in getImage "+NFTName+" (ImageMaps.java)");


        // if (!file.exists())
        //     return null;

        // image = ImageIO.read(file);
        imageCache.put(NFTName.toLowerCase(), image);

        return image;
    }

    public static void deleteImageFromCache(String nftName) { 
        imageCache.remove(nftName);
    }


    @SuppressWarnings("deprecation")
    public boolean reloadImage(String nftName) {
        // used to be in ImageMaps.java
        if (!imageCache.containsKey(nftName.toLowerCase()))
            return false;

        imageCache.remove(nftName.toLowerCase());
        BufferedImage image = getImage(nftName);

        if (image == null) {
            // getLogger().warning(() -> "Failed to reload image: " + nftName);
            System.out.println("Failed to reload image: " + nftName);
            return false;
        }

        maps.entrySet().stream().filter(a -> a.getKey().getFilename().equalsIgnoreCase(nftName)).map(a -> Bukkit.getMap(a.getValue()))
                .flatMap(a -> a.getRenderers().stream()).filter(ImageMapRenderer.class::isInstance).forEach(a -> ((ImageMapRenderer) a).recalculateInput(image));
        return true;
    }

}
