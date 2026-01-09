#include <iostream>
#include <string>
#include <algorithm>
#include <cctype>
#include <limits>   // For numeric_limits<streamsize>

using namespace std;

// Apply ROT13 cipher to the text.
string rot13(const string& text) {
    string result = text;

    for (char& ch : result) {
        if (isupper(ch)) {
            ch = ((ch - 'A' + 13) % 26) + 'A';
        } else if (islower(ch)) {
            ch = ((ch - 'a' + 13) % 26) + 'a';
        }
    }

    return result;
}

// Reverse the entire string.
string reverseString(const string& text) {
    string result = text;
    reverse(result.begin(), result.end());
    return result;
}

// Display the challenge prompt
void displayChallenge() {

    cout << "\n                      KNIGHT'S OATH                     " << endl;
    cout << "============================================================\n" << endl;

    // Ciphertext for FLAME{THE_DRAGON_GRANDMASTER_FIGHTER}
    // ROT13: SYNZR{GUR_QENTBA_TENAQZNFGRE_SVTUGRE}
    // Reverse: }ERGUTVS_ERGFNZQANET_ABTNEQ_RUG{RZNYS
    cout << "The knight's secret oath is engraved on the stone:" << endl;
    cout << "  }ERGUTVS_ERGFNZQANET_ABTNEQ_RUG{RZNYS\n" << endl;

    cout << "Recover the hidden message and submit the flag in the form:" << endl;
    cout << "  FLAME{...}\n" << endl;

    cout << "============================================================\n" << endl;
}


// Interactive mode - let user try to solve
void interactiveMode() {
    // Clear leftover newline from previous input
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    string ciphertext = "}ERGUTVS_ERGFNZQANET_ABTNEQ_RUG{RZNYS";
    string userInput;

    cout << "\n--- INTERACTIVE SOLVING MODE ---\n" << endl;

    cout << "The ciphertext is: " << ciphertext << "\n" << endl;

    // Step 1: Reverse
    cout << "Enter the reversed string: ";
    getline(cin, userInput);

    string correctReverse = reverseString(ciphertext);
    if (userInput == correctReverse) {
        cout << "Correct. The reversed string is: " << correctReverse << "\n" << endl;
    } else {
        cout << "Incorrect. Try again.\n" << endl;
        return;
    }

    // Step 2: ROT13
    cout << "Now apply ROT13 to the reversed string." << endl;
    cout << "Enter the final flag: ";
    getline(cin, userInput);

    string correctFlag = rot13(correctReverse);
    if (userInput == correctFlag) {
        cout << "\nCongratulations." << endl;
        cout << "You have recovered the knight's oath." << endl;
        cout << "Flag: " << correctFlag << endl;
    } else {
        cout << "Incorrect. Keep trying." << endl;
    }

    cout << endl;
}

// Display the main menu.
void displayMenu() {
    cout << "\nChoose an option:" << endl;
    cout << "1. View Challenge" << endl;
    cout << "2. Submit Your Solution" << endl;
    cout << "3. Exit" << endl;
    cout << endl;
}

// Main function with interactive menu.
int main() {
    cout << "============================================================" << endl;
    cout << "                    KNIGHT'S OATH CTF CHALLENGE              " << endl;
    cout << "============================================================" << endl;

    int choice;

    while (true) {
        displayMenu();
        cout << "Enter your choice (1-3): ";
        cin >> choice;

        if (choice == 1) {
            displayChallenge();

        } else if (choice == 2) {
            interactiveMode();

        } else if (choice == 3) {
            cout << "\nExiting. Farewell, knight." << endl;
            break;

        } else {
            cout << "Invalid choice. Please try again." << endl;
        }
    }

    return 0;
}

