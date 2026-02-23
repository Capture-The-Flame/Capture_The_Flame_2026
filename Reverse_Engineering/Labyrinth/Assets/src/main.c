#include <stdio.h>
#include <stdlib.h>

#include "Labyrinth.h"

int main(){
    //node is now the start of the maze that you can enter and evaluate
    ListNode* node = CreateMaze();

    printf("%s", "Maze Created!\n");

    DestroyMaze(node);
    printf("%s","Maze Destroyed\n");
    
    return 0;
}