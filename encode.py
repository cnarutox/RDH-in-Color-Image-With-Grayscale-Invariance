#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from fractions import Fraction


def build_prob(input_codes):
    counts = defaultdict(int)

    for code in input_codes:
        counts[code] += 1

    counts[256] = 1

    output_prob = dict()
    length = len(input_codes)
    cumulative_count = 0

    for code in sorted(counts, key=counts.get, reverse=True):
        current_count = counts[code]
        prob_pair = Fraction(cumulative_count, length), Fraction(current_count, length)
        output_prob[code] = prob_pair
        cumulative_count += current_count

    return output_prob


def encode_fraction_range(input_codes, input_prob):
    start = Fraction(0, 1)
    width = Fraction(1, 1)

    for code in input_codes:
        d_start, d_width = input_prob[code]
        start += d_start * width
        width *= d_width

    return start, start + width


def find_binary_fraction(input_start, input_end):
    output_fraction = Fraction(0, 1)
    output_denominator = 1

    while not (input_start <= output_fraction < input_end):
        output_numerator = 1 + ((input_start.numerator * output_denominator) // input_start.denominator)
        output_fraction = Fraction(output_numerator, output_denominator)
        output_denominator *= 2

    return output_fraction


def decode_fraction(input_fraction, input_prob):
    output_codes = []
    code = 257

    while code != 256:
        for code, (start, width) in input_prob.items():
            if 0 <= (input_fraction - start) < width:
                input_fraction = (input_fraction - start) / width

                if code < 256:
                    output_codes.append(code)
                break

    return ''.join([chr(code) for code in output_codes])


def encode(msg):
    # codes = [ord(str(char)) for char in msg] + [256]
    # prob = build_prob(codes)
    # fraction_range = encode_fraction_range(codes, prob)
    # binary_fraction = find_binary_fraction(*fraction_range)
    return ''.join([f"{bin(ord(i))[2:]:>08}" for i in msg])


def decode(msg):
    return ''.join([chr(int(i, 2)) for i in (msg[i:i + 8] for i in range(0, len(msg), 8))])


if __name__ == '__main__':
    string = '0100011'
    codes = [ord(char) for char in string] + [256]

    prob = build_prob(codes)
    print('prob:', repr(prob))
    print('len(prob):', repr(len(prob)))

    fraction_range = encode_fraction_range(codes, prob)
    print('fraction_range:', repr(fraction_range))

    decoded_fraction = decode_fraction(fraction_range[0], prob)
    print('decoded_fraction:', repr(decoded_fraction))

    binary_fraction = find_binary_fraction(fraction_range[0], fraction_range[1])
    print('binary_fraction:', repr(binary_fraction))

    decoded_binary_fraction = decode_fraction(binary_fraction, prob)
    print('decoded_binary_fraction:', repr(decoded_binary_fraction))