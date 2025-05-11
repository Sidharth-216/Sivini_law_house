#include<stdio.h>
#include<stdlib.h>
struct node{
    int info;
    struct node *link;
};
int main()
{
    int count=0;
    struct node *start ,*new , *temp;
    new =(struct node*)malloc(sizeof(struct node));
    int item ;
    printf("enter the item :");
    scanf("%d",&item);
    new->info=item;
    new->link= NULL;
    start=new;
    temp=new;
    while(1)
    {
        new=NULL;
        temp =start;//again storing the start node to temp to print all the node from starting(previouly temp stored last node)
        while(temp!=NULL)
        {
             printf("%d ",temp->info);
             temp=temp->link;
             count++;
        }
        printf("\n1.Create new node/at the end");
        printf("\n2.Print the list");
        printf("\n3.Create new node/at the begning");
        printf("\n4.Create new node/at specific position");
        printf("\n5.Exit");
        int ch;
        printf("\nenter the choice :");
        scanf("%d",&ch);
        switch (ch)
        {
            case 1:
                new=(struct node*)malloc(sizeof(struct node));
                int item2;
                printf("enter the item:");
                scanf("%d",&item);
                new->info=item;
                new->link = NULL; // setting the link of the new node to NULL
                temp = start;
                while(temp->link != NULL) {
                    temp = temp->link;
                }
                temp->link = new;
                break;
            case 2:
               temp =start;//again storing the start node to temp to print all the node from starting(previouly temp stored last node)
               while(temp!=NULL)
               {
                  printf("%d ",temp->info);
                  temp=temp->link;
                }
                break;
            case 3:
                if(start!=NULL)
                {
                    new=(struct node*)malloc(sizeof(struct node));
                    int item2;
                    printf("enter the item:");
                    scanf("%d",&item);
                    new->info=item;
                    new->link=start;
                    start=new;
                }
                else
                {
                    printf("the list is empty");
                }
                break;
            case 4:
                int pos;
                printf("enter the position:");
                scanf("%d",&pos);
                if(pos>count)
                {
                    printf("invalid position");
                }
                else
                {
                    temp=start;
                    int i=0;
                    while(i<pos)
                    {
                        temp=temp->link;
                        i++;
                    }
                    new=(struct node*)malloc(sizeof(struct node));
                    int item3;
                    printf("enter the item ");
                    scanf("%d",&item);
                    new->info=item;
                    new->link=temp->link;
                    temp->link=new;
                }
                break;
            case 5:
                return 0;
                break;
            default:
               printf("invalid input\n");
               break;
        }
    }
    
    return 0;
}