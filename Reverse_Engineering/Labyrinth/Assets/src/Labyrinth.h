#ifndef LABYRINTH_H
#define LABYRINTH_H

typedef struct ListNode{
    struct ListNode *up;
    struct ListNode *left;
    struct ListNode *down;
    struct ListNode *right;
    char value[50];
} ListNode;

ListNode* CreateMaze();
void DestroyMaze(ListNode*);


#endif