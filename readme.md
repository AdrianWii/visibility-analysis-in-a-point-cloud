# Bound Block Elimination Algorithm for Point Cloud Analysis

<p align="center">
  <img src="/images/input.png" alt="Input" width="300">
  <img src="/images/visible_area.png" alt="Visible Area" width="300">
</p>

## Project Description
This repository contains the source code implementation of the Bound Block Elimination Algorithm, developed for accurate visibility computation in point cloud analysis. The algorithm is based on research findings presented in the following scientific paper:

> ** Widłak, Adrian; Ozimek, Paweł; Łabędź, Piotr; Orlof, Jerzy;**  
> *Bound block elimination algorithm for accurate visibility computation in point cloud analysis.*  
> Proceedings, 2024. DOI: [10.7148/2024-0490](https://doi.org/10.7148/2024-0490)

## Repository Contents

- **`data/`**: Example point cloud data used for testing the algorithm.
- **`main.py`** mainly reading and writing operations based on point cloud files, checking if data is available. Process te main algorithm from `face.py`
- **`README.md`**: Project documentation file.

## Requirements

To run the code, the following requirements must be met:

- Python 3.8 or newer
- Python libraries:
    - trimesh
    - math
    - pathlib
    - tqdm
    - time

Install the required libraries using the following command:

```bash
pip install -r requirements.txt
```

## Citation

If you use this repository in your scientific research, please cite the paper:

```bibtex
@inproceedings{inproceedings,
  author = {Widłak, Adrian and Ozimek, Paweł and Łabędź, Piotr and Orlof, Jerzy},
  year = {2024},
  month = {06},
  pages = {},
  title = {Bound block elimination algorithm for accurate visibility computation in point cloud analysis},
  doi = {10.7148/2024-0490}
}
```

## Contact

For questions, please contact the authors via email: 
- Adrian Widłak: adrian.widlak@pk.edu.pl

