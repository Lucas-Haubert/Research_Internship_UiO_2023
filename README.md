
# Research Internship in Stochastics and Statistics, University of Oslo, 2023

## Overview

This repository is contains my work as a research intern at the University of Oslo (UiO), in 2023, oriented towards the study of stochastic volatility models with high-frequancy financial data. The objective is to explore the methodologies and implications of volatility models, for a various range of assets, in order to model prices in a relevant way.

A simple formulation to describe the price process $\(S_t\)_t$ is the model of continuous semi-martingale:

$$
{\large
\begin{equation}
    S_t = a_t S_t \, dt + \sigma_t S_t \, dW_t
\end{equation}
}
$$

## Repository Contents

- `data/` : Raw and pre-processed high-frequency financial data (HFFD).
- `utils/` : Utilitary files (data loaders, conversion, plots).
- `quadratic_vars_estim.py` : First step of the variational analysis of stochastic volatility.
- `quadratic_vars_estim_bis.py` : Second step of the variational analysis of stochastic volatility.
- `markovianity_test.py` : Implementation of the statistical test of local volatility hypothesis.
- `Report.pdf`: A detailed report of my work and findings.

## Acknowledgements

I would like to ackowledge [Giulia Di Nunno](https://sites.google.com/view/giuliadinunno/home), who have been my professor as an Exchange student in the Univeristy of Oslo, then my academic reference during this research internship. I also thank [Anton Yurchenko-Tytarenko](https://www.linkedin.com/in/antonyurty/), post-doc at this time, who helped me a lot to solve problems and implement solutions.
