%% VAR ESTIMATION
%****************************************************************** 
% VAR estimation is achieved in two steps. First, select list of 
% endogenous variables (these will be pulled from the structure DATA, 
% where all data is stored). Second, set desired number of lags and 
% deterministic variables and run the VARmodel function.

function [varmod, varopt, estimates, coeff, aic] = VARestimate(data, explanatories, depend, sents)

    % Set the deterministic variable in the VAR (1=constant, 2=trend)
    det = 1;
    
    % Lag Selection Process:
    AIC ={};
    SBC={};
    logL = {};
    pmax = 20;
    %nlags = {};
    


    nvars = size(explanatories, 2);                % number of topics
    datas = cell(1,nvars);                         % create an empty list of lists to separate the variables for bivariate 
    V = cell(1,nvars);  
    VAR = {};
    VARopt = {};

    TABLE = {};
    beta = {};
    
    for i = 1:nvars
        datas{i} = [explanatories(:,i), depend];  % fill in the dataset with the right 
        V{i} = size(datas{i}, 2);                 % Number of Variables equal to 2
        
        % Choose Lags:
        [AIC{i}, SBC{i}, logL{i}] = VARlag(datas{i}, pmax, det);
        
        % Set number of lags
        % nlags{i} = AIC{i};
    
        % Estimate VAR by OLS
        [VAR{i}, VARopt{i}] = VARmodel(datas{i}, AIC{i}, det);
    
        % Print at screen the outputs of the VARmodel estimation
        %format short
        %disp(VAR{i})
        %disp(VAR{i}.F)
        %disp(VAR{i}.sigma)
        %disp(VARopt{i})
    
        % Update the VARopt structure with additional details
        if sents == 0
            % Get the names:
            Xnames = data.Properties.VariableNames(3:22);
            VARopt{i}.vnames = { Xnames{i}, 'Log_Returns'};
                
        elseif sents == 1    
             Xnames = data.Properties.VariableNames(2:end);
             VARopt{i}.vnames = { Xnames{i}, 'Log_Returns'};
                
        elseif sents == 2
             Xnames = data.Properties.VariableNames([2,23:end]);
             VARopt{i}.vnames = { Xnames{i}, 'Log_Returns'};
        
        else 
             Xnames = data.Properties.VariableNames(2:end);
             VARopt{i}.vnames = { Xnames{i}, 'Log_Returns'};
        end
        % Print at screen VAR coefficients and create table 
        [TABLE{i}, beta{i}] = VARprint(VAR{i}, VARopt{i}, 2);
    end
    
    % Outputs:
    varmod = VAR;
    varopt = VARopt;
    estimates = TABLE;
    coeff = beta;
    aic = AIC;

       
end
