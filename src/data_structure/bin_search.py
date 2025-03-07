def search(nums: list, number: int) -> bool:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == number:
            return True
        elif number < nums[mid]:
            right = mid - 1
        else:
            left = mid + 1
    return False


if __name__ == "__main__":
    numbers = [1, 2, 3, 45, 356, 569, 600, 705, 923]
    for num in numbers:
        assert search(numbers, num)

    not_in_numbers = [0, 4, 355, 706, 945]
    for num in not_in_numbers:
        assert not search(numbers, num)
