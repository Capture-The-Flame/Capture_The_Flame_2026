// Page navigation
function showPage(page) {
    if (page === 'landing') {
        document.getElementById('landingPage').style.display = 'block';
        document.getElementById('artifactsPage').style.display = 'none';
    } else if (page === 'artifacts') {
        document.getElementById('landingPage').style.display = 'none';
        document.getElementById('artifactsPage').style.display = 'block';
    }
}

// Smooth scroll to contributors
document.querySelectorAll('a[href="#contributors"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector('#contributors').scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Password checking with obfuscated secret
function checkPassword() {
    const input = document.getElementById('passwordInput').value;
    const errorMsg = document.getElementById('errorMessage');
    const secretReveal = document.getElementById('secretReveal');
    
    // Obfuscated password check (password is "72901")
    const p = String.fromCharCode(55, 50, 57, 48, 49);
    
    if (input === p) {
        // Construct the secret message dynamically - "flame{open_the_box}"
        const s1 = String.fromCharCode(102, 108, 97, 109, 101);
        const s2 = String.fromCharCode(123);
        const s3 = String.fromCharCode(111, 112, 101, 110);
        const s4 = String.fromCharCode(95);
        const s5 = String.fromCharCode(116, 104, 101);
        const s6 = String.fromCharCode(95);
        const s7 = String.fromCharCode(98, 111, 120);
        const s8 = String.fromCharCode(125);
        
        const secretMessage = s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8;
        
        document.getElementById('secretText').textContent = secretMessage;
        secretReveal.classList.add('show');
        errorMsg.style.display = 'none';
        document.getElementById('passwordInput').value = '';
    } else {
        errorMsg.style.display = 'block';
        secretReveal.classList.remove('show');
    }
}

// Disable right-click context menu
document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
    return false;
});

// Disable F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+U
document.addEventListener('keydown', function(e) {
    // F12
    if (e.keyCode === 123) {
        e.preventDefault();
        return false;
    }
    // Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+U
    if (e.ctrlKey && e.shiftKey && (e.keyCode === 73 || e.keyCode === 74)) {
        e.preventDefault();
        return false;
    }
    // Ctrl+U (View Source)
    if (e.ctrlKey && e.keyCode === 85) {
        e.preventDefault();
        return false;
    }
});

// Enter key support
document.getElementById('passwordInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        checkPassword();
    }
});