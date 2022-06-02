package net.craftcitizen.imagemaps.db;

import java.io.ByteArrayOutputStream;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;

import javax.imageio.IIOImage;
import javax.imageio.ImageIO;
import javax.imageio.ImageWriteParam;
import javax.imageio.ImageWriter;
import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.gridfs.GridFSBucket;
import com.mongodb.client.gridfs.GridFSBuckets;
import com.mongodb.client.gridfs.GridFSFindIterable;
import com.mongodb.client.gridfs.model.GridFSFile;
import com.mongodb.client.gridfs.model.GridFSUploadOptions;
import com.mongodb.client.model.Filters;

import net.craftcitizen.imagemaps.ImageMaps;

import org.bson.Document;
import org.bson.types.ObjectId;
import org.bukkit.Bukkit;

public class ImageThings {
    private static String URI = "mongodb://root:akashmongodb19pass@782sk60c31ell6dbee3ntqc9lo.ingress.provider-2.prod.ewr1.akash.pub:31543/?authSource=admin";

    // private static MongoClientOptions mco = new MongoClientOptions.Builder()
    // .maxConnectionIdleTime(0)
    // .connectionsPerHost(5)
    // .build();

    private static MongoClient mongoClient = new MongoClient(new MongoClientURI(URI));

    // These would be in main classw tih getters
    static MongoDatabase database = mongoClient.getDatabase("NFTs");
    static MongoCollection<Document> ASSETS_COLL = database.getCollection("AssetHoldings");
    static MongoCollection<Document> IMAGES_COLL = database.getCollection("IMAGES"); // make its own DB, as a GridFS
                                                                                     // Bucket
    static MongoCollection<Document> PLACED_NFTS_COLL = database.getCollection("PLACED_NFTS"); // maps.yml will be here

    static MongoDatabase ImageDBGridFS = mongoClient.getDatabase("IMAGE_NFTS"); // replaces IMAGES_COLL

    private Document doc = null;
    private final String address;

    public ImageThings(String address) {
        this.address = address;

        doc = getDocument(this.address);
        if (doc == null) {
            System.out.println(
                    "You dont have any NFTs with " + address + ", make sure to sync you wallet with the webapp...");
        }
    }

    // ---
    private Document getDocument(String address) {
        Document query = new Document("address", address);
        Document doc = ASSETS_COLL.find(query).first();
        return doc;
    }

    public String getIPFSLink(String name) {
        doc = getDocument(this.address);
        Document nftDoc = (Document) doc.get("nfts");
        // System.out.println(nftDoc.keySet());
        String myLink = (String) nftDoc.get(name);
        System.out.println("getIPFSLink:  -> " + myLink);
        
        if(myLink == null) {
            System.out.println("getIPFSLink returns null, most likely bc you lowercased before calling OR didnt remove _'s ...");
        }
        return myLink;
    }

    // gets all NFT Names
    public Set<String> getMyNFTNames() {
        Document nftDoc = (Document) doc.get("nfts");
        if (nftDoc == null) {
            return null;
        }
        return nftDoc.keySet();
    }

    public Map<String, ArrayList<String>> sortNFts() {
        // useful for the GUI
        Map<String, ArrayList<String>> OurNFTs = new HashMap<String, ArrayList<String>>();

        if (!(doc.keySet().contains("nfts"))) {
            System.out.println("This document does not have any NFTs");
            return null;
        }

        Document nfts = (Document) doc.get("nfts");

        for (String key : nfts.keySet()) {
            // This should work for all NFTs, if not they go into other
            // Future we can regex split at # or last space
            if (key.contains("#")) {
                String[] values = key.split("#"); // ["Oblitus ", "0961"]
                String name = values[0];
                String id = "#" + values[1]; // we need to add back in for requesting since we split at it

                // System.out.println(name + " " + id);

                if (!OurNFTs.containsKey(name)) {
                    ArrayList<String> newList = new ArrayList<String>();
                    OurNFTs.put(name, newList);
                }

                OurNFTs.get(name).add(id);

            } else {

                if (!OurNFTs.containsKey("others")) {
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

    public List<Document> getAllDocsFromCollection(boolean debug) {
        List<Document> documents = (List<Document>) ASSETS_COLL.find().into(new ArrayList<Document>());
        // print them
        if (debug) {
            for (Document document : documents) {
                System.out.println(document);
            }
        }
        return documents;
    }

    public static List<String> getAllSavedNFTFilenames() {
        // List<Document> documents = IMAGES_COLL.find().into(new
        // ArrayList<Document>());
        // System.out.println("Size:" + documents.size());

        // List<String> keys = new ArrayList<>();
        // for (Document document : documents) {
        // keys.add(document.get("name").toString());
        // }
        // return keys.toArray(new String[0]);
        List<String> s = new ArrayList<>();
        try {

            // Create a gridFSBucket
            GridFSBucket gridBucket = GridFSBuckets.create(ImageDBGridFS);
            GridFSFindIterable files = gridBucket.find();
            for (GridFSFile file : files) {
                s.add(file.getFilename());
            }

        } catch (Exception e) {
            System.out.println("Error with getting all placed NFTs");
        }

        return s;
    }

    // === In game stuff ===
    // When a user clicks on a map, we need to get the IPFS Link, Download to
    // memory, and put on the map
    public static BufferedImage downloadNFT(String link) {
        // from ImageMapDownload (Download & place should be all in 1)

        // check if nftName is in the database, if so just return that

        // May just be able to do a null check, and show without saving to file?
        URL srcURL = null;
        BufferedImage image = null;
        try {
            srcURL = new URL(link);
            java.net.URLConnection connection = srcURL.openConnection();
            connection.setRequestProperty("User-Agent", "CraftNFTs/0");
            if (((HttpURLConnection) connection).getResponseCode() != 200) {
                System.out.println(String.format("Download failed, HTTP Error code %d.",
                        ((HttpURLConnection) connection).getResponseCode()));
                return null;
            }
            System.out.println(connection.getHeaderField("Content-type"));

            try (InputStream str = connection.getInputStream()) {
                image = ImageIO.read(str); // FUTURE: compress this to JPG (RGB), see if I can condense

                // If this is a video, I assume it fails?
                image = pngToJPEG(image);
                image = changeImageQuality(image, 0.7f);
            }

        } catch (IOException e) {
            e.printStackTrace();
        }

        // Add NFT Cache here in future?

        return image;
    }

    private static BufferedImage changeImageQuality(BufferedImage image, float quality) throws IOException {
        // save jpeg image with specific quality. "1f" corresponds to 100% , "0.7f"
        // corresponds to 70%

        ImageWriter jpgWriter = ImageIO.getImageWritersByFormatName("jpg").next();
        ImageWriteParam jpgWriteParam = jpgWriter.getDefaultWriteParam();
        jpgWriteParam.setCompressionMode(ImageWriteParam.MODE_EXPLICIT);
        jpgWriteParam.setCompressionQuality(quality);

        // create image output stream
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        jpgWriter.setOutput(ImageIO.createImageOutputStream(baos));
        IIOImage outputImage = new IIOImage(image, null, null);
        jpgWriter.write(null, outputImage, jpgWriteParam);
        jpgWriter.dispose();

        // convert jpgWriter to BufferedImage
        InputStream in = new ByteArrayInputStream(baos.toByteArray());
        BufferedImage newImage = ImageIO.read(in);
        return newImage;
    }

    private static BufferedImage pngToJPEG(BufferedImage image) {
        BufferedImage newImage = new BufferedImage(image.getWidth(), image.getHeight(), BufferedImage.TYPE_INT_RGB);
        // create a graphics object
        Graphics2D g2 = newImage.createGraphics();
        // draw the image
        g2.drawImage(image, 0, 0, null);
        // dispose of the graphics object
        g2.dispose();
        return newImage;
    }

    public static void uploadAsyncToMongo(String nftName, BufferedImage bImage) {
        // Give this is async, ensure we let the user place the cached version before.

        ObjectId fileId = getObjectIDFromName(nftName);
        if (fileId != null) {
            System.out.println(nftName + " was already in mongodb, skipping");
            return;
        }

        System.out.println("Uploading Image to MongoDB as Async...");

        // adding to cache incase its not already there
        NFTCache.addImage(nftName, bImage);

        // TODO Is this a good idea?
        Bukkit.getScheduler().runTaskAsynchronously(ImageMaps.getPlugin(), () -> {
            try {
                // Create a gridFSBucket
                GridFSBucket gridBucket = GridFSBuckets.create(ImageDBGridFS);

                // converts image -> input stream to save to MongoDB
                ByteArrayOutputStream os = new ByteArrayOutputStream();
                ImageIO.write(bImage, "jpg", os);
                InputStream inStream = new ByteArrayInputStream(os.toByteArray());

                // upload it async

                // Create some customize options for the details that describes
                // the uploaded image
                GridFSUploadOptions uploadOptions = new GridFSUploadOptions()
                        .chunkSizeBytes(2048)
                        .metadata(new Document("type", "image").append("content_type", "image/jpg"));

                gridBucket.uploadFromStream(nftName, inStream, uploadOptions);
                System.out.println("Uploaded " + nftName + " to MongoDB completed (async)");
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                // mongoClient.close();
            }
        });
    }

    private static ObjectId getObjectIDFromName(String nftName) {
        System.out.println("Getting object id of " + nftName + " in the database if it is there.");
        ObjectId fileId = null;
        try {

            // Create a gridFSBucket
            GridFSBucket gridBucket = GridFSBuckets.create(ImageDBGridFS);

            GridFSFindIterable iter = gridBucket.find(Filters.eq("filename", nftName));
            for (GridFSFile file : iter) {
                fileId = file.getObjectId();
            }

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            // mongoClient.close();
        }
        return fileId;
    }

    public static BufferedImage loadFromMongo(String fileName) {
        System.out.println("Calling download...");

        BufferedImage image = null;
        try {
            GridFSBucket gridBucket = GridFSBuckets.create(ImageDBGridFS);

            // Create in memory output stream
            ByteArrayOutputStream os = new ByteArrayOutputStream();
            gridBucket.downloadToStream(fileName, os);
            // os.close();
            image = ImageIO.read(new ByteArrayInputStream(os.toByteArray()));

        } catch (Exception e) {
            System.out.println(e.getMessage()); // No file found with the filename: cousin #320 and revision: -1
            // e.printStackTrace();
        } finally {
            // mongoClient.close();
        }
        return image;
    }

    // Will try gridfs if this doesnt work
    // https://kb.objectrocket.com/mongo-db/how-to-save-an-image-in-mongodb-using-java-394
    // public void saveImageIOToMongoDB(BufferedImage image, String name) {
    // byte[] imageBytes = toByteArray(image, "png");

    // Document doc = new Document("name", name);
    // // check if this exist in PLACED_IMAGES collection
    // if(IMAGES_COLL.find(doc).first() != null) {
    // // doc already exist, we are not saving it
    // System.out.println("This image already exists in the database");
    // return;
    // }

    // String imgToSave = encodeBase64String(imageBytes);
    // doc.append("image", imgToSave);
    // IMAGES_COLL.insertOne(doc);
    // }

    // public static BufferedImage loadImageFromMongDB(String name) {
    // // load images which are on the server (useful for reboots)

    // Document query = new Document("name", name);
    // // check if this exist in PLACED_IMAGES collection
    // Document doc = IMAGES_COLL.find(query).first();
    // if(doc == null) {
    // System.out.println("This image is not found in the collection! name: " +
    // name);
    // return null;
    // }

    // String myImgString = (String) doc.get("image");
    // System.out.println("ImageThings.java loadImageFromMongDB: " + name + " ");
    // // System.out.println("Image String: " + myImgString);
    // // decode to bvytes
    // byte[] decodedBytes = decodeBase64String(myImgString);
    // // return decodedImage;
    // return toBufferedImage(decodedBytes);
    // }

    // convert BufferedImage to byte[] to save in MongoDB
    // https://mkyong.com/java/how-to-convert-bufferedimage-to-byte-in-java/
    // private byte[] toByteArray(java.awt.image.BufferedImage image, String
    // format){
    // ByteArrayOutputStream baos = new ByteArrayOutputStream();
    // try {
    // ImageIO.write(image, format, baos);
    // } catch (IOException e) {
    // e.printStackTrace();
    // }
    // byte[] bytes = baos.toByteArray();
    // return bytes;

    // }
    // convert byte[] to BufferedImage
    // private static java.awt.image.BufferedImage toBufferedImage(byte[] bytes) {

    // InputStream is = new ByteArrayInputStream(bytes);
    // java.awt.image.BufferedImage bi = null;
    // try {
    // bi = ImageIO.read(is);
    // } catch (IOException e) {
    // e.printStackTrace();
    // }
    // return bi;

    // }
    // private static String encodeBase64String(byte[] binaryData) {
    // return Base64.getEncoder().encodeToString(binaryData);
    // }
    // private static byte[] decodeBase64String(String base64String) {
    // return Base64.getDecoder().decode(base64String);
    // }

}
