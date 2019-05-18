



#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <stdint.h>
#include <string.h>
#include <linux/fb.h>
#include <sys/ioctl.h>

#define FILEPATH "/dev/fb1"
#define NUM_WORDS 64
#define FILESIZE (NUM_WORDS * sizeof(uint16_t))

void delay(int);

void delay(int t)
{
    usleep(t * 1000);
}

void flashGreen(uint16_t *p, uint16_t *map){
for (int i = 0; i < 3; i++) {
	delay(100);
	memset(map,0x077F, FILESIZE);
	delay(100);
	memset(map, 0, FILESIZE);
    }
}

void oneByOneColor(uint16_t *p, uint16_t *map){
    memset(map, 0, FILESIZE);

    printf("\nGREEN");
    
    for (int i = 0; i < NUM_WORDS; i++) {
	*(p + i) = 0x7FE2;
	delay(25);
    } 
    memset(map, 0, FILESIZE);
}

int main(void)
{
    int fbfd;
    uint16_t *map;
    uint16_t *p;
    struct fb_fix_screeninfo fix_info;

    /* open the led frame buffer device */
    fbfd = open(FILEPATH, O_RDWR);
    if (fbfd == -1) {
	perror("Error (call to 'open')");
	exit(EXIT_FAILURE);
    }

    /* read fixed screen info for the open device */
    if (ioctl(fbfd, FBIOGET_FSCREENINFO, &fix_info) == -1) {
	perror("Error (call to 'ioctl')");
	close(fbfd);
	exit(EXIT_FAILURE);
    }
    

    /* now check the correct device has been found */
    if (strcmp(fix_info.id, "RPi-Sense FB") != 0) {
	printf("%s\n", "Error: RPi-Sense FB not found");
	close(fbfd);
	exit(EXIT_FAILURE);
    }

    /* map the led frame buffer device into memory */
    map =
	mmap(NULL, FILESIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fbfd, 0);
    if (map == MAP_FAILED) {
	close(fbfd);
	perror("Error mmapping the file");
	exit(EXIT_FAILURE);
    }

    /* set a pointer to the start of the memory area */
    p = map;
    
   
    for (int i = 0; i < NUM_WORDS; i++) {
		if (i >= 0 && i <= 7){ // primera columna verde
			*(p + i) = 0x0;
		}
		else if (i >= 7 && i <= 15){ //segunda ... vrde
			*(p + i) = 0x0;
		}
		else if (i >= 15 && i <= 23){ //3 amarilla
			*(p + i) = 0x0;
		}
		else if (i >= 23  && i <= 31){ // 4 amarilla
			*(p + i) = 0xFFC0;
		}
		else if (i >= 31 && i <= 39){ // 5 nar
			*(p + i) = 0xFCA0;
		}
		else if (i >= 39  && i <= 47){ // 6 nar
			*(p + i) = 0xFCA0;
		}
		else if (i >= 47 && i <= 55){ // 7 roj
			*(p + i) = 0xF800;
		}
		else if (i >= 55  && i <= 64){ // 8 roj
			*(p + i) = 0xF800;
		}
		delay(3);
    }
    
    //memset(map, 0, FILESIZE);
   
   
   
   
    /* un-map and close */
    if (munmap(map, FILESIZE) == -1) {
	perror("Error un-mmapping the file");
    }
    close(fbfd);
    
    return 0;
}

