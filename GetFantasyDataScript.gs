/*
Author: Noel Rogers
Date: 25/10/16

Script to retrieve and parse JSON data from the Fantasy Premierleague API and save to google sheet.
*/

/* Set global vars */

var bootstrap_url = 'https://fantasy.premierleague.com/drf/bootstrap-static';
var element_url = 'https://fantasy.premierleague.com/drf/element-summary/';
var teams = ['Arsenal', 'Bournemouth', 'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Hull', 'Leicester', 'Liverpool', 'Man City', 'Man Utd', 'Middlesbrough', 'Southampton', 'Stoke', 'Sunderland', 'Swansea', 'Spurs', 'Watford', 'West Brom', 'West Ham'];
var positions = ['Goalkeeper', 'Defender', 'Midfielder', 'Forward'];
var header = ['Id', 'WebName', 'FirstName', 'SecondName', 'DreamTeam', 'SelectedBy', 'Position', 'Team', 'GameWeek', 'Points', 'Cost', 'NetTransfers', 'MinutesPlayed', 'Goals', 'Assists', 'CleanSheet', 'Bonus', 'YellowCards', 'RedCards', 'GoalsConceded'];

/* Get list of players and basic details */
function getPlayerList() {
  var response = UrlFetchApp.fetch(bootstrap_url);
  var data = JSON.parse(response.getContentText());

  var players = data.elements;
  var playerData = new Array();

  for (var i = 0; i < players.length; i++) {
    var summary = [data.elements[i].id, data.elements[i].web_name, data.elements[i].first_name,
                       data.elements[i].second_name, data.elements[i].in_dreamteam,
                       data.elements[i].selected_by_percent, positions[data.elements[i].element_type - 1],
                       teams[data.elements[i].team - 1]];
    playerData.push(summary);

  }
  return playerData
}

/* Retrieve match history for a given player */
function getPlayerDetails(player) {
  var data = JSON.parse(UrlFetchApp.fetch(element_url + String(player[0])));
  var playerSummary = new Array;
  var match_hist = data.history;

  for (var i = 0; i < match_hist.length; i++) {
    var match_summary = [data.history[i].round, data.history[i].total_points, data.history[i].value, data.history[i].transfers_balance,
                        data.history[i].minutes, data.history[i].goals_scored, data.history[i].assists, data.history[i].clean_sheets,
                        data.history[i].bonus, data.history[i].yellow_cards, data.history[i].red_cards, data.history[i].goals_conceded];

    playerSummary.push(player.concat(match_summary));
  }
  return playerSummary
}

/* Populate google sheet /CSV with data */
function writeCSV() {
  var sheet = SpreadsheetApp.getActiveSheet();
  sheet.clearContents();
  var newData = [header];
  
  var player_data = getPlayerList();

  for (var i=0; i<player_data.length; i++) {
    //Logger.log(player_data[i]);
    var match_stats = getPlayerDetails(player_data[i]);
    newData = newData.concat(match_stats);

  }
  //Logger.log(newData.length);
  //Logger.log(newData[1]);
  sheet.getRange(1, 1, newData.length, newData[0].length).setValues(newData);  
}
