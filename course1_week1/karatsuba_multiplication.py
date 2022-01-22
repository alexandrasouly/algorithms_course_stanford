# This implements the Karatsuba multiplication, a recursive algorithm
import math


def single_digit_multiplication(a: int, b:int) -> int:
    assert a< 10 or b<10
    return a*b

def karatsuba_multiplication(a:int, b:int):
    # base case:
    if a<10 or b<10:
        return single_digit_multiplication(a,b)
    else:
        # Finding "middle" of smallest number
        # we round up here but could round down too.
        # Need to get that many chars from the  right so that 0s match up
        # in case of uneven number length.
        middle_length = math.ceil(min(len(str(a)),len(str(b)))/2)
        a_high = int(str(a)[:-middle_length])
        a_low = int(str(a)[-middle_length:])
        b_high = int(str(b)[:-middle_length])
        b_low =  int(str(b)[-middle_length:])

        step1 = karatsuba_multiplication(a_high, b_high)
        step2 = karatsuba_multiplication(a_low, b_low)
        step3 = karatsuba_multiplication(a_high+a_low, b_high+b_low)
        step4 = step3-step2-step1 # (so a_high * b_low + a_low * b_high)
        return (int(str(step1)+ '0'*middle_length*2) +int(str(step4)+ '0'*middle_length) + step2 )






if __name__=="__main__":
    input1 = 3141592653589793238462643383279502884197169399375105820974944592
    input2 = 2718281828459045235360287471352662497757247093699959574966967627
    assert (karatsuba_multiplication(input1, input2)) == input1*input2