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
* Optimization of reaction conditions for **Suzuki–Miyaura cross-coupling** (fully categorical) 
* Optimization of **crossed-barrel design** to augment mechanical toughness (mixed-integer)
* Solvent design for enhanced **Menschutkin reaction** rate (mixed-integer and categorical with linear constraints)

By comparing with conventional optimization algorithms, we offer insights into the practical applicability of _PWAS_.

We refer readers to the [**manuscript**](toadd) for detailed discussions. 

<a name="pwas"></a>
## PWAS
The package is available in the [repository](https://github.com/mjzhu-p/PWAS), which can be installed via the following:
~~~code
pip install pwasopt
~~~

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
* [_Genetic_](https://github.com/DEAP/deap)
* [_Hyperopt_](https://github.com/hyperopt/hyperopt) (tpe)
* [_Botorch_](https://github.com/pytorch/botorch) (BO with GP)
* [_EDBO_](https://github.com/b-shields/edbo) (BO with GP trained on reaction optimization data)

We note that solver _Random Search_, _Genetic_, _Hyperopt_, and _BoTorch_ have been interfaced in the [_Olympus_](https://github.com/aspuru-guzik-group/olympus) package; therefore, we use the algorithmic structure implemented in the
package for benchmark tests with their default solver parameters. A customized forked version tailored for our testing is also available on GitHub at https://github.com/mjzhu-p/olympus/tree/pwas_comp (Branch “pwas_comp“), which you can see all the modifications. Note, some modifications are only necessary for Windows systems.

The tests were repeated **30** times. Within each run, the maximum iteration was set to **50**, with 10 initial samples.

As for the solvent design case study, due to the relatively large number of constraints involved, comparisons with the aforementioned solvers are impractical, instead, it is compared with a recently proposed [_DoE-QM-CAMD_](https://www.sciencedirect.com/science/article/pii/S0098135423002156#sec4)  method.

### Suzuki coupling

<p align = "center">
<img src="https://github.com/mjzhu-p/ExpDesign/blob/main/case%20study%20notes/suzuki_rxn.png" alt="drawing" width=60%/>
</p>

* **Design space**: fully categorical
* **Parameters to optimize**: electrophile (X), nucleophile (Y), base, ligand, and solvent
* **Notes on the code**:
  * Relevant folder: [`suzuki_edbo`](https://github.com/mjzhu-p/olympus/tree/pwas_comp/case_studies/case_study_pwas/z_comparisonStudy/suzuki_edbo)
  * The files needed to run each solver are included.
  * The results and the files used to generate figures are available at [`z_results`](https://github.com/mjzhu-p/olympus/tree/pwas_comp/case_studies/case_study_pwas/z_comparisonStudy/suzuki_edbo/z_results)

* **Results**: 
<p align = "center">
<img src="https://github.com/mjzhu-p/olympus/blob/pwas_comp/case_studies/case_study_pwas/z_comparisonStudy/suzuki_edbo/z_results/yield_trace_mean_suzuki_edbo.png" alt="drawing" width=33%/> &nbsp;
<img src="https://github.com/mjzhu-p/olympus/blob/pwas_comp/case_studies/case_study_pwas/z_comparisonStudy/suzuki_edbo/z_results/yield_rank_traces_suzuki_edbo.png" alt="drawing" width=33%/> &nbsp;
<img src="https://github.com/mjzhu-p/olympus/blob/pwas_comp/case_studies/case_study_pwas/z_comparisonStudy/suzuki_edbo/z_results/yield_boxplots_suzuki_edbo.png" alt="drawing" width=33%/>
</p>



### Crossed barrel

<p align = "center">
<img src="https://github.com/mjzhu-p/ExpDesign/blob/main/case%20study%20notes/crossed_barrel_example.png" alt="drawing" width=30%/>
</p>

* **Design space**: mixed-integer
* **Parameters to optimize**:
  * number of hollow columns ($n$), twist angle of the columns ($\theta$), outer radius of the columns ($r$), and thickness of the hollow columns ($t$)
* **Notes on the code**:
  * Relevant folder: [`crossed_barrel`](https://github.com/mjzhu-p/olympus/tree/pwas_comp/case_studies/case_study_pwas/z_comparisonStudy/crossed_barrel)
  * The files needed to run each solver are included.
  * The results and the files used to generate figures are available at [`z_results`](https://github.com/mjzhu-p/olympus/tree/pwas_comp/case_studies/case_study_pwas/z_comparisonStudy/crossed_barrel/z_results)

* **Results**: 
<p align = "center">
<img src="https://github.com/mjzhu-p/olympus/blob/pwas_comp/case_studies/case_study_pwas/z_comparisonStudy/crossed_barrel/z_results/toughness_trace_mean_crossedBarrel.png" alt="drawing" width=33%/>
</p>

### Solvent design

<p align = "center">
<img src="https://github.com/mjzhu-p/ExpDesign/blob/main/case%20study%20notes/menschutkin%20rxn.png" alt="drawing" width=60%/>
</p>

* **Design space**: mixed-integer and categorical
* **Variables to optimize**:
  * 46 integer variables indicating the number of each atom group present in the designed solvent
  * 1 auxiliary categorical variable to delineate the solvent's structure (acrylic, monocyclic, bicyclic)
  * 7 auxiliary binary variables for structure-related constraints
  * Along with 115 linear inequality constraints and 5 linear equality constraints to enforce structure-property, chemical feasibility- and complexity-related solution features.
      * For instance, constraints are used to ensure the octet rule, to specify the minimum of the octanol/water partition coefficient, and other relevant properties.
      * See the detailed list in [Gui et al, 2023](https://www.sciencedirect.com/science/article/pii/S0098135423002156#sec4)
      * Also formatted in this [Excel file](https://github.com/mjzhu-p/ExpDesign/blob/main/solvent%20design%20case%20study/solvent_list_matrix.xlsx)
* **Notes on the code**:
  * Relevant folder: [`solvent design case study`](https://github.com/mjzhu-p/ExpDesign/tree/main/solvent%20design%20case%20study)
  * The files needed to run _PWAS_ are included (`main.py`).
  * The results and the files used to generate figures are available at [`z_results`](https://github.com/mjzhu-p/ExpDesign/tree/main/solvent%20design%20case%20study/z_results)


* **Results** 
  
<p align = "center">
<img src="https://github.com/mjzhu-p/ExpDesign/blob/main/solvent%20design%20case%20study/z_results/figures/radarChart_initialSample.png" alt="drawing" width=30%/> &nbsp;
<img src="https://github.com/mjzhu-p/ExpDesign/blob/main/solvent%20design%20case%20study/z_results/figures/radarChart_first10AS.png" alt="drawing" width=30%/> &nbsp;
<img src="https://github.com/mjzhu-p/ExpDesign/blob/main/solvent%20design%20case%20study/z_results/figures/radarChart_last10AS.png" alt="drawing" width=30%/> 
</p>

**Solvent properties of the initial samples (left), the first 10 active-learning samples (middle), and the last 10 active-learning samples (right)**: $n^2$: refractive index at 298K, $B$: Abraham’s overall hydrogen-bond basicity, $\epsilon$: dielectric constant at 298K.

<p align = "center">
<img src="https://github.com/mjzhu-p/ExpDesign/blob/main/solvent%20design%20case%20study/z_results/figures/bubble_chart.png" alt="drawing" width=90%/>
</p>

**Bubble chart of chemical properties of the solvents**: $n^2$: refractive index at 298K, $\epsilon$: dielectric constant at 298K. Abraham’s overall hydrogen-bond basicity is represented by the size of each bubble, with the relevant bubble size scale shown in the legend.

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
