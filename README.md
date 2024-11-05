# Supplementary material for "[_Discrete and mixed-variable experimental design with surrogate-based approach_](https://doi.org/10.1039/D4DD00113C)"

# Contents

* [Description](#description)

* [How to use this repository](#howto)

* [PWAS](#pwas)
  
* [Case studies](#casestudies)

* [Authors](#contributors)

* [Citing ](#bibliography)

* [License](#license)

<a name="description"></a>
## Description
**Full paper link**: [Link](https://doi.org/10.1039/D4DD00113C)

Experimental design aims to efficiently collect informative data and derive meaningful conclusions while operating within resource constraints. We propose the use of a different framework with mixed-integer surrogates and acquisition functions, where we adopt [_PWAS_](https://github.com/mjzhu-p/PWAS) (Piecewise Affine Surrogate-based optimization), which is designed to address the challenges posed by mixed-variable problems subject to linear constraints. _PWAS_ enables the direct incorporation of discrete and mixed-variable decision variables, facilitating a more realistic representation of real-world problems. Moreover, _PWAS_ accommodates linear equality and inequality constraints commonly encountered in physical systems, ensuring feasible solutions are proposed. 

We demonstrate the effectiveness of _PWAS_ in optimizing experimental designs through three case studies, each with a different size of design space and numerical complexity: 
* Optimization of reaction conditions for **Suzuki–Miyaura cross-coupling** (fully categorical) 
* Optimization of **crossed-barrel design** to augment mechanical toughness (mixed-integer)
* Solvent design for enhanced **Menschutkin reaction** rate (mixed-integer and categorical with linear constraints)

By comparing with conventional optimization algorithms, we offer insights into the practical applicability of _PWAS_.

We refer readers to the [**paper**](https://doi.org/10.1039/D4DD00113C) for detailed discussions. 

<a name="howto"></a>
## How to use this repository
The case studies and relevant files needed to reproduce the results in the paper are available.

To obtain a local copy of the repository:
~~~code
git clone https://github.com/MolChemML/ExpDesign.git
~~~

To run the case studies, the following steps need to be followed:

First, install the [_PWAS_](https://github.com/mjzhu-p/PWAS) package. 
  * 🔴IMPORTANT: there are **external** dependencies of _PWAS_. See the package [repository](https://github.com/mjzhu-p/PWAS) for the detailed installation instructions for the MILP solvers used by _PWAS_. You can either obtain a free [academic license](https://www.gurobi.com/academia/academic-program-and-licenses/) (if applicable) for [`GUROBI`](https://support.gurobi.com/hc/en-us/articles/14799677517585-Getting-Started-with-Gurobi-Optimizer) or download the free [`GLPK`](https://stackoverflow.com/questions/17513666/installing-glpk-gnu-linear-programming-kit-on-windows) package or interface other MILP solvers following the instruction noted in [_PWAS_](https://github.com/mjzhu-p/PWAS). We used `GUROBI` for our case studies.
  * See an overview of _PWAS_ at [this section](#pwas)

Second, to run the case studies and the relevant analysis to generate figures, you need to include the following additional packages to load the dataset and export the results:
* [pandas](https://pypi.org/project/pandas/) >= 2.1.0
* [openpyxl](https://pypi.org/project/openpyxl/) >= 3.1.2
* [seaborn](https://pypi.org/project/seaborn/) >= 0.13.2
* [matplotlib](https://pypi.org/project/matplotlib/) >= 3.8.3
* [sklearn](https://pypi.org/project/scikit-learn/) >= 1.3.0

Other notes:
* For the information on each case study, please see the relevant folder noted at [Case studies](#casestudies)
* We used the [_Olympus_](https://github.com/aspuru-guzik-group/olympus) package to run comparison studies. Please see the [forked version](https://github.com/mjzhu-p/olympus/tree/pwas_comp) for the relevant updates required to run the case studies.
    * 🔴IMPORTANT: _Olympus_ require tensorflow==1.15, therefore, **python version < 3.8 is required**
    * The `yml` file used by the authors to run the comparison studies is included: [`olympus_pwas_comp.yml`](https://github.com/MolChemML/ExpDesign/blob/main/utils/olympus_pwas_comp.yml)

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
For Suzuki coupling and crossed barrel case studies, we compare the performances of _PWAS_ with the algorithms implemented in the following packages:
* [_Genetic_](https://github.com/DEAP/deap)
* [_Hyperopt_](https://github.com/hyperopt/hyperopt) (tpe)
* [_Botorch_](https://github.com/pytorch/botorch) (BO with GP)
* [_EDBO_](https://github.com/b-shields/edbo) (BO with GP trained on reaction optimization data)
Additionally, we also consider _Random Search_ as a baseline

We note that _Random Search_, _Genetic_, _Hyperopt_, and _BoTorch_ have been interfaced in the [_Olympus_](https://github.com/aspuru-guzik-group/olympus) package; therefore, we use the algorithmic structure implemented in the
package for benchmark tests with their default solver parameters. A customized forked version tailored for our testing is also available on GitHub at [Branch “pwas_comp“](https://github.com/mjzhu-p/olympus/tree/pwas_comp), which you can see all the modifications. Note, some modifications are only necessary for Windows systems.

The tests were repeated **30** times. Within each run, the maximum iteration was set to **50**, with 10 initial samples.

As for the solvent design case study, due to the relatively large number of constraints involved, comparisons with the aforementioned solvers are impractical, instead, it is compared with a recently proposed [_DoE-QM-CAMD_](https://www.sciencedirect.com/science/article/pii/S0098135423002156#sec4)  method.

### Suzuki–Miyaura cross-coupling

<p align = "center">
<img src="https://github.com/mjzhu-p/ExpDesign/blob/main/case%20study%20notes/suzuki_rxn.png" alt="drawing" width=90%/>
</p>

* **Design space**: fully categorical
* **Optimization goal**: to identify optimial combinatorial sets of precursors that can **_maximize the yield_** of the desired product
* **Parameters to optimize**: aryl halide (X), boronic acid derivative (Y), base, ligand, and solvent
* **Notes on the code**:
  * Relevant folder: [`suzuki_edbo`](https://github.com/mjzhu-p/olympus/tree/pwas_comp/case_studies/case_study_pwas/z_comparisonStudy/suzuki_edbo)
  * The files needed to run each optimization method are included:
      * `run_xx.py`: run xx opt. method to solve the case study
      * for  _Random Search_, _Genetic_, _Hyperopt_, and _BoTorch_, `run_xx.py` files are based on the files included in the [_Olympus_](https://github.com/mjzhu-p/olympus/tree/pwas_comp/case_studies/case_study_2_suzuki) package
      * for _EDBO_, `run_edbo.py` is based on the file included in the [_EDBO_](https://github.com/b-shields/edbo/blob/master/experiments/edbo_demo_and_simulations.ipynb) package
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
* **Optimization goal**: to identify optimial combinatorial sets of structure parameters that can **_maximize the toughness_** of the resulting crossed-barrel strucure while not exceeding a specified force threshold
* **Parameters to optimize**:
  * number of hollow columns ($n$), twist angle of the columns ($\theta$), outer radius of the columns ($r$), and thickness of the hollow columns ($t$)
* **Notes on the code**:
  * Relevant folder: [`crossed_barrel`](https://github.com/mjzhu-p/olympus/tree/pwas_comp/case_studies/case_study_pwas/z_comparisonStudy/crossed_barrel)
  * The files needed to run each solver are included.
      * `corssed_barrel_othersolvers.py`:  run  _Random Search_, _Genetic_, _Hyperopt_, and _BoTorch_ to solve the case study. This file is based on the file included in the [_Olympus_](https://github.com/mjzhu-p/olympus/blob/pwas_comp/case_studies/case_study_1/run.py) package
      * for _EDBO_, `crossedBarrel_ebdo.py` is based on the file included in the [_EDBO_](https://github.com/b-shields/edbo/blob/master/experiments/edbo_demo_and_simulations.ipynb) package
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
* **Optimization goal**: to identify optimial solvent compositions to **_enhance the reaction rate_** of the Menschutkin reaction of phenacyl bromide and pyridine
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
  * `main.py`: run _PWAS_ to solve the case study
  * `gc_lnkCal.py`: calculate the ln(K) data from group contribution
  * `qm_simulator.py`: return the ln(k) value given the structure of the solvent, ln(k) value is obtained from quantum-mechanical (QM) calculations 
  * `solvent_list_matrix.xlsx`: Excel file including the full feasible design space, bounds and constraints on the optimization variables, group contribution values
      * This file is updated based on [Gui _et al_, 2023](https://www.sciencedirect.com/science/article/pii/S0098135423002156#sec4)
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
@article{ExpDesign2024,
  title={Discrete and mixed-variable experimental design with surrogate-based approach},
  author={Zhu, Mengjia and Mroz, Austin and Gui, Lingfeng and Jelfs, Kim E and Bemporad, Alberto and Chanona, Antonio Del Rio and Lee, Ye Seol},
  journal={Digital Discovery},
  year={2024},
  publisher={Royal Society of Chemistry}
}
```

<a name="license"><a>
## License

MIT
