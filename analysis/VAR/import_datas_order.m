function [topics_returns, dates, dependent, explan_vars_topics, explan_vars_topics_sent, sentiment] = import_datas(file)
    %% Import and Data Pre-Processing:
    import_data = readtable(file, 'PreserveVariableNames', true); 

    % Put together the data:
    topics_returns = import_data(:, [1, 3:103]);                     % obtain explanatory variables
    dates = import_data(1:end,2);                                    % vector of dates in string format
    explan_vars_topics = table2array(topics_returns(:, 2:(end-1)));  % only the topics {T0,..,T99}
    dependent = table2array(topics_returns(:, 1));                   % dependent variable are log-returns
    sentiment = table2array(import_data(:, 103));                    % sentiment
    ntopics = size(explan_vars_topics, 2);                           % number of topics

    explan_vars_topics_sent = [];                                    % initialize topics*sentiment variable
    % Create the topics*sentiment variable:
    for i = 1:ntopics
        explan_vars_topics_sent(:,i) = times(explan_vars_topics(:,i), table2array(topics_returns(:,end)));
    end
    
    explan_vars_topics_sent = [explan_vars_topics_sent, sentiment];
end