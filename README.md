![python ray logo](python-ray.png)

# Summary

The script builds lookup tables that group large ranges of numbers by a “reduced signature” rapidly by leveraging parallel processing via [Python](https://www.python.org/) and the [Ray](https://www.ray.io/) library. 

**You are most welcome to use this code in your commercial projects, all that I ask in return is that you credit my work by providing a link back to this repository. Thank you & Enjoy!**

# Background
This script was originally part of one of my projects that involved optimising a dictionary-based compression algorithm with machine learning. However, I thought it is a useful template demonstrating how you can use [Ray](https://www.ray.io/) to perform data processing in parrallel easily using your local machine.

You can also modify this template to work with multiple machines on your local network. [See Ray docs](https://docs.ray.io/en/latest/ray-core/walkthrough.html)  

# Convenience and cost savings
Traditionally, setting up and maintaining the infrastructure required for parrallel processing is time-consuming and costly, and even more costly longterm in the cloud. However, with the introduction of [Ray python library](https://docs.ray.io/en/latest/index.html), you can now leverage the processing power of every machine on your local network with minimal configuration, and a python script. 

## Example scenario
At home, I have 3 PCs, 4 laptops. specs are:

| MACHINE  | RAM   | LOGICAL_CPUS |
|----------|-------|--------------|
| PC 1      | 128gb | 64           |
| PC 2      | 64gb  | 20           |
| PC 3      | 64gb  | 20           |
| LAPTOP 1  | 8gb   | 4            |
| LAPTOP 2  | 16gb  | 6            |
| LAPTOP 3  | 8gb   | 4            |
| LAPTOP 4  | 8gb   | 4            |


If I were to use max resources of all machines for 7 days, my only costs would be electricity, which would be ~$30 AUD.

Whereas, if I ran the same resources via EC2 instance on AWS at max usuage, it would cost >$1K... and if i used a cloud service specialising in ML workloads, it would still cost >$600.

# What does the script do?

The script `run.py` builds lookup tables that group large ranges of numbers by a reduced signature. This approach is useful in situations where you need to bucket large numbers into compressed categories, such as for reduction/normalization or lookup table generation.

## Ray Features
- Uses Ray "Futures" to provide a progress indicator in the console
- Splits dictionaries by job to avoid any overlap between workers

# How to Run

1. Install dependencies:
```bash
pip install ray
```

2. Create an empty directory called `tables` in the project's root folder. 

3. (Optional) In `run.py` set the number of CPUs you would like to use:
```py
ray.init(num_cpus=6)
```
or leave blank to use all cpus available on the machine:
```py
ray.init()
```

4. Run
```
python run.py
```