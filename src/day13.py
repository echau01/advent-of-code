def gcd(a: int, b: int) -> int:
    """
    Returns the greatest common divisor of a and b, assuming that a and b are positive.
    """

    while b != 0:
        temp = b
        b = a % b
        a = temp

    return a


def lcm(a: int, b: int) -> int:
    """
    Returns the least common multiple of a and b, assuming that a and b are positive.
    """

    # The prime factorizations of a and b can be written in the form:
    # a = 2^(m_1) * 3^(m_2) * 5^(m_3) * ...
    # b = 2^(n_1) * 3^(n_2) * 5^(n_3) * ...
    # where the m_k and n_k are integers greater than or equal to 0.
    #
    # Then gcd(a, b) = 2^min(m_1,n_1) * 3^min(m_2,n_2) * 5^min(m_3,n_3) * ...
    # and lcm(a, b) = 2^max(m_1,n_1) * 3^max(m_2,n_2) * 5^max(m_3,n_3) * ...
    #
    # gcd(a, b) * lcm(a, b)
    # = 2^[min(m_1,n_1) + max(m_1,n_1)] * 3^[min(m_2,n_2) + max(m_2,n_2)] * 5^[min(m_3,n_3) + max(m_3,n_3)] * ...
    # = 2^(m_1 + n_1) * 3^(m_2 + n_2) * 5^(m_3 + n_3) * ... (because min(x,y) + max(x,y) = x+y for all x and y)
    # = ab
    # Hence lcm(a, b) = ab/gcd(a,b).
    return (a // gcd(a, b)) * b


with open("day13.txt", "r") as f:
    contents = f.read().splitlines()

time = int(contents[0])
buses = contents[1].split(",")

# Maps bus ID to the index where that bus ID appears in the buses list.
buses_indices_map = {int(buses[i]): i for i in range(len(buses)) if buses[i] != "x"}

earliest_bus_id = None
waiting_time = None

for bus_id in buses_indices_map:
    if waiting_time is None or (bus_id - (time % bus_id)) % bus_id < waiting_time:
        waiting_time = (bus_id - (time % bus_id)) % bus_id
        earliest_bus_id = bus_id

print(earliest_bus_id * waiting_time)

# Part 2

# Theorem:
# Suppose we have sets of positive integers X = {x_1, ..., x_n},
# M = {m_1, ..., m_n}, and R = {r_1, ..., r_n} such that x_i ≡ r_i (mod m_i)
# for all 1 <= i <= n (where n is some positive integer). Define L to be the lowest
# common multiple of all the numbers in M. Then x_i + L ≡ r_i (mod m_i) for all i.
# Furthermore, if p is a positive number such that x_i + p ≡ r_i (mod m_i) for all i,
# then p must be a multiple of L.

# Proof:
# Consider an arbitrary integer n >= 1.
# We have defined L = lcm(m_1, m_2, ..., m_n). It follows that L is divisible by m_i
# for all 1 <= i <= n. Suppose x_i ≡ r_i (mod m_i) for all i. Then:
# x_i + L ≡ r_i + L (mod m_i)
# ≡ r_i + 0 (mod m_i)
# ≡ r_i (mod m_i)
#
# Suppose there is some positive number p such that x_i + p ≡ r_i (mod m_i) for all i. Then:
# x_i + p ≡ r_i (mod m_i)
# => r_i + p ≡ r_i (mod m_i) [because x_i ≡ r_i (mod m_i)]
# => p ≡ 0 (mod m_i)
# => p is divisible by m_i for all i
# It follows that p must be a multiple of L, since L is the lowest positive number that is
# divisible by m_i for all i. QED.


# Now we define our loop invariants.
# Suppose the iterator of buses_indices_map gives us bus IDs in the order b_0, b_1, ..., b_(n-1)
# where n is the size of the dict. At the beginning of iteration i:
# 1. current_lcm is the LCM of all b_k for 0 <= k < i.
# 2. result is the *smallest* positive integer such that for all 0 <= k < i,
# result + buses_indices_map[b_k] is a multiple of b_k. Equivalently, result
# is the smallest integer such that result ≡ b_k - buses_indices_map[b_k] (mod b_k)
# for all 0 <= k < i.

current_lcm = 1
result = 1

for bus_id, offset in buses_indices_map.items():
    # Here, we restore invariant 2 for iteration i+1. Note that b_i == bus_id
    # and offset == buses_indices_map[b_i]. We want to find a value of result
    # such that result + offset is a multiple of bus_id. In the process,
    # we want to maintain the property that result + buses_indices_map[b_k]
    # is a multiple of b_k for all 0 <= k < i.
    #
    # The algorithm for restoring invariant 2 is as follows:
    #
    # 1. Check if result + offset is a multiple of bus_id. If it is, then we
    # are done, since result + buses_indices_map[b_k] is a multiple of b_k
    # for all 0 <= k < i+1.
    # 2. If the above conditional check fails, then we will add current_lcm to result.
    # Invariant 1 tells us that current_lcm = lcm(b_0, b_1, ..., b_(i-1)),
    # and invariant 2 tells us that result ≡ b_k - buses_indices_map[b_k] (mod b_k)
    # for 0 <= k < i. By the theorem above, the new value of result is the next smallest
    # value that satisfies invariant 2 for 0 <= k < i. After updating result, we go back 
    # to step 1 to check if we are done.
    #
    # This algorithm terminates assuming that there exists a value of result that
    # restores invariant 2 for iteration i+1. There might not be a solution, however.
    # For example, if buses_indices_map = {4: 0, 6: 1}, then the following will happen:
    # - on the first iteration, result will be set to 4, and current_lcm will also
    # be set to 4.
    # - on the second iteration, we will try to find a value of result such that
    # result + 0 is a multiple of 4 and result + 1 is a multiple of 6. However, no such
    # value of result exists, because if result + 0 is a multiple of 4, then
    # result + 1 must be an odd number, which can never be a multiple of 6. The algorithm
    # will loop forever.
    #
    # How can we detect an infinite loop? If the loop runs more than bus_id times,
    # we have an infinite loop. More precisely, suppose we keep track of the values
    # of (result + offset) % bus_id that we have seen so far. If we see the same
    # value twice, we have an infinite loop. There are bus_id possible values
    # of (result + offset) % bus_id, so by the pigeonhole principle, we will have
    # seen one of those values more than once if the loop runs more than bus_id times.
    # We can then break out of the loop.

    counter = 0

    while (result + offset) % bus_id != 0:
        result += current_lcm
        counter += 1

        if counter > bus_id:
            result = None
            break

    if result is None:
        break

    # Restore invariant 1 for iteration i+1.
    current_lcm = lcm(current_lcm, bus_id)

print(result if result is not None else "No solution exists.")
