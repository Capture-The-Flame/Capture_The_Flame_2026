#include <iostream>
#include <string>
#include <cctype>
#include <vector>
#include <cstdlib>
#include <ctime> 

using namespace std;

const string ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";


class Session{
    private:
        string key;
        int tries;
        vector<string> keys =  {"CTF", "WICYS", "LOGICA", "UIC"};
    public:
        Session(){
            key = setKey();
            tries = 0;
        }
        
        string setKey(){
            return keys[rand()%2];
        }

        void resetKey(){
            key=setKey();
            cout<< "Key reset!"<<endl;
        }

        string getFlag(string testKey){
            return (key==testKey) ? "Congrats.......flame{woah_u_smart}" : "";
        }

        void increaseTries(){
            tries+=1;

            if(tries>2){
                cout<<"Number of tries exceeded!"<<endl;
                resetKey();
            };
        }

        string buildKey(int length){
            int keyLength = key.length();
            string fullKey; 
            char currLetter;
            int keyIndex=0;
            
            for(int i=0;i<length;i++){
                if(keyIndex == key.length())
                    keyIndex=0;

                currLetter = key.at(keyIndex);
                fullKey.push_back(((char) toupper(currLetter)));
                keyIndex+=1;
            }

            return fullKey;
        }

        char rotate(char text, char key){
            int textPos = ALPHABET.find(text);
            textPos += ALPHABET.find(key);

            if(textPos>25)
                textPos-=26;

            return ALPHABET.at(textPos);
        }

        void cipher(string plaintext){
            int length = plaintext.length();
            string fullKey = buildKey(length);
            string cipher;
            
            for(int i=0;i<length;i++){
                cipher.push_back((char) rotate((char) toupper(plaintext[i]),(char) toupper(fullKey[i])));
            }
            
            cout << "Here is the cipher text: " << cipher << endl;
        }

};

void print_menu(){
    cout << endl;
    cout << "\t1. Convert a plaintext to cipher text" << endl;
    cout << "\t2. Test the flag" << endl;
    cout << "\tx. Quit" << endl;
    cout << "\tSelection: ";
}

bool checkInvalid(string plaintext){
    char* start = &plaintext[0];
    char* end = &plaintext[plaintext.length()-1];

    while(start < end){
        if(ALPHABET.find(*start) == string::npos || ALPHABET.find(*end) == string::npos) 
            return true;
        start+=0x1;
        end-=0x1;
    }
    return false;
}

void convert_plain_text(Session& session){
    string plaintext;
    cout<< "Please enter the plaintext that you want to check: ";
    getline(cin,plaintext);
    if(checkInvalid(plaintext))
        cout << "Please only input text with letters of the alphabet :(" << endl;
    else
        session.cipher(plaintext);
}

void test_for_flag(Session& session){
    string guess;
    cout << "Enter your guess for the key: ";
    getline(cin,guess);
    string output= (session.getFlag(guess));

    if(output==""){
        cout << "Incorrect guess!!" << endl;
        session.increaseTries();
    }
    else{
        cout<<output<<endl;
    }
        
}

void process_result(Session*& session, string decision){
    if(decision=="1")
        convert_plain_text(*session);
    else if(decision=="2")
        test_for_flag(*session);
    else if(decision=="x")
        cout << "App ended...." << endl;
    else
        cout << "Try again..." << endl;
}

int main(){
    srand(time(nullptr));
    cout << endl << "\tWelcome to the Chipper!" << endl;
    cout << "\tHere you will try to find the key out to convert the flag" << endl;
    cout << "\tYour goal is to find out one of the keys being used in this cryptographic simulator!"<<endl;
    cout <<"\tWe are specializing in one specific type of cipher! But beware!! Too many incorrect guesses and the key changes!" << endl;
    cout << "\t===============================================================" << endl;

    string selection = "";
    Session* session = new Session();

    while(selection != "x"){
        print_menu();
        getline(cin,selection);
        cout<<endl;
        process_result(session, selection);
    }

    delete session;
    return 0;
}