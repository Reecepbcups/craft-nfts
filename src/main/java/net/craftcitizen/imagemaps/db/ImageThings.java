package net.craftcitizen.imagemaps.db;

import java.io.ByteArrayOutputStream;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.Base64;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;

import java.awt.image.BufferedImage;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;

import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

import org.bson.Document;


public class ImageThings {
    private static String URI = "mongodb://root:akashmongodb19pass@782sk60c31ell6dbee3ntqc9lo.ingress.provider-2.prod.ewr1.akash.pub:31543/?authSource=admin";
    private static MongoClient mongoClient = new MongoClient(new MongoClientURI(URI));

    // These would be in main classw tih getters     
    static MongoDatabase database = mongoClient.getDatabase("NFTs");
    static MongoCollection<Document> collection = database.getCollection("OWNERS");
    static MongoCollection<Document> PLACED_NFTS = database.getCollection("PLACED_NFTS");

    private Document doc = null;
    private String address = null;
      
    public ImageThings(String address) {
        doc = getDocument(address);
        if(doc == null) {
            System.out.println("You dont have any NFTs, make sure to sync you wallet with the webapp...");
        }
    }

    // ---
    private Document getDocument(String address) {
        Document query = new Document("address", address);
        Document doc = collection.find(query).first();
        return doc;
    }

    public String getIPFSLink(String name) {
        Document nftDoc = (Document) doc.get("nfts");
        String myLink = (String) nftDoc.get(name);
        if (myLink == null) {
            return null;
        }
        return myLink.toString();
    }

    // gets all NFT Names
    public Set<String> getNFTNames() {
        Document nftDoc = (Document) doc.get("nfts");        
        if (nftDoc == null) {
            return null;
        }
        return nftDoc.keySet();
    }

    public Map<String, ArrayList<String>> sortNFts() {
        // useful for the GUI
        Map<String, ArrayList<String>> OurNFTs = new HashMap<String, ArrayList<String>>();

        if(!(doc.keySet().contains("nfts"))) {
            System.out.println("This document does not have any NFTs");
            return null;
        }

        Document nfts = (Document) doc.get("nfts");

        for(String key : nfts.keySet()) {
            // This should work for all NFTs, if not they go into other
            // Future we can regex split at # or last space
            if(key.contains("#")) { 
                String[] values = key.split("#"); // ["Oblitus ", "0961"]            
                String name = values[0];
                String id = "#"+values[1]; // we need to add back in for requesting since we split at it

                // System.out.println(name + " " + id);

                if(!OurNFTs.containsKey(name)) {
                    ArrayList<String> newList = new ArrayList<String>();
                    OurNFTs.put(name, newList);
                } 

                OurNFTs.get(name).add(id);

            } else {   
                
                if(!OurNFTs.containsKey("others")) {
                    ArrayList<String> temp = new ArrayList<String>();
                    temp.add(key);   
                    OurNFTs.put("others", temp);                 
                }

                // System.out.println("OTHERS: Added" + key); 
                OurNFTs.get("others").add(key);
            }
        }
        return OurNFTs;
    }

    public void getAllDocsFromCollection() {
        List<Document> documents = (List<Document>) collection.find().into(new ArrayList<Document>());
        // print them
        for (Document document : documents) {
            System.out.println(document);
        }
    }


    public static String[] getAllPlacedNFTs() {
        List<Document> documents = (List<Document>) PLACED_NFTS.find().into(new ArrayList<Document>());
        List<String> keys = new ArrayList<>();
        for (Document document : documents) {
            keys.add(document.get("name").toString());
        }
        return keys.toArray(new String[0]);
    }



    // === In game stuff ===
    // When a user clicks on a map, we need to get the IPFS Link, Download to memory, and put on the map
    public static BufferedImage downloadNFT(String link) {
        // from ImageMapDownload (Download & place should be all in 1)

        // May just be able to do a null check, and show without saving to file?
        URL srcURL = null;
        BufferedImage image = null;
        try {
            srcURL = new URL(link);
            java.net.URLConnection connection = srcURL.openConnection();
            connection.setRequestProperty("User-Agent", "CraftNFTs/0");
            if (((HttpURLConnection) connection).getResponseCode() != 200) {
                System.out.println(String.format("Download failed, HTTP Error code %d.", ((HttpURLConnection) connection).getResponseCode()));
                return null;
            }
            System.out.println(connection.getHeaderField("Content-type"));

            try (InputStream str = connection.getInputStream()) {
                image = ImageIO.read(str); // FUTURE: compress this to JPG (RGB), see if I can condense

                // open image in a frame DEBUGGING
                // JFrame frame = new JFrame();
                // frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                // frame.getContentPane().add(new JLabel(new ImageIcon(image)));
                // frame.pack();
                // frame.setVisible(true);                              
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
        
        return image;
    }

    // Will try gridfs if this doesnt work
    // https://kb.objectrocket.com/mongo-db/how-to-save-an-image-in-mongodb-using-java-394
    public void saveImageIOToMongoDB(BufferedImage image, String name) {
        byte[] imageBytes = toByteArray(image, "png");

        Document doc = new Document("name", name);
        // check if this exist in PLACED_IMAGES collection
        if(PLACED_NFTS.find(doc).first() != null) {
            // doc already exist, we are not saving it
            System.out.println("This image already exists in the database");
            return;
        }

        String imgToSave = encodeBase64String(imageBytes);
        doc.append("image", imgToSave);
        PLACED_NFTS.insertOne(doc);
    }

    public BufferedImage loadImageFromMongDB(String name) {
        // load images which are on the server (useful for reboots)

        Document query = new Document("name", name);
        // check if this exist in PLACED_IMAGES collection
        Document doc = PLACED_NFTS.find(query).first();
        if(doc == null) {
            System.out.println("This image is not found in the collection! name: " + name);
            return null;
        }

        String myImgString = (String) doc.get("image");
        System.out.println("ImageThings.java loadImageFromMongDB: " + name + " ");
        // System.out.println("Image String: " + myImgString);
        // decode to bvytes
        byte[] decodedBytes = decodeBase64String(myImgString);  
        // return decodedImage;  
        return toBufferedImage(decodedBytes);        
    }

    // convert BufferedImage to byte[] to save in MongoDB
    // https://mkyong.com/java/how-to-convert-bufferedimage-to-byte-in-java/
    private byte[] toByteArray(java.awt.image.BufferedImage image, String format){
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        try {
            ImageIO.write(image, format, baos);
        } catch (IOException e) {
            e.printStackTrace();
        }
        byte[] bytes = baos.toByteArray();
        return bytes;

    }
    // convert byte[] to BufferedImage
    private java.awt.image.BufferedImage toBufferedImage(byte[] bytes) {

        InputStream is = new ByteArrayInputStream(bytes);
        java.awt.image.BufferedImage bi = null;
        try {
            bi = ImageIO.read(is);
        } catch (IOException e) {            
            e.printStackTrace();            
        }
        return bi;

    }
    private String encodeBase64String(byte[] binaryData) {
        return Base64.getEncoder().encodeToString(binaryData);
    }
    private byte[] decodeBase64String(String base64String) {
        return Base64.getDecoder().decode(base64String);
    }

    


}
