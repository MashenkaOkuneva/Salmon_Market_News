clear
close all 
clc
warning off all
format short g
%% Import Data (depending on the frequency)

% Daily Returns (Topics, LM sentiment, no components, all articles):
[daily_topics_returns, daily_topics_absrets, dates, dependent_abs, dependent, explan_vars_topics, explan_vars_topics_sent, sentiment] = import_datas('daily_topics_LM.csv');

% Daily Returns (Topics, extended sentiment, no components, all articles):
[daily_topics_returns, daily_topics_absrets, dates, dependent_abs, dependent, explan_vars_topics, explan_vars_topics_sent, sentiment] = import_datas('daily_topics_extend_comp_rev.csv');

% Daily Returns (Topics, extended sentiment, no components, articles about index firms and their competitors):
[daily_topics_returns, daily_topics_absrets, dates, dependent_abs, dependent, explan_vars_topics, explan_vars_topics_sent, sentiment] = import_datas('daily_topics_extend_our_comp.csv');

% Daily Returns (Topics, components based on topics and topics*LM sentiment, LM sentiment):
[daily_topics_comp, daily_topics_comp_absrets, dates_comp, depend_abs, dependent_log, explan_vars_topics_comp,  explan_topics_comp_sent, explan_vars_topics_sent_comp, sentiment_comp] = import_data_comp('daily_topics_LM_components.csv');
% Reverse for the significant components 5 & 6:
daily_topics_comp_absrets.Component5 = (-1)*daily_topics_comp_absrets.Component5;
daily_topics_comp_absrets.Component6 = (-1)*daily_topics_comp_absrets.Component6;
daily_topics_comp_absrets.Component9 = (-1)*daily_topics_comp_absrets.Component9;
explan_vars_topics_comp(:,[5,6,9]) = (-1)*explan_vars_topics_comp(:,[5,6,9]);

% Daily returns (Topics, components based on topics*extended sentiment, extended sentiment):
[daily_topics_comp, daily_topics_comp_absrets, dates_comp, depend_abs, dependent_log, explan_topics_comp_sent, explan_vars_topics_sent_comp, sentiment_comp] = import_data_extend_comp('daily_topics_extend_comp_rev_components.csv');

% Daily returns (Topics, components based on topics*extended sentiment, extended sentiment, and returns of OSE):
[daily_topics_comp, daily_topics_comp_absrets, dates_comp, depend_abs, dependent_log, explan_topics_comp_sent, explan_vars_topics_sent_comp, sentiment_comp] = import_data_extend_comp_ose('daily_topics_extend_comp_rev_components_ose.csv');
%% VAR Selection & Estimation:
addpath(genpath('VAR-Toolbox/v3dot0/'))

% Run the function:

% topics*sentiment & log-returns (use this for any sentiment - LM or
% extended - and for any sample - all articles or our firms +
% competitors)
[varmod_topics_sent, varopt_topics_sent, topics_sent_estimate, topics_sent_betas, topics_sent_aic] = VARestimate(daily_topics_returns, explan_vars_topics_sent, dependent, 1);

% components based on topics & absolute returns:
[varmod_topics_comp, varopt_topics_comp, topics_estimate_comp, topics_betas_comp, topics_aic_comp] = VARestimate(daily_topics_comp_absrets, explan_vars_topics_comp, depend_abs, 0);

% components based on topics * LM sentiment & log-returns:
[varmod_topics_sent_comp, varopt_topics_sent_comp, topics_sent_estimate_comp, topics_sent_betas_comp, topics_sent_aic_comp] = VARestimate(daily_topics_comp, explan_vars_topics_sent_comp, dependent_log, 2);

% components based on topics * extended sentiment & log-returns:
[varmod_topics_sent_comp, varopt_topics_sent_comp, topics_sent_estimate_comp, topics_sent_betas_comp, topics_sent_aic_comp] = VARestimate(daily_topics_comp, explan_vars_topics_sent_comp, dependent_log, 3);

% components based on topics * extended sentiment & log-returns & log-returns of ose:
[varmod_topics_sent_comp, varopt_topics_sent_comp, topics_sent_estimate_comp, topics_sent_betas_comp, topics_sent_aic_comp] = VARestimate_ose(daily_topics_comp, explan_vars_topics_sent_comp, dependent_log, 4);
%% IDENTIFICATION WITH ZERO SHORT-RUN RESTRICTIONS (DAILY) for ALL topics:

% topics*sentiment & log-returns (LM sentiment, all articles)
[irr_topics_sent_zeros, VAR_estimate_topics_sent_zeros, figure_topics_sent_short, lower_irr_topics_sent, upper_irr_topics_sent, irr_topics_sent_mean, var_opts_topics_sent, ses_topics_sent] = VARidentzeroshortrunrest(daily_topics_returns, explan_vars_topics_sent, varopt_topics_sent, varmod_topics_sent, 0, 0, 0, '/daily_all_LM');

% topics*sentiment & log-returns (extended sentiment, all articles)
[irr_topics_sent_zeros, VAR_estimate_topics_sent_zeros, figure_topics_sent_short, lower_irr_topics_sent, upper_irr_topics_sent, irr_topics_sent_mean, var_opts_topics_sent, ses_topics_sent] = VARidentzeroshortrunrest(daily_topics_returns, explan_vars_topics_sent, varopt_topics_sent, varmod_topics_sent, 0, 0, 0, '/daily_all_our_sentiment_new');

% topics*sentiment & log-returns (extended sentiment, articles about our firms and competitors)
[irr_topics_sent_zeros, VAR_estimate_topics_sent_zeros, figure_topics_sent_short, lower_irr_topics_sent, upper_irr_topics_sent, irr_topics_sent_mean, var_opts_topics_sent, ses_topics_sent] = VARidentzeroshortrunrest(daily_topics_returns, explan_vars_topics_sent, varopt_topics_sent, varmod_topics_sent, 0, 0, 0, '/daily_oursentiment_comp_firms_new');
%% IDENTIFICATION WITH ZERO SHORT-RUN RESTRICTIONS (DAILY) for PCA results:

% components based on topics & absolute returns:
[irr_topics_zeros_comp, VAR_estimate_topics_zeros_comp, figure_topics_short_comp, lower_irr_topics_comp, upper_irr_topics_comp, irr_topics_mean_comp, var_opts_topics_comp] = VARidentzeroshortrunrest(daily_topics_comp_absrets, explan_vars_topics_comp, varopt_topics_comp, varmod_topics_comp, 2, 0, 2,'/daily_all_topics_PCA_new');

% component based on topics * LM sentiment & log-returns:
[irr_topics_sent_zeros_comp, VAR_estimate_topics_sent_zeros_comp, figure_topics_sent_short_comp, lower_irr_topics_sent_comp, upper_irr_topics_sent_comp, irr_topics_sent_mean_comp, var_opts_topics_sent_comp] = VARidentzeroshortrunrest(daily_topics_comp, explan_vars_topics_sent_comp, varopt_topics_sent_comp, varmod_topics_sent_comp, 3, 0, 3,'/daily_all_topics_sent_PCA_new');

% components based on topics * extended sentiment & log-returns:
[irr_topics_sent_zeros_comp, VAR_estimate_topics_sent_zeros_comp, figure_topics_sent_short_comp, lower_irr_topics_sent_comp, upper_irr_topics_sent_comp, irr_topics_sent_mean_comp, var_opts_topics_sent_comp] = VARidentzeroshortrunrest(daily_topics_comp, explan_vars_topics_sent_comp, varopt_topics_sent_comp, varmod_topics_sent_comp, 4, 0, 4,'/daily_PCA_oursentiment_new');

% components based on topics * extended sentiment & log-returns & log-returns of ose:
[irr_topics_sent_zeros_comp, VAR_estimate_topics_sent_zeros_comp, figure_topics_sent_short_comp, lower_irr_topics_sent_comp, upper_irr_topics_sent_comp, irr_topics_sent_mean_comp, var_opts_topics_sent_comp] = VARidentzeroshortrunrest_ose(daily_topics_comp, explan_vars_topics_sent_comp, varopt_topics_sent_comp, varmod_topics_sent_comp, 5, 0, 5,'/daily_PCA_oursentiment_OSE_new');

%% END
 


