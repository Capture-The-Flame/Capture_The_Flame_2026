const express = require("express");
const sqlite3 = require("sqlite3").verbose();

const app = express();
app.use(express.json());
app.use(express.static("public"));

const db = new sqlite3.Database(":memory:");

db.serialize(() => {
    db.run(`
        CREATE TABLE profiles (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        bio TEXT,
        interests TEXT,
        photo TEXT,
        private_note TEXT
        )
    `);
    const profiles = [
        ["Alice", 21, "Matcha over coffee ☕ Sunsets & long walks", "Hiking, journaling, cats", "alice.jpg", "flame{love_is_"],
        ["Ben", 23, "Gym rat. Probably smarter than your ex.", "Powerlifting, nutrition", "ben.jpg", "never_sql_"],
        ["Chloe", 22, "Thrifted outfits > fast fashion", "Photography, film", "chloe.jpg", "safe_"],
        ["Dylan", 24, "Quiet until you get to know me", "Vinyl, cold brew", "dylan.jpg", "when_you_"],
        ["Eve", 25, "I know things. You’ll find out 😉", "Puzzles, traveling", "eve.jpg", "trust_input}"]
    ];

    const stmt = db.prepare(
    "INSERT INTO profiles (name, age, bio, interests, photo, private_note) VALUES (?, ?, ?, ?, ?, ?)"
    );
    profiles.forEach(p => stmt.run(p));
    stmt.finalize();
});

// Get next profile
app.get("/profile/:id", (req, res) => {
  db.get(
    "SELECT id, name, age, bio, interests, photo FROM profiles WHERE id = ?",
    [req.params.id],
    (err, row) => res.json(row)
  );
});


// swipe endpoint (!!)
app.post("/swipe", (req, res) => {
  const id = req.body.id;
  const query = `SELECT private_note FROM profiles WHERE id = ${id}`;
  console.log(query);

  db.all(query, [], (err, rows) => {
    if (err) return res.status(500).send(err.message);
    res.json({ result: "swiped", data: rows });
  });
});

app.listen(3000, () => {
  console.log("HeartStrings running on http://localhost:3000");
});
