data {
  int<lower=0> N;           // items
  int<lower=0> K[N];        // initial trials
  int<lower=0> y[N];        // initial successes

  int<lower=0> K_new[N];    // new trials
  int<lower=0> y_new[N];    // new successes
}

parameters {
  real mu;                       // population mean of success log-odds
  real<lower=0> sigma;           // population sd of success log-odds
  vector[N] alpha;               // success log-odds
}

model {
  // recall cp leads to divergent behavior

  mu ~ normal(-1, 1);               // hyperprior
  sigma ~ normal(0, 1);             // hyperprior
  alpha ~ normal(mu, sigma);        // prior (hierarchical)
  y ~ binomial_logit(K, alpha);     // likelihood
}
