// npm i mongoose
const {MongoClient} = require('mongodb');

const uri = "mongodb://root:akashmongodb19pass@782sk60c31ell6dbee3ntqc9lo.ingress.provider-2.prod.ewr1.akash.pub:31543/NFTs?authSource=admin";

async function main(address) {
	const client = new MongoClient(uri);
 
    try {
        // Connect to the MongoDB cluster
        await client.connect();
 
        // Make the appropriate DB calls
        // await listDatabases(client);

        const res = await isDocumentInCollection(client, "NFTs", "OWNERS", {address: address});
        console.log(res);
 
    } catch (e) {
        console.error(e);
    } finally {
        await client.close();
    }
}

async function listDatabases(client){
    databasesList = await client.db().admin().listDatabases(); 
    console.log("Databases:");
    databasesList.databases.forEach(db => console.log(` - ${db.name}`));
};

async function isDocumentInCollection(client, dbName, collectionName, document) {
    const db = client.db(dbName);
    const collection = db.collection(collectionName);
    const result = await collection.findOne(document);
    return result.address !== null;
}

main("craft12wdcv2lm6uhyh5f6ytjvh2nlkukrmkdk4qt20v").catch(console.error);