/*
 *  C code to read pressure and temperature from the
 *  Raspberry Pi Sense HAT add-on board (LPS25H sensor)
 *  
 *  sudo raspi-config --> advanced options --> enable i2c
 *
 *  sudo apt-get install libi2c-dev i2c-tools
 *
 *  Then build with:
 *
 *       gcc -Wall accelerometer.c -o accelerometer
 *
 */
#include <unistd.h>
 
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include <time.h>
#include <stdint.h>
#include <linux/i2c-dev.h>
#include <math.h>
 
 
#define DEV_ID 0x6A
#define DEV_PATH "/dev/i2c-1"
#define WHO_AM_I 0x0F
#define CTRL_REG8 0x22
#define CTRL_REG2 0x18
 
#define CTRL_REG5_XL 0x1F
#define CTRL_REG6_XL 0x20
 
 
#define LSM9DS1_CTRL_REG4 0x1E
#define LSM9DS1_CTRL_REG1_G 0x10
#define LSM9DS1_ORIENT_CFG_G 0x13
 
 
#define MPI 3.141592653
#define RAD2DEG 57.2978
 
int fd = 0;
 
void delay(int);
 
void writeReg(uint8_t reg, uint8_t value){
    int res = i2c_smbus_write_byte_data(fd, reg, value);
    printf("res: 0%x \n", res);
}
 
void readBlock(uint8_t  command, uint8_t size, uint8_t *data){
    int result = i2c_smbus_read_i2c_block_data(fd, command, size, data);
    //printf("block: 0%x \n", result);
    if(result  != size ){
        printf("Fail to read i2c");
        exit(1);
    }
}
 
 
void readGyro(int *a){
    uint8_t block[6];
    readBlock(0x80 | CTRL_REG2, sizeof(block), block);
    *a = (int16_t)(block[0] | block[1] << 8);
    *(a + 1) = (int16_t)(block[2] | block[3] << 8);
    *(a + 2) = (int16_t)(block[4] | block[5] << 8);
}

void readAcc(int *a){
    uint8_t block[6];
    readBlock(0x80 | CTRL_REG2, sizeof(block), block);
    *a = (int16_t)(block[0] | block[1] << 8);
    *(a + 1) = (int16_t)(block[2] | block[3] << 8);
    *(a + 2) = (int16_t)(block[4] | block[5] << 8);
}

 
 
int main(void)
{
 
    //uint8_t status = 0;
 
 
    /* open i2c comms */
    if ((fd = open(DEV_PATH, O_RDWR)) < 0) {
    perror("Unable to open i2c device");
    exit(1);
    }
 
    /* configure i2c slave */
    if (ioctl(fd, I2C_SLAVE, DEV_ID) < 0) {
    perror("Unable to configure i2c slave device");
    close(fd);
    exit(1);
    }
 
   
    /* check we are who we should be */
    int who = i2c_smbus_read_byte_data(fd, WHO_AM_I);
    printf(" who: 0%x \n", who);
    if (who != 0x68) {
    printf("%s\n", "who_am_i error");
    close(fd);
    exit(1);
    }
 
    printf(" Enabled \n");
    writeReg(LSM9DS1_CTRL_REG4, 0b00111000);
    writeReg(LSM9DS1_CTRL_REG1_G, 0b10111000);
    writeReg(LSM9DS1_ORIENT_CFG_G, 0b10111000);
    int gyroRaw[3];
    float accXAngle = 0.0;
    float accYAngle = 0.0;
   
    int averageSpan = 1000;
    double averageXGyr = 0.0;
    double averageYGyr = 0.0;
    double averageZGyr = 0.0;


	averageXGyr = 0;
	averageYGyr = 0;
	averageZGyr = 0;
	for(int i = 0; i < averageSpan; i++){
			readGyro(gyroRaw);
			averageXGyr= averageXGyr + gyroRaw[0]/10000;
			averageYGyr= averageYGyr + gyroRaw[1]/10000;
			averageZGyr= averageZGyr + gyroRaw[2]/10000;
	}
	averageXGyr = averageXGyr/averageSpan; 
	averageYGyr = averageYGyr/averageSpan; 
	averageZGyr = averageZGyr/averageSpan; 
	float roll = atan2(averageXGyr, averageZGyr) * 180/MPI;
	float pitch = atan2(-averageXGyr, sqrt(averageYGyr*averageYGyr + averageZGyr*averageZGyr)) * 180/MPI;
	float yaw = atan2(averageXGyr, averageYGyr);
	printf(" %f,%f,%f\n", yaw, roll, pitch);
    close(fd);
 
    return (0);
}
 
 
void delay(int t)
{
    usleep(t * 1000);
}
