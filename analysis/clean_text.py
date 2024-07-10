# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 12:40:15 2022

@author: mOkuneva
"""

import re

# strings that find articles that should be deleted entirely (regexs)
delete_article_strings = [
    "^Land-based salmon production\: Experts",
    "^New\: Sign up for our daily",
    "^We're updating this page live with the latest",
    "^2020 in review",
    "^Download the new IntraFish App",
    "^We're back in Bremen",
    '^Welcome to ',
    '^Seafood world descends on Iceland',
    '^IntraFish Podcast\: Mowi Wowie\:',
    "^Editor's Picks\: ",
    '^New report\! Land-based Salmon Farming: Aquaculture\'s New Disrupter\.',
    "^Bienvenidos a Barcelona",
    "^Let's get it started",
    "^Let the show begin",
    "^Bangkok welcomes seafood world",
    "^Week's",
    "Chile to hold salmon farming conference in June",
    "Iceland Seafood Investor Forum Early Bird registration open",
    "The salmon stories that shaped 2019",
    '^VIDEO\: How should salmon buyers deal with algae crisis\?',
    '^VIDEO\: Hear what this TED speaker thinks about salmon aquaculture today\.',
    '^VIDEO\: Atlantic Sapphire\'s \'Salmon City\'\.',
    '^VIDEO\: Scottish Salmon Company sees big opportunities with BAP\.',
    '^VIDEO\: Why Chilean salmon companies are moving into Oslo\.',
    '^VIDEO\: Scottish Salmon Company CEO says group facing down fish health issues\.',
    '^VIDEO\: SalMar\'s giant offshore aquaculture facility arrives in Norway\.',
    '^VIDEO\: Inside Grieg Newfoundland\'s ambitious',
    '^VIDEO\: Australia\'s salmon farmers rescue more than 100 stranded whales\.',
    '^VIDEO\: Blaze ravages Atlantic Sapphire\'s Denmark facility',
    '^Photo gallery\: Inside the IntraFish Salmon Summit at AquaNor\.',
    '^PHOTOS\: \'Aquatraz\' salmon farm',
    '^2019\'s mega-deals, mergers and acquisitions -- so far ',
    '^What could happen to shrimp\?',
    '^All IntraFish\, all the time',
    '^IntraFish Seafood Investor Forum',
    '^Three days of news'
]

def delete_articles_with_strings(delete_article_strings, df):
    for string in delete_article_strings:
        df = df[~df['texts'].str.contains(string)]
    # reset index
    df.reset_index(inplace=True)
    return df

# snippets that appear in the end
end_strings = [
    #'New: Sign up for our daily',
    'You can check',
    'The Nasdaq Salmon Index is the weighted average of weekly reported sales',
    'Comments? Email', # This one appears once before the Chinese translation of the article, otherwise always in the end
    'Comments? email',
    'Comments? Contact',
    'Feedback? Email',
    'Comments? E-mail',
    'Feedback? Contact',
    "--- To find out more",
    'Click through',
    '(PS -- IntraFish',
    'Debuting in a few days', # advertisement for the IntraFish Business Intelligence report
    'Check out the',
    'Check out a',
    '--- Check out our newly',
    'Check out prices',
    'Check out our listing',
    'View the video',
    'The SalmonEx Index represents',
    'These is what prices look like', # quantitative information
    'Average prices were reported', # quantitative information
    'The data is based on average prices', # data source
    'See the video below',
    'Here\'s the quick take',
    'The 50 biggest', # a table with 50 biggest salmon farming sites
    'Pareto Securities recommendations', # a table
    'Salmon farming companies listed on the Santiago Stock Exchange ordered by volumes', # a table
    'For more fish prices', # reference to the IntraFish Price Tracker page
    '--- IntraFish will soon release',
    'Keep up with us',
    '-- New! To purchase',
    'Find out in a newly released',
    'Read the interview',
    '--- Who are the top investors',
    'The prices reported to IntraFish',
    'For more information',
    'An upcoming IntraFish',
    '--- IntraFish is soon to release',
    'I\'m curious to hear your thoughts',
    '-- Looking for a more in-depth look',
    'IntraFish Media will host',
    '-- IntraFish Media',
    'Discover the potential in the sector',
    'You can also follow us on',
    'In a Twitter message , an investor refers',
    '--- To buy a copy or view',
    'Here are a few additional facts:',
    '-- Looking for a more in-depth look',
    '--- IntraFish will soon to',
    'Watch the company\'s',
    '-- The IntraFish Business Intelligence Unit provides',
    '-- IntraFish Webinar'
]

mid_strings = [
    ' PromoBox : Sign up for our Salmon Newsletter ',
    'Follow me on Twitter: @drewcherry',
    '(For a list of the specific closures, click here now. )',
    'To see the MSC\'s full rebuttal, click here .',
    'Check out our weekly price graph.',
    'Check out our interactive weekly price graph.',
    'Source: Bloomberg', # data source
    '\xad', # remove soft hyphens
    'xefx82xbe',
    'xefx82xb7',
    '</h2>',
    '</ol> ',
    ' </blockquote>'
]

# '&amp;amp;amp;.+?</iframe>(?: \"){0,1}': link to the video
# 'xe4xb8xad.+$': Chinese translation of the article
# For more info on.+$': For more info on Chilean and Norwegian salmon prices visit the IntraFish Price Tracker
# 'The Nasdaq Salmon Index is the weighted average.+$': an explanation of what the Nasdaq salmon index is.
# '(?:Read the full)(?! list)(?:.+$)': Read the full story/interview/report here. Except for 'Read the full list of the wealthiest seafood moguls below.'
# '(?:Read full.+$)': Read full story here.
# 'Read also.+$': recommendations of related articles
# "(?:\(Click here for)(?:[\S\s]+?\))": (Click here for in-depth coverage of the battle for control of Copeinca and Cermaq )
#"(?:\(WANT MORE ON GM SALMON)(?:[\S\s]+?\))": (WANT MORE ON GM SALMON? Click here to read our full coverage )
#"(?:Click here to read IntraFish)(?:[\S\s]+?\.)": Click here to read IntraFish\'s extensive coverage of the GM salmon issue.
#"(?:Click here to see where)(?:[\S\s]+?\.)": Click here to see where the fish are being caught .
#"(?:-- ){0,1}(?:\([ ]{0,1}Click here to)(?:[\S\s]+?\))": (Click here to view the IntraFish Price Tracker page )
#"(?:-- Click here to get the IntraFish)(?:[\S\s]+?revolution)": -- Click here to get the IntraFish Industry Report: The land-based salmon farming revolution
#"(?:Click here to follow all)(?:[\S\s]+?\.)": Click here to follow all of the news related to coronavirus .
#"(?:-- Click here to read)(?:[\S\s]+?\.)": -- Click here to read the letter in full and the full list of protocols the companies committed to (pdf).
#"(?:--|-){0,1}(?: \[Click here)(?:[\S\s]+?\][\.]{0,1})": -- [Click here to see a map of all the major land based salmon farms announced over the past year]
#"(?:Click here to see our line-up)(?:[\S\s]+?\!)": Click here to see our line-up of speakers and register today!
#"(?:Click here to see the video)(?:[\S\s]+?\.)": Click here to see the video .
#"(?:-- ){0,1}(?:Click here)(?:[\S\s]+$)": Click here to sign up to the free IntraFish Salmon Newsletter . ---
#"(?:-- )(?:\[Want more land-based salmon)(?:[\S\s]+$)": -- [Want more land-based salmon farming news? IntraFish has you covered. Click here four our dedicated section.]
#"(?:--- ){0,1}(?:For(?! the))(?:[\S\s]+?)(?:click here.+$)": For a video of Jim Flynn talking about the barramundi, and other videos from the show, click here .
#"(?:--- |- ){0,1}(?:To )(?:[\S\s]+?)(?:click here.+$)": To see a video of Chef Greenaway talking about Scottish seafood, and many other videos from the show, click here .
#"(?:Watch)(?:[\S\s]+?)(?:click here.+$)": Watch the interview below and click here to download Matthiasson\'s presentation from the IntraFish Seafood Investor Forum in Iceland last month . </iframe> --
#"(?:Vist)(?:[\S\s]+?)(?:click here.+$)": Vist here for more DataSalmon prices and information, click here.
#'(?:\"Click below)(?:[\S\s]+?$)': "Click below to watch the IntraFish interview with The Scottish Salmon Company (SSC) CEO Craig Anderson, who discusses his group\'s second-quarter results, and what the group is doing to tackle some of its key issues. ---
#'(?:Key figures for.+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}(?:-- ){0,1}(?:---){0,1}': Tables that start from 'Key figures for'
#'(?<=\.\s)[^.]+?(?:\(figures in MNOK\).+?|\(Figures in MNOK\).+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}(?:-- ){0,1}(?:---){0,1}': Tables that start from smth like '. Hofseth International AS, group figures (figures in MNOK)'
#'(?:(?<=\.\"\s)|(?<=\.\s))[^.]+?(?:\(NOK million\).+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}(?:-- ){0,1}(?:---){0,1}': Tables that start from smth like '. Ellingsen Seafood Holding consolidated 2015 results (NOK million)'
#'(?:(?<=\.\s)|(?:In the))(?:[^.]+?){0,1}(?:IntraFish was told the following prices.+?|IntraFish has been given the following prices.+?)(?:Sizes 6\+{0,1} kilos.+?|Sizes 5-6.+?|Sizes 6-7.+?)(?:to.+?)(?:\))(?: per kilo){0,1}(?: Sizes 6-7.+? per kilo| Sizes 6\+{0,1} kilos.+?to.+?\)){0,1}(?: per kilo){0,1}[ ]{0,1}(?:--- ){0,1}': quantitative information
#'(?<=\.\s)[^.]+?(?:new price targets are as follows.+?$)': quantitative information.
#'(?<=\.\s)(?:Executives gave the following ranges.+?$)': quantitative information.
#'(?:(?<=\.\s)|(?<=\.\"\s))(?:[^.]+?){0,1}(?:IntraFish was informed of the following prices.+?|IntraFish has been informed of the following prices.+?|IntraFish was informed of following prices.+?|IntraFish gathered the following prices.+?)(?:Size[s]{0,1} 6\+{0,1} kg.+?|Size[s]{0,1} 6-7 kg.+?)(?:to.+?\) per kg|\) per kg|to.+?\)|lower\" \")(?: \(up to.+$){0,1}[ ]{0,1}(?:--- ){0,1}': quantitative information
#'(?:Overall\, ){0,1}(?:IntraFish was provided with the following prices.+?|IntraFish was told of the following prices.+?)(?:Size[s]{0,1} 6.+?)(?: per kg.+?$| per kilo.+?$)': quantitative information
#'(?:A buyer in Europe informed IntraFish of the following prices.+?)(?=\"It\'s about)': quantitative information
#'Another foreign broker reports.+$': quantitative information
#'(?:A number of exporters and importers said.+?)(?=These levels mean)': quantitative information
#'(?:---)(?: Sign up to our FREE.+?)(?:---)': --- Sign up to our FREE Salmon Newsletter here ! --- in the midde of the text
#'(?:--- ){0,1}(?:\[Sign up to.+?\])(?: ---){0,1}':[Sign up to our FREE monthly land-based salmon newsletter here] in the middle of the text
#'(?:- ){0,1}(?:\[Join the next.+?\])(?: -){0,1}': - [Join the next IntraFish Webinar: Disruption in the Salmon Farming Sector. Register today!] - in the middle of the text
#'(?:PromoBox \: Sign up for.+?)(?:a story)': PromoBox : Sign up for Alerts and never miss a story in the middle of the text
#'(?:--- ){0,1}(?:Sign up(?! for our daily| here for free).+?$)': --- Sign up to our FREE weekly Salmon Newsletter here . at the end of the text
#(?:\(Figures in NOK millions\).+?)(?:</tbody>[ ]{0,1}</table>)': tables
#'(?<=\.\s)[^.]+?(?:\(figures in NOK million[s]{0,1}\).+?|figures in NOK million.+?)(?:</tbody>[ ]{0,1}</table>)': tables
#'Figures in millions.+$': a table
#'(?:PromoBox(?! \: Despite facing).+?)(?:Sector|subscribers|IntraFish Subscribers|Intrafish Subscribers|Aquaculture news|Rachel Mutter|matters to you|Forum|Round-up|competition|Alerts[\!]{0,1}|the first to know (?:with Alerts){0,1}|pollock story|Seafood Economy|seafood sustainability(?: event){0,1}|IntraFish App[\!]{0,1}|Shipping Crisis|Story|story(?: on Cooke \"){0,1}|inbox|update|sector|the App|on the move|Salmon Market|industry\'s future\?|next week \"|research reports|reporting|US market|High Liner|Aquaculture Innovation(?: news\? \"){0,1}|News First|Acquisitions|on Mowi|seafood deal|The Race to Replace|Salmon Forum 2021|Farmed Salmon \"|Salmon Prices \"|Salmon News \"|Norway Royal Salmon \"|edge in Salmon \"|edge in Feed|eye on Cooke|Salmon market|eye on Cargill|Salmon industry|salmon farming|Salmon news(?: on the move){0,1}|Ukraine Crisis|in Barcelona|newsletter|Salmon Season \"|more in NYC|in NYC on May 25|business\-critical news|US salmon market|Offshore Aquaculture|Never miss a move|Summit Dec\. 14|eye on Samherji|IntraFish journalists|missing out\?|Follow John Fiorillo|eye on Cermaq|Land\-based Aquaculture|Land\-Based Salmon Farming|Land-Based Salmon Revolution|Track Land-Based Salmon [\"]{0,1}|Follow Land\-Based Salmon|Land\-Based Aquaculture|eye on Land\-Based Salmon|industry news that matters|Feed Ingredients|Alaska salmon season|feed ingredients|Seafood Oultook|post-COVID landscape|post-COVID era)': 'PromoBox : Report: The Land-Based Salmon Sector'
#'(?:The following average prices.+?$)': quantitative information
#'(?:--.+?)(?:GMT)': remove the dates from the series
#'(?:--.+?)(?:PDT)': remove the dates from the series
#"(?:VIDEO\: )(?=What\'s|Marine Harvest top exec|Washington State|Inside Marine Harvest Canada\'s|Bakkafrost profit jumps|Confident Marine Harvest)" # not finished
#'(?:Company</th>.+?)(?:</tbody>[ ]{0,1}</table>)': a table that starts from 'Company</th>'
#'(?<=\.\s)[^.]+?(?:\({0,1}figures in million NOK\){0,1}.+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}[\"]{0,1}': a table that starts from smth like 'Lovundlaks AS financial results (figures in million NOK)'
#'(?<=\.\s)[^.]+?(?:\({0,1}in million NOK\){0,1}.+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}[\"]{0,1}(?:-- ){0,1}(?:---){0,1}': a table that starts from smth like 'NTS 2016 results (in million NOK)'
#'(?<=\.\s)[^.]+?(?:figures in millions of NOK.+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}[\"]{0,1}(?:-- ){0,1}(?:---){0,1}': a table that starts from smth like 'Eidsfjord Sjøfarm figures in millions of NOK'
#'(?<=\.\s)(?:See our overview HERE.+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}': a table that starts from 'See our overview HERE'
#'(?:Nr\..+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}': a table that starts from 'Nr. selected'
#(?<=Mowi\:)(?:[^.]+?){0,1}(?:</td>.+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}[\"]{0,1}(?:-- ){0,1}(?:---){0,1}(?: \"){0,1}': a table that starts from 'Name </td> Title </td>'
#'(?:Product name</th> </tr>.+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}[\"]{0,1}(?:-- ){0,1}(?:---){0,1}(?: \"){0,1}': a table that starts from 'Product name</th> </tr>'
#'(?:(?<=\.\s)|(?<=\.\"))(?:[^.]+?){0,1}(?:</td>.+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}[\"]{0,1}(?:-- ){0,1}(?:---){0,1}(?: \"){0,1}(?:</colgroup>.+?</tbody>[ ]{0,1}</table>){0,1}': a table that starts from smth like 'Marine Harvest Q3 production (MT) and EBIT/kg (EUR) Norway</td>'
#'(?:</th>.+?)(?:</table>)[ ]{0,1}[\"]{0,1}': '</th> </th> </th> </th> </tr> </tbody> </table> "'
regexs = [
    '(\[Sign up .*? \])',
    '&amp;amp;amp;.+?</iframe>(?: \"){0,1}',
    'xe4xb8xad.+$',
    'For more info on.+$', # Put the Nasdaq Salmon index into endstrings, always appears in the end
    '(?:Read the full)(?! list)(?:.+$)',
    '(?:Read full.+$)',
    '(?:Read also.+?)(?:Ron Stotish.+?|.?$)',
    '(-- OUT NOW.*? (?:--.+?|free sample here.+?|sample pages or to order today\!.+?))', # fixed it
    '(-- (?:Read.+?|READ.+?).*?--)', # fixed it
    '(?:---.|Also\,.)(?:IntraFish is excited.+?$)',
    '(?:---.|.)(?:This article is part of.+?$)',
    '(?:---.|.)(?:The next IntraFish Seafood Investor Forum.+?$)',
    '(?:---.|.)(?:To purchase the new IntraFish.+?$)',
    '(?:--.|.)(?:IntraFish newest industry report.+?$)',
    "(-- New! To purchase the new IntraFish.*?$)", 
    "([A-Za-z]*\.[A-Za-z]*@.*?\.[com|no]+)", # Emails with name.surname@domain.com/no pattern (mostly infrafish.com)
    "(\s[a-z]*@intrafish\.[com|no]+)", # Emails like editorial@intrafish.com/no
    "(?:www\.)\s{0,1}[a-zA-Z0-9]+?(?:\.com)", # websites like www. intrafishevents.com
    "(?:[a-zA-Z]+?)(?:@)(?:[a-zA-Z]+?)\.{0,1}\s{0,1}(?:com)", #Emails like events@intrafish. com
    "(?:\(Click here for)(?:[\S\s]+?\))",
    "(?:\(WANT MORE ON GM SALMON)(?:[\S\s]+?\))",
    "(?:Click here to read IntraFish)(?:[\S\s]+?\.)",
    "(?:Click here to see where)(?:[\S\s]+?\.)",
    "(?:-- ){0,1}(?:\([ ]{0,1}Click here to)(?:[\S\s]+?\))",
    "(?:-- Click here to get the IntraFish)(?:[\S\s]+?revolution)",
    "(?:Click here to follow all)(?:[\S\s]+?\.)",
    "(?:-- Click here to read)(?:[\S\s]+?\.)",
    "(?:--|-){0,1}(?: \[Click here)(?:[\S\s]+?\][\.]{0,1})",
    "(?:Click here to see our line-up)(?:[\S\s]+?\!)",
    "(?:Click here to see the video)(?:[\S\s]+?\.)",
    "(?:-- ){0,1}(?:Click here)(?:[\S\s]+$)",
    "(?:-- )(?:\[Want more land-based salmon)(?:[\S\s]+$)",
    "(?:--- ){0,1}(?:For(?! the))(?:[\S\s]+?)(?:click here.+$)",
    "(?:--- |- ){0,1}(?:To )(?:[\S\s]+?)(?:click here.+$)",
    "(?:Watch)(?:[\S\s]+?)(?:click here.+$)",
    "(?:Vist)(?:[\S\s]+?)(?:click here.+$)",
    '(?:\"Click below)(?:[\S\s]+?$)',
    '(?:Key figures for.+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}(?:-- ){0,1}(?:---){0,1}',
    '(?<=\.\s)[^.]+?(?:\(figures in MNOK\).+?|\(Figures in MNOK\).+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}(?:-- ){0,1}(?:---){0,1}',
    '(?:(?<=\.\"\s)|(?<=\.\s))[^.]+?(?:\(NOK million\).+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}(?:-- ){0,1}(?:---){0,1}',
    '(?:(?<=\.\s)|(?:In the))(?:[^.]+?){0,1}(?:IntraFish was told the following prices.+?|IntraFish has been given the following prices.+?)(?:Sizes 6\+{0,1} kilos.+?|Sizes 5-6.+?|Sizes 6-7.+?)(?:to.+?)(?:\))(?: per kilo){0,1}(?: Sizes 6-7.+? per kilo| Sizes 6\+{0,1} kilos.+?to.+?\)){0,1}(?: per kilo){0,1}[ ]{0,1}(?:--- ){0,1}',
    '(?<=\.\s)[^.]+?(?:new price targets are as follows.+?$)',
    '(?<=\.\s)(?:Executives gave the following ranges.+?$)',
    '(?:(?<=\.\s)|(?<=\.\"\s))(?:[^.]+?){0,1}(?:IntraFish was informed of the following prices.+?|IntraFish has been informed of the following prices.+?|IntraFish was informed of following prices.+?|IntraFish gathered the following prices.+?)(?:Size[s]{0,1} 6\+{0,1} kg.+?|Size[s]{0,1} 6-7 kg.+?)(?:to.+?\) per kg|\) per kg|to.+?\)|lower\" \")(?: \(up to.+$){0,1}[ ]{0,1}(?:--- ){0,1}',
    '(?:Overall\, ){0,1}(?:IntraFish was provided with the following prices.+?|IntraFish was told of the following prices.+?)(?:Size[s]{0,1} 6.+?)(?: per kg.+?$| per kilo.+?$)',
    '(?:A buyer in Europe informed IntraFish of the following prices.+?)(?=\"It\'s about)', # until that word
    'Another foreign broker reports.+$',
    '(?:A number of exporters and importers said.+?)(?=These levels mean)',
    '(?:^|(?<=\.\s)|(?<=\.\"\s))(?:[^.]+?){0,1}(?:Industry players told IntraFish.+?|\"IntraFish spoke to spot market participants.+?|IntraFish was quoted the following prices.+?|Four players told IntraFish.+?|IntraFish was told of the following spot prices.+?|IntraFish was informed of the following price.+?|The few who provided concrete prices.+?|The highest prices are paid in southern Norway.+?|IntraFish was given the following prices.+?|The second exporter reported.+?|Various players told IntraFish.+?|Norwegian salmon prices  NOK.+?|Another exporter said the market is.+?|On Friday IntraFish was told.+?|IntraFish was told of the following prices.+?|On average\, prices are expected to be around.+?|The following prices were reported on average.+?|IntraFish was given the follow prices.+?|This week\, IntraFish was given the following range.+?|An IntraFish survey of market sources revealed.+?|On Friday\, IntraFish was given the following.+?)(?:Size[s]{0,1} 6-7 kilos.+?|Size[s]{0,1} 6\+{0,1} kg.+?|Size 6 kilos.+?|Size over 6 kilos.+?|Size[s]{0,1} 6\+{0,1} kilograms.+?|Size[s]{0,1} 6.+?)(?:to.+?\) per kilo|\)[ ]{0,1}per kg|\) per kilo|to.+?\)|\)/ kg|\) per kilogram)(?: per kg){0,1}(?: if you include airfreight\.|gram| / kg| \(depending on the market\) | Salmon prices.+$){0,1}[ ]{0,1}(?:--- ){0,1}', #quantitative information
    '(?:(?<=\.\s)|(?<=\.\"\s))(?:[^.]+?){0,1}(?:IntraFish was quoted the following prices.+?)(?:Contracts for Q3 and Q4 saw.+?$)', #quantitative information
    '(?:Size 4-5 kg.+?)(?:Other players report.+?)(?:Size[s]{0,1} 6\+{0,1} kg.+?)(?:\) per kg)', #quantitative information
    '(?:IntraFish was told of the following prices.+?|IntraFish has been informed of the following prices.+?|IntraFish was informed of the following prices.+?|The farmer told IntraFish.+?|IntraFish was given the following prices.+?|A Danish buyer told IntraFish of the following prices.+?|IntraFish was given the following average.+?)(?:Size[s]{0,1} 5-6.+?)(?:\) per kg|\) per kilo)[ ]{0,1}(?:--- ){0,1}', #quantitative information
    '(?:Size 3-4 kg.+?)(?:Size[s]{0,1} 5-6.+?)(?:\) per kg)', #quantitative information
    '(?:IntraFish was told of the following prices.+?)(?:Sizes 4.+?)(?:\) per kg)[ ]{0,1}(?:--- ){0,1}', #quantitative information
    '(?:Size 3-4 kg.+?)(?:Size[s]{0,1} 6\+{0,1} kg.+?)(?:\) per kg)(?: \(airfreight\)){0,1}', #quantitative information
    '(?:Another exporter told IntraFish the following prices:.+?)(?:Sizes 5.+?)(?:\) per kilo)[ ]{0,1}(?:--- ){0,1}', #quantitative information
    '(We\'ll be updating.*?$)',
    '(Head over to IntraFish\'s Business Intelligence.*?$)',
    '(Participants in Iceland: Company.*?\</table>)',
    '(?:-- IntraFish\'s.+?$)',
    '(?:As IntraFish Media previously reported.+?\.)', # remove only sentence because there is a link
    '(?:\(click HERE.+?\.)',
    '(?:IntraFish Media\'s.+?)(?=$|With)', # we do not want to delete 'IntraFish Media'
    '(?:-- OUT NOW!.|Out now!.)(?:The IntraFish Land-Based Salmon Farming Report.+?$)',
    '(?:---.|--.|)(?:For more seafood news.+?$)',
    '(?<=\,\s)[^,]+?(?:presented the following\:.+?)(?=\"With)',
    '(?:-- IntraFish recently.+?$|IntraFish recently published.+?$)', 
    '(?<=\.\s)[^.]+?(?:catch up with our blog.+?$)', # it tackles both: "You can watch the video below" and "You can catch up with our blog"
    '(?:Prices told to IntraFish.+?)(?=.The highest|$)',
    '(\*Ed\'s note\:.+?$)',
    '(?:---)(?: Sign up to our FREE.+?)(?:---)',
    '(?:--- ){0,1}(?:\[Sign up to.+?\])(?: ---){0,1}',
    '(?:- ){0,1}(?:\[Join the next.+?\])(?: -){0,1}',
    '(?:PromoBox \: Sign up for.+?)(?:a story)',
    '(?:--- ){0,1}(?:Sign up(?! for our daily| here for free).+?$)',
    '(?<=\.\s)[^.]+?(?:gave IntraFish the following prices.+?)(?=Volume|$)', 
    '(?:SSB price averages.+?)(?=At FishPool)',
    '(?<=\.\s)[^.]+?(?:can be found here.+?)(?=SeaChoice|US|$)',
    '(?:\(below\))',
    '(?<=\.\s)[^.]+?(?:a table.*?\</table>)',
    '(\(see Tweet below\).+?)',
    '(?:(?:\(Read.|\(READ).*?\))', # part of (READ ALSO: as well found some other (Read..) as well
    '(?:• 3-4 kg.+?)(?=One importer|$)',
    '(?:\(Figures in NOK millions\).+?)(?:</tbody>[ ]{0,1}</table>)',
    '(?<=\.\s)[^.]+?(?:\(figures in NOK million[s]{0,1}\).+?|figures in NOK million.+?)(?:</tbody>[ ]{0,1}</table>)',
    'Figures in millions.+$',
    '(Watch real\-time.+?)(?<=\.)', # related to VIDEOS
    '(?:\"After a long journey.+?\.)', # related to videos and links I found
    '(?<=\,)[^,]+?(?:according to kafe\. com.+?\,)', # found in a video, contains a link
    '(?:during the group\'s Q1 results presentation Wednesday.+?\.)',
    '(?:Watch the exclusive.+?$)',
    '(?:PromoBox(?! \: Despite facing).+?)(?:Sector|subscribers|IntraFish Subscribers|Intrafish Subscribers|Aquaculture news|Rachel Mutter|matters to you|Forum|Round-up|competition|Alerts[\!]{0,1}|the first to know (?:with Alerts){0,1}|pollock story|Seafood Economy|seafood sustainability(?: event){0,1}|IntraFish App[\!]{0,1}|Shipping Crisis|Story|story(?: on Cooke \"){0,1}|inbox|update|sector|the App|on the move|Salmon Market|industry\'s future\?|next week \"|research reports|reporting|US market|High Liner|Aquaculture Innovation(?: news\? \"){0,1}|News First|Acquisitions|on Mowi|seafood deal|The Race to Replace|Salmon Forum 2021|Farmed Salmon \"|Salmon Prices \"|Salmon News \"|Norway Royal Salmon \"|edge in Salmon \"|edge in Feed|eye on Cooke|Salmon market|eye on Cargill|Salmon industry|salmon farming|Salmon news(?: on the move){0,1}|Ukraine Crisis|in Barcelona|newsletter|Salmon Season \"|more in NYC|in NYC on May 25|business\-critical news|US salmon market|Offshore Aquaculture|Never miss a move|Summit Dec\. 14|eye on Samherji|IntraFish journalists|missing out\?|Follow John Fiorillo|eye on Cermaq|Land\-based Aquaculture|Land\-Based Salmon Farming|Land-Based Salmon Revolution|Track Land-Based Salmon [\"]{0,1}|Follow Land\-Based Salmon|Land\-Based Aquaculture|eye on Land\-Based Salmon|industry news that matters|Feed Ingredients|Alaska salmon season|feed ingredients|Seafood Oultook|post-COVID landscape|post-COVID era)',
    '(?:PromoBox(?! \: Despite facing).+?)(?:know about COVID|views on the future of salmon|know about M\&As \"|Tracking Bakkafrost\? \"|Atlantic Sapphire|Keep up with Cooke \"|Track the Aquaculture industry \"|Keep up with Bakkafrost \"|Cooke news \"|eye on the Markets \"|miss a deal \"|on top of Chile \"|People Move \"|Your IntraFish|Find Out First \"|with Cargill ")',
    '(?:PromoBox(?! \: Despite facing).+?)(?:with Brexit \"|buying who\? \"|Plant-Based Seafood \"|Green Money \"|with JBS \"|eye on Young\'s \"|your customers|on competitors|UK seafood news \"|IntraFish Podcast \"|People move \"|GM salmon developments|Mowi move|seafood news headlines|farmed salmon \"|Mowi makes|more often|land-based salmon|Peter Pan|winners and losers|on the go\!|and more|Rachel Sapin)',
    '(?:PromoBox \:)',
    '(?:The following average prices.+?$)',
    '(?:--.+?)(?:GMT)',
    '(?:--.+?)(?:PDT)',
    '(Get a snapshot.+?)(?:GMT)',
    '(?: DKK.| NOK.| \$.| JPY.)(?:[0-9.]+ \(.|[0-9.]+ million \(.|[0-9.]+ billion \(.).+?(?<=\))',
    '(?: </iframe>)(?= |\.|--)', # delete those that do not include link or ar part of a link
    '(?:</iframe></p><p >|</iframe>&lt;.+?)(?=--|W|$)', # also contain </iframe>
    '(?: Go on an exclusive tour now\.)',
    "(?:[0-9]+\,[0-9.]+ |[0-9.]+ |[0-9]+\. )(?:metric tons)", # to delete a number plus metric tons
    "(?:\$|\€|NOK)(?:[0-9]+\,[0-9.]+ .|[0-9.]+ .|[0-9]+\.[0-9]+ .)(?:per metric ton)", # similar
    '(?:\$|\€|NOK)(?:[0-9]+\,[0-9.]+ |[0-9.]+ |[0-9]+\.[0-9]+ )(?:per metric ton)',
    "(?:\$|\€|NOK).(?:[0-9]+\,[0-9.]+ |[0-9.]+ |[0-9]+\.[0-9]+)(?:per kilogram|per kilo)", # same as above for all quant. info $2.05 per kilo
    "(?:\(\$|\(\€|\(NOK)(?:[0-9]+\,[0-9.]+ |[0-9.]+ |[0-9]+\. )(?:million|billion|trillion)(?:/\$.|/\€.|/NOK.)(?:[0-9]+\,[0-9.]+ |[0-9.]+ |[0-9]+\. )(?:million\)|billion\)|trillion\))", # quantitative information like: ($2.05 million/$3.95 million)
    "(?:\(\$|\(€|\(NOK)(?:[0-9]+\,[0-9]+\)|[0-9]+\.[0-9]+\)|[0-9]+\))", # quantitative information like ($31.45)
    "(?:\(\$|\(\€|\(NOK)(?:[0-9]+\,[0-9.]+ |[0-9.]+ |[0-9]+\. )(?:million\)|billion\)|trillion\))", # quantitative information like (€4.6 million)
    "(?:VIDEO\: )(?=What\'s|Marine Harvest top exec|Washington State|Inside Marine Harvest Canada\'s|Bakkafrost profit jumps|Confident Marine Harvest|AquaChile\'s Puchi talks|Hear what Iceland\'s|Leroy CEO says US will|Land-based salmon farming about to get nationwide)", # delete the word VIDE0:
    "(?:--)(?: VIDEO\: .).+?(?:--)",
    "(?:</span></span>)",
    "(?:</span> )",
    '(?:</span.)(?=\,|\"|[a-z]|\.|[A-Z]|\')',
    "(?:IntraFish reported the following prices\:.+?$)",
    '(?:\(\$|\(\€|\(NOK)(?:[0-9]+\.[0-9]/|[0-9]+\,[0-9]+/|[0-9]+/).+?(?:\))', # remove quantitative info like (€265.5/$302.2)
    '(?:[0-9]\-[0-9] kg.|[0-9]kg.|[0-9]\+kg.|6 kg.)(?:-.|\+.).+?(?:/kg|/ kg)', # remove quant info
    '(?:Company</th>.+?)(?:</tbody>[ ]{0,1}</table>)', # remove tables
    '(?<=\.\s)[^.]+?(?:\({0,1}figures in million NOK\){0,1}.+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}[\"]{0,1}', # remove tables
    '(?<=\.\s)[^.]+?(?:\({0,1}in million NOK\){0,1}.+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}[\"]{0,1}(?:-- ){0,1}(?:---){0,1}', # remove tables
    '(?<=\.\s)[^.]+?(?:figures in millions of NOK.+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}[\"]{0,1}(?:-- ){0,1}(?:---){0,1}', # remove tables
    '(?<=\.\s)(?:See our overview HERE.+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}', # remove tables
    '(?:Nr\..+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}', # remove tables
    '(?<=Mowi\:)(?:[^.]+?){0,1}(?:</td>.+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}[\"]{0,1}(?:-- ){0,1}(?:---){0,1}(?: \"){0,1}', # remove tables
    '(?:Product name</th> </tr>.+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}[\"]{0,1}(?:-- ){0,1}(?:---){0,1}(?: \"){0,1}', # remove tables
    '(?:(?<=\.\s)|(?<=\.\"))(?:[^.]+?){0,1}(?:</td>.+?)(?:</tbody>[ ]{0,1}</table>)[ ]{0,1}[\"]{0,1}(?:-- ){0,1}(?:---){0,1}(?: \"){0,1}(?:</colgroup>.+?</tbody>[ ]{0,1}</table>){0,1}', # remove tables
    '(?:</th>.+?)(?:</table>)[ ]{0,1}[\"]{0,1}', # remove some leftovers from one of the tables
    '(?<=\.| )(?:</p><p >|---</p><p ><em>)',
    '(?:</h5>)(?=[A-Z]| )',
    '(?<=.)(?:</h4>)',
    '(?: </font>)(?= )', # remove </font>
    '(?:</font></font>)(?=The)', # remove </font>
    '(?<=[a-z])(?:</font> )', # remove </font>
    '(?<=Denmark\.)(?:</font></font>)(?= )', # remove </font>
    '(?<=[a-z])(?:</font></font> \.</font></font>)',
    '(?<=\.)(?:</font></font>|</font></font></font>|</font></font></font></font></font></font></font></font></font></font></font></font></font></font></font></font></font></font></font></font></font></font>)(?= Bakkafrost)',
    '(?<=\.|[a-z]|\"|\,)(?:</font>|</font></font>|</font></font></font>|</font></font></font></font>|</font></font></font></font></font></font>|</font></font></font></font></font></font></font>|</font></font></font></font></font></font></font></font>)(?= )',
    '(?: </font></font>)(?= )',
    '(?:\")(</font>|</font>.+?)(?=[A-Z])',
    '(?:\.| )(</font></font></font>.+?)(?= |[A-Z])',
    '(?<= )(?:</font></font>)(?=Nilsen)',
    '(?<=[a-z])(?:</font></font>.+?)(?= )',
    '(?: ---</font></font> )',
    '(?: SP20-06\.pdf \(1\.7MB\) </figure> )', 
    '(?:</sub>|</sup>)',
    '(?:DOWNLOAD\:.+?)(?:Download it now\! \")',
    '(?:-- |\[){0,1}(?:CLICK HERE.+?)(?:\(pdf\))(?: --| \]){0,1}',
    '(?:-- DOWNLOAD.+?)(?:\(pdf\) --)',
    '(?:\[Download.+?)(?:\(pdf\)\])',
    '(?:- \[READ\:.+?)(?:\] -)'
    
    
    

    
    
]

# strings that should be removed after the ones identified by regular expressions
after_re_strings = [
    'amp;'
    ]

def clean_text(text):

    """
    This function removes strings that are unlikely to be relevant for sentiment and topic
    analysis.
    """

    for endstring in end_strings:
        # check if endstring is in the text
        if endstring in text:
            # Check whether strings are reliably in the end before adding them to the list
            text = text[:text.find(endstring)]
    for midstring in mid_strings:
        # check if midstring is in the text
        if midstring in text:
            # if so, remove it
            text = text.replace(midstring, '')
    for regex in regexs:
        # check if regex is in the text
        if re.search(regex, text):
            # if so, remove it
            text = re.sub(regex, '', text)

    for after_re_string in after_re_strings:
        # check if after_re_string is in the text
        if after_re_string in text:
            # if so, remove it
            text = text.replace(after_re_string, '')

    return(text)