const { Client } = require("@jeffe/tankille");
const fs = require("fs");
const { Parser } = require("json2csv");
require("dotenv").config();

const client = new Client();

async function run() {
    await client.login({
        email: process.env.EMAIL,
        password: process.env.PASSWORD,
    });

    const stations = await client.getStations();

    const filteredStations = stations.map((station) => ({
        address: station.address,
        fuels: station.fuels,
        chain: station.chain,
        brand: station.brand,
        price: station.price.map((item) => ({
            tag: item.tag,
            price: item.price,
        })),
    }));

    const json2csvParser = new Parser();
    const csv = json2csvParser.parse(filteredStations);

    fs.writeFile("stations.csv", csv, function (err) {
        if (err) throw err;
        console.log("File saved as stations.csv");
        console.log(filteredStations);
    });
}

run();
