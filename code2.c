#include<stdio.h>
#include<stdlib.h>
struct node{
    int info;
    struct node *next;
};
int main()
{
    struct node *new,*temp,*head;
    int size;
    printf("enter the size of list:");
    scanf("%d",&size);
    for (int i=0;i<size;i++)
    {
        new=(struct node*)malloc(sizeof(struct node));
        int item;
        printf("enter the item:");
        scanf("%d",&item);
        new->info=item;
        new->next=NULL;
        if(head==0)
        {
            head=new;
            temp=head;
        }
        else
        {
            temp->next=new;
            temp=new;
        }
    }
    temp=head;
    while(temp!=NULL)
    {
        printf("%d ",temp->info);
        temp=temp->next;
    }
    return 0;
}