# This python program does all these:
  
  1)  finds coefficients for the regression curve z = (b1 * y + b3)* e^(-b2 * x) + b0 :   
          where b0, b1, b2, b3 are the coefficients of regression line  
          and x, y, z are the 3 random variables  
      precision set to 5 decimal places (adjustable to any value 'n' by using 10^n wherever 10^5 used)

  2)  displays the 3d scatter plot of 3 variables by extracting the data from the specified excel file.  
      Try to keep azimuth = 31 deg, elevation = 11 deg for general ease of viewing
      
  3)  simulates -from observed values- the estimated model of relation between x,y and z where they are related as
      z = (b1 * y + b3)* e^(-b2 * x) + b0 :   
          where b0, b1, b2, b3 are the coefficients of regression line  
          and x, y, z are the 3 random variables  
      precision set to 5 decimal places (adjustable to any value 'n' by using 10^n wherever 10^5 used)

# Method of regression solution used: 
Sum of Squares of Errors Minimization

# Important Note:   
Due to the nonlinear nature of the model relation as well as the presence of 4 coefficients in the same, it is nigh-impossible to     actually find the real solution for the problem posed. However due to the nature of the approach taken to "solve" it, we can find the closest solution for a selected arbitrary precision value, provided the user can provide a reasonable range of values between which one of the coefficients (b2 in this implementation case) will have its true value.

This range can be easily found out by rerunning the code and checking if the output value for b2 coincides with the boundary of the range the user has provided. If it coincides with the upper boundary, it implies that the above-mentioned true value lies after the provided range. similarly, if it coincides with the lower boundary, it implies that the above-mentioned true value lies before the provided range.
#
Code logic adapted from a currently-ongoing (as of 17-06-2020) astrophysics research paper being co-authored by op
#
Proper deliberation of the implementation and derivation of the solution approach can be found in the Word file "Approach to solution.docx"
