//#include <stdio.h>
#include "Eco/reg24e1.h"
#include "Eco/eco_sys.h"
#include "utils/utils.h"
#include "serial/serial.h"
#include "isr/isr_rf.h"
#include "eeprom/eeprom.h"
#include "eco_page.h"
#include "adc/adc.h"

#define GRAPHSIZE 12
#define INFINITY GRAPHSIZE*GRAPHSIZE
#define MAX(a, b) ((a > b) ? (a) : (b))

//char e = 10; /* The number of nonzero edges in the graph */
char n; /* The number of nodes in the graph */
char idata dist[GRAPHSIZE][GRAPHSIZE]; /* dist[i][j] is the distance between node i and j; or 0 if there is no direct connection */
char idata d[GRAPHSIZE]; /* d[i] is the length of the shortest path between the source (s) and node i */

volatile int dij_counter = 0;


void printD() {
	int idata i;
	puts("1:");	
	for (i = 1; i <= n; i++)
		int_print(i);
	puts("\r\n2:");
	for (i = 1; i <= n; i++) 
		int_print(d[i]);
	puts("\r\n");
}

void dijkstra(char s) 
{
	idata char i, k, mini;
	char idata visited[GRAPHSIZE];

	for (i = 1; i <= n; i++) 
	{
		d[i] = INFINITY;
		visited[i] = 0; /* the i-th element has not yet been visited */
	}

	d[s] = 0;

	for (k = 1; k <= n; k++) 
	{
		mini = -1;
		for (i = 1; i <= n; i++)
			if (!visited[i] && ((mini == -1) || (d[i] < d[mini])))
				mini = i;

		visited[mini] = 1;

		for (i = 1; i <= n; ++i)
			if (dist[mini][i])
				if (d[mini] + dist[mini][i] < d[i]) 
					d[i] = d[mini] + dist[mini][i];
	}
}

int main() 
{
	char i, j , k = 5;
	//char u = 1, v = 2, w = 4;

	store_cpu_rate(16);

	P0_DIR &= ~0x28;
	P0_ALT &= ~0x28;

	serial_init(19200);

	for(n=0;n<6;n++)
	{
		blink_led();
		mdelay(400);
	}

	n = GRAPHSIZE;


	while(1)
	{
		for (i = 0; i < n; i++)
			for (j = 0; j < n; j++)
				dist[i][j] = (k++)%30;
		//n = -1;
		//for (i = 0; i < 6; i++) {
		//fscanf(fin, "%d%d%d", &u, &v, &w);
		//	dist[u][v] = w++;
		//	n = MAX(u, MAX(v+w, n));
		//}
		//fclose(fin);
		for(j=0;j<n;j++)	
			dijkstra(j);

		dij_counter++;

		int_print(dij_counter);
		puts("\r\n");
		
		printD();
	}

	return 0;
}

