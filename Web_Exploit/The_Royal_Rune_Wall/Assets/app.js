const runeWall = document.getElementById("runeWall");
const flag = document.getElementById("flag");

function revealScroll() {
  const words = ["flame", "king", "forgot", "innerHTML", "csp"];
  flag.textContent = `🏆 ${words[0]}{the_${words[1]}_${words[2]}_${words[3]}_${words[4]}}`;
  flag.style.display = "block";
}


// User input handler
function engraveRune() {
  const input = document.getElementById("runeInput").value;

  runeWall.innerHTML += `
    <div class="rune">
      🜁 ${input}
    </div>
  `;

  document.getElementById("runeInput").value = "";
}
