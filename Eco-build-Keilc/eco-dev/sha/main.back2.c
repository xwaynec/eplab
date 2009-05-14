#include "Eco/reg24e1.h"
#include "Eco/eco_sys.h"
#include "utils/utils.h"
#include "serial/serial.h"
#include "eeprom/eeprom.h"
#include "eco_page.h"
//#include "adc/adc.h"
//#include "isr/isr_rf.h"
//#include <stdlib.h>

//#include <malloc.c>

#define NUM_NODES                          10
#define NONE                               9999

#ifndef NULL
 #define NULL ((void *) 0L)
#endif

#define _MALLOC_MEM_	xdata

extern void _MALLOC_MEM_ *malloc  (unsigned int size);
extern void free                  (void _MALLOC_MEM_ *p);

struct _NODE
{
	int iDist;
	int iPrev;
};
typedef struct _NODE xdata NODE;

struct _QITEM
{
	int iNode;
	int iDist;
	int iPrev;
	struct _QITEM xdata *qNext;
};
typedef struct _QITEM xdata QITEM;

QITEM xdata *qHead = NULL;


xdata int AdjMatrix[NUM_NODES][NUM_NODES];

volatile int g_qCount = 0;
NODE xdata rgnNodes[NUM_NODES];
idata int ch;
idata int iPrev, iNode;
int i, iCost, iDist;

/*
   void print_path (NODE *rgnNodes, int chNode)
   {
   if (rgnNodes[chNode].iPrev != NONE)
   {
   print_path(rgnNodes, rgnNodes[chNode].iPrev);
   }
   printf (" %d", chNode);
   fflush(stdout);
   }
 */

void enqueue (int iNode, int iDist, int iPrev)
{
	QITEM xdata *qNew = (QITEM *) malloc(sizeof(QITEM));
	QITEM xdata *qLast = qHead;
	/*  
		if (!qNew) 
		{
		fprintf(stderr, "Out of memory.\n");
		exit(1);
		}
	 */
	qNew->iNode = iNode;
	qNew->iDist = iDist;
	qNew->iPrev = iPrev;
	qNew->qNext = NULL;

	if (!qLast) 
	{
		qHead = qNew;
	}
	else
	{
		while (qLast->qNext) qLast = qLast->qNext;
		qLast->qNext = qNew;
	}
	g_qCount++;
	//puts("e ");
	//int_print(g_qCount);

	//puts("\r\n");
	//               ASSERT(g_qCount);
}


void dequeue (int *piNode, int *piDist, int *piPrev)
{
	QITEM xdata *qKill = qHead;

	if (qHead)
	{
		//                 ASSERT(g_qCount);
		*piNode = qHead->iNode;
		*piDist = qHead->iDist;
		*piPrev = qHead->iPrev;
		qHead = qHead->qNext;
		free(qKill);
		g_qCount--;
	
	//puts("d ");
	//int_print(g_qCount);
	//puts("\r\n");
	}
}


int qcount (void)
{
	//puts("c:");
	//int_print(g_qCount);
	//puts("\r\n");
	return g_qCount;
}

void dijkstra(int chStart, int chEnd) 
{

	for (ch = 0; ch < NUM_NODES; ch++)
	{
		rgnNodes[ch].iDist = NONE;
		rgnNodes[ch].iPrev = NONE;
	}

	if (chStart == chEnd) 
	{
		puts("fuck\r\n");
	}
	else
	{
		rgnNodes[chStart].iDist = 0;
		rgnNodes[chStart].iPrev = NONE;

		enqueue (chStart, 0, NONE);

		while (qcount() > 0)
		{
			dequeue (&iNode, &iDist, &iPrev);
			for (i = 0; i < NUM_NODES; i++)
			{
				if ((iCost = AdjMatrix[iNode][i]) != NONE)
				{
					if ((NONE == rgnNodes[i].iDist) || (rgnNodes[i].iDist > (iCost + iDist)))
					{
						rgnNodes[i].iDist = iDist + iCost;
						rgnNodes[i].iPrev = iNode;
						enqueue (i, iDist + iCost, iNode);
					}
				}
			}
			
			
			puts("w");
			int_print(g_qCount);
			puts("\r\n");
		}
		/*      
				printf("Shortest path is %d in cost. ", rgnNodes[chEnd].iDist);
				printf("Path is: ");
				print_path(rgnNodes, chEnd);
				printf("\n");
		 */
	}
}

void main() 
{
	idata char i,j,k = 5;

	store_cpu_rate(16);
	/* init led */
	P0_DIR &= ~0x28;
	P0_ALT &= ~0x28;

	for (i = 0; i < 6; i++) {
		blink_led();
		mdelay(400);
	}
	/* init serial */
	serial_init(19200);

	while(1)
	{
		/* make a fully connected matrix */
		for (i=0;i<NUM_NODES;i++) {
			for (j=0;j<NUM_NODES;j++) {
				/* make it more sparce */
				AdjMatrix[i][j]= k;
				k++;
			}
		}

		/* finds 10 shortest paths between nodes */
		for (i=0,j=NUM_NODES/2;i<10;i++,j++) {
			j=j%NUM_NODES;
			dijkstra(i,j);
		}
	
		blink_led();
		//mdelay(100);
	}	

}
