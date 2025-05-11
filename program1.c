// all in one program to check for armstrong, perfect and strong number
#include <stdio.h>
#include<math.h>
int strong();
int arm();
int per();
int facto(int);

#include <math.h>
int main()
{
    int n;
read:
    printf("Enter Choice you want to check for a number {1,2,3}\n1)Perfect Number\n2)Armstrong number\n3)Strong number\n: ");
    scanf("%d", &n);
    switch (n)
    {
    case 1:
    {
        per();
        break;
    }
    case 2:
    {
        arm();
        break;
    }
    case 3:
    {
        strong();
        break;
    }
    default:
        printf("Enter Valid choice: \n");
        goto read;
        break;
    }
}
int facto(int n)
{
    int fact = 1;
    for (int i = 1; i <= n; i++)
    {
        fact *= i;
    }
    return fact;
}
int strong()
{
    // int num = 0;
    // int sum = 0;
    // int fac2 = 0;
    // printf("enter the number:");
    // scanf("%d", &num);
    // int old = num;
    // while (num != 0)
    // {
    //     int fac = 1;
    //     sum = num % 10;
    //     for (int i = 1; i <= sum; i++)
    //     {
    //         fac = fac * i;
    //     }
    //     num = num / 10;
    //     fac2 = fac2 + fac;
    // }
    // if (fac2 == old)
    // {
    //     printf("strong number");
    // }
    // else
    // {
    //     printf("not strong");
    // }
    int n = 0, sum = 0;
    printf("Enter number to check\n");
    scanf("%d", &n);
    int p = n;
    int rem = 0;
    while (n != 0)
    {
        rem = n % 10;
        sum = sum + facto(rem);
        n = n / 10;
    }
    printf("%d", sum);
    if (p == sum)
    {
        printf("strong number\n");
    }
    else
    {
        printf("not strong\n");
    }
    main();
}
int arm()
{
    int num;
    printf("enter the number:");
    scanf("%d", &num);
    int sum = 0;
    int old=num;
    while (num != 0)
    {
        sum = sum + pow((num % 10), 3);
        num = num / 10;
    }
    printf("sum:%d\n", sum);
    if (sum == old)
    {
        printf("It is an armstrong number\n");
    }
    else
    {
        printf("it is not an armstrong number\n");
    }
    main();
}
int per()
{
    int n, sum = 0;

    printf("Enter number: ");
    scanf("%d", &n);

    for (int i = 1; i < n; i++)
    {
        if (n % i == 0)
        {
            sum = sum + i;
        }
    }

    if (n == sum)
    {
        printf("it is a perfect number \n");
    }
    else
        printf("it is not a perfect number\n");
    main();
}