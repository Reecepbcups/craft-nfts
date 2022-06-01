# Craft NFTs

TODO:
- Take GUI from https://github.com/zDevelopers/ImageOnMap

Database:
- GridFS  (https://www.mongodb.com/docs/drivers/java/sync/v4.3/fundamentals/gridfs/#std-label-gridfs-create-bucket)
- Image Compression (JPG, 75%)
- Do we need to reload maps on start? If map data is already saved to server, then no. Just new ones

- Remove toLowerCase for NFT names. We want absolute
- add wallet checks when placing / trying to download

```
/image place <NFT_Name> 1x1
- checks if you own that NFT, or auto populate with your keySet
- 1x1, 2x2, 3x3 are the biggest normal players can do.
```


Comamands:
- /imagemap download test link
- /imagemap place test true true false 1x1

- /imagemap info test


## Usage
In order for you use place images they must be present in the `images` folder. You can either put them
there via FTP or just copying it, or by using the plugin's download command, allowing you to access
images from the Internet.

To place images just run the `/imagemap place` command and right click the block that should be the
upper left corner of the image (based on your perspective).

Images will by default split into 128x128 pixel sub-images to fit on a map. The image may be scaled via
command parameters, however **it is recommended to prepare correctly scaled images**.

### Commands
* /imagemap place &lt;filename> [frameInvisible] [frameFixed] [frameGlowing] [size]
  * Starts the placement process
  * frameInvisible and frameFixed are only available on 1.16+
  * frameGlowing is only available on 1.17+
* /imagemap download &lt;filename> &lt;sourceURL>
  * downloads an image from the given URL into the `images` folder
* /imagemap delete &lt;filename>
  * deletes an image from the `images` folder
* /imagemap info &lt;filename>
  * prints info, such as resolution and expected size
* /imagemap reload &lt;filename>
  * reloads an image, to be used when the image file changed
* /imagemap list [page]
  * lists all images in the `images` folder
* /imagemap help [command]
  * prints help for commands
  
### Permissions
`imagemaps.*` - grants access to all permissions  
`imagemaps.place` - grants access to /imagemap place command  
`imagemaps.download` - grants access to /imagemap download command  
`imagemaps.delete` - grants access to /imagemap delete command  
`imagemaps.info` - grants access to /imagemap info command  
`imagemaps.list` - grants access to /imagemap list command  
`imagemaps.reload` - grants access to /imagemap reload command  
`imagemaps.help` - grants access to /imagemap help command  
`imagemaps.toggleFixed` - allows to toggle the "fixed" state of frames with a wooden hoe  
`imagemaps.toggleVisible` - allows to toggle the "visible" state of frames with a wooden hoe  

All permissions are default true for OPs.


## Maven
You will need to [configure your environment to access GitHub repositories](https://docs.github.com/en/packages/using-github-packages-with-your-projects-ecosystem/configuring-apache-maven-for-use-with-github-packages).

```
<repository>
  <id>github</id>
  <name>ImageMaps repository</name>
  <url>https://maven.pkg.github.com/SydMontague/ImageMaps</url>
</repository>
```
```
<dependency>
  <groupId>net.craftcitizen</groupId>
  <artifactId>imagemaps</artifactId>
  <version>1.0.1</version>
</dependency>
```

## Contact 
* Discord: SydMontague#8056
* directly on GitHub
* E-Mail: sydmontague@web.de
* Spigot: https://www.spigotmc.org/members/sydmontague.37699/

This plugin has been developed for the [CraftCitizen](https://craftcitizen.net) survival Minecraft server.