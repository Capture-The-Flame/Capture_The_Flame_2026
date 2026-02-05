let currentId = 1;
let started = false;

function startApp() {
  document.getElementById("landing").classList.add("hidden");
  document.getElementById("app").classList.remove("hidden");
  started = true;
  loadProfile();
}

async function loadProfile() {
  if (!started) return;

  const res = await fetch(`/profile/${currentId}`);
  const p = await res.json();

  if (!p) {
    document.getElementById("app").classList.add("hidden");
    document.getElementById("landing").classList.remove("hidden");
    currentId = 1; 
    started = false;
    return;
  }

  document.getElementById("photo").src = `/images/${p.photo}`;
  document.getElementById("name").innerText = `${p.name}, ${p.age}`;
  document.getElementById("bio").innerText = p.bio;
  document.getElementById("interests").innerText = p.interests;
}

async function swipe(action) {
  await fetch("/swipe", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id: currentId })
  });

  currentId++;
  // if > 5, reset to 1
  if (currentId > 5) {
    document.getElementById("app").classList.add("hidden");
    document.getElementById("landing").classList.remove("hidden");
    currentId = 1; // Reset the ID so the game starts over from the first person
    started = false;
    return;
  }
  loadProfile();
}

// Make functions available globally
window.startApp = startApp;
window.swipe = swipe;