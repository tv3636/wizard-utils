# wizard-utils

Python scripts to find wizard listings based on affinity and names

## Usage

`pip install -r requirements.txt`

- `python listings.py [AFFINITY_TOTAL]`
  - AFFINITY_TOTAL is a number 2-5, to search for wizards with 2/2, 3/3, 4/4, or 5/5 affinity. If no number is provided, the results will be for wizards with 5/5 affinity.

- `python names.py [NAME_LENGTH]`
  - Name length must be 1-7. Defaults to 1 if no length is provided

## Example

`python listings.py 5`


`python names.py 3`
