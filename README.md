# Supplementary material for "_Discrete and mixed-variable experimental design with surrogate-based approach_"

# Contents

* [Description](#description)

* [Case studies](#casestudies)

* [Contributors](#contributors)

* [Citing ](#bibliography)

* [License](#license)

<a name="description"></a>
## Description

Experimental design aims to efficiently collect informative data and derive meaningful conclusions while operating within resource constraints. We propose the use of [_PWAS_](https://github.com/mjzhu-p/PWAS) (Piecewise Affine Surrogate-based optimization), designed to address the challenges posed by mixed-variable experimental designs. _PWAS_ enables the direct incorporation of discrete and mixed-variable decision variables, facilitating a more realistic representation of real-world problems. Moreover, _PWAS_ accommodates linear equality and inequality constraints commonly encountered in physical systems, ensuring feasible solutions are proposed. 

We demonstrate the effectiveness of _PWAS_ in optimizing experimental designs through three case studies, each with a different size of design space and numerical complexity: 
* optimization of reaction conditions for Suzuki–Miyaura cross-coupling (fully categorical), 
* optimization of crossed-barrel design to augment mechanical toughness (mixed-integer), 
* solvent design for enhanced Menschutkin reaction rate (mixed-integer and categorical with linear constraints).

By comparing with conventional optimization algorithms, we offer insights into the practical applicability of _PWAS_

<a name="casestudies"></a>
## Case studies

### Suzuki coupling


### Crossed barrel


### Solvent design




<a name="contributors"><a>
## Contributors

Mengjia Zhu, Austin Mroz, Lingfeng Gui, Kim Jelfs, Alberto Bemporad, Ehecatl Antonio del Río Chanona, and Ye Seol Lee


This repository is distributed without any warranty. Please cite the paper below if you use it.

<a name="bibliography"><a>
## Citing the material

<a name="ref1"></a>
```
To add (arXiv)
```

<a name="license"><a>
## License

MIT

(C) 2023-2024 M. Zhu, A. Bemporad
