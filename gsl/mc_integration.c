#include <stdlib.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_monte.h>
#include <gsl/gsl_monte_plain.h>
#include <gsl/gsl_monte_miser.h>
#include <gsl/gsl_monte_vegas.h>

/* adapted from
   https://www.gnu.org/software/gsl/manual/html_node/Monte-Carlo-Examples.html */

/* For simplicity we compute the integral over the region 
   (0,0,0) -> (pi,pi,pi) and multiply by 8 */

/* double exact = 1.3932039296856768591842462603255; */
/* double g (double *k, size_t dim, void *params)
{
  double A = 1.0 / (M_PI * M_PI * M_PI);
  return A / (1.0 - cos (k[0]) * cos (k[1]) * cos (k[2]));
} */

double gauss (double x) {
    return exp(-x * x / 2) / sqrt(2 * M_PI)
}

void display_results(char *title, double result, double error)
{
  printf ("%s ==================\n", title);
  printf ("result = % .6f\n", result);
  printf ("sigma  = % .6f\n", error);
  printf ("exact  = % .6f\n", exact);
  printf ("error  = % .6f = %.2g sigma\n\n", result - exact,
          fabs (result - exact) / error);
}

int main(void) {
  const dims = 3;
  double res, err;

  /* limits of integration */
  double xl = -10000;
  double xu = -xl;

  /* double xl[3] = { 0, 0, 0 };
  double xu[3] = { M_PI, M_PI, M_PI }; */

  const gsl_rng_type *T;
  gsl_rng *r;

  /* gsl_monte_function G = { &g, 3, 0 }; */
  gsl_monte_function monte_fn = { &gauss, dims, 0 };

  size_t calls = 500000;

  gsl_rng_env_setup (); /* sets rng defaults from env variables ??? */

  T = gsl_rng_default;
  r = gsl_rng_alloc (T);

  {
    gsl_monte_plain_state *s = gsl_monte_plain_alloc (dims);
    gsl_monte_plain_integrate (&monte_fn, xl, xu, 3, calls, r, s, &res, &err);
    gsl_monte_plain_free (s);
    display_results ("plain", res, err);
  }

  {
    gsl_monte_miser_state *s = gsl_monte_miser_alloc (3);
    gsl_monte_miser_integrate (&monte_fn, xl, xu, 3, calls, r, s, &res, &err);
    gsl_monte_miser_free (s);
    display_results ("miser", res, err);
  }

  {
    gsl_monte_vegas_state *s = gsl_monte_vegas_alloc (3);

    gsl_monte_vegas_integrate (&monte_fn, xl, xu, 3, 10000, r, s,
                               &res, &err);
    display_results ("vegas warm-up", res, err);

    printf ("converging...\n");

    do
      {
        gsl_monte_vegas_integrate (&monte_fn, xl, xu, 3, calls/5, r, s,
                                   &res, &err);
        printf ("result = % .6f sigma = % .6f "
                "chisq/dof = %.1f\n", res, err, gsl_monte_vegas_chisq (s));
      }
    while (fabs (gsl_monte_vegas_chisq (s) - 1.0) > 0.5);

    display_results("vegas final", res, err);

    gsl_monte_vegas_free(s);
  }

  gsl_rng_free (r);

  return 0;
}
