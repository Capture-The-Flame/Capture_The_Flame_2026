#include <iostream>
#include <string>
#include <algorithm>
#include <cctype>

using namespace std;

// Function to display the banner
void displayBanner() {
    cout << "\n";
    cout << "=========================================\n";
    cout << "         THE KING'S SECRET SCROLL \n";
    cout << "    A Beginner Cryptography Challenge\n";
    cout << "=========================================\n\n";
}

// Function to display the story
void displayStory() {
    cout << " THE STORY:\n";
    cout << "─────────────────────────────────────────\n";
    cout << "A royal messenger was caught sneaking through\n";
    cout << "the castle gates carrying a sealed scroll\n";
    cout << "addressed to the king. The scroll's text makes\n";
    cout << "no sense — perhaps the scribe used a secret\n";
    cout << "code to protect its message.\n\n";
    cout << "Can you decipher what the scribe was trying\n";
    cout << "to tell His Majesty?\n";
    cout << "─────────────────────────────────────────\n\n";
}

// Function to display the encrypted scroll
void displayScroll() {
    cout << " THE ENCRYPTED SCROLL:\n";
    cout << "═════════════════════════════════════════\n";
    cout << "Uryyb, zl sevraqf! Gur xvat arrqf lbh gb\n";
    cout << "qrpbqr guvf zrffntr.\n";
    cout << "Abg nyy vf nf vg nccrnef — fbhaqf yvxr na\n";
    cout << "rkcerffngr bs fbzrglcr bs fvtangher.\n";
    cout << "Unir n avpr qnl va gur zrqvnaf, naq erzrzore:\n";
    cout << "Synt{Fvzcyr_Pnrfne_Fuvsg}\n";
    cout << "═════════════════════════════════════════\n\n";
}

// Function to display hint
void displayHint() {
    cout << "\n HINT:\n";
    cout << "─────────────────────────────────────────\n";
    cout << "The royal scribe was known for shifting\n";
    cout << "letters — 13 places, to be exact.\n";
    cout << "─────────────────────────────────────────\n\n";
}

// Function to perform ROT13 decoding
string rot13(const string& text) {
    string result = text;
    
    for (size_t i = 0; i < result.length(); i++) {
        char c = result[i];
        
        if (isalpha(c)) {
            char base = isupper(c) ? 'A' : 'a';
            result[i] = static_cast<char>((c - base + 13) % 26 + base);
        }
    }
    
    return result;
}

// Function to convert string to uppercase
string toUpper(string str) {
    transform(str.begin(), str.end(), str.begin(), ::toupper);
    return str;
}

// Function to validate the flag
bool validateFlag(const string& userFlag, const string& correctFlag) {
    return toUpper(userFlag) == toUpper(correctFlag);
}

// Function to display the decoded message (for admin/testing purposes)
void displaySolution() {
    string encrypted = "Uryyb, zl sevraqf! Gur xvat arrqf lbh gb qrpbqr guvf zrffntr. Abg nyy vf nf vg nccrnef — fbhaqf yvxr na rkcerffngr bs fbzrglcr bs fvtangher. Unir n avpr qnl va gur zrqvnaf, naq erzrzore: Synt{Fvzcyr_Pnrfne_Fuvsg}";
    
    cout << "\n DECODED MESSAGE:\n";
    cout << "─────────────────────────────────────────\n";
    cout << rot13(encrypted) << "\n";
    cout << "─────────────────────────────────────────\n\n";
}

// Function to display menu
void displayMenu() {
    cout << "MENU OPTIONS:\n";
    cout << "─────────────────────────────────────────\n";
    cout << "1. View the encrypted scroll\n";
    cout << "2. Get a hint\n";
    cout << "3. Submit your flag\n";
    cout << "4. View solution (for testing)\n";
    cout << "5. Exit\n";
    cout << "─────────────────────────────────────────\n";
    cout << "Enter your choice: ";
}

int main() {
    const string CORRECT_FLAG = "flame{Simple_Caesar_Shift}";
    int attempts = 0;
    bool solved = false;
    
    displayBanner();
    displayStory();
    
    while (!solved) {
        displayMenu();
        
        int choice;
        cin >> choice;
        cin.ignore(); // Clear the newline from input buffer
        
        cout << "\n";
        
        switch (choice) {
            case 1:
                displayScroll();
                break;
                
            case 2:
                displayHint();
                break;
                
            case 3: {
                cout << " SUBMIT YOUR FLAG\n";
                cout << "─────────────────────────────────────────\n";
                cout << "Enter the flag (format: flame{...}): ";
                
                string userFlag;
                getline(cin, userFlag);
                
                attempts++;
                
                if (userFlag.empty()) {
                    cout << "\n Please enter a flag!\n\n";
                    break;
                }
                
                if (validateFlag(userFlag, CORRECT_FLAG)) {
                    cout << "\n";
                    cout << "═════════════════════════════════════════\n";
                    cout << "         CONGRATULATIONS! \n";
                    cout << "═════════════════════════════════════════\n";
                    cout << "You've successfully decoded the King's\n";
                    cout << "Secret Scroll!\n\n";
                    cout << "The message revealed:\n";
                    cout << "\"Hello, my friends! The king needs you\n";
                    cout << "to decode this message...\"\n\n";
                    cout << "Correct Flag: " << CORRECT_FLAG << "\n";
                    cout << "Total Attempts: " << attempts << "\n";
                    cout << "═════════════════════════════════════════\n\n";
                    solved = true;
                } else if (toUpper(userFlag).find("SIMPLE") != string::npos ||
                           toUpper(userFlag).find("CAESAR") != string::npos ||
                           toUpper(userFlag).find("SHIFT") != string::npos) {
                    cout << "\n You're on the right track!\n";
                    cout << "Check your flag format carefully.\n";
                    cout << "(Note: Flag is case-sensitive)\n";
                    cout << "Attempts: " << attempts << "\n\n";
                } else {
                    cout << "\n Incorrect flag. Try again!\n";
                    cout << "Attempts: " << attempts << "\n";
                    cout << "\nTip: Have you tried decoding the entire\n";
                    cout << "message first?\n\n";
                }
                break;
            }
                
            case 4:
                displaySolution();
                break;
                
            case 5:
                cout << "Thanks for playing! Good luck, brave solver! 🗡️\n\n";
                return 0;
                
            default:
                cout << "Invalid choice. Please try again.\n\n";
        }
    }
    
    cout << "Challenge completed! Exiting...\n";
    cout << " May the kingdom be forever grateful! \n\n";
    
    return 0;
}
