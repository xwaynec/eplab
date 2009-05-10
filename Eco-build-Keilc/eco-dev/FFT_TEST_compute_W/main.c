/* gets no. of points from the user, initialize the points and roots of unity lookup table 
 * and lets fft go. finally bit-reverses the results and outputs them into a file. 
 * n should be a power of 2. 
 */
#include "Eco/reg24e1.h"
#include "Eco/eco_sys.h"
#include "utils/utils.h"
#include "serial/serial.h"
#include "isr/isr_rf.h"
#include "eeprom/eeprom.h"
#include "eco_page.h"
#include "adc/adc.h"

#include <math.h>

/* treats inp as a numbits number and bitreverses it. 
 * inp < 2^(numbits) for meaningful bit-reversal
 */ 
int bitrev(int idata inp, int idata numbits)
{
	int idata i;
	int idata rev=0;
	for (i=0; i < numbits; i++)
	{
		rev = (rev << 1) | (inp & 1);
		inp >>= 1;
	}
	return rev;
}


/* returns log n (to the base 2), if n is positive and power of 2 */ 
int log_2(int idata n) 
{
	int idata res; 
	for (res=0; n >= 2; res++) 
		n = n >> 1; 
	return res; 
}



/* W will contain roots of unity so that W[bitrev(i,log2n-1)] = e^(2*pi*i/n)
 * n should be a power of 2
 * Note: W is bit-reversal permuted because fft(..) goes faster if this is done.
 *       see that function for more details on why we treat 'i' as a (log2n-1) bit number.
 */
void compute_W(int idata n, int idata W_re[], int idata W_im[])
{
	int idata i;
	int idata br;
	int log2n = log_2(n);

	for (i=0; i<(n/2); i++)
	{
		br = bitrev(i,log2n-1); 
		W_re[br] = cos((i*2*3)/(n));  
		W_im[br] = sin((i*2*3)/(n));  
	}
//#ifdef COMMENT_ONLY 
//	for (i=0;i<(n/2);i++)
//	{ 
//		br = i; //bitrev(i,log2n-1); 
//		printf("(%g\t%g)\n", W_re[br], W_im[br]);
//	}  
//#endif 
}


/* permutes the array using a bit-reversal permutation */ 
void permute_bitrev(int n, int *A_re, int *A_im) 
{ 
	int idata i;
	int idata bri;
	int idata log2n;
	int idata t_re;
	int idata t_im;

	log2n = log_2(n); 

	for (i=0; i<n; i++)
	{
		bri  = bitrev(i, log2n);

		/* skip already swapped elements */
		if (bri <= i) continue;

		t_re = A_re[i];
		t_im = A_im[i];
		A_re[i]= A_re[bri];
		A_im[i]= A_im[bri];
		A_re[bri]= t_re;
		A_im[bri]= t_im;
	}  
} 


/* fft on a set of n points given by A_re and A_im. Bit-reversal permuted roots-of-unity lookup table
 * is given by W_re and W_im. More specifically,  W is the array of first n/2 nth roots of unity stored
 * in a permuted bitreversal order.
 *
 * FFT - Decimation In Time FFT with input array in correct order and output array in bit-reversed order.
 *
 * REQ: n should be a power of 2 to work. 
 *
 * Note: - See www.cs.berkeley.edu/~randit for her thesis on VIRAM FFTs and other details about VHALF section of the algo
 *         (thesis link - http://www.cs.berkeley.edu/~randit/papers/csd-00-1106.pdf)
 *       - See the foll. CS267 website for details of the Decimation In Time FFT implemented here.
 *         (www.cs.berkeley.edu/~demmel/cs267/lecture24/lecture24.html)
 *       - Also, look "Cormen Leicester Rivest [CLR] - Introduction to Algorithms" book for another variant of Iterative-FFT
 */

//void fft(int n, double *A_re, double *A_im, double *W_re, double *W_im) 
void fft(int n, int A_re[], int A_im[], int W_re[], int W_im[]) 
{
	int idata w_re, w_im, u_re, u_im, t_re, t_im;
	int idata m, g, b;
	//int i;
	int idata mt, k;

	/* for each stage */  
	for (m=n; m>=2; m=m>>1) 
	{
		/* m = n/2^s; mt = m/2; */
		mt = m >> 1;

		/* for each group of butterfly */ 
		for (g=0,k=0; g<n; g+=m,k++) 
		{
			/* each butterfly group uses only one root of unity. actually, it is the bitrev of this group's number k.
			 * BUT 'bitrev' it as a log2n-1 bit number because we are using a lookup array of nth root of unity and
			 * using cancellation lemma to scale nth root to n/2, n/4,... th root.
			 *
			 * It turns out like the foll.
			 *   w.re = W[bitrev(k, log2n-1)].re;
			 *   w.im = W[bitrev(k, log2n-1)].im;
			 * Still, we just use k, because the lookup array itself is bit-reversal permuted. 
			 */
			w_re = W_re[k];
			w_im = W_im[k];

			/* for each butterfly */ 
			for (b=g; b<(g+mt); b++) 
			{
				/* printf("bf %d %d %d %f %f %f %f\n", m, g, b, A_re[b], A_im[b], A_re[b+mt], A_im[b+mt]);
				 */ 
				//printf("bf %d %d %d (u,t) %g %g %g %g (w) %g %g\n", m, g, b, A_re[b], A_im[b], A_re[b+mt], A_im[b+mt], w_re, w_im);

				/* t = w * A[b+mt] */
				t_re = w_re * A_re[b+mt] - w_im * A_im[b+mt];
				t_im = w_re * A_im[b+mt] + w_im * A_re[b+mt];

				/* u = A[b]; in[b] = u + t; in[b+mt] = u - t; */
				u_re = A_re[b];
				u_im = A_im[b];
				A_re[b] = u_re + t_re;
				A_im[b] = u_im + t_im;
				A_re[b+mt] = u_re - t_re;
				A_im[b+mt] = u_im - t_im;

				/*  printf("af %d %d %d %f %f %f %f\n", m, g, b, A_re[b], A_im[b], A_re[b+mt], A_im[b+mt]);
				 */         
				//printf("af %d %d %d (u,t) %g %g %g %g (w) %g %g\n", m, g, b, A_re[b], A_im[b], A_re[b+mt], A_im[b+mt], w_re, w_im);
			}
		}
	}
}

int main()
{
	int idata n;
	//int idata i;
	//int idata A_re[8];
	//int idata A_im[8];
	int idata W_re[4];
	int idata W_im[4]; 
	//int idata A_re[16];
	//int idata A_im[16];
	//int idata W_re[8];
	//int idata W_im[8]; 

	
	store_cpu_rate(16);

	P0_DIR &= ~0x28;
	P0_ALT &= ~0x28;

	for(n=0;n<6;n++)
	{
		blink_led();
		mdelay(400);
	}
	//A_re = (double*)malloc(sizeof(double)*n); 
	//A_im = (double*)malloc(sizeof(double)*n); 
	//W_re = (double*)malloc(sizeof(double)*n/2); 
	//W_im = (double*)malloc(sizeof(double)*n/2); 
	//assert(A_re != NULL && A_im != NULL && W_re != NULL && W_im != NULL); 
	
	while(1)
	{
	//for (i=0; i<3; i++) {
		//init_array(n, A_re, A_im); 
		n = 8;
		blink_led();

		compute_W(n, W_re, W_im); 
		//fft(n, A_re, A_im, W_re, W_im);
		//permute_bitrev(n, A_re, A_im);

		mdelay(100);
	//}
	}
	//free(A_re); 
	//free(A_im); 
	//free(W_re); 
	//free(W_im); 
	//exit(0);
	return 0;
}


