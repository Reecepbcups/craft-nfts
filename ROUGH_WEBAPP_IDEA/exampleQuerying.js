// https://npm.io/package/convert-bech32-address
var converter = require('convert-bech32-address');

// const https = require("https");
const request = require('request');
const axios = require('axios');

// we get this from keplr
const cosmosAddr = "cosmos12wdcv2lm6uhyh5f6ytjvh2nlkukrmkdk5kca2s"; // some random person
const prefixes = ["stars", "omniflix"]; // "secret" in the future has to be its own bc not 118
// const myAddressToQuery = [];

var allMyNFTs = {};

// taken from FINAL.py in NFT-POCS
for (const prefix of prefixes) {

    const address = converter.lookup(cosmosAddr, prefix);

    if (address.startsWith("stars")) {
        queryStargazeNFTs(address).then(data => {
            for(const nft of data) {
                // console.log(nft[0], nft[1]);
                // allMyNFTs.set(nft[0], nft[1]);
            }  
        });

    } else if (address.startsWith("omniflix")) {
        queryOmniflixNFTs(address).then(data => {
            for (const nft of data) {
                // allMyNFTs[name] = name;
                // console.log(nft);
                // allMyNFTs.set(nft[0], nft[1]);
            }
        });
    }
}
// Then we need to save this to its mongodb collection as:
/*
{
    "address": "cosmos12wdcv2lm6uhyh5f6ytjvh2nlkukrmkdk5kca2s",
    "nfts": {
        "StarNots #557": "https://ipfs.stargaze.zone/ipfs/QmYmaZjwzDPirPqZdQYLFzA4NQ8GNTf7VKe5jBsiz9diQk/557.png",
        "Sunnyside Nightlife #503": "https://ipfs.io/ipfs/bafybeidkkvxfkjyuvg53iby65rkpfvjm43mrcokazzhsiad7qwhgeuxdse/images/503.png"
    }, 
    "realestate": {
        -- Same format as NFTs, we will just query a CRAFT/onft module like: `queryCraftNFTs`
    }
}
*/


async function queryStargazeNFTs(starsWallet) {
    const API = `https://nft-api.stargaze-apis.com/api/v1beta/profile/${starsWallet}/nfts`
    // console.log(API);

    const value = await axios.get(API);
    const JSON = value.data;

    const allowedExtensions = [".png", ".jpg", ".jpeg"];
    var myStargazeNFTs = new Map();

    for (const nftObject of JSON) {
        const myName = nftObject['name'];
        const myImage = nftObject['image'];
        // console.log(myName, myImage);
        for (const extension of allowedExtensions) {
            if (myImage.endsWith(extension)) {
                // console.log(myName, myImage);                   
                // myStargazeNFTs[myName] = myImage;
                myStargazeNFTs.set(myName, myImage);
            }
        }
    }
    return myStargazeNFTs;
}


async function queryOmniflixNFTs(omniflixWallet) {
    const API = `https://data-api.omniflix.studio/nfts?owner=${omniflixWallet}`
    // https://data-api.omniflix.studio/nfts?owner=omniflix12wdcv2lm6uhyh5f6ytjvh2nlkukrmkdkfgfyaw

    const value = await axios.get(API);
    // log value keys
    // console.log(value.result);
    const JSON = value;

    const allowedExtensions = [".png", ".jpg", ".jpeg"];
    var myOmniflixNFTs = new Map();

    for (const nftObject of JSON) {
        const myName = nftObject['name'];
        const myImage = nftObject['media_uri'];
        // console.log(myName, myImage);
        for (const extension of allowedExtensions) {
            if (myImage.endsWith(extension)) {
                // console.log(myName, myImage);                   
                // myStargazeNFTs[myName] = myImage;
                myOmniflixNFTs.set(myName, myImage);
            }
        }
    }
    return myOmniflixNFTs;
}


// 
// 
// for(const nftObject of body) {
//     const myName = nftObject['name'];
//     const myImage = nftObject['image'];        

//     
// }   