function [vars_select, topics_returns, dates, dependent_abs, dependent_logs, explan_topics_comp_sent, explan_vars_topics_sent, sentiment] = import_data_extend_comp_ose(file)
    %% Import and Data Pre-Processing:
    import_data = readtable(file, 'PreserveVariableNames', true); 

    % Put together the data:
    vars_select = import_data(:, [1,103:end]);                       % obtain returns, sentiment, components - until nrow = 1038 if for before Covid
    dates = import_data(:,2);                                        % vector of dates in string format
    explan_topics_comp_sent = table2array(vars_select(:, (end-10):(end-1)));
    
    dependent_logs = table2array(vars_select(:, 1));
    dependent_abs = abs(table2array(vars_select(:, 1)));             % dependent variable is abs-returns
    topics_returns = [array2table(dependent_abs, 'VariableNames',{'log_returns'}), vars_select(:,2:end)];  % main data frame
    sentiment = table2array(import_data(:, 103));                    % sentiment
   
    explan_vars_topics_sent = [sentiment, explan_topics_comp_sent];
end