# Supplementary material for "_Discrete and mixed-variable experimental design with surrogate-based approach_"

# Contents

* [Description](#description)

* [Basic usage](#basic-usage)

* [Contributors](#contributors)

* [Citing ](#bibliography)

* [License](#license)

<a name="description"></a>
## Description

Experimental design aims to efficiently collect informative data and derive meaningful conclusions while operating within resource constraints. Conventional approaches often confine exploration to predetermined conditions, potentially overlooking valuable insights. Recent advancements, integrate high-throughput experimentation and machine learning, to enhance experimental capabilities, however, they face challenges in navigating complex search spaces. Moreover, constrained mixed-variable and/or combinatorial design spaces commonly present in chemical and physical applications introduce additional difficulties for Bayesian optimization approaches, which are currently the go-to methods in the field. In this context, we propose the use of _PWAS_ (Piecewise Affine Surrogate-based optimization), designed to address the challenges posed by mixed-variable experimental designs. _PWAS_ enables the direct incorporation of discrete and mixed-variable decision variables, facilitating a more realistic representation of real-world problems. Moreover, _PWAS_ accommodates linear equality and inequality constraints commonly encountered in physical systems, ensuring feasible solutions are proposed. We demonstrate the effectiveness of _PWAS_ in optimizing experimental designs through three case studies, each with a different size of design space and numerical complexity: i) optimization of reaction conditions for Suzuki–Miyaura cross-coupling (fully categorical), ii) optimization of crossed-barrel design to augment mechanical toughness (mixed-integer), and iii) solvent design for enhanced Menschutkin reaction rate (mixed-integer and categorical with linear constraints). By comparing with conventional optimization algorithms, we offer insights into the practical applicability of _PWAS_
