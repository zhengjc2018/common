from time import perf_counter


def get_array(n, sort=False):
    from random import randint

    val = [randint(1, 100) for i in range(n)]
    if sort:
        return sorted(val)
    return val


# 获得排序算法执行时间
def timeit(f):
    def inner(*array):
        a = perf_counter()
        data = f(*array)
        b = perf_counter()

        try:
            print(f'run {f.__doc__.strip()} time: {b-a}s, sorted ok:\n')
        except Exception:
            pass
            print(f'array:{array}, \ndata: {data}, \nsorted: {sorted(*array)}')
    return inner


# 最优O(n)， 最差O(n^2)   空间O(1)
@timeit
def sort1(array):
    """     冒泡排序     """
    length = len(array) - 1
    for i in range(length):
        for j in range(0, length-i):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]

    assert array == sorted(array)
    return array


@timeit
def sort2(array):
    """     鸡尾酒排序     """
    left = 0
    right = len(array)-1
    while left < right:
        # print(array)
        for i in range(left, right):
            if array[i] > array[i+1]:
                array[i], array[i+1] = array[i+1], array[i]

        left += 1

        for i in range(right, left-1, -1):
            if array[i] < array[i-1]:
                array[i], array[i-1] = array[i-1], array[i]

        right -= 1

    assert array == sorted(array)
    return array


# 最优O(n^2)， 最差O(n^2)   空间O(1)
@timeit
def sort3(array):
    """     选择排序     """
    length = len(array)
    for i in range(length):
        _min = i
        for j in range(i+1, length):
            if array[_min] > array[j]:
                _min = j
        array[i], array[_min] = array[_min], array[i]

    assert array == sorted(array)
    return array


# 最优O(n)， 最差O(n^2)   空间O(1)
@timeit
def sort4(array):
    """     插入排序     """
    res = []
    res.append(array.pop(0))
    for i in range(1, len(array)):
        data = array.pop(0)
        for i in range(len(res)):
            if res[i] >= data:
                res.insert(i, data)
                break
        else:
            res.append(data)

    assert res == sorted(res)
    return res


# 最优O(nlogn)， 最差O(nlogn)   空间O(n)
@timeit
def sort5(array1, array2):
    """     归并排序     """
    res = []
    i = j = 0
    while i < len(array1) and j < len(array2):
        if array1[i] < array2[j]:
            res.append(array1[i])
            i += 1
        else:
            res.append(array2[j])
            j += 1

    assert res == sorted(res)
    return res


# 最优O(nlogn)， 最差O(nlogn)   空间O(n)
def quick(args):
    if args == []:
        return []
    else:
        pivot = args[0]
        left = quick([i for i in args[1:] if i < pivot])
        high = quick([i for i in args[1:] if i > pivot])
        return left + [pivot] + high


@timeit
def sort6(seq):
    """     快速排序     """
    return quick(seq)


@timeit
def sort7(seq):
    ''' 快速排序2 '''
    return quick_sort_standord(seq, 0, len(seq)-1)


def quick_sort_standord(array, low, high):
    if low < high:
        key_index = partion(array, low, high)
        quick_sort_standord(array, low, key_index)
        quick_sort_standord(array, key_index+1, high)


def partion(array, low, high):
    key = array[low]
    while low < high:
        while low < high and array[high] >= key:
            high -= 1
        if low < high:
            array[low] = array[high]

        while low < high and array[low] < key:
            low += 1
        if low < high:
            array[high] = array[low]

    array[low] = key
    return low


def test():
    num = 5000
    array = get_array(num)
    sort1(array)
    array = get_array(num)
    sort2(array)
    array = get_array(num)
    sort3(array)
    array = get_array(num)
    sort4(array)
    array1 = get_array(num, True)
    array2 = get_array(num, True)
    sort5(array1, array2)
    array = get_array(num)
    sort6(array)
    array = get_array(num)
    sort7(array)


def binary_search(array, key):
    left = 0
    right = len(array) - 1

    while left <= right:
        middle = (left + right)//2

        if array[middle] > key:
            right = middle - 1
        elif array[middle] == key:
            return middle
        else:
            left = middle + 1

    return None


def test_binary_search():
    array1 = [1, 2, 3, 4, 5, 11, 15, 16, 20]
    array2 = [1, 2, 3, 4, 5, 11, 15, 16]
    assert binary_search(array1, 0) is None
    assert binary_search(array1, 21) is None

    assert binary_search(array2, 0) is None
    assert binary_search(array2, 21) is None

    for array in [array1, array2]:
        for i, j in enumerate(array):
            assert binary_search(array, j) == i


if __name__ == '__main__':
    test()
