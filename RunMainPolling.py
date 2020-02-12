import sys, json

#Read data from stdin
def read_in():
    return sys.stdin.readlines()



def main():
    #get our data as an array from read_in()
    lines = read_in()
    print(lines)

    # Sum  of all the items in the providen array
    # total_sum_inArray = 0
    # for item in lines:
    #     total_sum_inArray += item
    #
    # #return the sum to the output stream
    # print(total_sum_inArray)

# Start process
if __name__ == '__main__':
    main()
