# program for solving pothole repair problem
# as seen on Max Taylor's (go Bucks!) blog
# I used Max's mathematical argument but not his (probably far superior) code
# Here's the link: https://maxtaylor.dev/posts/2022/08/repairing-potholes

# we have to do two things:
# 1. decide which segment to switch lanes in for each starting lane 
#       l1: (argmax_C( num_potholes(l2[:C]) + num_potholes(l1[C+1:])) )
#       l2: (argmax_C( num_potholes(l1[:C]) + num_potholes(l2[C+1:])) )
#       keep an array to keep track of potholes avoided from :i and i+1:
# 2. decide which lane to start out in
#       take argmax_l(num_potholes(l'[:C]) + num_potholes(l'[C+1:]))

POTHOLE = 'x'
ROAD = '-'

# helper function determining number of potholes in a string:
def _potholes_avoided(start_l: str, end_l: str) -> int:

    start_l_potholes, end_l_potholes = 0, 0
    # count from the end in the lane where you start
    # count from the start in the lane where you end
    start_potholes_avoided, end_potholes_avoided = [0 for _ in start_l], [0 for _ in end_l]

    for i, start_segment in reversed(list(enumerate(start_l))):
        if i == len(start_l) - 1:
            start_potholes_avoided[i - 1] = 1 if start_segment == POTHOLE else 0 
        elif i > 0:
            start_potholes_avoided[i - 1] = start_potholes_avoided[i] + ( 1 if start_segment == POTHOLE else 0 )

    for i, end_segment in enumerate(end_l):
        # if i == len(end_l) - 1:
        #     end_potholes_avoided[i] = end_potholes_avoided[i - 1]
        if i > 0 and i < len(end_l) - 1:
            end_potholes_avoided[i + 1] = end_potholes_avoided[i] + ( 1 if end_segment == POTHOLE else 0 )
        elif i == 0:
            # i == 0
            end_potholes_avoided[1] = 1 if end_segment == POTHOLE else 0

    return start_potholes_avoided, end_potholes_avoided

def max_potholes(l1, l2):
    start_l1_potholes_avoided, end_l2_potholes_avoided = _potholes_avoided(l1, l2)
    max_C_start_l1, max_C_start_l2, max_l1_start_avoided, max_l2_start_avoided = 0, 0, 0, 0

    for i, (l1_avoided, l2_avoided) in enumerate(zip(start_l1_potholes_avoided, end_l2_potholes_avoided)):
        if l1_avoided + l2_avoided > max_l1_start_avoided:
            max_l1_start_avoided = l1_avoided + l2_avoided
            max_C_start_l1 = i

    start_l2_potholes_avoided, end_l1_potholes_avoided = _potholes_avoided(l2, l1)

    for i, (l2_avoided, l1_avoided) in enumerate(zip(start_l2_potholes_avoided, end_l1_potholes_avoided)):
        if l2_avoided + l1_avoided > max_l2_start_avoided:
            max_l2_start_avoided = l2_avoided + l1_avoided
            max_C_start_l2 = i
    print("argmax C for a start in l1 is: ", max_C_start_l1)
    print("max for a start in l1 is ", max_l1_start_avoided)
    
    print("argmax C for a start in l2 is: ", max_C_start_l2)
    print("max for a start in l2 is ", max_l2_start_avoided)

    return max(max_l1_start_avoided, max_l2_start_avoided)



def main():
    l1 = input(f"Enter lane 1 (potholes are '{POTHOLE}', road is '{ROAD}'):\n")
    l2 = input("Enter lane 2 (potholes are '{POTHOLE}', road is '{ROAD}'):\n")
    print("potholes avoided for starting in l1 is: ", _potholes_avoided(l1, l2))
    print("potholes avoided for starting in l2 is: ", _potholes_avoided(l2, l1))

    print("maximum potholes that can be avoided (and hence repaired): ", max_potholes(l1, l2))

if __name__ == '__main__':
    main()
