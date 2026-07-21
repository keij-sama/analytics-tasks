from math import sqrt
from statistics import NormalDist

CONTROL_CONVERSIONS = 621
CONTROL_SIZE = 6076
TEST_CONVERSIONS = 745
TEST_SIZE = 6076
ALPHA = 0.05


def main() -> None:
    p_control = CONTROL_CONVERSIONS / CONTROL_SIZE
    p_test = TEST_CONVERSIONS / TEST_SIZE
    effect = p_test - p_control

    pooled = (CONTROL_CONVERSIONS + TEST_CONVERSIONS) / (CONTROL_SIZE + TEST_SIZE)
    pooled_se = sqrt(pooled * (1 - pooled) * (1 / CONTROL_SIZE + 1 / TEST_SIZE))
    z_stat = effect / pooled_se
    p_value = 2 * (1 - NormalDist().cdf(abs(z_stat)))

    ci_se = sqrt(
        p_control * (1 - p_control) / CONTROL_SIZE
        + p_test * (1 - p_test) / TEST_SIZE
    )
    critical = NormalDist().inv_cdf(1 - ALPHA / 2)
    ci_low = effect - critical * ci_se
    ci_high = effect + critical * ci_se

    print(f"Control conversion: {p_control:.4%}")
    print(f"Test conversion: {p_test:.4%}")
    print(f"Absolute effect: {effect * 100:.4f} pp")
    print(f"Relative uplift: {effect / p_control:.2%}")
    print(f"z-statistic: {z_stat:.4f}")
    print(f"Two-sided p-value: {p_value:.6f}")
    print(f"95% CI: [{ci_low * 100:.4f}, {ci_high * 100:.4f}] pp")


if __name__ == "__main__":
    main()
