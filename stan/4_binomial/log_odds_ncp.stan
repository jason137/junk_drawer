data {
  int<lower=0> N;           // num trials

  int<lower=0> K[N];        // trials in train period
  int<lower=0> y[N];        // successes in train period

  int<lower=0> K_new[N];    // trials in test period
  int<lower=0> y_new[N];    // successes in test period
}

parameters {
  real mu;                       // population mean of success log-odds
  real<lower=0> sigma;           // population sd of success log-odds
  vector[N] alpha_std;           // success log-odds
}
model {
  mu ~ normal(-1, 1);                             // hyperprior
  sigma ~ normal(0, 1);                           // hyperprior
  alpha_std ~ normal(0, 1);                       // prior
  y ~ binomial_logit(K, mu + sigma * alpha_std);  // likelihood
}

generated quantities {
  vector[N] theta;  // chance of success

  for (n in 1:N)
    theta[n] = inv_logit(mu + sigma * alpha_std[n]);

}
