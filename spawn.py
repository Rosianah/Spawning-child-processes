#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<sys/types.h>
#include<string.h>
#include<sys/wait.h>
#include<signal.h>

int main()
{
    int pipeone[2];
    int pipetwo[2];
    int num[3];
    printf("Enter two numbers to multiply\n");
    printf("number one:\n");
    scanf("%d",&num[0]);
    printf("number two:\n");
    scanf("%d",&num[1]);
    
    
    //rep process id
    pid_t p;
    
    
     for(int i=0;i<10;i++)
    {
        if (pipe(pipeone)==-1)
        {
        fprintf(stderr, "Pipe Failed" );
        return 1;
        }
    if (pipe(pipetwo)==-1)
        {
        fprintf(stderr, "Pipe Failed" );
        return 1;
        }
    
    p = fork();
    
    if (p < 0)
    {
        fprintf(stderr, "fork Failed" );
        return 1;
    }
    
    // Parent process
    else if (p > 0)
    {

        int product[2];
 
        close(pipeone[0]);  // Close reading end of first pipe
 
        // Write input string and close writing end of first
        // pipe.
        write(pipeone[1], &num, sizeof(num));
        close(pipeone[1]);
 
        // Wait for child to send a string
        wait(NULL);
 
        close(pipetwo[1]); // Close writing end of second pipe
 
        // Read string from child, print it and close
        // reading end.
        read(pipetwo[0], &product, sizeof(product));
        printf("The product is %d from child process with id %d \n", product[0], product[1]);
        kill(product[0], SIGKILL);
        close(pipetwo[0]);
    }
 
    // child process
    else
    {
        
        close(pipeone[1]);  // Close writing end of first pipe
 
        // Read a string using first pipe
        
        
        int twonums[2];
     
        read(pipeone[0], &twonums, sizeof(twonums));
        
        int product[2];
        product[0] = twonums[0]*twonums[1];
        product[1] = getpid();
 
        
        // Close both reading ends
        close(pipeone[0]);
        close(pipetwo[0]);
 
        // Write the sum and close writing end
        write(pipetwo[1], &product, sizeof(product));
        close(pipetwo[1]);
 
        exit(0);
    }
    }
    for(int i=0;i<10;i++) 
    wait(NULL);
    
    
    return 0;
}

