clear
close all 
clc
warning off all
format short g

%% Import Data (depending on the frequency)

% Daily topics, LM sentiment:
[daily_topics_returns, dates, dependent, explan_vars_topics, explan_vars_topics_sent, sentiment] = import_datas_order('daily_topics_LM.csv');

%% PCA topics
% Standardize
X_pca = zscore(explan_vars_topics);

% PCA
[loadings, scores, latent] = pca(X_pca, 'Cov');

% Explained variation
latent = latent./sum(latent)

% Plot
figure
plot(dates.date, scores(:,1))
ylabel('PC Score 1')
xlabel('time')


scores_t = array2table(scores(:,[1:20]), 'VariableNames', {'Component1', 'Component2', 'Component3', 'Component4', 'Component5', ...
    'Component6', 'Component7', 'Component8', 'Component9', 'Component10', 'Component11', 'Component12', 'Component13', ...
    'Component14', 'Component15', 'Component16', 'Component17', 'Component18', 'Component19', 'Component20'});
scores_t.date = dates.date
writetable(scores_t,'components.csv','Delimiter',',','QuoteStrings',true);

% Correaltions of components and topics
corrs = zeros(100,20);
for i=1:100
    for j=1:20
        C = corrcoef(scores(:,j),explan_vars_topics(1:end,i));
        corrs(i,j) = C(1,2);
    end
end

highest_corr = zeros(15,20);
highest_indices = zeros(15,20);
highest_corr_sign = zeros(15,20);
for i=1:20
    [B,I] = maxk(abs(corrs(:,i)),15)
    highest_corr(:,i) = B;
    highest_indices(:,i) = I;
    for j=1:15
        highest_corr_sign(j,i) = corrs(highest_indices(j,i),i);
    end
end


%% PCA topics*sentiment
% Standardize
X_pca_sent = zscore(explan_vars_topics_sent(:,1:(end-1)));

% PCA
[loadings_sent, scores_sent, latent_sent] = pca(X_pca_sent, 'Cov');

% Explained variation
latent_sent = latent_sent./sum(latent_sent)

% Plot
figure
plot(dates.date, scores_sent(:,1))
ylabel('PC Score 1')
xlabel('time')


scores_t_sent = array2table(scores_sent(:,[1:10]), 'VariableNames', {'Component1LM', 'Component2LM', 'Component3LM', 'Component4LM', 'Component5LM', ...
    'Component6LM', 'Component7LM', 'Component8LM', 'Component9LM', 'Component10LM'});
scores_t_sent.date = dates.date
writetable(scores_t_sent,'components_sent.csv','Delimiter',',','QuoteStrings',true);

% Correaltions of components and topics
corrs_sent = zeros(100,10);
for i=1:100
    for j=1:10
        C = corrcoef(scores_sent(:,j),explan_vars_topics_sent(1:end,i));
        corrs_sent(i,j) = C(1,2);
    end
end

highest_corr_sent = zeros(10,10);
highest_indices_sent = zeros(10,10);
highest_corr_sign_sent = zeros(10,10);
for i=1:10
    [B,I] = maxk(abs(corrs_sent(:,i)),10)
    highest_corr_sent(:,i) = B;
    highest_indices_sent(:,i) = I;
    for j=1:10
        highest_corr_sign_sent(j,i) = corrs_sent(highest_indices_sent(j,i),i);
    end
end

%% Import Data (depending on the frequency)

% Daily topics, extended sentiment:
[daily_topics_returns, dates, dependent, explan_vars_topics, explan_vars_topics_sent, sentiment] = import_datas_order('daily_topics_extend_comp_rev.csv');


%% PCA topics*extended sentiment
% Standardize
X_pca_sent = zscore(explan_vars_topics_sent(:,1:(end-1)));

% PCA
[loadings_sent, scores_sent, latent_sent] = pca(X_pca_sent, 'Cov');

% Explained variation
latent_sent = latent_sent./sum(latent_sent)

% Plot
figure
plot(dates.date, scores_sent(:,1))
ylabel('PC Score 1')
xlabel('time')


scores_t_sent = array2table(scores_sent(:,[1:10]), 'VariableNames', {'Component1extend', 'Component2extend', 'Component3extend', 'Component4extend', 'Component5extend', ...
    'Component6extend', 'Component7extend', 'Component8extend', 'Component9extend', 'Component10extend'});
scores_t_sent.date = dates.date
writetable(scores_t_sent,'components_sent_extend.csv','Delimiter',',','QuoteStrings',true);

% Correaltions of components and topics
corrs_sent = zeros(100,10);
for i=1:100
    for j=1:10
        C = corrcoef(scores_sent(:,j),explan_vars_topics_sent(1:end,i));
        corrs_sent(i,j) = C(1,2);
    end
end

highest_corr_sent = zeros(10,10);
highest_indices_sent = zeros(10,10);
highest_corr_sign_sent = zeros(10,10);
for i=1:10
    [B,I] = maxk(abs(corrs_sent(:,i)),10)
    highest_corr_sent(:,i) = B;
    highest_indices_sent(:,i) = I;
    for j=1:10
        highest_corr_sign_sent(j,i) = corrs_sent(highest_indices_sent(j,i),i);
    end
end

%% Import Data (depending on the frequency)

% Daily topics estimated on the train portion of the dataset, LM sentiment:
[daily_topics_returns, dates, dependent, explan_vars_topics, explan_vars_topics_sent, sentiment] = import_datas_order('daily_topics_LM_forecasting.csv');

%% PCA topics*sentiment

% Split the data
splitPoint = 1465
X_train = explan_vars_topics_sent(1:splitPoint, 1:(end-1));
X_test = explan_vars_topics_sent(splitPoint+1:end, 1:(end-1));

% Standardize
mu_train = mean(X_train);
sigma_train = std(X_train);
X_pca_sent_train = zscore(X_train);

% PCA on the training set
[loadings_train, scores_train, latent_train] = pca(X_pca_sent_train, 'Cov');

% Standardize and transform TEST set using the mean and sd of the TRAINING set
X_test_pca = (X_test - mu_train) ./ sigma_train;
scores_test = X_test_pca * loadings_train;

scores_forecast = [scores_train; scores_test];

scores_10_forecast = array2table(scores_forecast(:,[1:10]), 'VariableNames', {'Component1LM', 'Component2LM', 'Component3LM', 'Component4LM', 'Component5LM', ...
    'Component6LM', 'Component7LM', 'Component8LM', 'Component9LM', 'Component10LM'});
scores_10_forecast.date = dates.date
writetable(scores_10_forecast,'components_sent_forecast.csv','Delimiter',',','QuoteStrings',true);

%% Import Data (depending on the frequency)

% Daily topics estimated on the train portion of the dataset, extended sentiment:
[daily_topics_returns, dates, dependent, explan_vars_topics, explan_vars_topics_sent, sentiment] = import_datas_order('daily_topics_extend_comp_rev_forecasting.csv');

%% PCA topics*extended sentiment

% Split the data
splitPoint = 1465
X_train = explan_vars_topics_sent(1:splitPoint, 1:(end-1));
X_test = explan_vars_topics_sent(splitPoint+1:end, 1:(end-1));

% Standardize
mu_train = mean(X_train);
sigma_train = std(X_train);
X_pca_sent_train = zscore(X_train);

% PCA on the training set
[loadings_train, scores_train, latent_train] = pca(X_pca_sent_train, 'Cov');

% Standardize and transform TEST set using the mean and sd of the TRAINING set
X_test_pca = (X_test - mu_train) ./ sigma_train;
scores_test = X_test_pca * loadings_train;

scores_forecast = [scores_train; scores_test];

scores_10_forecast = array2table(scores_forecast(:,[1:10]), 'VariableNames', {'Component1extend', 'Component2extend', 'Component3extend', 'Component4extend', 'Component5extend', ...
    'Component6extend', 'Component7extend', 'Component8extend', 'Component9extend', 'Component10extend'});
scores_10_forecast.date = dates.date
writetable(scores_10_forecast,'components_sent_extend_forecast.csv','Delimiter',',','QuoteStrings',true);

