# Zero-Run-Length-Bound-Theorem

## Overview

This project explores the logarithmic bounds on the lengths of consecutive zeros (zero runs) in binary expansions of algebraic and transcendental numbers. By leveraging tools from Diophantine approximation theory, including Roth's theorem and Mahler's irrationality measure, it rigorously establishes these bounds, offering valuable insights into the structure of binary expansions and their connections to randomness, cryptography, and number theory.

---

## Key Results

### Algebraic Numbers
- For an algebraic number of degree \(d\), the maximum zero-run length \(k\) satisfies:
  ```math
  k \leq d \cdot \log_2(n)
  ```
  where \(n\) represents the position of the zero run.

### Transcendental Numbers
- For transcendental numbers, the maximum zero-run length \(k\) satisfies:
  ```math
  k \leq \mu \cdot \log_2(n)
  ```
  where \(\mu\) is the irrationality measure.

---

## Applications

1. **Number Theory**: Insights into the binary expansions of numbers and their patterns.
2. **Cryptography**: Provides statistical tests to evaluate randomness in sequences.
3. **Ergodic Theory**: Connections between zero runs and symbolic dynamics in binary expansions.
4. **Complexity Theory**: Links between Kolmogorov complexity and digit patterns.

---

## Structure of the Paper

1. **Introduction**: Background on binary expansions and their significance.
2. **Objective**: Definition of bounds on zero runs for algebraic and transcendental numbers.
3. **Proofs**:
   - **Algebraic Numbers**: Bounds derived using Roth's theorem.
   - **Transcendental Numbers**: Results based on Mahler's irrationality measure.
4. **Numerical Examples**: Empirical validations for \(\sqrt{2}\), the golden ratio (\(\phi\)), and more.
5. **Applications**: Implications in randomness, cryptography, and number theory.
6. **Future Directions**:
   - Generalizing bounds to base-\(b\) expansions.
   - Pattern analysis beyond zero runs.

---

## Supplementary Materials

All additional resources, including source code and computational examples, are available in the [GitHub repository](https://github.com/DJ-Greenwood/Zero-Run-Length-Bound-Theorem).

---

## References

This work builds on foundational theories and results, including:

1. Roth, K. F. (1955). Rational approximations to algebraic numbers. Mathematika, 2(1), 1-20.
2. Khintchine, A. (1926). Continued fractions. Mathematical Sbornik, 32(4), 14-40.
3. Borel, É. (1909). Les probabilités dénombrables et leurs applications arithmétiques. Rendiconti del Circolo Matematico di Palermo, 27(1), 247-271.
4. Baker, A. (1975). Transcendental Number Theory. Cambridge University Press.
5. Mahler, K. (1932). Zur Approximation der Exponentialfunktion und des Logarithmus. Journal für die reine und angewandte Mathematik, 166, 118-150.
6. Walters, P. (1982). An Introduction to Ergodic Theory. Springer-Verlag.
7. Li, M. and Vitányi, P. (2008). An Introduction to Kolmogorov Complexity and Its Applications. Springer.
8. Katok, A. and Hasselblatt, B. (1995). Introduction to the Modern Theory of Dynamical Systems. Cambridge University Press.
9. Schmidt, W. M. (1980). Diophantine Approximation. Springer-Verlag.
10. Niederreiter, H. (1992). Random Number Generation and Quasi-Monte Carlo Methods. SIAM.
11. Drmota, M. and Rivat, J. (2015). The sum-of-digits function of squares. Journal of the London Mathematical Society, 93(3), 587-605.
12. Bugeaud, Y. (2012). Distribution Modulo One and Diophantine Approximation. Cambridge University Press.
13. Mauduit, C. and Sárközy, A. (1997). On finite pseudorandom binary sequences. Journal of Complexity, 13(4), 466-475.
14. Pollicott, M. and Yuri, M. (1998). Dynamical Systems and Ergodic Theory. Cambridge University Press.
15. Lagarias, J. C. (1985). The computational complexity of simultaneous Diophantine approximation problems. SIAM Journal on Computing, 14(1), 196-209.

---

For detailed mathematical derivations, proofs, and discussions, refer to the full paper.

