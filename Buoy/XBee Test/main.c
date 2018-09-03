#include <msp430.h> 


/**
 * main.c
 */


int main(void)
{
	WDTCTL = WDTPW | WDTHOLD;	    // stop watchdog timer

	P3SEL |= BIT3+BIT4;             // P3.3 and P3.4 are USCI_A0 TX/RX
	UCA0CTL1 |= UCSWRST;            // Reset the state machine
	UCA0CTL1 |= UCSSEL_2;           // Using SMCLK
	UCA0BR0 = 0x68;                 // 1 MHz/9600 =~ 104 (0x68)
	UCA0BR1 = 0x00;                 //
	UCA0MCTL |= UCBRS_1 + UCBRF_0;  // Modulation UCBRSx=1, UCBRFx = 0
	UCA0CTL1 &= ~UCSWRST;           // Initialize the state machine
	UCA0IE |= UCRXIE;               // Enable USCI_A0 RX Interrupt

	_bis_SR_register(GIE);          // Interrupts enabled

	
	return 0;
}

#pragma vector=USCI_A0_VECTOR
__interrupt void USCI_A0_ISR(void)
{
    unsigned int apiframe[20];
    unsigned int data[20];

    unsigned int j = 0;
    unsigned int dh = 0;
    unsigned int dl = 0;

    // RX interrupt code here
    apiframe[j] = UCA0RXBUF;
    if((j==0 && apiframe[j] == 0x7E) || j>0)
    {
        data[j] = apiframe[j];
        if(j==11)
        {
            dh = apiframe[j];
        }
        if(j==12)
        {
            dl = apiframe[j];
        }
        if(j>sizeof apiframe-1)
        {
            j = 0;
        }
    }

    j++;

}
