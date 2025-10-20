const express = require('express');
const app = express();
const port = 3000; 

const CORRECT_USER = process.env.CTF_USERNAME;
const CORRECT_PASS = process.env.CTF_PASSWORD;
const CTF_FLAG = process.env.CTF_FLAG;


app.use(express.json());
app.use(express.static('public'));

// This receives the username and password from the browser.
app.post('/api/login', (req, res) => {
    // req.body contains the JSON data sent from the browser
    const { username, password } = req.body;

    console.log(`Attempting login for user: ${username}`);

    // Check credentials on the server
    if (username === CORRECT_USER && password === CORRECT_PASS) {
        // Send success response with the flag
        res.json({ 
            success: true, 
            message: "Login successful!",
            flag: CTF_FLAG 
        });
    } else {
        // Send failure response
        res.status(401).json({ 
            success: false, 
            message: "Invalid credentials. Please try again." 
        });
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
    console.log(`Press CTRL+C to stop the server.`);
});