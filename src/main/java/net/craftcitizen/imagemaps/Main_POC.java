package net.craftcitizen.imagemaps;


import java.io.ByteArrayOutputStream;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.Base64;
import java.util.HashMap;
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


public class Main_POC {

    // TODO Idea, when an NFT is palces, could save name => ipfs link as PLACED_NFTS
    // TODO then on load, we just download it at run time for every placed instance?

    // TODO ^ switch to GridFS if not doing that way
    
    private static String URI = "mongodb://root:akashmongodb19pass@782sk60c31ell6dbee3ntqc9lo.ingress.provider-2.prod.ewr1.akash.pub:31543/?authSource=admin";
    private static MongoClient mongoClient = new MongoClient(new MongoClientURI(URI));

    // These would be in main classw tih getters     
    static MongoDatabase database = mongoClient.getDatabase("NFTs");
    static MongoCollection<Document> collection = database.getCollection("OWNERS");
    static MongoCollection<Document> PLACED_NFTS = database.getCollection("PLACED_NFTS");

    public static void main(String[] args) {
        System.out.println("Hello World!");


        // getAllDocsFromCollection(collection);
    
        // we get this from the collection where wallet = username
        String address = "craft178n8r8wmkjy2e3ark3c2dhp4jma0r6zwce9z7k";

        Document doc = getDocument(address);
        if(doc == null) {
            System.out.println("You dont have any NFTs, make sure to sync you wallet with the webapp...");
        }

        
        // Set<String> names = getNFTNames(doc);
        // System.out.println(names);

        // Groups the NFTs by their name
        Map<String, ArrayList<String>> myNFTsSorted = sortNFts(doc);
        // System.out.println(myNFTsSorted.keySet());
        System.out.println();
        for (String key : myNFTsSorted.keySet()) {
            // TODO! SOME HAVE A SPACE SO THEY KEY IS ACTUALLY 'NFTName ' before the #.
            // TODO Need to trim() / .stip() when saving to mongo I guess in the future?
            // TODO Make them all 'MyNFT#1234' if they have #. Replace spaces with _ ?
            System.out.println(key + ": " + myNFTsSorted.get(key));
        }
        


        // would be done via GUI in future
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter your NFT name: ");
        String nftName = scanner.nextLine();
        scanner.close();
        String link = getIPFSLink(doc, nftName);
        System.out.println(link);

        // we do this when the user wants to place it, so it saves to DB
        java.awt.image.BufferedImage bImg = downloadNFT(link);
        saveImageIOToMongoDB(bImg, nftName);

        // load it from the DB
        // byte[] byteArray = loadImageFromMongDB("1170");
        // BufferedImage myBufferedImgFromDB = toBufferedImage(byteArray);
        // JFrame frame = new JFrame();
        // frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        // frame.setVisible(true);  
        // frame.getContentPane().add(new JLabel(new ImageIcon(myBufferedImgFromDB)));
        // frame.pack();




    }

    private static Document getDocument(String address) {
        Document query = new Document("address", address);
        Document doc = collection.find(query).first();
        return doc;
    }

    private static String getIPFSLink(Document doc, String name) {
        Document nftDoc = (Document) doc.get("nfts");
        String myLink = (String) nftDoc.get(name);
        if (myLink == null) {
            return null;
        }
        return myLink.toString();
    }

    // gets all NFT Names
    private static Set<String> getNFTNames(Document doc) {
        Document nftDoc = (Document) doc.get("nfts");        
        if (nftDoc == null) {
            return null;
        }
        return nftDoc.keySet();
    }

    private static Map<String, ArrayList<String>> sortNFts(Document doc) {
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

    private static void getAllDocsFromCollection(MongoCollection<Document> collection) {
        List<Document> documents = (List<Document>) collection.find().into(new ArrayList<Document>());
        // print them
        for (Document document : documents) {
            System.out.println(document);
        }
    }



    // === In game stuff ===
    // When a user clicks on a map, we need to get the IPFS Link, Download to memory, and put on the map
    private static BufferedImage downloadNFT(String link) {
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
    private static void saveImageIOToMongoDB(BufferedImage image, String name) {
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

    private static byte[] loadImageFromMongDB(String name) {
        // load images which are on the server (useful for reboots)

        Document query = new Document("name", name);
        // check if this exist in PLACED_IMAGES collection
        Document doc = PLACED_NFTS.find(query).first();
        if(doc == null) {
            System.out.println("This image is not found in the collection! name:" + name);
            return null;
        }

        String myImgString = (String) doc.get("image");
        // System.out.println("Image String: " + myImgString);
        // decode to bvytes
        byte[] decodedImage = decodeBase64String(myImgString);        
        return decodedImage; // we are able to load in game with this yes?
    }

    // convert BufferedImage to byte[] to save in MongoDB
    // https://mkyong.com/java/how-to-convert-bufferedimage-to-byte-in-java/
    public static byte[] toByteArray(java.awt.image.BufferedImage image, String format){
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
    public static java.awt.image.BufferedImage toBufferedImage(byte[] bytes) {

        InputStream is = new ByteArrayInputStream(bytes);
        java.awt.image.BufferedImage bi = null;
        try {
            bi = ImageIO.read(is);
        } catch (IOException e) {            
            e.printStackTrace();            
        }
        return bi;

    }


    private static String encodeBase64String(byte[] binaryData) {
        return Base64.getEncoder().encodeToString(binaryData);
    }
    private static byte[] decodeBase64String(String base64String) {
        return Base64.getDecoder().decode(base64String);
    }

}
