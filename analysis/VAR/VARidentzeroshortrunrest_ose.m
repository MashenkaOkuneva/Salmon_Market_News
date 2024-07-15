function [irr_, VAR_, figures, inf_, sup_, bar_, var_opts, ses] = VARidentzeroshortrunrest_ose(data, explanatories, VARopts, varmods, sents, freqs, name, fold)
    % Identification with zero short-run restrictions is achieved in two 
    % steps: (1) set the identification scheme mnemonic in the structure 
    % VARopt to the desired one, in this case "short"; (2) run VARir, VARvd or
    % VARhd functions. 
    %------------------------------------------------------------------ 
    
   
    IR = {};
    VARRS = {};
    
    INF={};
    SUP={};
    MED={};
    BAR={};
    SE = {};
    
    %Initialize:
    INFS = {};
    SUPS = {};

    nvar = size(explanatories, 2);
  
    eps_short ={};
    
    for i = 1:nvar
    % Update the VARopt structure to select zero short-run restrictions 
        VARopts{i}.ident = 'short';
    
    % variable names in plots
        if sents == 1
            % Get the names:
            Xnames = data.Properties.VariableNames(2:end);
            VARopts{i}.vnames = {Xnames{i}, 'Log Returns'};
            VARopts{i}.snames = {'\epsilon^{' Xnames{i} '}'}; % shocks names
        elseif sents == 0
            % Get the names:
            Xnames = data.Properties.VariableNames(2:end);
            VARopts{i}.vnames = {Xnames{i} 'x Sentiment', 'Log Returns'};
            VARopts{i}.snames = {'\epsilon^{' Xnames{i} 'x Sentiment}'}; % shocks names
        elseif sents == 2
            % Get the names:
            Xnames = data.Properties.VariableNames(3:22);
            VARopts{i}.vnames = {Xnames{i}, 'Log Returns'};
            VARopts{i}.snames = {'\epsilon^{' Xnames{i} '}'}; % shocks names
        elseif sents == 3
            Xnames = data.Properties.VariableNames([2,23:end]);
            VARopts{i}.vnames = {Xnames{i}, 'Log Returns'};
            VARopts{i}.snames = {'\epsilon^{' Xnames{i} '}'}; % shocks names
        elseif sents == 4
            Xnames = data.Properties.VariableNames(2:end);
            VARopts{i}.vnames = {Xnames{i}, 'Log Returns'};
            VARopts{i}.snames = {'\epsilon^{' Xnames{i} '}'}; % shocks names
        else
            Xnames = data.Properties.VariableNames(2:(end-1));
            VARopts{i}.vnames = {Xnames{i}, 'Log_Returns_OSE', 'Log Returns'};
            VARopts{i}.snames = {'\epsilon^{' Xnames{i} '}'}; % shocks names
        end
        
    % Change frequency
        if freqs == 0
            VARopts{i}.frequency = 'd';
        elseif freqs == 1
            VARopts{i}.frequency = 'w';
        else
            VARopts{i}.frequency = 'm';
        end
        
        % Change 'pick':
        VARopts{i}.pick = 0;
        
        % Change the fored IRF of one variable to be zero:
        VARopts{i}.shut = 0;
        
        % Change the Wold decomposition:
        VARopts{i}.recurs = 'wold';
        
        % Change the CI to 68% instead of 95%:
        VARopts{i}.pctg = 68;
    
        % The shock is One S.D.:
        VARopts{i}.impact = 0;
    
        % Compute impulse responses in the short run and plot
        VARopts{i}.nsteps = 20;
    
        % Choose the number of draws for the bootsrap:
        VARopts{i}.ndraws = 1000; 
    
        % Choose the bootstrapping method:
        VARopts{i}.method = 'bs'; % ’bs’ sampling with replacement; 
                                  % if we want the wild bootstrap option it is 'wild';
    
        % Compute impulse responses
        %rng(1);
        [IR{i}, VARRS{i}] = VARir(varmods{i}, VARopts{i});
        % Compute the lower and upper confidence band:
        [INF{i}, SUP{i}, MED{i}, BAR{i}, SE{i}] = VARirmod(varmods{i}, VARopts{i});
        
        % INFIMUM:
        INFS{i} = IR{i} - 1*SE{i};
        SUPS{i} = IR{i}+ 1*SE{i};
        
        % Plot Short-term response:
        figure(i);
        set(gca,'DefaultTextFontSize',18);
        SwatheOpt = PlotSwatheOption;
        SwatheOpt.marker = '*';
        SwatheOpt.trans = 1;
        FigSize(16,14)
        plot(cumsum(IR{i}(:,3,1)),'LineWidth',2,'LineStyle','--','Color',cmap(1)); hold on
        PlotSwathe(cumsum(IR{i}(:,3,1)),[INF{i}(:,3,1) SUP{i}(:,3,1)], SwatheOpt); hold on
        % IR(:,ii,jj) where ii is the response variable vnames and jj is the shock or snames
        plot(zeros(VARopts{i}.nsteps),'--k','LineWidth',0.5); hold on
        %xlim([1 VARopts{i}.nsteps]);
        %plot([cumsum(INF{i}(:,2,1)) cumsum(SUP{i}(:,2,1))],'r--');
        ylim([(min(INF{i}(:,3,1))-0.002) (max(SUPS{i}(:,3,1))+0.002)]);
        if name == 1
            Xnames = data.Properties.VariableNames(2:end);
            %title(['Accumulated response of Log Returns to ' Xnames{i}])
        elseif name == 0
            Xnames = data.Properties.VariableNames(2:end);
            %title(['Accumulated response of Log Returns to ' Xnames{i} ' x Sentiment'])
        elseif name == 2
            Xnames = data.Properties.VariableNames(3:22);
            %legend({Xnames{i},'Lower-bound', 'Upper-bound'},'Location','southoutside','Orientation','horizontal')
        elseif name == 3
            Xnames = data.Properties.VariableNames([2,23:end]);
            %legend({Xnames{i},'Lower-bound', 'Upper-bound'},'Location','southoutside','Orientation','horizontal')
        elseif name == 4
            Xnames = data.Properties.VariableNames(2:end);
        else
            Xnames = data.Properties.VariableNames(2:(end-1));
        end
    
    % Save the Figures:
    path = pwd;   % mention your path
    
        if freqs == 0 
           myfolder = '/plots/Ambrogio/daily' ;    % direction 
           specfold = fold;
           folder = mkdir([path,filesep,myfolder, specfold]) ;
           path  = [path,filesep,myfolder,specfold];
       
        elseif freqs == 1
           myfolder = '/plots/Ambrogio/weekly' ;   % direction
           specfold = fold;
           folder = mkdir([path,filesep,myfolder, specfold]) ;
           path  = [path,filesep,myfolder, specfold];
       
        else
           myfolder = '/plots/Ambrogio/monthly' ;   % direction
           specfold = fold;
           folder = mkdir([path,filesep,myfolder, specfold]) ;
           path  = [path,filesep,myfolder, specfold];
        end
            
        if sents == 1
           temp=[path,filesep,'topic_',num2str(i-1),'.png'];
           saveas(gca,temp);
        elseif sents == 0
           temp=[path,filesep,'topic_',num2str(i-1),'xsent.png'];
           saveas(gca,temp);
        elseif sents == 2
           temp=[path,filesep,'component_',num2str(i),'.png'];
           saveas(gca,temp);
        else 
           temp=[path,filesep,'component_',num2str(i-1),'sent.png'];
           saveas(gca,temp);
        end
    clf('reset')
    
    % Compute structural shocks (Tx2)
    eps_short{i} = (VARRS{i}.B\VARRS{i}.resid')';
    end
        
    % Output:
    irr_ = IR;
    VAR_ = VARRS;
    figures = figure;
    inf_= INF;
    sup_ = SUP;
    bar_ = BAR;
    var_opts = VARopts;
    ses = SE;
end