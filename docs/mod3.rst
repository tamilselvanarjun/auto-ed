Module 3: The Reverse Mode of Automatic Differentiation
=======================================================
So far we have considered one mode of automatic differentiation, forward mode.  In forward mode, we carried derivatives along as we traversed the graph so that  the graph itself did not need to be explicitly stored in memory.  In reverse mode, we build the graph and store derivative information at each node but do not compute the derivative until the backward pass of the graph.  We will see that this approach can have computational advantages over forward mode and hence is commonly used, most well known in the backpropagation algorithm.


The Basics of Reverse Mode
--------------------------
As in forward mode, reverse mode still relies on the underlying computational graph structure of functions.  As we will see using the visualization tool, the same graph can be used for forward and reverse mode, but just the direction that derivative information is propagated changes.  Recall that in forward mode we passed derivative information forward to store the derivative at each node.

In reverse mode, instead of storing full derivative information at each node, only the partial derivatives of nodes relative to its children are stored.  For example, if node :math:`x_3` has inputs nodes :math:`x_1` and :math:`x_2`, only the partial derivatives :math:`\frac{\partial x_3}{\partial x_1}` and :math:`\frac{\partial x_3}{\partial x_2}` are stored.  (Contrast this with forward mode, where for a function with inputs x and y, this node would store :math:`\frac{\partial x_3}{\partial x}` and :math:`\frac{\partial x_3}{\partial y}`.)

The reverse mode consists of two passes.  The forward pass first builds the computational graph while storing just the partial derivative information.  The reverse pass then starts at the output node and traverses the graph in the reverse direction to find the full partial derivatives.  

We introduce the bar notation to denote our backward pass tangents, :math:`\bar{x_i} = \frac{\partial f}{\partial x_i}`, which are sometimes also called the adjoint variable.  At the final node, :math:`f = x_N`, we have :math:`\bar{x_N} = \frac{\partial f}{\partial x_N} = 1`.  We then traverse backward through the graph to construct the partial derivative from the chain rule.  :math:`\bar{x_{N-1}}  = \bar{x_N}\frac{\partial x_N}{\partial x_{N-1}}`.  Note that the partial derivative is exactly the value that has already been stored by the forward pass of the graph.

We see that this process is relatively straightforward for nodes with only one child.  When we encounter nodes with multiple children, we must perform a summation over the children, which follows directly from the multivariate chain rule.

For :math:`x_i` with children :math:`$x_j` and :math:`x_k`, we have

.. :math::
        \bar{x_i} = \bar{x_j}\frac{\partial x_j}{\partial x_i} + \bar{x_k}\frac{\partial x_k}{\partial x_i}.


Practice with the Visualization Tool
------------------------------------
Let's revisit our typical example.  As with forward mode, we input the function into the interface in the same way and can compute the function value and derivative, but now we know a little bit about what reverse mode computes.

Press the Reverse Computational Graph button.  You'll see a graph that looks very similar to the one produced in forward mode.  Notice that the only difference is the direction of the errors, representing the fact that derivatives are propagated in different directions.

Now let's dynamically visualize the process of reverse mode.  Press the df/dx button.  Use the arrow keys to step through the process of reverse mode.  At each step you'll see the edge that the computation traverses being highlighted.  

Let's consider another example but with multiple inputs.  Note that this function also has a branch in its underlying graph structure.
(SOME NOTE HERE ABOUT BRANCHING)

**Key Takeaways**

- Reverse mode and forward mode propagate the derivative in different directions.
- The underlying graph structure of the function is the same for both modes of automatic differentiation.
- Reverse mode computes derivatives by making a backward pass starting at the output.


More Theory
-----------
In the previous module, we demonstrated that forward mode computes the Jacobian vector product Jp.  (depends on number of input variables)

In contrast, reverse mode computes :math:`J^Tp` which is independent of the number of inputs.

This difference can result in different operation counts, accounting for the popularity of the backpropagation algorithm.

A Comparison of Forward and Reverse Mode
----------------------------------------
As the names suggest, the primary difference between forward and reverse mode is the direciton in which the computational graph is traversed, as we saw in the direction of the errors of the visualization tool.  This has implications for the computational efficiency of the two approaches.

As we just showed, reverse mode computes :math:`J^Tp`, while in module 2, we learned that forward mode computes :math:`Jp`.  This means that reverse mode will be more efficient (require fewer operations) for functions with a fewer number of outputs and many inputs, while forward mode will be more efficient for functions with many outputs and fewer inputs.  Let's consider an example of this.

**Demo: A Comparison of Forward and Reverse Mode**
Let's consider the function :math:`f(w_1, w_2, w_3, w_4, w_5) = w_1w_2w_3w_4w_5`.  We want to compare the process of computing the partial derivatives in forward and reverse mode.  Let's start with an example of reverse mode, where we do not store the results of the chain rule but just the values of the partial derivatives at each step.



To compute the derivatives, we will now traverse through the graph using our update equations.  You can visualize this graph by using the dynamic visualization tool.


Going Forward
-------------
In the next unit, we explore an alternate interpretation of automatic differentiation in terms of dual numbers and consider questions of implementation in software.

Other extensions for further reading include automatic differentiation for higher order derivatives, including computing Hessians, and algorithmic differentiation of computer programs.  We can also consider the efficiency of the algorithms in terms of memory and efficient graph storage, access, and traversal.  Such efficiency may be better achieved in cases where the Jacobian and Hessian are sparse.  Other work has explored using a mixture of forward and reverse mode for computations.

Exercises
---------
TO DO

