#include <stdio.h>
#include <string.h>

#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif

int main ()
{
   int delay = 1000;
   char command[50];
   
   int Tempature = 0;
   int Water_Level = 0;
   int Step_Number = 0;
	
   while(1 == 1) {  
	  sprintf(command, "python changeMachineCGI.py 1 %d %d %d",Tempature, Water_Level, Step_Number);	
	  system(command);  
	  
	  Tempature += 10;
	  Water_Level += 2;
	  Step_Number += 1;
	  
	  #ifdef _WIN32
	  Sleep(delay);
	  #else
	  usleep(delay*1000);
	  #endif
   }

   return(0);
} 