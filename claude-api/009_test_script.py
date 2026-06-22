def greeting():
    print ("Hi there")

def calculate_pi():
    """
    Calculate pi to the 5th decimal place (3.14159)
    using the Leibniz formula for pi:
      pi/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 - ...
    We iterate until the result is accurate to 5 decimal places.
    """
    pi_approx = 0
    denominator = 1
    sign = 1
    # A high number of iterations ensures 5 decimal place accuracy
    for _ in range(1_000_000):
        pi_approx += sign * (4 / denominator)
        denominator += 2
        sign *= -1

    # Round to the 5th decimal place
    return round(pi_approx, 5)