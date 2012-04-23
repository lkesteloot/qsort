#!/usr/bin/python

"""See if I can implement Quick Sort."""

import random

def qsort(a):
    """Quick Sort array "a" in place."""

    def sort_part(first, last):
        """First and last point to the first and last elements (inclusive) in
        "a" to be sorted."""

        if last <= first:
            # A zero- or one-element array is already sorted. A more efficient implementation
            # would check whether the array was short (say, 5 or fewer items) and fall back
            # on an insertion sort, which is faster than Quick Sort for small arrays.
            return

        # We pick our pivot element from the middle of the array so that the sort
        # will behave well if the array is already sorted. Another option here is
        # to shuffle the entire array when we're first given it (in qsort(), not
        # in this subroutine) and just use the first element here (and skip the
        # swap just below). Our approach here will result in a more even partition
        # if the array is already sorted, since a pure shuffle will have some
        # imbalance.
        #
        # Note the method used to find the middle element. We could use
        # (first + last)/2, but that may overflow in languages with limited
        # range. (E.g., a 2-billion element array in Java).
        pivot_index = first + (last - first)/2
        pivot_value = a[pivot_index]

        # Put pivot at the front so we can partition the rest of the elements. We need
        # to keep the pivot element separate so that the two partitions we recurse into
        # are guaranteed to be smaller than the original.
        a[pivot_index], a[first] = a[first], a[pivot_index]

        # The entire array is split into four sections:
        #
        #     1. The pivot (length 1).
        #     2. Elements <= the pivot value (initially empty, possibly always empty).
        #     3. Unprocessed elements (empty at the end).
        #     4. Elements >= the pivot value (initially empty, possibly always empty).
        #
        # The "low" and "high" indices point to the first and last unprocessed elements.
        low = first + 1
        high = last

        # Throughout the partitioning process we maintain the following invariant:
        #
        #   a[first..low) <= pivot_value <= a(high..last]

        # Continue this loop as long as we have any unprocessed elements left.
        while low <= high:
            # See if we can shorten the unprocessed area on the left. If the left-most
            # element (at "low") is <= pivot_value, just move "low" up. Only do this
            # if the unprocessed section is non-empty (low <= high).
            while low <= high and a[low] <= pivot_value:
                low += 1

            # See if we can shorten the unprocessed area on the right. If the right-most
            # element (at "high") is >= pivot_value, just move "high" down. Only do this
            # if the unprocessed section is non-empty (low <= high).
            while low <= high and a[high] >= pivot_value:
                high -= 1

            # After the above two loops, we either have no more unprocessed elements left
            # (low > high) or the two indices got stuck. Note that we'll never have
            # low == high since we won't have a case above where both loops get stuck on
            # the same element. So we don't need to check for "low <= high".
            assert low != high
            if low < high:
                # If they got stuck, then they each got stuck at elements that should be
                # in the opposite section (since both criteria together cover the entire
                # domain). We swap the two elements they got stuck on.
                assert a[low] > a[high]
                a[low], a[high] = a[high], a[low]

                # Since these two elements are now processed, we move the indices to
                # push the elements into the processed sections. This part is optional
                # since the above loops will do that for us anyway, but it's a nice way
                # to capture the idea that the swap moved the elements into the outer
                # sections. Also it's a convenient way to prove that this loop will
                # eventually terminate: at each iteration, either this "if" will run
                # (and the unprocessed section will shrink) or it will be the last
                # iteration.
                low += 1
                high -= 1

        # The processed section is now empty. The array looks like this:
        #
        #     1. The pivot (length 1).
        #     2. Elements <= the pivot value (possibly empty).
        #     3. Unprocessed elements (empty).
        #     4. Elements >= the pivot value (possibly empty).
        #
        # The "low" and "high" indices are adjacent (low == high + 1) and represent
        # the empty section 3. That means that "high" points to the last element of
        # section 2 and "low" points to the first element of section 4.
        assert low == high + 1

        # We could now recurse on sub-arrays [first..high] and [low..last],
        # since the pivot technically is allowed to belong to section 2. If
        # this terminated, the array would be correctly sorted. But it's not
        # guaranteed to terminate since section 4 may be empty (if all elements
        # in the array are <= the pivot).
        #
        # To guarantee that the recursion is always smaller than the original,
        # we don't recurse on the pivot element. But after sorting we'll want
        # the pivot to be between the two sub-arrays. To put the pivot in the
        # right place we could swap it to either a[high] or a[low], but the
        # swapped element will end up in a[first], which we'll recurse with
        # section 2, so we must swap the pivot with a[high].
        pivot_index = high

        # Note also that it's possible that first == pivot_index, if section 2
        # is empty. That's fine, we'll swap with ourselves and the first
        # recursion below will do nothing.
        a[first], a[pivot_index] = a[pivot_index], a[first]

        # Recurse on our two sub-arrays, avoiding the pivot. If the "pivot_value"
        # appeared multiple times in the original array, it'll be in one or both
        # of the sub-arrays and will end up adjacent to "pivot_index".
        sort_part(first, pivot_index - 1)
        sort_part(pivot_index + 1, last)

    # Sort the entire array.
    sort_part(0, len(a) - 1)

def test():
    # Many tests.
    for i in range(100000):
        # Generate random array. Keep it short so we have duplicates.
        a = []
        for j in range(random.randint(0, 1000)):
            a.append(random.randint(-100, 100))

        # Make a copy that we'll sort separately.
        b = a[:]

        # Our own sort.
        qsort(a)

        # Python's sort.
        b.sort()

        # Progress bar.
        if i % 1000 == 0:
            print i

        # See if we got it right.
        if a != b:
            print a
            print b

if __name__ == "__main__":
    try:
        test()
    except KeyboardInterrupt:
        # After the ^C printed by the terminal (or by Python?).
        print

