const express = require('express');
const app = express();
const port = 3000;
const Cloudant = require('@cloudant/cloudant');

// Initialize Cloudant connection
function dbCloudantConnect() {
    return new Promise((resolve, reject) => {
        const cloudant = Cloudant({
            url: "https://dbf3cb2c-12e3-4722-a180-7cd9df65617d-bluemix.cloudantnosqldb.appdomain.cloud",
            plugins: {
                iamauth: {
                    iamApiKey: "fE4stiQzvZBSJ6Hmh6KnhWa-s7IVbBJrr4OIgwfOGAio" // Your API key here
                }
            }
        });

        const db = cloudant.use("dealerships");
        resolve(db);
    });
}

let db;

dbCloudantConnect().then((database) => {
    db = database;
}).catch((err) => {
    throw err;
});

app.use(express.json());

// Define a route to get all dealerships with optional state and ID filters
// Define a route to get dealerships with optional state and id filters
app.get('/dealerships/get', (req, res) => {
    const { state, id } = req.query;

    // Prepare the selector based on provided state and/or id
    const selector = {};
    if (state) {
        selector.state = state;
    }
    if (id) {
        selector.id = Number(id); // Convert id to a number
    }
    console.log('Query parameters:', req.query);
    console.log('Selector:', selector);
    // Query the Cloudant database using the selector
    db.find({
        selector: selector
    }).then(result => {
        // Send the fetched data as a JSON response
        res.json(result.docs);
    }).catch(error => {
        console.error('Error fetching data:', error);
        res.status(500).json({ error: 'An error occurred while fetching data' });
    });
});

// Start the Express server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});

