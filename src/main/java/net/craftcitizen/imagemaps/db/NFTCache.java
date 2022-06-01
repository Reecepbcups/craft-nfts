package net.craftcitizen.imagemaps.db;

import java.awt.image.BufferedImage;
import java.util.HashMap;
import java.util.Map;

import com.mongodb.client.FindIterable;
import com.mongodb.client.model.Filters;

import org.bson.Document;
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

    public static BufferedImage getImage(String NFTName) {
        NFTName = NFTName.toLowerCase();
        // Gets image or adds it to cache

        // gets already placed images. 
        if (imageCache.containsKey(NFTName)) {
            return imageCache.get(NFTName);
        }
            

        // get from IMAGES collection
        // FindIterable<Document> s = ImageThings.IMAGES_COLL.find(Filters.eq("name", NFTName));
        // Document doc = s.first();
        // if (doc == null) {
        //     System.out.println("No image found in DB or cache, probably use need to save it from an ImageThing object");
        //     return null;
        // }
        
        BufferedImage bI = ImageThings.loadImageFromMongDB(NFTName);
        if (bI == null) {
            System.out.println("No image found in DB or cache, probably use need to save it from an ImageThing object");
            return null;
        }
        imageCache.put(NFTName, bI);
        return bI;
    }

    public static void addImage(String NFTName, BufferedImage img) {
        imageCache.putIfAbsent(NFTName.toLowerCase(), img);
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
