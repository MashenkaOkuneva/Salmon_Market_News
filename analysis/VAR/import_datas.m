function [vars_select, topics_returns, dates, dependent_abs,dependent, explan_vars_topics, explan_vars_topics_sent, sentiment] = import_datas(file)
    %% Import and Data Pre-Processing:
    import_data = readtable(file, 'PreserveVariableNames', true); 

    % Put together the data:
    vars_select = import_data(:, [1,3:103]);                      % obtain explanatory variables
    dates = import_data(1:end,2);                                 % vector of dates in string format
    explan_vars_topics = table2array(vars_select(:, 2:(end-1)));  % only the topics {T0,..,T99}
    dependent_abs = abs(table2array(vars_select(:, 1)));          % dependent variable is abs-returns
    dependent = table2array(vars_select(:, 1));                   % dependent variable is log-returns
    topics_returns = [array2table(dependent, 'VariableNames',{'log_returns'}), vars_select(:,(2:end))];
    sentiment = table2array(import_data(:, 103));                 % sentiment
    ntopics = size(explan_vars_topics, 2);                        % number of topics

    explan_vars_topics_sent = [];                                 % initialize topics*sentiment variable
    % Create the topics*sentiment variable:
    for i = 1:ntopics
        explan_vars_topics_sent(:,i) = times(explan_vars_topics(:,i), table2array(topics_returns(:,end)));
    end
    
    explan_vars_topics_sent = [explan_vars_topics_sent, sentiment];
end