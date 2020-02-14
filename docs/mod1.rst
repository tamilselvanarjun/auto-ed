Module 1: The Basics of Forward Mode
====================================

Introduction
------------

Differentiation is a fundamental operation in computational science that is important in many applications, including optimization, sensitivity analysis, and solving differential equations.  To be useful in these applications, derivatives must be computed both precisely and efficiently.  **Automatic differentiation**, sometimes also called algorithmic differentiation or computational differentiation, is able to do both, distinguishing it from both numerical differentiation and symbolic differentiation.

* Automatic differentiation is not numerical differentiation.

*Numerical differentiation* refers to a class of methods that computes derivatives through finite difference formulae based on the definition of the derivative,

.. math::

        \frac{df(x)}{dx} = \lim_{h \rightarrow 0} \frac{f(x+h)-f(x)}{h}

Such methods are limited in precision due to truncation and roundoff errors as accuracy depends on choosing an appropriately sized h.  Let's consider a basic example.

Demo 1: Errors in The Finite Difference Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's consider the function :math:r`x-\exp(-2\sin^2(4x))`.  Using our basic differentiation rules, we can compute the derivative symbolically,

.. math::

        \frac{df}{dx} = 1 + 16\exp(-2\sin^2(4x))\sin(4x)\cos(4x)

INSERT PYTHON CODE AND PLOT FROM LECTURE 9 HERE

In the above, we see that the accuracy of the derivative calculation is highly dependent on our choice of h.  When we choose h to large, the numerical approximation is no longer accurate, but for h too small, we begin to see round off errors from limitations in machine precision.

See Exercise 1 for another example motivating the use of automatic differentiation.

* Automatic differentiation is not symbolic differentiation.

*Symbolic differentiation* computes exact expressions for derivatives using expression trees.  As seen in the function in Demo 1, exact expressions for derivatives can quickly become complex, making computing derivatives in this manner computationally inefficient.

* Automatic differentiation is a procedure that computes derivatives to machine precision without explicitly forming an expression for the derivative by employing the ideas of the chain rule to decompose complex functions into elementary functions for which we can compute the derivative exactly.

Automatic differentiation may perform this process through two different modes, forward and reverse, both allowing for efficient and accurate computation of derivatives.  These properties make automatic differentiation useful in a variety of applications including machine learning, parameter optimization, sensitivity analysis, physical modeling, and probabilistic inference.  In the rest of this module, we will explore the underlying theory that allows automatic differentiation to be applied in this wide variety of applications.

The Basics of Forward Mode
--------------------------
The major theoretical concept underlying automatic differentiation is *the chain rule*.  Recall from calculus that the chain rule states that to find the derivative of composition of functions, we multiply a series of derivatives; let f(t) = g(h(t)).  We have

.. math::

        \frac{df}{dt} = \frac{dg}{dh}\frac{dh}{dt}

This can be generalized to functions of multiple inputs, which we will discuss in more detail in Unit 2.


Elementary Functions
^^^^^^^^^^^^^^^^^^^^
Every function can be decomposed into a series of binary elementary operations or unary functions.  These elementary operations include addition, subtraction, multiplication, division, and exponentiation.  Elementary functions include the natrual exponential and natural logarithm, trigonometric functions, and hyperbolic trigonometric functions.  From basic calculus, we know closed form differentiation rules for these elementary functions.  This means that we can compose these functions to form more complex functions and find the derivative of these more complex functions using the chain rule.  To understand this composition from elementary functions, we can think of the composition of functions as having an underlying graph structure.

A Tool for Visualizing Automatic Differentiation
------------------------------------------------
The ???? tool is a pedagogical tool to help visualize the processes underlying automatic differentiation.  In particular, this tool allows us to visualize the underlying graph structure of a calculation when decomposed into elementary functions.  In addition to helping to visualize this graph, the tool can also be used to view the computational traces that occur at each node of the graph which will be discussed in more detail in Unit 2.

Installation
^^^^^^^^^^^^
The tool can be downloaded by

Basic Instructions
^^^^^^^^^^^^^^^^^^
Launch the tool in the terminal...

A First Demo of Automatic Differentiation
-----------------------------------------
Let's use the tool to visualize the function from our first demo.
#. The function has a single input variable, x, so we enter that our function has 1 input into the tool.
#. Our function is scalar valued so we enter that our function has 1 output.
#. We use the calculator interface to enter our function.  (Note that we can use the backspace key or the clear all (CHECK THIS NAME) to correct the function if we make a mistake when entering it.)
#. Press calculate.  This will open a second screen with options to help you visualize both the forward and reverse mode of automatic differentiation.
#. Enter the value for x at which you'd like to evaluate the function.  For the purposes of this demo, we'll choose x=4.  Hit the enter button on the far left.
#. You'll see the values for the function and derivative appear in green in the center column.
#. Below this you'll see a buttons for graph and table (CHECK BUTTON NAMES).  We'll talk more about the computational table in the next unit, so for now let's just hit the graph button.
#. This will open a new window with the underlying computational graph for the function.  Notice that there is a single magenta node, representing our single input to the function, and a single green output node, the output value of our function.  The red nodes represent intermediate function values.  Notice that all of the nodes are connected by elementary operations on the labelled edges.  (Hint: If you find the graph difficult to read, try maximizing the graph window to give more space between the nodes.)

Some Key Takeaways
^^^^^^^^^^^^^^^^^^
* Our function was decomposed into a series of elementary operations
* These operations include both basic binary operations (addition, subtraction, multiplication, and division) and unary operations (exponential functions, trigonometric functions)
* Using this graph to compute the derivative is the same process as using the chain rule to compute the derivative, allowing the derivative to be computed to machine precision

Practice Exercises
------------------
Exercise 1: Motivating Automatic Differentiation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Problem from HW 4

Exercise 2: Basic Graph Structure of Calculations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Try drawing the graph by hand.  Compare results to that using the visualization tool.

Exercise 3: Looking Toward Multiple Inputs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We can use the same process to compute derivatives for functions of multiple inputs.  Practice drawing the computational graph for this function.  We'll discuss the theory behind functions of multiple inputs in the next unit.
