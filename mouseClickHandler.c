#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/wait.h> 

int main(int argc, char** argv)
{
    int fd, bytes;
    unsigned char data[3];

    const char *pDevice = "/dev/input/mice";

    // Open Mouse
    fd = open(pDevice, O_RDWR);
    if(fd == -1)
    {
        printf("ERROR Opening %s\n", pDevice);
        return -1;
    }

    int left, middle, right;
    signed char x, y;
    while(1)
    {
        // Read Mouse     
        bytes = read(fd, data, sizeof(data));

        if(bytes > 0)
        {
            left = data[0] & 0x1;
            right = data[0] & 0x2;
            middle = data[0] & 0x4;

            x = data[1];
            y = data[2];
            
            if (left == 1) {
	        int pid = fork();
	        if (pid == 0) {
		    execlp("python3", "python3", "./voice_assistant.py", (char *)NULL);
		} else {
		    wait(NULL);
		}
	    }
        }   
    }
    return 0; 
}
