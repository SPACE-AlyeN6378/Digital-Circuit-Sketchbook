def next_number(numbers: list[int]) -> int:
    """
    Returns the next number to be added to the numerical list, otherwise it fills the gap
    """
    
    # If the list is empty
    if not numbers:
        return 1
    
    else:
        for i in range(1, max(numbers)+2):
            if i not in numbers:
                return i
            
        return i
    
if __name__ == "__main__":

    nums = [2, 3, 5, 7, 8, 9, 14, 15]
    for i in range(10):
        print(nums)
        nums.append(next_number(nums))
        nums.sort()