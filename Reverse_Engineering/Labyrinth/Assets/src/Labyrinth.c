#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "Labyrinth.h"

ListNode* CreateMaze(){
    char temp[100]="Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucib";
    char temp2[250]="us ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed d";
    char temp3[150]="iam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hen";
    char tmp4[110]="drerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos";
    
    ListNode* start = (ListNode*)malloc(sizeof(ListNode));
    ListNode* second = (ListNode*)malloc(sizeof(ListNode));
    ListNode* third = (ListNode*)malloc(sizeof(ListNode));
    ListNode* fourth = (ListNode*)malloc(sizeof(ListNode));

    strcpy((start->value), "Start");
    start->up=start;
    start->left= third;
    start->right=second;
    start->down=third;

    strcpy(second->value,"flame{giH");
    second->up = fourth;
    second->left=start;
    second->down = second->right = third;

    strcpy(third->value,"{matcha_gkHtcha}. Tricked you!");
    third->up =second;
    third->down=start;
    third->left = third->right = third;

    strcpy(fourth->value,"real_flag: flame{w31c0m3_t0_th3_f1r$t_1}");
    fourth->down=fourth->left=fourth->up=fourth->right=fourth;

    return start;
}

void DestroyMaze(ListNode *start){   
    free(start->right->up);
    free(start->right);
    free(start->down);
    free(start);
}