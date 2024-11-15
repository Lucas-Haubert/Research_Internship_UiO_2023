
# Research Internship in Stochastics and Statistics, University of Oslo, 2023

## Context

This repository is contains my work as a research intern at the University of Oslo (UiO), in 2023, oriented towards the study of stochastic volatility models with high-frequancy financial data. The objective is to explore the methodologies and implications of volatility models, for a various range of assets, in order to model prices in a relevant way.

A simple formulation to describe the price process $\(S_t\)$ is the model of continuous semi-martingale:

$$
{\large
\begin{equation}
    dS_t = a_t S_t dt + \sigma_t S_t dW_t
\end{equation}
}
$$

To complete this first step, we introduce the notion of jump process $\(J_t\)$ added to the log-price $X_t = \log S_t$, so that:

$$
{\large
\begin{equation}
    X_t = X_0 + \int_{0}^t a_s ds + \int_{0}^t \sigma_s dW_s + J_t
\end{equation}
}
$$

Finally, in the context of high frequency financial data, it is common to measure a corrupted value $Y_{t_k}$ instead of $X_{t_k}$, due to the presence of micro-structure noise. This is given by:

$$
{\large
\begin{equation}
    Y_{t_k} = X_{t_k} + \eta_{t_k}
\end{equation}
}
$$

## Problem

Within this context, it may be needed to model the volatility coefficient $\sigma$, as it gives relevant information about the variability of the prices. Several models, from classical to stochastic, exist to model this coefficient. Here, the focus is on the hypothesis of local volatility, which assumes that the volatility can be written as a function of the price, i.e. it exists a function a on $\mathbb{R}$ such that:

$$
{\large
\begin{equation}
    \sigma = a(X)
\end{equation}
}
$$

Given the previous modeling and the availability of high frequency financial data (HFFD's), the purpose of the internship was to implement a statistical test, designed by Jean Jacod and Yacine Aït-Sahalia, that allows to confirm or reject the hypothesis. In particular, given a time series of the historical prices $S_1, ..., S_n$, we compute a statistic $T_n$ that converges to a normal law under the local volatility hypothesis $(\mathcal{H})$, and diverges otherwise $(\mathcal{H'})$, i.e.: 

$$
{\large
\begin{equation}
    \begin{aligned}
        &(\mathcal{H}) \quad T_n \xrightarrow{\mathscr{L}} N(0,1) \\
        &(\mathcal{H'}) \quad T_n \text{diverges}
    \end{aligned}
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
