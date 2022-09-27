import math

import numpy.linalg


class DirectionalDerivative:
    def __init__(self, base_origin_point):
        self.base_origin_point = base_origin_point

    def __call__(self, perturbation, section):
        origin_fiber = section(self.base_origin_point)
        # TODO : sequence of smaller t? find equivalence class of paths ?
        t = 1e-3
        perturbed_base_point = self.base_origin_point + perturbation(t)
        perturbed_fiber = section(perturbed_base_point)
        # TODO: Do we need to use connection here ?
        directional_derivative = (perturbed_fiber - origin_fiber) / t
        return directional_derivative


class SchwarzschildMetricTensorSection:
    def __init__(self, schwarzschild_radius):
        self.event_horizon = schwarzschild_radius / 4

    def __call__(self, point):
        radius = math.sqrt(point[1] ** 2 + point[2] ** 2 + point[3] ** 2)
        relative_radius = self.event_horizon / radius
        negatively_perturbed_squared = (1 - relative_radius) ** 2
        positively_perturbed_squared = (1 + relative_radius) ** 2
        metric_tensor = numpy.array(
            [
                [-(negatively_perturbed_squared / positively_perturbed_squared), 0, 0, 0],
                [0, positively_perturbed_squared, 0, 0],
                [0, 0, positively_perturbed_squared, 0],
                [0, 0, 0, positively_perturbed_squared],
            ]
        )
        return metric_tensor


class EinsteinFieldEquations:
    def __init__(
        self,
        perturbations,
        einstein_gravitational_constant,
        metric_tensor_section,
        cosmological_constant,
        stress_energy_tensor_section,
    ):
        self.einstein_gravitational_constant = einstein_gravitational_constant
        self.cosmological_constant = cosmological_constant
        self.metric_tensor_section = metric_tensor_section
        self.metric_tensor_inverse_section = lambda point: numpy.linalg.inv(self.metric_tensor_section(point))
        self.metric_tensor_determinant_section = lambda point: numpy.linalg.det(self.metric_tensor_section(point))
        self.metric_tensor_determinant_section_first_derivatives_section = lambda point: numpy.array(
            [
                DirectionalDerivative(point)(perturbation, self.metric_tensor_determinant_section)
                for perturbation in perturbations
            ]
        )
        self.metric_tensor_section_first_derivatives_section = lambda point: numpy.array(
            [DirectionalDerivative(point)(perturbation, self.metric_tensor_section) for perturbation in perturbations]
        )
        self.metric_tensor_section_second_derivatives_section = lambda point: numpy.array(
            [
                DirectionalDerivative(point)(perturbation, self.metric_tensor_section_first_derivatives_section)
                for perturbation in perturbations
            ]
        )
        self.stress_energy_tensor_section = stress_energy_tensor_section

    @staticmethod
    def formula_einstein_gravitational_constant(gravitational_constant=6.67430e-11, speed_of_light=299792458):
        return 8 * math.pi * gravitational_constant / (speed_of_light**4)

    def formula_stress_energy_part(self, point):
        return self.einstein_gravitational_constant * self.stress_energy_tensor_section(point)

    def formula_geometric_part(self, point):
        result = self.cosmological_constant * self.metric_tensor_section(point)
        metric_tensor_section_first_derivatives_fiber = self.metric_tensor_section_first_derivatives_section(point)
        metric_tensor_inverse_fiber = self.metric_tensor_inverse_section(point)
        metric_tensor_section_second_derivatives_fiber = self.metric_tensor_section_second_derivatives_section(point)
        metric_tensor_determinant_fiber = self.metric_tensor_determinant_section(point)
        metric_tensor_determinant_section_first_derivatives_fiber = (
            self.metric_tensor_determinant_section_first_derivatives_section(point)
        )

        for out0 in range(4):
            for out1 in range(4):
                for c0 in range(4):
                    for c1 in range(4):
                        for c2 in range(4):
                            for c3 in range(4):
                                result[out0][out1] += (
                                    metric_tensor_inverse_fiber[c1][c2]
                                    * metric_tensor_inverse_fiber[c0][c3]
                                    * (
                                        -1
                                        / 2
                                        * metric_tensor_section_first_derivatives_fiber[c0][c3][c2]
                                        * metric_tensor_section_first_derivatives_fiber[out0][c1][out1]
                                        - 1
                                        / 2
                                        * metric_tensor_section_first_derivatives_fiber[c0][c3][c2]
                                        * metric_tensor_section_first_derivatives_fiber[out1][out0][c1]
                                        - 1
                                        / 2
                                        * metric_tensor_section_first_derivatives_fiber[out1][c0][c2]
                                        * metric_tensor_section_first_derivatives_fiber[out0][c3][c1]
                                    )
                                )
                        result[out0][out1] += metric_tensor_inverse_fiber[c0][c1] * (
                            1 / 2 * metric_tensor_section_second_derivatives_fiber[c0][out0][c1][out1]
                            + 1 / 2 * metric_tensor_section_second_derivatives_fiber[c0][out1][out0][c1]
                            - 1 / 2 * metric_tensor_section_second_derivatives_fiber[c0][c1][out0][out1]
                            - 3 / 2 * metric_tensor_section_second_derivatives_fiber[out0][out1][c0][c1]
                            + 1
                            / (4 * metric_tensor_determinant_fiber)
                            * metric_tensor_determinant_section_first_derivatives_fiber[c1]
                            * metric_tensor_section_first_derivatives_fiber[out1][out0][c0]
                            - 1
                            / (4 * metric_tensor_determinant_fiber)
                            * metric_tensor_determinant_section_first_derivatives_fiber[c1]
                            * metric_tensor_section_first_derivatives_fiber[c0][out0][out1]
                            - 1
                            / (4 * metric_tensor_determinant_fiber)
                            * metric_tensor_determinant_section_first_derivatives_fiber[c1]
                            * metric_tensor_section_first_derivatives_fiber[out0][c0][out1]
                        )

        return numpy.array(result)


if __name__ == "__main__":
    metric_tensor_section = SchwarzschildMetricTensorSection(3000)
    perturbations = [
        lambda _: numpy.array([1, 0, 0, 0]),
        lambda _: numpy.array([0, 1, 0, 0]),
        lambda _: numpy.array([0, 0, 1, 0]),
        lambda _: numpy.array([0, 0, 0, 1]),
    ]
    efe = EinsteinFieldEquations(
        perturbations, EinsteinFieldEquations.formula_einstein_gravitational_constant(), metric_tensor_section, 0, None
    )
    value = efe.formula_geometric_part(numpy.array([0, 0, 0, 3001]))
