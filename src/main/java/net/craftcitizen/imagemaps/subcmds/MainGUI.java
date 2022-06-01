package net.craftcitizen.imagemaps.subcmds;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Material;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.player.AsyncPlayerChatEvent;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;

import de.craftlancer.core.util.MessageLevel;
import de.craftlancer.core.util.MessageUtil;
import net.craftcitizen.imagemaps.ImageMaps;
import net.craftcitizen.imagemaps.db.ImageThings;
import net.craftcitizen.imagemaps.rendering.ImageMap;

import java.io.File;
import java.util.*;

// change to our GUI thing in the future
public class MainGUI extends ImageMapSubCommand implements Listener {

    // public Inventory PLAYER_NFT_INV;
	private static final String TITLE = "My NFTs";
    private String mySubMenuName = ""; // the name of the parent NFT collection

    // use his command thing
    public MainGUI(ImageMaps plugin) {
        super("craftnfts.gui", plugin, false);
		// register bukkit listener
		Bukkit.getPluginManager().registerEvents(this, plugin);
    }

    public Inventory initCreateInv() {
		Inventory PLAYER_NFT_INV = Bukkit.createInventory(null, 6*9, TITLE); 

		int slotIdx = 0;

        List<String> lore = new ArrayList<String>();
        lore.add("");	

        ImageThings iT = new ImageThings(ImageMaps.MY_ADDRESS);
        // add a null check here / boolean check if user has any documents?

        Map<String, ArrayList<String>> myNFTSections = iT.sortNFts();
        for(String key : myNFTSections.keySet()) {
            createDisplay(PLAYER_NFT_INV, new ItemStack(Material.MAP, 1), slotIdx, key, lore);
            slotIdx += 1;
        }    
        
        return PLAYER_NFT_INV;
	}

	public Inventory createSubInv() {
		Inventory SUB_NFT_INV = Bukkit.createInventory(null, 6*9, mySubMenuName); 

		int slotIdx = 0;

        List<String> lore = new ArrayList<String>();
        lore.add("");	

        ImageThings iT = new ImageThings(ImageMaps.MY_ADDRESS);
        // add a null check here / boolean check if user has any documents?

        ArrayList<String> myNFTSections = iT.sortNFts().get(mySubMenuName);

        for(String nftName : myNFTSections) {
			if(!mySubMenuName.equalsIgnoreCase("others")) {
				// "cousins "+"#320"
				createDisplay(SUB_NFT_INV, new ItemStack(Material.MAP, 1), slotIdx, mySubMenuName + nftName, lore);
			} else {
				createDisplay(SUB_NFT_INV, new ItemStack(Material.MAP, 1), slotIdx,  nftName, lore);
			}			
			
            slotIdx += 1;
        }    
        
        return SUB_NFT_INV;
	}

	public static void createDisplay(Inventory inv, ItemStack itemStack, int Slot, String name, List<String> list) { //
		ItemStack item = itemStack;
		ItemMeta meta = item.getItemMeta();
		meta.setDisplayName(color(name));			

		ArrayList<String> Lore = new ArrayList<String>();
		if(list.size() > 0) {
			for(String l : list) {
				Lore.add(color(l));
			}
		}
		meta.setLore(Lore);		
		
		item.setItemMeta(meta);

		inv.setItem(Slot, item); 

	}


	@EventHandler
	public void onInventoryClick(InventoryClickEvent event) {	
		ItemStack clicked = event.getCurrentItem();
		if(clicked == null || !clicked.hasItemMeta()) {return;}
		Player p = (Player) event.getWhoClicked();
		String DisplayName = clicked.getItemMeta().getDisplayName();
		
		
		if(event.getView().getTitle().equalsIgnoreCase(TITLE)) {
			System.out.println("Clicked: " + DisplayName + " " + clicked.getType() + " in MainGUI.java for ImageMaps (init Inv)!");
			event.setCancelled(true);	
			mySubMenuName = stripColor(DisplayName); // TODO Strip color here, but not spacing
			System.out.println("Set my sub menu name as "+ mySubMenuName);
			p.closeInventory();

			// open sub panel for selecting the NFt you want to place
			p.openInventory(createSubInv());
			return;

		} else if(event.getView().getTitle().equalsIgnoreCase(mySubMenuName)) {			
			System.out.println("Clicked: " + DisplayName + " in MainGUI.java for ImageMaps (subMenuName)!");
			// download it from the players wallet thing to the IMAGES collection
			ImageThings im = new ImageThings(ImageMaps.MY_ADDRESS);	
			String ipfsLink = im.getIPFSLink(DisplayName);			
			java.awt.image.BufferedImage bImg = ImageThings.downloadNFT(ipfsLink);

			DisplayName = DisplayName.toLowerCase(); System.out.println("Lowercased " + DisplayName + " since we have to save it like that...");
        	im.saveImageIOToMongoDB(bImg, DisplayName);

			// open up sub GUI here for 1x1, 2x2, 3x3
			event.setCancelled(true);
			p.closeInventory();
			// Allow placement
			// run command for player
			System.out.println("Running place map command for player as 2x2");
			p.performCommand("nfts place " + DisplayName.replace(" ", "_") + " 2x2");
			return;
		}
	}

    private static String color(String msg) {
        return ChatColor.translateAlternateColorCodes('&', msg);
    }

	private static String stripColor(String msg) {
		return ChatColor.stripColor(color(msg));
	}

	@Override
	protected String execute(CommandSender sender, Command arg1, String arg2, String[] arg3) {
		if (!checkSender(sender)) {
            MessageUtil.sendMessage(getPlugin(), sender, MessageLevel.WARNING, "You can't run this command.");
            return null;
        }
		
		Player p = (Player) sender;		
		p.openInventory(initCreateInv());
		return null;
	}

	@Override
	public void help(CommandSender arg0) {
		// TODO Auto-generated method stub
		
	}


}
