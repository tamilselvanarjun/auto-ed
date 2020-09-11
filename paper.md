---
title: 'Auto-eD: A visual learning tool for automatic differentiation'
tags:
 - Python
 - automatic differentiation
authors:
 - name: Lindsey S. Brown
   orcid: 0000-0002-9387-1387
   affiliation: 1
 - name: Rachel Moon
   orcid:
   affiliation:
 - name: David Sondak
   orcid: 0000-0002-2730-9097
   affiliation: 1
affiliations:
 - name: Harvard John A. Paulson School of Engineering and Applied Sciences
   index: 1
date: 11 September 2020
bibliography: paper.bib

---
# Summary
Recent research has shown the growing power of machine learning to analyze data, build models, and predict outcomes, particularly through the use of neural networks.  Automatic differentiation is the basic concept underlying the backpropagation algorithm, typically employed to fit these neural networks.  However, automatic differentiation is not limited to this application but is a powerful computational tool for a range of applications, making it important for students to understand the basics of automatic differentiation.

Automatic differentiation is a method of computing derivatives to machine precision based on the decomposition of functions into a series of elementary operations.  These operations can be conceptualized as forming a graph structure, which allows us to perform automatic differentiation in either the forward or reverse mode, depending on the direction of the traversal of the graph.  The goal of this software and accompanying unit is to enhance students' understanding of automatic differentiation by helping them to visualize the underlying graph structure of the computations.

## Auto-eD Visualization Software
Goal of being able to visualize underlying graphs and calculations
Basic simple automatic differentiation package
Graph features to see forward and reverse mode as well as visualize steps of reverse dynamically
Available for developers to download and use as a package
Available to be downloaded locally and launched as a web app
Available on heroku

## Accompanying Automatic Differentiation Unit
This software package is accompanied by a series of modules available on Read the Docs to help students understand the theory behind automatic differentiation that is performed and visualized by the package. In the first module, we motivate the need for automatic differentiation as opposed to numeric or symbolic differentiation and introduce the basics of forward mode for a single input single output function.  In the second module, we expand on the first modeule to include more of the theory underlying forward mode, including a consideration of multiple input variables.  In the third module, we introduce the reverse mode of automatic differentiation.  In the fourth module, we conclude with a series of possible extensions and a discussion of how automatic differentiation might be performed in software.  Each module is accompanied by a series of exercises.

A similar structure has been used to teach these concepts in Harvard IACS CS 207, and in Fall 2019, the course introduced a GUI based on portions of this software, which received positive feedback from students.

# Statement of Need

# Acknowledgements
Xinyue Wang, Kevin Yoon

# References
