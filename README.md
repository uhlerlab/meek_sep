# Meek Separator
Code for paper: _Meek Separators and Their Applications in Targeted Causal Discovery (NeurIPS 2023)_.

arXiv link: https://arxiv.org/abs/2310.20075

For **Algorithm 1 (Meek Separator)**, a function that takes a causal DAG as input and produces outputs as set I to find the Meek separator is in `meekseparator.py`.


## Application to Subset Search
The full pipeline to reproduce the comparisons in the paper can be found in `subset_search/test_policy.ipynb`.

In particular, the problem instances are generated using functions in `subset_search/graphs`. The algorithms, including **Algorithm 2 (Atomic Adaptive Subset Search)** and baselines, are implemented in `subset_search/policys`. The verification lower bound is computed by calling `subset_search/subset_verify.py` (original implementation from https://github.com/cxjdavin/subset-verification-and-search-algorithms-for-causal-DAGs).


## Application to Causal Mean Matching
The full pipeline to reproduce the comparisons in the paper can be found in `causal_mean_matching/test_policy.ipynb` (code adapted from https://github.com/uhlerlab/causal_mean_matching).

In particular, the problem instances are generated using functions in `causal_mean_matching/graphs`. The algorithms, including **Algorithm 3 & 4 (Find Source and Causal Mean Matching)** and baselines, are implemented in `causal_mean_matching/policys`.
