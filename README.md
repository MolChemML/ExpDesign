# Supplementary material for "_Discrete and mixed-variable experimental design with surrogate-based approach_"

# Contents

* [Description](#description)

* [PWAS](#pwas)
  
* [Case studies](#casestudies)

* [Authors](#contributors)

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

<a name="pwas"></a>
## PWAS
The package is available in the [repository](https://github.com/mjzhu-p/PWAS)

The flowchart of the solver is shown here:
<p align = "center">
<img src="https://github.com/mjzhu-p/ExpDesign/blob/main/case%20study%20notes/pwas%20flowchart.png" alt="drawing" width=60%/>
</p>

where [_PARC_](https://github.com/bemporad/PyPARC) is the package used to fit the surrogate, whose flowchart is shown below:
<p align = "center">
<img src="https://github.com/mjzhu-p/ExpDesign/blob/main/case%20study%20notes/parc_flowchart.png" alt="drawing" width=60%/>
</p>



<a name="casestudies"></a>
## Case studies
For Suzuki coupling and crossed barrel case studies, we compare the performances of _PWAS_ with the following solvers:
* _Random Search_
* _Genetic_
* [_Hyperopt_]() (tpe)
* [_Botorch_]()
* [_EDBO_]()

We note that solver _Random Search_, _Genetic_, _Hyperopt_, and _BoTorch_ have been interfaced in the [_Olympus_]() package; therefore, we use the algorithmic structure implemented in the
package for benchmark tests with their default solver parameters. A customized forked version tailored for our testing is also available on GitHub at https://github.com/mjzhu-p/olympus/tree/pwas_comp (Branch “pwas_comp“).


### Suzuki coupling
<p align = "center">
<img src="https://github.com/mjzhu-p/ExpDesign/blob/main/case%20study%20notes/suzuki_rxn.png" alt="drawing" width=60%/>
</p>

### Crossed barrel
<p align = "center">
<img src="https://github.com/mjzhu-p/ExpDesign/blob/main/case%20study%20notes/crossed_barrel_example.png" alt="drawing" width=30%/>
</p>

### Solvent design
<p align = "center">
<img src="https://github.com/mjzhu-p/ExpDesign/blob/main/case%20study%20notes/menschutkin%20rxn.png" alt="drawing" width=60%/>
</p>



<a name="contributors"><a>
## Authors

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
